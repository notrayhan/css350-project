#include <Python.h>
#include <iostream>
#include <string>
#include <locale>
#include <codecvt>
#include <windows.h>

std::wstring GetExeFolder() {
    wchar_t buffer[MAX_PATH];
    GetModuleFileNameW(NULL, buffer, MAX_PATH);
    std::wstring exePath(buffer);
    size_t pos = exePath.find_last_of(L"\\/");
    return exePath.substr(0, pos);
}

int main() {
    std::cout << "=== Starting embedded Python debug2 ===\n";

    std::wstring exeFolder = GetExeFolder();
    std::wstring pythonHomeW = exeFolder + L"\\python";
    std::wstring pythonLibW  = pythonHomeW + L"\\Lib";

    // Convert wide string to UTF-8
    std::wstring_convert<std::codecvt_utf8_utf16<wchar_t>> converter;
    std::string pythonHome = converter.to_bytes(pythonHomeW);
    std::string pythonLib  = converter.to_bytes(pythonLibW);

    std::cout << "Python home (UTF-8): " << pythonHome << "\n";
    std::cout << "Python Lib (UTF-8): " << pythonLib << "\n";

    PyStatus status;
    PyConfig config;
    PyConfig_InitPythonConfig(&config);

    // Disable automatic path configuration
    config.module_search_paths_set = 1;

    // Set Python home and program name
    config.home = Py_DecodeLocale(pythonHome.c_str(), nullptr);
    config.program_name = Py_DecodeLocale((pythonHome + "\\python.exe").c_str(), nullptr);

    // Explicitly tell Python where to search for modules
    wchar_t* libPath = Py_DecodeLocale(pythonLib.c_str(), nullptr);
    PyWideStringList_Append(&config.module_search_paths, libPath);

    // (Optional but helpful)
    config.site_import = 0;  // disable site.py during testing

    // Initialize Python
    status = Py_InitializeFromConfig(&config);
    if (PyStatus_Exception(status)) {
        std::cerr << "Python failed to initialize!\n";
        Py_ExitStatusException(status);
        return 1;
    }

    std::cout << "Python initialized successfully!\n";

    // Run a test Python command
    // This is where we can run any python script, including our game
    int result = PyRun_SimpleString("print('Hello from embedded Python!')");
    std::cout << "PyRun_SimpleString result: " << result << "\n";

    Py_Finalize();
    std::cout << "Python finalized.\n";
    return 0;
}