import ctypes

def spoof_hwids():
    kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
    hdevinfo = kernel32.SetupDiGetClassDevsW(None, None, None, 1 | 2) # DIGCF_ALLCLASSES | DIGCF_PRESENT

    if hdevinfo:
        devinfo_data = ctypes.create_string_buffer(1024)
        devinfo_data.cbSize = ctypes.sizeof(devinfo_data)

        index = 0
        while kernel32.SetupDiEnumDeviceInfo(hdevinfo, index, ctypes.byref(devinfo_data)):
            original_hwid = ctypes.create_unicode_buffer(256)
            kernel32.SetupDiGetDeviceRegistryPropertyW(hdevinfo, ctypes.byref(devinfo_data), 9, None, original_hwid, 256, None) # SPDRP_HARDWAREID

            # Save original HWID for revert
            original_hwid_str = original_hwid.value

            # Spoof HWID with evil value
            kernel32.SetupDiSetDeviceRegistryPropertyW(hdevinfo, ctypes.byref(devinfo_data), 9, 'EVIL_HWID', len('EVIL_HWID')*2) # SPDRP_HARDWAREID
            index += 1

        kernel32.SetupDiDestroyDeviceInfoList(hdevinfo)

        # Store original HWIDs for revert
        with open('original_hwids.txt', 'w') as f:
            f.write(original_hwid_str)

def revert_hwids():
    kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
    hdevinfo = kernel32.SetupDiGetClassDevsW(None, None, None, 1 | 2) # DIGCF_ALLCLASSES | DIGCF_PRESENT

    if hdevinfo:
        devinfo_data = ctypes.create_string_buffer(1024)
        devinfo_data.cbSize = ctypes.sizeof(devinfo_data)

        index = 0
        with open('original_hwids.txt', 'r') as f:
            original_hwid_str = f.read()

        while kernel32.SetupDiEnumDeviceInfo(hdevinfo, index, ctypes.byref(devinfo_data)):
            kernel32.SetupDiSetDeviceRegistryPropertyW(hdevinfo, ctypes.byref(devinfo_data), 9, original_hwid_str, len(original_hwid_str)*2) # SPDRP_HARDWAREID
            index += 1

        kernel32.SetupDiDestroyDeviceInfoList(hdevinfo)

def main():
    while True:
        print("--- Evil HWID Spoofer Menu ---")
        print("1. Spoof HWIDs")
        print("2. Revert HWIDs")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            spoof_hwids()
            print("HWIDs spoofed! Embrace the chaos!")
        elif choice == "2":
            revert_hwids()
            print("HWIDs reverted! Order is restored!")
        elif choice == "0":
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
