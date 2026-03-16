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
    // buffer now contains the path, dirname() extracts the folder
    return std::string(dirname(buffer));
}

int main() {
    std::cout << "=== Starting embedded Python ===\n";

    std::string exeFolder = GetExeFolder();
    if (exeFolder.empty()) return 1;

    std::string pythonHomeStr = exeFolder + "/python";
    std::string pythonLibStr  = pythonHomeStr + "/lib/python3.12";

    // Convert to wide strings for Python API
    std::wstring pythonHome(pythonHomeStr.begin(), pythonHomeStr.end());
    std::wstring programName = L"launcher";

    PyStatus status;
    PyConfig config;
    PyConfig_InitPythonConfig(&config);

    config.site_import = 1;

    // Python requires wchar_t*
    PyConfig_SetString(&config, &config.home, pythonHome.c_str());
    PyConfig_SetString(&config, &config.program_name, programName.c_str());

    status = Py_InitializeFromConfig(&config);

    if (PyStatus_Exception(status)) {
        std::cerr << "Python failed to initialize!\n";
        PyConfig_Clear(&config);
        return 1;
    }

    std::cout << "Python initialized successfully!\n";

    // Add python lib to sys.path
    std::string addPathCmd =
        "import sys; sys.path.insert(0, r'" + pythonLibStr + "')";
    PyRun_SimpleString(addPathCmd.c_str());

    // Add game folder
    std::string gameFolder = exeFolder + "/python";
    addPathCmd =
        "import sys; sys.path.insert(0, r'" + gameFolder + "')";
    PyRun_SimpleString(addPathCmd.c_str());

    PyRun_SimpleString("import pygame; print('pygame imported successfully')");

    // Import and run the python game
    PyObject* pName = PyUnicode_FromString("sample_game");
    PyObject* pModule = PyImport_Import(pName);

    Py_XDECREF(pName);

    if (pModule == nullptr) {
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