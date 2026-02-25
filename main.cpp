#include <Python.h>
#include <iostream>
#include <string>
#include <windows.h>

std::wstring GetExeFolder() {
    wchar_t buffer[MAX_PATH];
    GetModuleFileNameW(NULL, buffer, MAX_PATH);
    std::wstring exePath(buffer);
    size_t pos = exePath.find_last_of(L"\\/");
    return exePath.substr(0, pos);
}

int main() {
    std::cout << "=== Starting embedded Python ===\n";

    std::wstring exeFolder = GetExeFolder();
    std::wstring pythonHomeW = exeFolder + L"\\python";
    std::wstring pythonLibW  = pythonHomeW + L"\\Lib";

    std::wcout << L"Python home: " << pythonHomeW << L"\n";
    std::wcout << L"Python Lib : " << pythonLibW << L"\n";

    PyStatus status;
    PyConfig config;
    PyConfig_InitPythonConfig(&config);

    // following line turns on manual specification for lib path
    // see line 39
    // config.module_search_paths_set = 1;

    // keep this disabled (0), unless necessary
    config.site_import = 0; // ensures library deletions do not affect run

    // set python home and program name
    PyConfig_SetString(&config, &config.home, pythonHomeW.c_str());
    PyConfig_SetString(&config, &config.program_name, L"launcher");

    // PyWideStringList_Append(&config.module_search_paths, pythonLibW.c_str()); // manual lib pathing

    status = Py_InitializeFromConfig(&config);
    if (PyStatus_Exception(status)) {
        std::cerr << "Python failed to initialize!\n";
        PyConfig_Clear(&config);
        return 1;
    }

    std::cout << "Python initialized successfully!\n";

    // More UTF-16 to UTF-8 conversion nonsense
    // apparantly forcing UTF-8 conversion from its parent language is highly pythonic
    int size_needed = WideCharToMultiByte(CP_UTF8, 0, pythonHomeW.c_str(), -1, NULL, 0, NULL, NULL);
    std::string pythonHomeUtf8(size_needed, 0);
    WideCharToMultiByte(CP_UTF8, 0, pythonHomeW.c_str(), -1, &pythonHomeUtf8[0], size_needed, NULL, NULL);
    // remove the extra null terminator at the end
    if (!pythonHomeUtf8.empty() && pythonHomeUtf8.back() == '\0') pythonHomeUtf8.pop_back();

    // Add the python folder to sys.path
    std::string addPathCmd = "import sys; sys.path.insert(0, r'" + pythonHomeUtf8 + "')";
    PyRun_SimpleString(addPathCmd.c_str());

    // The game run command
    // replace "sample_game" with any .py runnable
    PyObject* pName = PyUnicode_FromString("sample_game"); // filename without .py
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

    std::cout << "Python finalized.\n";
    return 0;
}