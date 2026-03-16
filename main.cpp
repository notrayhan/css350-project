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

    // Top-level python folder (contains python3.12 and lib/)
    std::string pythonHome = exeFolder + "/python";

    // Standard library + site-packages (includes pygame)
    std::string pythonLib  = pythonHome + "/lib";

    // Game scripts folder
    std::string gameFolder = pythonHome + "/game";

    PyStatus status;
    PyConfig config;
    PyConfig_InitPythonConfig(&config);

    config.site_import = 1; // ensure site packages are found

    // Set Python home and program name
    PyConfig_SetString(&config, &config.home, pythonHome.c_str());
    PyConfig_SetString(&config, &config.program_name, "launcher");

    status = Py_InitializeFromConfig(&config);
    if (PyStatus_Exception(status)) {
        std::cerr << "Python failed to initialize!\n";
        PyConfig_Clear(&config);
        return 1;
    }

    // Append game folder to sys.path first
    std::string addPathCmd = "import sys; sys.path.insert(0, r'" + gameFolder + "')";
    PyRun_SimpleString(addPathCmd.c_str());

    // Append Python lib folder to sys.path
    addPathCmd = "import sys; sys.path.insert(0, r'" + pythonLib + "')";
    PyRun_SimpleString(addPathCmd.c_str());

    std::cout << "Python initialized successfully!\n";

    // Test Pygame import
    PyRun_SimpleString("import pygame; print('pygame imported successfully')");

    // Import and run your game
    PyObject* pName = PyUnicode_FromString("tetris"); // your game script (without .py)
    PyObject* pModule = PyImport_Import(pName);
    Py_XDECREF(pName);

    if (pModule == nullptr) {
        PyErr_Print();
        std::cerr << "Failed to load tetris.py\n";
    } else {
        std::cout << "tetris.py run successfully!\n";
        Py_XDECREF(pModule);
    }

    Py_Finalize();
    PyConfig_Clear(&config);

    std::cout << "Python finalized. Press Enter to exit...";
    std::cin.get(); // wait for Enter
    return 0;
}