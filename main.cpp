#include <Python.h>
#include <iostream>
#include <string>
#include <limits.h>
#include <mach-o/dyld.h>
#include <unistd.h>
#include <libgen.h> // for dirname

// Returns the folder containing the running executable
std::string GetExeFolder() {
    char buffer[PATH_MAX];
    uint32_t size = PATH_MAX;
    if (_NSGetExecutablePath(buffer, &size) != 0) {
        std::cerr << "Failed to get executable path (buffer too small?)\n";
        return "";
    }
    return std::string(dirname(buffer));
}

int main() {
    std::cout << "=== Starting embedded Python ===\n";

    std::string exeFolder = GetExeFolder();
    std::string pythonHomeStr = exeFolder + "/python";  // points to the "python/" folder

    // Python folders
    std::string pythonLib      = pythonHomeStr + "/lib/python3.12";
    std::string pythonDynLoad  = pythonLib + "/lib-dynload";
    std::string pythonSite     = pythonLib + "/site-packages";
    std::string gameFolder     = exeFolder + "/game";    // folder containing sample_game.py

    // Initialize Python
    PyStatus status;
    PyConfig config;
    PyConfig_InitPythonConfig(&config);

    config.site_import = 1;

    std::wstring pythonHomeW(pythonHomeStr.begin(), pythonHomeStr.end());
    std::wstring programName = L"launcher";

    PyConfig_SetString(&config, &config.home, pythonHomeW.c_str());
    PyConfig_SetString(&config, &config.program_name, programName.c_str());

    status = Py_InitializeFromConfig(&config);
    if (PyStatus_Exception(status)) {
        std::cerr << "Python failed to initialize!\n";
        PyConfig_Clear(&config);
        return 1;
    }

    std::cout << "Python initialized successfully!\n";

    // ================= macOS embedded Python sys.path fix ==================
    PyRun_SimpleString(("import sys; sys.path.insert(0, r'" + pythonLib + "')").c_str());
    PyRun_SimpleString(("import sys; sys.path.insert(0, r'" + pythonDynLoad + "')").c_str());
    PyRun_SimpleString(("import sys; sys.path.insert(0, r'" + pythonSite + "')").c_str());
    PyRun_SimpleString(("import sys; sys.path.insert(0, r'" + gameFolder + "')").c_str());
    // =======================================================================

    // Test import
    PyRun_SimpleString("import pygame; print('pygame imported successfully')");

    // Import and run the python game
    PyObject* pName = PyUnicode_FromString("main");  // main.py in python/game/ folder
    PyObject* pModule = PyImport_Import(pName);
    Py_XDECREF(pName);

    if (!pModule) {
        PyErr_Print();
        std::cerr << "Failed to load sample_game.py\n";
    } else {
        std::cout << "sample_game.py run successfully!\n";
        Py_XDECREF(pModule);
    }

    Py_Finalize();
    PyConfig_Clear(&config);

    std::cout << "Python finalized. Press Enter to exit...";
    std::cin.get(); // wait for Enter
    return 0;
}