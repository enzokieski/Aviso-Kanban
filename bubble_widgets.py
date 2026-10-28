import tkinter as tk
from tkinter import messagebox
from config import (
    CHROMA_BG, COLOR_WHITE, COLOR_TEXT_MAIN, COLOR_TEXT_MUTED,
    COLOR_BORDER, COLUMNS, MINUTES_OPTIONS
)

class BubbleCard(tk.Frame):
    """
    Balão de mensagem individual que representa uma tarefa no Kanban.
    Possui formato de balão com 'rabicho' à esquerda, fundo branco 100% sólido
    e botões de ação para mover entre Fazer, Fazendo e Feito.
    """
    def __init__(self, parent, task, on_move=None, on_edit=None, on_delete=None, **kwargs):
        super().__init__(parent, bg=CHROMA_BG, **kwargs)
        self.task = task
        self.on_move = on_move
        self.on_edit = on_edit
        self.on_delete = on_delete

        col_key = task.get("column", "fazer")
        col_cfg = COLUMNS.get(col_key, COLUMNS["fazer"])

        # Container horizontal: Rabicho à esquerda + Corpo do balão
        self.card_row = tk.Frame(self, bg=CHROMA_BG)
        self.card_row.pack(fill="x", pady=5, padx=2)

        # 1. Rabicho do balão (Canvas triangular)
        self.tail = tk.Canvas(self.card_row, width=10, height=28, bg=CHROMA_BG, highlightthickness=0)
        self.tail.pack(side="left", anchor="n", pady=(10, 0))
        
        # Desenha o triângulo do balão
        self.tail.create_polygon(10, 2, 0, 12, 10, 22, fill=COLOR_WHITE, outline=col_cfg["border"], width=1)
        # Linha para mascarar a borda direita e conectar com perfeição ao corpo branco
        self.tail.create_line(10, 3, 10, 21, fill=COLOR_WHITE, width=2)

        # 2. Corpo do balão (Fundo branco sólido, borda na cor da coluna)
        self.body = tk.Frame(
            self.card_row,
            bg=COLOR_WHITE,
            highlightbackground=col_cfg["border"],
            highlightthickness=1,
            padx=12,
            pady=10
        )
        self.body.pack(side="left", fill="x", expand=True)

        # Cabeçalho interno do balão: Tag de status e Horário
        header_frame = tk.Frame(self.body, bg=COLOR_WHITE)
        header_frame.pack(fill="x", pady=(0, 4))

        # Tag/Badge com estilo de pílula
        priority = task.get("priority", "normal")
        priority_icon = "🔥 " if priority == "alta" else ("⚡ " if priority == "urgente" else "")
        
        badge_lbl = tk.Label(
            header_frame,
            text=f"{priority_icon}{col_cfg['badge']}",
            font=("Segoe UI", 8, "bold"),
            bg=col_cfg["badge_bg"],
            fg=col_cfg["color"],
            padx=6,
            pady=1
        )
        badge_lbl.pack(side="left")

        # Timestamp no canto direito
        time_text = task.get("created_at", "")
        if time_text:
            time_lbl = tk.Label(
                header_frame,
                text=time_text,
                font=("Segoe UI", 8),
                bg=COLOR_WHITE,
                fg=COLOR_TEXT_MUTED
            )
            time_lbl.pack(side="right")

        # Título da Tarefa (Negrito, alta legibilidade)
        title_font = ("Segoe UI", 10, "bold")
        # Se concluído, efeito visual diferenciado opcional
        title_fg = COLOR_TEXT_MAIN
        
        self.title_lbl = tk.Label(
            self.body,
            text=task.get("title", ""),
            font=title_font,
            bg=COLOR_WHITE,
            fg=title_fg,
            wraplength=250,
            justify="left",
            anchor="w"
        )
        self.title_lbl.pack(fill="x", pady=(2, 2))

        # Descrição opcional (se houver)
        desc = task.get("description", "")
        if desc:
            self.desc_lbl = tk.Label(
                self.body,
                text=desc,
                font=("Segoe UI", 9),
                bg=COLOR_WHITE,
                fg="#475569",
                wraplength=250,
                justify="left",
                anchor="w"
            )
            self.desc_lbl.pack(fill="x", pady=(0, 4))

        # Linha inferior: Botões de navegação Kanban e Ações
        actions_frame = tk.Frame(self.body, bg=COLOR_WHITE)
        actions_frame.pack(fill="x", pady=(6, 0))

        # Botão Voltar (se não estiver em 'fazer')
        if col_key == "fazendo":
            btn_prev = self._create_btn(actions_frame, "◀ Fazer", lambda: self.on_move(task["id"], "fazer"))
            btn_prev.pack(side="left", padx=(0, 4))
        elif col_key == "feito":
            btn_prev = self._create_btn(actions_frame, "◀ Fazendo", lambda: self.on_move(task["id"], "fazendo"))
            btn_prev.pack(side="left", padx=(0, 4))

        # Botão Avançar (se não estiver em 'feito')
        if col_key == "fazer":
            btn_next = self._create_btn(actions_frame, "Fazendo ▶", lambda: self.on_move(task["id"], "fazendo"), accent=True, col=COLUMNS["fazendo"]["color"])
            btn_next.pack(side="left", padx=(0, 4))
        elif col_key == "fazendo":
            btn_next = self._create_btn(actions_frame, "Feito ✅", lambda: self.on_move(task["id"], "feito"), accent=True, col=COLUMNS["feito"]["color"])
            btn_next.pack(side="left", padx=(0, 4))

        # Ações auxiliares à direita: Editar e Excluir
        btn_del = self._create_icon_btn(actions_frame, "🗑️", lambda: self.on_delete(task["id"]), hover_col="#FEE2E2", text_col="#DC2626")
        btn_del.pack(side="right")

        btn_edit = self._create_icon_btn(actions_frame, "✏️", lambda: self.on_edit(task), hover_col="#F1F5F9", text_col="#475569")
        btn_edit.pack(side="right", padx=(0, 4))

    def _create_btn(self, parent, text, command, accent=False, col=COLOR_TEXT_MAIN):
        bg_col = "#F8FAFC"
        border_col = COLOR_BORDER
        if accent:
            bg_col = "#FFFFFF"
            border_col = col

        btn = tk.Button(
            parent,
            text=text,
            font=("Segoe UI", 8, "bold" if accent else "normal"),
            bg=bg_col,
            fg=col,
            activebackground="#E2E8F0",
            activeforeground=col,
            bd=1,
            relief="solid",
            highlightthickness=0,
            padx=8,
            pady=2,
            cursor="hand2",
            command=command
        )
        return btn

    def _create_icon_btn(self, parent, icon, command, hover_col="#F1F5F9", text_col="#475569"):
        btn = tk.Button(
            parent,
            text=icon,
            font=("Segoe UI", 9),
            bg=COLOR_WHITE,
            fg=text_col,
            activebackground=hover_col,
            activeforeground=text_col,
            bd=0,
            padx=4,
            pady=1,
            cursor="hand2",
            command=command
        )
        return btn


class ColumnHeaderBubble(tk.Frame):
    """
    Balão superior de cabeçalho da coluna (Fazer, Fazendo, Feito).
    Fundo branco sólido, indicador de quantidade e botão de ação rápida.
    """
    def __init__(self, parent, col_key, count=0, on_add=None, on_clear=None, **kwargs):
        super().__init__(parent, bg=CHROMA_BG, **kwargs)
        col_cfg = COLUMNS.get(col_key, COLUMNS["fazer"])

        # Balão do título
        self.bubble = tk.Frame(
            self,
            bg=COLOR_WHITE,
            highlightbackground=col_cfg["border"],
            highlightthickness=1.5,
            padx=14,
            pady=8
        )
        self.bubble.pack(fill="x")

        # Título da coluna
        title_lbl = tk.Label(
            self.bubble,
            text=col_cfg["title"],
            font=("Segoe UI", 11, "bold"),
            bg=COLOR_WHITE,
            fg=col_cfg["color"]
        )
        title_lbl.pack(side="left")

        # Contador de tarefas
        self.count_badge = tk.Label(
            self.bubble,
            text=f" {count} ",
            font=("Segoe UI", 9, "bold"),
            bg=col_cfg["badge_bg"],
            fg=col_cfg["color"],
            padx=4,
            pady=0
        )
        self.count_badge.pack(side="left", padx=(8, 0))

        # Botão + para adicionar na coluna 'fazer'
        if col_key == "fazer" and on_add:
            btn_add = tk.Button(
                self.bubble,
                text="➕ Nova Tarefa",
                font=("Segoe UI", 8, "bold"),
                bg="#EFF6FF",
                fg="#2563EB",
                activebackground="#DBEAFE",
                bd=0,
                padx=8,
                pady=2,
                cursor="hand2",
                command=lambda: on_add(col_key)
            )
            btn_add.pack(side="right")
        elif col_key == "feito" and on_clear and count > 0:
            btn_clear = tk.Button(
                self.bubble,
                text="🧹 Limpar Feitos",
                font=("Segoe UI", 8),
                bg="#F1F5F9",
                fg="#64748B",
                activebackground="#E2E8F0",
                bd=0,
                padx=6,
                pady=2,
                cursor="hand2",
                command=on_clear
            )
            btn_clear.pack(side="right")

    def update_count(self, count):
        self.count_badge.config(text=f" {count} ")


class ScrollableColumn(tk.Frame):
    """
    Área rolável para exibir as tarefas de uma coluna mantendo
    a transparência entre os balões.
    """
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=CHROMA_BG, **kwargs)

        self.canvas = tk.Canvas(self, bg=CHROMA_BG, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        
        self.scrollable_frame = tk.Frame(self.canvas, bg=CHROMA_BG)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.window_id = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        # Barra de rolagem aparece apenas se necessário, mas para visual clean podemos esconder ou mostrar sutil
        self.canvas.bind("<Configure>", self._on_canvas_configure)

        # Bind mouse wheel para rolagem suave
        self.bind_mousewheel(self.canvas)
        self.bind_mousewheel(self.scrollable_frame)

    def _on_canvas_configure(self, event):
        self.canvas.itemconfig(self.window_id, width=event.width)

    def bind_mousewheel(self, widget):
        widget.bind("<MouseWheel>", self._on_mousewheel, add="+")
        for child in widget.winfo_children():
            self.bind_mousewheel(child)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


class TaskDialog(tk.Toplevel):
    """
    Janela flutuante modal para adicionar ou editar uma tarefa.
    Fundo branco sólido e design moderno.
    """
    def __init__(self, parent, task=None, default_column="fazer", on_save=None):
        super().__init__(parent)
        self.task = task
        self.on_save = on_save
        self.result = None

        self.title("Editar Tarefa" if task else "Nova Tarefa")
        self.configure(bg=COLOR_WHITE)
        self.geometry("450x380")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        # Centraliza sobre a janela pai
        self.update_idletasks()
        pw = parent.winfo_width()
        ph = parent.winfo_height()
        px = parent.winfo_x()
        py = parent.winfo_y()
        x = px + (pw - 450) // 2
        y = py + (ph - 380) // 2
        self.geometry(f"+{max(0, x)}+{max(0, y)}")

        # Container interno com padding
        pad_frame = tk.Frame(self, bg=COLOR_WHITE, padx=24, pady=20)
        pad_frame.pack(fill="both", expand=True)

        # Título do modal
        header_text = "✏️ Editar Tarefa" if task else "➕ Nova Tarefa"
        lbl_h = tk.Label(pad_frame, text=header_text, font=("Segoe UI", 13, "bold"), bg=COLOR_WHITE, fg=COLOR_TEXT_MAIN)
        lbl_h.pack(anchor="w", pady=(0, 15))

        # Campo: Título da Tarefa
        lbl_title = tk.Label(pad_frame, text="Título da Tarefa:", font=("Segoe UI", 9, "bold"), bg=COLOR_WHITE, fg=COLOR_TEXT_MAIN)
        lbl_title.pack(anchor="w", pady=(0, 4))

        self.entry_title = tk.Entry(
            pad_frame,
            font=("Segoe UI", 10),
            bg="#F8FAFC",
            fg=COLOR_TEXT_MAIN,
            relief="solid",
            bd=1,
            highlightthickness=1,
            highlightcolor="#3B82F6",
            highlightbackground=COLOR_BORDER
        )
        self.entry_title.pack(fill="x", pady=(0, 12), ipady=5)
        if task:
            self.entry_title.insert(0, task.get("title", ""))

        # Campo: Descrição / Anotação
        lbl_desc = tk.Label(pad_frame, text="Descrição / Detalhes (Opcional):", font=("Segoe UI", 9, "bold"), bg=COLOR_WHITE, fg=COLOR_TEXT_MAIN)
        lbl_desc.pack(anchor="w", pady=(0, 4))

        self.text_desc = tk.Text(
            pad_frame,
            font=("Segoe UI", 9),
            height=3,
            bg="#F8FAFC",
            fg=COLOR_TEXT_MAIN,
            relief="solid",
            bd=1,
            highlightthickness=1,
            highlightcolor="#3B82F6",
            highlightbackground=COLOR_BORDER
        )
        self.text_desc.pack(fill="x", pady=(0, 12))
        if task and task.get("description"):
            self.text_desc.insert("1.0", task.get("description"))

        # Opções: Coluna e Prioridade
        opts_frame = tk.Frame(pad_frame, bg=COLOR_WHITE)
        opts_frame.pack(fill="x", pady=(0, 15))

        # Coluna inicial
        lbl_col = tk.Label(opts_frame, text="Coluna:", font=("Segoe UI", 9, "bold"), bg=COLOR_WHITE, fg=COLOR_TEXT_MAIN)
        lbl_col.pack(side="left", padx=(0, 8))

        self.var_col = tk.StringVar(value=task.get("column", default_column) if task else default_column)
        
        for k in ["fazer", "fazendo", "feito"]:
            rb = tk.Radiobutton(
                opts_frame,
                text=COLUMNS[k]["title"],
                value=k,
                variable=self.var_col,
                bg=COLOR_WHITE,
                fg=COLUMNS[k]["color"],
                activebackground=COLOR_WHITE,
                font=("Segoe UI", 9, "bold")
            )
            rb.pack(side="left", padx=4)

        # Prioridade
        prio_frame = tk.Frame(pad_frame, bg=COLOR_WHITE)
        prio_frame.pack(fill="x", pady=(0, 15))

        lbl_prio = tk.Label(prio_frame, text="Prioridade:", font=("Segoe UI", 9, "bold"), bg=COLOR_WHITE, fg=COLOR_TEXT_MAIN)
        lbl_prio.pack(side="left", padx=(0, 8))

        self.var_prio = tk.StringVar(value=task.get("priority", "normal") if task else "normal")
        for p, label in [("normal", "Normal"), ("alta", "🔥 Alta"), ("urgente", "⚡ Urgente")]:
            rb_p = tk.Radiobutton(
                prio_frame,
                text=label,
                value=p,
                variable=self.var_prio,
                bg=COLOR_WHITE,
                fg=COLOR_TEXT_MAIN,
                activebackground=COLOR_WHITE,
                font=("Segoe UI", 9)
            )
            rb_p.pack(side="left", padx=4)

        # Botões de Ação
        btn_frame = tk.Frame(pad_frame, bg=COLOR_WHITE)
        btn_frame.pack(fill="x", pady=(10, 0))

        btn_cancel = tk.Button(
            btn_frame,
            text="Cancelar",
            font=("Segoe UI", 9),
            bg="#F1F5F9",
            fg="#475569",
            bd=0,
            padx=14,
            pady=6,
            cursor="hand2",
            command=self.destroy
        )
        btn_cancel.pack(side="right", padx=(8, 0))

        btn_save = tk.Button(
            btn_frame,
            text="Salvar Tarefa",
            font=("Segoe UI", 9, "bold"),
            bg="#2563EB",
            fg=COLOR_WHITE,
            activebackground="#1D4ED8",
            activeforeground=COLOR_WHITE,
            bd=0,
            padx=16,
            pady=6,
            cursor="hand2",
            command=self._save
        )
        btn_save.pack(side="right")

        self.entry_title.focus_set()
        self.bind("<Return>", lambda e: self._save())
        self.bind("<Escape>", lambda e: self.destroy())

    def _save(self):
        title = self.entry_title.get().strip()
        if not title:
            messagebox.showwarning("Atenção", "Por favor, digite o título da tarefa.", parent=self)
            self.entry_title.focus_set()
            return
        
        desc = self.text_desc.get("1.0", "end").strip()
        col = self.var_col.get()
        prio = self.var_prio.get()

        if self.on_save:
            self.on_save(title, desc, col, prio, self.task)
        self.destroy()


class SettingsDialog(tk.Toplevel):
    """
    Janela flutuante modal para alterar configurações (intervalo de aviso em minutos, etc).
    """
    def __init__(self, parent, storage, on_update=None):
        super().__init__(parent)
        self.storage = storage
        self.on_update = on_update

        self.title("Configurações do Kanban")
        self.configure(bg=COLOR_WHITE)
        self.geometry("420x350")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        # Centraliza
        self.update_idletasks()
        pw = parent.winfo_width()
        ph = parent.winfo_height()
        px = parent.winfo_x()
        py = parent.winfo_y()
        self.geometry(f"+{max(0, px + (pw - 420) // 2)}+{max(0, py + (ph - 350) // 2)}")

        pad = tk.Frame(self, bg=COLOR_WHITE, padx=24, pady=20)
        pad.pack(fill="both", expand=True)

        lbl_h = tk.Label(pad, text="⚙️ Configurações de Aviso", font=("Segoe UI", 12, "bold"), bg=COLOR_WHITE, fg=COLOR_TEXT_MAIN)
        lbl_h.pack(anchor="w", pady=(0, 15))

        # Intervalo em minutos
        lbl_int = tk.Label(pad, text="Aparecer automaticamente na tela a cada:", font=("Segoe UI", 9, "bold"), bg=COLOR_WHITE, fg=COLOR_TEXT_MAIN)
        lbl_int.pack(anchor="w", pady=(0, 6))

        current_int = self.storage.get_setting("interval_minutes", 15)
        self.var_interval = tk.IntVar(value=current_int)

        grid_frame = tk.Frame(pad, bg=COLOR_WHITE)
        grid_frame.pack(fill="x", pady=(0, 15))

        for idx, m in enumerate(MINUTES_OPTIONS):
            rb = tk.Radiobutton(
                grid_frame,
                text=f"{m} min",
                value=m,
                variable=self.var_interval,
                bg=COLOR_WHITE,
                fg=COLOR_TEXT_MAIN,
                activebackground=COLOR_WHITE,
                font=("Segoe UI", 9)
            )
            rb.grid(row=idx // 4, column=idx % 4, sticky="w", padx=6, pady=4)

        # Notificações sonoras e balão
        lbl_notif = tk.Label(pad, text="Notificações:", font=("Segoe UI", 9, "bold"), bg=COLOR_WHITE, fg=COLOR_TEXT_MAIN)
        lbl_notif.pack(anchor="w", pady=(0, 4))

        self.var_sound = tk.BooleanVar(value=self.storage.get_setting("sound_alert", True))
        chk_sound = tk.Checkbutton(
            pad,
            text="Emitir som suave ao abrir a cada 15 minutos",
            variable=self.var_sound,
            bg=COLOR_WHITE,
            fg=COLOR_TEXT_MAIN,
            activebackground=COLOR_WHITE,
            font=("Segoe UI", 9)
        )
        chk_sound.pack(anchor="w", pady=2)

        self.var_balloon = tk.BooleanVar(value=self.storage.get_setting("notify_balloon", True))
        chk_balloon = tk.Checkbutton(
            pad,
            text="Exibir notificação balão na bandeja do Windows",
            variable=self.var_balloon,
            bg=COLOR_WHITE,
            fg=COLOR_TEXT_MAIN,
            activebackground=COLOR_WHITE,
            font=("Segoe UI", 9)
        )
        chk_balloon.pack(anchor="w", pady=2)

        # Botões
        btn_frame = tk.Frame(pad, bg=COLOR_WHITE)
        btn_frame.pack(fill="x", pady=(20, 0))

        btn_cancel = tk.Button(btn_frame, text="Cancelar", font=("Segoe UI", 9), bg="#F1F5F9", fg="#475569", bd=0, padx=14, pady=6, cursor="hand2", command=self.destroy)
        btn_cancel.pack(side="right", padx=(8, 0))

        btn_save = tk.Button(btn_frame, text="Salvar Configurações", font=("Segoe UI", 9, "bold"), bg="#2563EB", fg=COLOR_WHITE, bd=0, padx=16, pady=6, cursor="hand2", command=self._save)
        btn_save.pack(side="right")

    def _save(self):
        new_interval = self.var_interval.get()
        self.storage.set_setting("interval_minutes", new_interval)
        self.storage.set_setting("sound_alert", self.var_sound.get())
        self.storage.set_setting("notify_balloon", self.var_balloon.get())

        if self.on_update:
            self.on_update()
        self.destroy()

