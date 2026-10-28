import json
import os
import time
import uuid
from datetime import datetime
from config import DATA_FILE, DEFAULT_INTERVAL_MINUTES

DEFAULT_DATA = {
    "version": "1.0",
    "settings": {
        "interval_minutes": DEFAULT_INTERVAL_MINUTES,
        "sound_alert": True,
        "notify_balloon": True,
        "window_x": None,
        "window_y": None
    },
    "tasks": [
        {
            "id": "sample-1",
            "title": "Definir prioridades e tarefas do dia",
            "description": "Organizar demandas mais importantes no topo da lista.",
            "column": "fazer",
            "created_at": datetime.now().strftime("%d/%m %H:%M"),
            "priority": "alta"
        },
        {
            "id": "sample-2",
            "title": "Responder e-mails e mensagens pendentes",
            "description": "Checar caixa de entrada e alinhar pendências com a equipe.",
            "column": "fazer",
            "created_at": datetime.now().strftime("%d/%m %H:%M"),
            "priority": "normal"
        },
        {
            "id": "sample-3",
            "title": "Desenvolver funcionalidade principal",
            "description": "Foco total na entrega sem distrações.",
            "column": "fazendo",
            "created_at": datetime.now().strftime("%d/%m %H:%M"),
            "priority": "alta"
        },
        {
            "id": "sample-4",
            "title": "Instalar e configurar sistema Kanban flutuante",
            "description": "Configurado para avisar a cada 15 minutos na tela.",
            "column": "feito",
            "created_at": datetime.now().strftime("%d/%m %H:%M"),
            "priority": "normal"
        }
    ]
}

class KanbanStorage:
    def __init__(self, filepath=DATA_FILE):
        self.filepath = filepath
        self.data = self.load()

    def load(self):
        if not os.path.exists(self.filepath):
            self.save(DEFAULT_DATA)
            return json.loads(json.dumps(DEFAULT_DATA))
        
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Garante que chaves essenciais existam
                if "tasks" not in data:
                    data["tasks"] = []
                if "settings" not in data:
                    data["settings"] = DEFAULT_DATA["settings"]
                return data
        except Exception as e:
            print(f"Erro ao ler arquivo de dados: {e}. Usando dados padrão.")
            return json.loads(json.dumps(DEFAULT_DATA))

    def save(self, data=None):
        if data is not None:
            self.data = data
        try:
            # Escrita atômica para evitar corrupção de arquivo
            temp_path = self.filepath + ".tmp"
            with open(temp_path, "w", encoding="utf-8") as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
            if os.path.exists(self.filepath):
                os.replace(temp_path, self.filepath)
            else:
                os.rename(temp_path, self.filepath)
        except Exception as e:
            print(f"Erro ao salvar dados: {e}")

    def get_tasks(self, column=None):
        tasks = self.data.get("tasks", [])
        if column:
            return [t for t in tasks if t.get("column") == column]
        return tasks

    def add_task(self, title, description="", column="fazer", priority="normal"):
        task = {
            "id": str(uuid.uuid4())[:8],
            "title": title.strip(),
            "description": description.strip(),
            "column": column if column in ("fazer", "fazendo", "feito") else "fazer",
            "created_at": datetime.now().strftime("%d/%m %H:%M"),
            "priority": priority
        }
        self.data.setdefault("tasks", []).append(task)
        self.save()
        return task

    def update_task_column(self, task_id, new_column):
        if new_column not in ("fazer", "fazendo", "feito"):
            return False
        for t in self.data.get("tasks", []):
            if t.get("id") == task_id:
                t["column"] = new_column
                t["updated_at"] = datetime.now().strftime("%d/%m %H:%M")
                self.save()
                return True
        return False

    def edit_task(self, task_id, title=None, description=None, priority=None):
        for t in self.data.get("tasks", []):
            if t.get("id") == task_id:
                if title is not None:
                    t["title"] = title.strip()
                if description is not None:
                    t["description"] = description.strip()
                if priority is not None:
                    t["priority"] = priority
                t["updated_at"] = datetime.now().strftime("%d/%m %H:%M")
                self.save()
                return True
        return False

    def delete_task(self, task_id):
        initial_len = len(self.data.get("tasks", []))
        self.data["tasks"] = [t for t in self.data.get("tasks", []) if t.get("id") != task_id]
        if len(self.data["tasks"]) != initial_len:
            self.save()
            return True
        return False

    def clear_completed(self):
        self.data["tasks"] = [t for t in self.data.get("tasks", []) if t.get("column") != "feito"]
        self.save()

    def get_setting(self, key, default=None):
        return self.data.get("settings", {}).get(key, default)

    def set_setting(self, key, value):
        self.data.setdefault("settings", {})[key] = value
        self.save()

    def save_window_pos(self, x, y):
        self.set_setting("window_x", x)
        self.set_setting("window_y", y)

