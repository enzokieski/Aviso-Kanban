import ctypes
from ctypes import wintypes
import os
import threading
import time

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32
shell32 = ctypes.windll.shell32

LRESULT = ctypes.c_longlong
user32.DefWindowProcW.argtypes = [wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM]
user32.DefWindowProcW.restype = LRESULT

WM_USER = 0x0400
WM_DESTROY = 0x0002
WM_CLOSE = 0x0010
WM_COMMAND = 0x0111
WM_RBUTTONUP = 0x0205
WM_LBUTTONUP = 0x0202
WM_LBUTTONDBLCLK = 0x0203

NIM_ADD = 0x00000000
NIM_MODIFY = 0x00000001
NIM_DELETE = 0x00000002
NIF_MESSAGE = 0x00000001
NIF_ICON = 0x00000002
NIF_TIP = 0x00000004
NIF_INFO = 0x00000010
NIIF_INFO = 0x00000001

IMAGE_ICON = 1
LR_LOADFROMFILE = 0x00000010
LR_DEFAULTSIZE = 0x00000040

TPM_RETURNCMD = 0x0100
TPM_RIGHTBUTTON = 0x0002
MF_STRING = 0x0000
MF_SEPARATOR = 0x0800
MF_DEFAULT = 0x1000

IDI_APPLICATION = 32512

class NOTIFYICONDATAW(ctypes.Structure):
    _fields_ = [
        ('cbSize', wintypes.DWORD),
        ('hWnd', wintypes.HWND),
        ('uID', wintypes.UINT),
        ('uFlags', wintypes.UINT),
        ('uCallbackMessage', wintypes.UINT),
        ('hIcon', wintypes.HICON),
        ('szTip', wintypes.WCHAR * 128),
        ('dwState', wintypes.DWORD),
        ('dwStateMask', wintypes.DWORD),
        ('szInfo', wintypes.WCHAR * 256),
        ('uTimeoutOrVersion', wintypes.UINT),
        ('szInfoTitle', wintypes.WCHAR * 64),
        ('dwInfoFlags', wintypes.DWORD),
        ('guidItem', wintypes.BYTE * 16),
        ('hBalloonIcon', wintypes.HICON),
    ]

WNDPROC = ctypes.WINFUNCTYPE(LRESULT, wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM)

class WNDCLASSEXW(ctypes.Structure):
    _fields_ = [
        ('cbSize', wintypes.UINT),
        ('style', wintypes.UINT),
        ('lpfnWndProc', WNDPROC),
        ('cbClsExtra', ctypes.c_int),
        ('cbWndExtra', ctypes.c_int),
        ('hInstance', wintypes.HINSTANCE),
        ('hIcon', wintypes.HICON),
        ('hCursor', wintypes.HCURSOR),
        ('hbrBackground', wintypes.HBRUSH),
        ('lpszMenuName', wintypes.LPCWSTR),
        ('lpszClassName', wintypes.LPCWSTR),
        ('hIconSm', wintypes.HICON),
    ]

class TrayManager:
    def __init__(self, icon_path=None, tooltip="Kanban Flutuante", on_open=None, on_add=None, on_hide=None, on_config=None, on_quit=None):
        self.icon_path = icon_path
        self.tooltip = tooltip
        self.on_open = on_open
        self.on_add = on_add
        self.on_hide = on_hide
        self.on_config = on_config
        self.on_quit = on_quit
        
        self.hwnd = None
        self.thread = None
        self.running = False
        self.wm_tray = WM_USER + 105
        self.nid = None
        self.hicon = None

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()

    def _load_icon(self):
        if self.icon_path and os.path.exists(self.icon_path):
            hicon = user32.LoadImageW(
                0,
                self.icon_path,
                IMAGE_ICON,
                0,
                0,
                LR_LOADFROMFILE | LR_DEFAULTSIZE
            )
            if hicon:
                return hicon
        return user32.LoadIconW(0, IDI_APPLICATION)

    def _run(self):
        hinst = kernel32.GetModuleHandleW(None)
        class_name = f"KanbanTrayClass_{id(self)}"

        def wnd_proc(hwnd, msg, wparam, lparam):
            if msg == self.wm_tray:
                if lparam in (WM_LBUTTONUP, WM_LBUTTONDBLCLK):
                    if self.on_open:
                        self.on_open()
                    return 0
                elif lparam == WM_RBUTTONUP:
                    self._show_menu(hwnd)
                    return 0
            elif msg == WM_DESTROY:
                user32.PostQuitMessage(0)
                return 0
            return user32.DefWindowProcW(hwnd, msg, wparam, lparam)

        self._wndproc = WNDPROC(wnd_proc)

        wc = WNDCLASSEXW()
        wc.cbSize = ctypes.sizeof(WNDCLASSEXW)
        wc.hInstance = hinst
        wc.lpszClassName = class_name
        wc.lpfnWndProc = self._wndproc

        user32.RegisterClassExW(ctypes.byref(wc))

        self.hwnd = user32.CreateWindowExW(
            0, class_name, "KanbanTrayWin", 0,
            0, 0, 0, 0, 0, 0, hinst, 0
        )

        self.hicon = self._load_icon()

        self.nid = NOTIFYICONDATAW()
        self.nid.cbSize = ctypes.sizeof(NOTIFYICONDATAW)
        self.nid.hWnd = self.hwnd
        self.nid.uID = 1
        self.nid.uFlags = NIF_ICON | NIF_MESSAGE | NIF_TIP
        self.nid.uCallbackMessage = self.wm_tray
        self.nid.hIcon = self.hicon
        self.nid.szTip = self.tooltip[:127]

        shell32.Shell_NotifyIconW(NIM_ADD, ctypes.byref(self.nid))

        msg = wintypes.MSG()
        while self.running and user32.GetMessageW(ctypes.byref(msg), 0, 0, 0) > 0:
            user32.TranslateMessage(ctypes.byref(msg))
            user32.DispatchMessageW(ctypes.byref(msg))

        if self.nid:
            shell32.Shell_NotifyIconW(NIM_DELETE, ctypes.byref(self.nid))
        if self.hwnd:
            user32.DestroyWindow(self.hwnd)
        user32.UnregisterClassW(class_name, hinst)

    def update_tooltip(self, text):
        if not self.hwnd or not self.nid:
            return
        self.nid.szTip = text[:127]
        self.nid.uFlags = NIF_TIP
        shell32.Shell_NotifyIconW(NIM_MODIFY, ctypes.byref(self.nid))

    def show_balloon(self, title, message):
        if not self.hwnd or not self.nid:
            return
        self.nid.uFlags = NIF_INFO
        self.nid.szInfoTitle = title[:63]
        self.nid.szInfo = message[:255]
        self.nid.dwInfoFlags = NIIF_INFO
        shell32.Shell_NotifyIconW(NIM_MODIFY, ctypes.byref(self.nid))

    def _show_menu(self, hwnd):
        pt = wintypes.POINT()
        user32.GetCursorPos(ctypes.byref(pt))
        hmenu = user32.CreatePopupMenu()

        CMD_OPEN = 101
        CMD_ADD = 102
        CMD_HIDE = 103
        CMD_CONFIG = 104
        CMD_QUIT = 105

        user32.AppendMenuW(hmenu, MF_STRING, CMD_OPEN, "💬 Abrir Kanban")
        user32.AppendMenuW(hmenu, MF_STRING, CMD_ADD, "➕ Nova Tarefa")
        user32.AppendMenuW(hmenu, MF_STRING, CMD_HIDE, "👁️ Ocultar Kanban")
        user32.AppendMenuW(hmenu, MF_SEPARATOR, 0, None)
        user32.AppendMenuW(hmenu, MF_STRING, CMD_CONFIG, "⚙️ Intervalo (15 min)...")
        user32.AppendMenuW(hmenu, MF_SEPARATOR, 0, None)
        user32.AppendMenuW(hmenu, MF_STRING, CMD_QUIT, "❌ Sair do Sistema")

        user32.SetForegroundWindow(hwnd)
        cmd = user32.TrackPopupMenu(hmenu, TPM_RETURNCMD | TPM_RIGHTBUTTON, pt.x, pt.y, 0, hwnd, None)
        user32.PostMessageW(hwnd, 0, 0, 0)
        user32.DestroyMenu(hmenu)

        if cmd == CMD_OPEN and self.on_open:
            self.on_open()
        elif cmd == CMD_ADD and self.on_add:
            self.on_add()
        elif cmd == CMD_HIDE and self.on_hide:
            self.on_hide()
        elif cmd == CMD_CONFIG and self.on_config:
            self.on_config()
        elif cmd == CMD_QUIT and self.on_quit:
            self.on_quit()

    def stop(self):
        self.running = False
        if self.hwnd:
            user32.PostMessageW(self.hwnd, WM_CLOSE, 0, 0)

