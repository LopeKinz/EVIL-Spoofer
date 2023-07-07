import ctypes

def spoof_hwids():
    kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
    hdevinfo = kernel32.SetupDiGetClassDevsW(None, None, None, 1 | 2) # DIGCF_ALLCLASSES | DIGCF_PRESENT

    if hdevinfo:
        devinfo_data = ctypes.create_string_buffer(1024)
        devinfo_data.cbSize = ctypes.sizeof(devinfo_data)

        index = 0
        while kernel32.SetupDiEnumDeviceInfo(hdevinfo, index, ctypes.byref(devinfo_data)):
            kernel32.SetupDiSetDeviceRegistryPropertyW(hdevinfo, ctypes.byref(devinfo_data), 9, 'EVIL_HWID', len('EVIL_HWID')*2) # SPDRP_HARDWAREID
            index += 1

        kernel32.SetupDiDestroyDeviceInfoList(hdevinfo)

spoof_hwids()
