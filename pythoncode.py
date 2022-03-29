import win32process
import ctypes
from win32gui import FindWindow
from ctypes import c_long , c_int , c_void_p, windll, WinDLL, c_ulonglong, byref,c_ulong,c_wchar_p

ntdll = WinDLL("ntdll.dll")
kernel32 = ctypes.windll.LoadLibrary("kernel32.dll")
GetLastError = kernel32.GetLastError
STANDARD_RIGHTS_REQUIRED = 0x000F0000
SYNCHRONIZE = 0x00100000
PROCESS_ALL_ACCESS = (STANDARD_RIGHTS_REQUIRED | SYNCHRONIZE | 0xFFF)

class PROCESS_BASIC_INFORMATION(ctypes.Structure):
    _fields_ = [('ExitStatus', ctypes.c_ulonglong),
                ('PebBaseAddress', ctypes.c_ulonglong),
                ('AffinityMask', ctypes.c_ulonglong),
                ('BasePriority', ctypes.c_ulonglong),
                ('UniqueProcessId', ctypes.c_ulonglong),
                ('InheritedFromUniqueProcessId', ctypes.c_ulonglong)]

## OpenProcess
OpenProcess = windll.kernel32.OpenProcess
OpenProcess.argtypes = [c_void_p, c_int, c_long]
OpenProcess.rettype = c_long
## CloseHandle
CloseHandle = windll.kernel32.CloseHandle
CloseHandle.argtypes = [c_void_p]
CloseHandle.rettype = c_int

def _GetProcessId(className,windowName):
    hGameWindow = FindWindow(className, windowName)
    pid = win32process.GetWindowThreadProcessId(hGameWindow)[1]
    return pid

def _GetPorcessHandle(pid):
    hGameHandle = OpenProcess(PROCESS_ALL_ACCESS, 0, pid)
    return hGameHandle

ProcessId = _GetProcessId("UnrealWindow", u"Combat Seasonal Event - High Score Mini-Challenge  ")
_hGameHandle = _GetPorcessHandle(ProcessId)

def _ReadMemeryLong64(addr, bufflength):
    addr = c_ulonglong(addr)
    ret = c_ulonglong()
    BufferLength = c_ulonglong(bufflength)
    ntdll.ZwWow64ReadVirtualMemory64(int(_hGameHandle), addr, byref(ret), BufferLength, 0)
    return ret.value

def WriteMemeryLong64(addr, bufflength, n):
    addr = c_ulonglong(addr)
    ret = c_ulonglong(bufflength)
    BufferLength = c_ulonglong(n)
    ntdll.ZwWow64WriteVirtualMemory64(int(_hGameHandle), addr, byref(ret), BufferLength, 0)

def ReadProcessMemory64_Wchar(addr, n,length):
    addr = c_ulonglong(addr)
    ret = c_wchar_p("0" * length)
    BufferLength = c_ulonglong(n)
    ntdll.NtWow64ReadVirtualMemory64(int(_hGameHandle), addr, ret, BufferLength, 0)
    return ret.value

def GetBaseAddr(ModuleName):
    NumberOfBytesRead = c_ulong()
    Buffer = PROCESS_BASIC_INFORMATION()
    Size = c_ulong(48)
    name_len = len(ModuleName)

    ntdll.NtWow64QueryInformationProcess64(int(_hGameHandle), 0, byref(Buffer), Size, byref(NumberOfBytesRead))
    ret = _ReadMemeryLong64(Buffer.PebBaseAddress + 24, 8)
    ret = _ReadMemeryLong64(ret + 24, 8)

    for i in range(100000):
        modulehandle = _ReadMemeryLong64(ret + 48, 8)
        if modulehandle == 0:
            break
        nameaddr = _ReadMemeryLong64(ret + 96, 8)
        name = ReadProcessMemory64_Wchar(nameaddr, name_len * 2 + 1, name_len)
        if name == ModuleName:
            return modulehandle
        ret = _ReadMemeryLong64(ret + 8, 8)

def get_green_ball(hGameHandle,baseadder):
    value = baseadder + 0x04A3C6E0
    value1 = _ReadMemeryLong64(value,8)
    value2 = _ReadMemeryLong64(value1+0x8,8)
    value3 = _ReadMemeryLong64(value2+0x60,8)
    value4 = _ReadMemeryLong64(value3+0x80,8)
    value5 = _ReadMemeryLong64(value4+0x278,8)
    value6 = _ReadMemeryLong64(value5+0x8, 8)
    return value6

def set_green_ball(hGameHandle,baseadder,score):
    value = baseadder + 0x04A3C6E0
    value1 = _ReadMemeryLong64(value,8)
    value2 = _ReadMemeryLong64(value1+0x8,8)
    value3 = _ReadMemeryLong64(value2+0x60,8)
    value4 = _ReadMemeryLong64(value3+0x80,8)
    value5 = _ReadMemeryLong64(value4+0x278,8)
    WriteMemeryLong64(value5+0x8, score, 4)

def get_blue_ball(hGameHandle,baseadder):
    value = baseadder + 0x04617D40
    value1 = _ReadMemeryLong64(value,8)
    value2 = _ReadMemeryLong64(value1+0x120,8)
    value3 = _ReadMemeryLong64(value2+0xD0,8)
    value4 = _ReadMemeryLong64(value3+0x10,8)
    value5 = _ReadMemeryLong64(value4+0x2A8,8)
    value6 = _ReadMemeryLong64(value5+0x20, 8)
    return value6

def set_blue_ball(hGameHandle,baseadder,score):
    value = baseadder + 0x04617D40
    value1 = _ReadMemeryLong64(value, 8)
    value2 = _ReadMemeryLong64(value1 + 0x120, 8)
    value3 = _ReadMemeryLong64(value2 + 0xD0, 8)
    value4 = _ReadMemeryLong64(value3 + 0x10, 8)
    value5 = _ReadMemeryLong64(value4 + 0x2A8, 8)
    WriteMemeryLong64(value5+0x20, score, 4)

def get_yellow_ball(hGameHandle,baseadder):
    value = baseadder + 0x04A3C6E0
    value1 = _ReadMemeryLong64(value,8)
    value2 = _ReadMemeryLong64(value1+0x8,8)
    value3 = _ReadMemeryLong64(value2+0x60,8)
    value4 = _ReadMemeryLong64(value3+0x80,8)
    value5 = _ReadMemeryLong64(value4+0x278,8)
    value6 = _ReadMemeryLong64(value5+0x38, 8)
    return value6

def set_yellow_ball(hGameHandle,baseadder,score):
    value = baseadder + 0x04A3C6E0
    value1 = _ReadMemeryLong64(value, 8)
    value2 = _ReadMemeryLong64(value1 + 0x8, 8)
    value3 = _ReadMemeryLong64(value2 + 0x60, 8)
    value4 = _ReadMemeryLong64(value3 + 0x80, 8)
    value5 = _ReadMemeryLong64(value4 + 0x278, 8)
    WriteMemeryLong64(value5+0x38, score, 4)

def get_score(hGameHandle,baseadder):
    value = baseadder + 0x045E8010
    value1 = _ReadMemeryLong64(value,8)
    value2 = _ReadMemeryLong64(value1+0x8,8)
    value3 = _ReadMemeryLong64(value2+0x20,8)
    value4 = _ReadMemeryLong64(value3+0x180,8)
    value5 = _ReadMemeryLong64(value4+0x198,8)
    value6 = _ReadMemeryLong64(value5+0x1BC, 8)
    return value6

def set_score(hGameHandle,baseadder,score):
    value = baseadder + 0x045E8010
    value1 = _ReadMemeryLong64(value, 8)
    value2 = _ReadMemeryLong64(value1 + 0x8, 8)
    value3 = _ReadMemeryLong64(value2 + 0x20, 8)
    value4 = _ReadMemeryLong64(value3 + 0x180, 8)
    value5 = _ReadMemeryLong64(value4 + 0x198, 8)
    WriteMemeryLong64(value5+0x1BC, score, 4)
def main():
    moudle = GetBaseAddr("Ascenders_CombatDemo-Win64-Shipping.exe")

    greenScore = get_green_ball(_hGameHandle, moudle)
    print('greenScore:' + str(greenScore))
    blueScore = get_blue_ball(_hGameHandle, moudle)
    print('blueScore:' + str(blueScore))
    yellowScore = get_yellow_ball(_hGameHandle, moudle)
    print('yellowScore:' + str(yellowScore))
    score = get_score(_hGameHandle, moudle)
    print('total score:' + str(score))

    greenScore = 654
    print('Modify the greenScore to:' + str(greenScore))
    set_green_ball(_hGameHandle,moudle,greenScore)
    blueScore = 352
    print('Modify the blueScore to:' + str(blueScore))
    set_blue_ball(_hGameHandle, moudle, blueScore)
    yellowScore = 20
    print('Modify the yellowScore to:' + str(yellowScore))
    set_yellow_ball(_hGameHandle, moudle, yellowScore)

    score = greenScore * 6 + blueScore * 13 + yellowScore * 25
    print('Modify the total score to:' + str(score))
    set_score(_hGameHandle, moudle, score)


    CloseHandle(_hGameHandle)

if __name__ == '__main__':
    main()
