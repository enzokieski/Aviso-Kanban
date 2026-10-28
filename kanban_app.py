import os
import sys
import time
import tkinter as tk
from tkinter import messagebox
import winsound

from config import (
    CHROMA_BG, COLOR_WHITE, COLOR_TEXT_MAIN, COLOR_TEXT_MUTED,
    COLOR_BORDER, COLUMNS, WINDOW_WIDTH, WINDOW_HEIGHT
)
from storage import KanbanStorage
from bubble_widgets import (
    BubbleCard, ColumnHeaderBubble, ScrollableColumn,
    TaskDialog, SettingsDialog
)

class KanbanApp:
    def __init__(self, root, tray_manager=None):
        self.root = root
        self.tray = tray_manager
        self.storage = KanbanStorage()
        self.is_visible = True

        # Timer de 15 minutos (em segundos)
        self.interval_minutes = self.storage.get_setting("interval_minutes", 15)
        self.remaining_seconds = self.interval_minutes * 60

        # Configuração da janela transparente
        self._setup_window()

        # Montagem dos componentes da interface
        self._build_top_bar()
        self._build_kanban_columns()

        # Renderiza as tarefas salvas
        self.reload_tasks()

        # Inicia o loop do timer de 15 minutos
        self._start_timer()

        # Atalhos de teclado
        self.root.bind("<Escape>", lambda e: self.hide_window())
        self.root.bind("<Control-n>", lambda e: self.open_new_task_dialog())
        self.root.bind("<Control-N>", lambda e: self.open_new_task_dialog())

    def _setup_window(self):
        self.root.title("Kanban Flutuante - Balões")
        self.root.overrideredirect(True)              # Sem bordas padrão do Windows
        self.root.attributes('-transparentcolor', CHROMA_BG)  # Transparência total no fundo
        self.root.attributes('-topmost', True)         # Fica sobreposto às outras janelas
        self.root.configure(bg=CHROMA_BG)

        # Restaura posição anterior ou centraliza
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        
        saved_x = self.storage.get_setting("window_x")
        saved_y = self.storage.get_setting("window_y")

        if saved_x is not None and saved_y is not None:
            # Validação para garantir que não fique fora da tela visível
            x = max(0, min(saved_x, sw - WINDOW_WIDTH))
            y = max(0, min(saved_y, sh - WINDOW_HEIGHT))
        else:
            x = (sw - WINDOW_WIDTH) // 2
            y = (sh - WINDOW_HEIGHT) // 2

        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")

    def _build_top_bar(self):
        """
        Barra de controle superior com fundo branco sólido em formato de balão flutuante.
        Permite arrastar a janela pela tela e contém os controles principais.
        """
        self.top_bar_container = tk.Frame(self.root, bg=CHROMA_BG)
        self.top_bar_container.pack(fill="x", padx=16, pady=(12, 8))

        # Balão branco da barra superior
        self.top_bubble = tk.Frame(
            self.top_bar_container,
            bg=COLOR_WHITE,
            highlightbackground=COLOR_BORDER,
            highlightthickness=1.5,
            padx=16,
            pady=8
        )
        self.top_bubble.pack(fill="x")

        # Ícone e Título
        self.lbl_title = tk.Label(
            self.top_bubble,
            text="💭 KANBAN DE TAREFAS",
            font=("Segoe UI", 11, "bold"),
            bg=COLOR_WHITE,
            fg=COLOR_TEXT_MAIN,
            cursor="fleur"
        )
        self.lbl_title.pack(side="left")

        # Indicador de tempo do próximo aviso
        self.lbl_timer = tk.Label(
            self.top_bubble,
            text=self._format_timer_text(),
            font=("Segoe UI", 9, "bold"),
            bg="#F1F5F9",
            fg="#2563EB",
            padx=10,
            pady=3,
            cursor="fleur"
        )
        self.lbl_timer.pack(side="left", padx=16)

        # Botão: Sair do Sistema
        btn_quit = tk.Button(
            self.top_bubble,
            text="✕",
            font=("Segoe UI", 9, "bold"),
            bg=COLOR_WHITE,
            fg="#94A3B8",
            activebackground="#FEE2E2",
            activeforeground="#DC2626",
            bd=0,
            padx=8,
            pady=2,
            cursor="hand2",
            command=self.confirm_exit
        )
        btn_quit.pack(side="right", padx=(4, 0))

        # Botão: Ocultar para Segundo Plano (ESC)
        btn_hide = tk.Button(
            self.top_bubble,
            text="👁️ Ocultar (ESC)",
            font=("Segoe UI", 9),
            bg="#F8FAFC",
            fg="#475569",
            activebackground="#E2E8F0",
            bd=1,
            relief="solid",
            highlightthickness=0,
            padx=10,
            pady=2,
            cursor="hand2",
            command=self.hide_window
        )
        btn_hide.pack(side="right", padx=(4, 4))

        # Botão: Configurações de Tempo
        self.btn_config = tk.Button(
            self.top_bubble,
            text=f"⚙️ {self.interval_minutes} min",
            font=("Segoe UI", 9),
            bg="#F8FAFC",
            fg="#475569",
            activebackground="#E2E8F0",
            bd=1,
            relief="solid",
            highlightthickness=0,
            padx=10,
            pady=2,
            cursor="hand2",
            command=self.open_settings_dialog
        )
        self.btn_config.pack(side="right", padx=(4, 4))

        # Botão: Nova Tarefa
        btn_new = tk.Button(
            self.top_bubble,
            text="➕ Nova Tarefa",
            font=("Segoe UI", 9, "bold"),
            bg="#2563EB",
            fg=COLOR_WHITE,
            activebackground="#1D4ED8",
            activeforeground=COLOR_WHITE,
            bd=0,
            padx=12,
            pady=3,
            cursor="hand2",
            command=self.open_new_task_dialog
        )
        btn_new.pack(side="right", padx=(4, 8))

        # Funcionalidade de arrastar a janela segurando a barra superior
        self._bind_drag(self.top_bubble)
        self._bind_drag(self.lbl_title)
        self._bind_drag(self.lbl_timer)

    def _bind_drag(self, widget):
        widget.bind("<Button-1>", self._on_drag_start)
        widget.bind("<B1-Motion>", self._on_drag_motion)
        widget.bind("<ButtonRelease-1>", self._on_drag_end)

    def _on_drag_start(self, event):
        self._drag_start_x = event.x_root - self.root.winfo_x()
        self._drag_start_y = event.y_root - self.root.winfo_y()

    def _on_drag_motion(self, event):
        x = event.x_root - self._drag_start_x
        y = event.y_root - self._drag_start_y
        self.root.geometry(f"+{x}+{y}")

    def _on_drag_end(self, event):
        self.storage.save_window_pos(self.root.winfo_x(), self.root.winfo_y())

    def _build_kanban_columns(self):
        """
        Cria as 3 colunas principais: Fazer, Fazendo, Feito.
        O fundo entre os balões é completamente transparente.
        """
        self.columns_container = tk.Frame(self.root, bg=CHROMA_BG)
        self.columns_container.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        self.col_widgets = {}

        for col_key in ["fazer", "fazendo", "feito"]:
            col_frame = tk.Frame(self.columns_container, bg=CHROMA_BG)
            col_frame.pack(side="left", fill="both", expand=True, padx=6)

            # Cabeçalho da coluna em formato de balão
            header = ColumnHeaderBubble(
                col_frame,
                col_key=col_key,
                count=0,
                on_add=self.open_new_task_dialog if col_key == "fazer" else None,
                on_clear=self.clear_completed_tasks if col_key == "feito" else None
            )
            header.pack(fill="x", pady=(0, 8))

            # Área rolável para os balões de tarefas
            scrollable = ScrollableColumn(col_frame)
            scrollable.pack(fill="both", expand=True)

            self.col_widgets[col_key] = {
                "header": header,
                "scrollable": scrollable
            }

    def reload_tasks(self):
        """
        Recarrega todas as tarefas salvas do arquivo JSON e atualiza os balões na tela.
        """
        tasks = self.storage.get_tasks()

        for col_key, widgets in self.col_widgets.items():
            scroll_frame = widgets["scrollable"].scrollable_frame
            # Limpa tarefas antigas da coluna
            for child in scroll_frame.winfo_children():
                child.destroy()

            # Filtra tarefas desta coluna
            col_tasks = [t for t in tasks if t.get("column") == col_key]
            widgets["header"].update_count(len(col_tasks))

            if not col_tasks:
                # Mensagem vazia sutil
                empty_lbl = tk.Label(
                    scroll_frame,
                    text="Nenhuma tarefa aqui",
                    font=("Segoe UI", 8, "italic"),
                    bg=CHROMA_BG,
                    fg="#64748B"
                )
                empty_lbl.pack(pady=15)
            else:
                for task in col_tasks:
                    card = BubbleCard(
                        scroll_frame,
                        task=task,
                        on_move=self.move_task,
                        on_edit=self.edit_task,
                        on_delete=self.delete_task
                    )
                    card.pack(fill="x", padx=2, pady=2)

    def move_task(self, task_id, new_column):
        if self.storage.update_task_column(task_id, new_column):
            self.reload_tasks()

    def delete_task(self, task_id):
        if self.storage.delete_task(task_id):
            self.reload_tasks()

    def clear_completed_tasks(self):
        if messagebox.askyesno("Limpar Concluídos", "Deseja remover todas as tarefas da coluna 'Feito'?", parent=self.root):
            self.storage.clear_completed()
            self.reload_tasks()

    def open_new_task_dialog(self, default_col="fazer"):
        self.show_window()
        TaskDialog(
            self.root,
            task=None,
            default_column=default_col,
            on_save=self._save_new_task
        )

    def _save_new_task(self, title, desc, col, prio, _original_task=None):
        self.storage.add_task(title=title, description=desc, column=col, priority=prio)
        self.reload_tasks()

    def edit_task(self, task):
        self.show_window()
        TaskDialog(
            self.root,
            task=task,
            default_column=task.get("column", "fazer"),
            on_save=self._save_edited_task
        )

    def _save_edited_task(self, title, desc, col, prio, original_task):
        task_id = original_task["id"]
        self.storage.edit_task(task_id, title=title, description=desc, priority=prio)
        if original_task.get("column") != col:
            self.storage.update_task_column(task_id, col)
        self.reload_tasks()

    def open_settings_dialog(self):
        self.show_window()
        SettingsDialog(self.root, self.storage, on_update=self._on_settings_updated)

    def _on_settings_updated(self):
        self.interval_minutes = self.storage.get_setting("interval_minutes", 15)
        self.remaining_seconds = self.interval_minutes * 60
        self.btn_config.config(text=f"⚙️ {self.interval_minutes} min")
        self.lbl_timer.config(text=self._format_timer_text())

    def _format_timer_text(self):
        m = self.remaining_seconds // 60
        s = self.remaining_seconds % 60
        return f"⏰ Próximo aviso em: {m:02d}:{s:02d}"

    def _start_timer(self):
        self._tick()

    def _tick(self):
        """
        Executado a cada 1 segundo.
        Atualiza o contador regressivo e exibe a janela a cada 15 minutos.
        """
        if self.remaining_seconds > 0:
            self.remaining_seconds -= 1
        else:
            # Tempo atingido! (15 minutos se passaram)
            self.remaining_seconds = self.interval_minutes * 60
            self.on_timer_triggered()

        # Atualiza o texto na barra superior
        self.lbl_timer.config(text=self._format_timer_text())

        # Atualiza tooltip do ícone da bandeja do Windows
        if self.tray:
            m = self.remaining_seconds // 60
            s = self.remaining_seconds % 60
            self.tray.update_tooltip(f"Kanban - Próximo aviso em {m:02d}:{s:02d}")

        self.root.after(1000, self._tick)

    def on_timer_triggered(self):
        """
        Disparado automaticamente ao término dos 15 minutos:
        Traz a janela de volta para a tela, emite som suave e notificação.
        """
        self.show_window(from_timer=True)

        if self.storage.get_setting("sound_alert", True):
            try:
                winsound.MessageBeep(winsound.MB_ICONASTERISK)
            except Exception:
                pass

        if self.storage.get_setting("notify_balloon", True) and self.tray:
            self.tray.show_balloon(
                "💭 Kanban de Tarefas",
                f"Passaram-se {self.interval_minutes} minutos! Revise e atualize suas tarefas."
            )

    def show_window(self, from_timer=False):
        """
        Restaura e traz a janela para a frente de todas as aplicações.
        """
        self.root.deiconify()
        self.root.lift()
        self.root.attributes('-topmost', True)
        self.is_visible = True
        self.root.focus_force()

    def hide_window(self):
        """
        Oculta a janela para a bandeja em segundo plano (System Tray).
        """
        self.root.withdraw()
        self.is_visible = False

    def toggle_window(self):
        if self.is_visible:
            self.hide_window()
        else:
            self.show_window()

    def confirm_exit(self):
        answer = messagebox.askyesnocancel(
            "Fechar Kanban",
            "Deseja apenas ocultar para segundo plano (lembrete em 15 min)?\n\n"
            "• Sim: Ocultar para a bandeja (continua avisando)\n"
            "• Não: Encerrar o programa completamente\n"
            "• Cancelar: Permanecer com o Kanban aberto",
            parent=self.root
        )
        if answer is True:
            self.hide_window()
        elif answer is False:
            self.quit_app()

    def quit_app(self):
        if self.tray:
            self.tray.stop()
        self.root.destroy()
        sys.exit(0)

