"""Non-destructive process existence probe (local integration addition)."""
import errno
import os


def _windows_pid_alive(pid):
    import ctypes
    from ctypes import wintypes
    kernel = ctypes.WinDLL('kernel32', use_last_error=True)
    kernel.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
    kernel.OpenProcess.restype = wintypes.HANDLE
    kernel.WaitForSingleObject.argtypes = [wintypes.HANDLE, wintypes.DWORD]
    kernel.WaitForSingleObject.restype = wintypes.DWORD
    kernel.CloseHandle.argtypes = [wintypes.HANDLE]
    kernel.CloseHandle.restype = wintypes.BOOL
    handle = kernel.OpenProcess(0x00100000, False, pid)  # SYNCHRONIZE only
    if not handle:
        code = ctypes.get_last_error()
        if code == 87:  # ERROR_INVALID_PARAMETER: no such positive PID
            return False
        raise ctypes.WinError(code)  # denied/unknown must not mean "gone"
    try:
        status = kernel.WaitForSingleObject(handle, 0)
        if status == 258: return True   # WAIT_TIMEOUT: still running
        if status == 0: return False    # WAIT_OBJECT_0: process terminated
        raise ctypes.WinError(ctypes.get_last_error())
    finally:
        kernel.CloseHandle(handle)


def pid_alive(pid):
    if isinstance(pid, bool): raise ValueError('PID must be a positive integer')
    try:
        parsed = int(pid)
    except (ValueError, TypeError, OverflowError):
        raise ValueError('PID must be a positive integer') from None
    if parsed <= 0 or str(parsed) != str(pid):
        raise ValueError('PID must be a positive integer')
    if os.name == 'nt': return _windows_pid_alive(parsed)
    try:
        os.kill(parsed, 0)  # POSIX existence probe only
        return True
    except OSError as error:
        if error.errno == errno.ESRCH: return False
        if error.errno == errno.EPERM: return True
        raise
