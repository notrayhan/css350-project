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

    int result = PyRun_SimpleString("print('Hello from embedded Python!')");
    std::cout << "PyRun_SimpleString result: " << result << "\n";

    Py_Finalize();
    PyConfig_Clear(&config);

    std::cout << "Python finalized.\n";
    return 0;
}