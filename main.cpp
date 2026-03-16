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

    // print file paths for python home and lib
    // std::wcout << L"Python home: " << pythonHomeW << L"\n";
    // std::wcout << L"Python Lib : " << pythonLibW << L"\n";

    PyStatus status;
    PyConfig config;
    PyConfig_InitPythonConfig(&config);


    config.site_import = 1; // ensure site packages are found

    // set python home and program name
    PyConfig_SetString(&config, &config.home, pythonHomeW.c_str());
    PyConfig_SetString(&config, &config.program_name, L"launcher");


    status = Py_InitializeFromConfig(&config);
    if (PyStatus_Exception(status)) {
        std::cerr << "Python failed to initialize!\n";
        PyConfig_Clear(&config);
        return 1;
    }

    // Manual sys.path append
    PyRun_SimpleString("import sys; sys.path.insert(0, r'path_to_extra_libs')");

    

    std::cout << "Python initialized successfully!\n";

    PyRun_SimpleString("import pygame; print('pygame imported successfully')");


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
    // replace "main" with any .py runnable entrypoint
    PyObject* pName = PyUnicode_FromString("main"); // filename without .py
    PyObject* pModule = PyImport_Import(pName);
    Py_XDECREF(pName);

    if (pModule == nullptr) {
        PyErr_Print();
        std::cerr << "Failed to load main.py\n";
    } else {
        std::cout << "main.py run successfully!\n";
        Py_XDECREF(pModule);
    }

    Py_Finalize();
    PyConfig_Clear(&config);
    
    std::cout << "Python finalized. Press Enter to exit...";
    std::cin.get(); // waits for Enter
    return 0;
}