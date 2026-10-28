import ctypes
from ctypes import wintypes
import os
import sys
import tkinter as tk

from config import ICON_FILE
from kanban_app import KanbanApp
from tray_manager import TrayManager

# Constantes Win32 para instância única
ERROR_ALREADY_EXISTS = 183
kernel32 = ctypes.windll.kernel32

def create_single_instance_mutex(mutex_name="Global\\KanbanBaloesAvisosMutex_v1"):
    """
    Garante que apenas uma instância do Kanban esteja rodando ao mesmo tempo.
    """
    mutex = kernel32.CreateMutexW(None, False, mutex_name)
    last_error = kernel32.GetLastError()
    if last_error == ERROR_ALREADY_EXISTS:
        return None
    return mutex

def main():
    # Verifica instância única
    mutex = create_single_instance_mutex()
    if not mutex:
        print("Uma instância do Kanban já está em execução.")
        # Se já estiver rodando, podemos apenas sair
        sys.exit(0)

    root = tk.Tk()

    # Criação do gerenciador da bandeja do Windows (System Tray)
    app = None
    tray = None

    def on_tray_open():
        if app:
            root.after(0, app.show_window)

    def on_tray_add():
        if app:
            root.after(0, lambda: app.open_new_task_dialog("fazer"))

    def on_tray_hide():
        if app:
            root.after(0, app.hide_window)

    def on_tray_config():
        if app:
            root.after(0, app.open_settings_dialog)

    def on_tray_quit():
        if app:
            root.after(0, app.quit_app)

    tray = TrayManager(
        icon_path=ICON_FILE,
        tooltip="Kanban Flutuante (Aviso a cada 15 min)",
        on_open=on_tray_open,
        on_add=on_tray_add,
        on_hide=on_tray_hide,
        on_config=on_tray_config,
        on_quit=on_tray_quit
    )

    app = KanbanApp(root, tray_manager=tray)

    # Inicia o ícone na bandeja em segundo plano
    tray.start()

    try:
        root.mainloop()
    finally:
        if tray:
            tray.stop()

if __name__ == "__main__":
    main()

