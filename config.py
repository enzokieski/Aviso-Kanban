import os
import sys

# Diretórios base
APP_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(APP_DIR, "kanban_data.json")
ICON_FILE = os.path.join(APP_DIR, "icon.ico")

# Configurações Visuais
# Cor de chroma-key: Qualquer pixel com esta cor torna-se 100% transparente no Windows
CHROMA_BG = "#010101"

# Cores sólidas para os balões de mensagens e textos legíveis
COLOR_WHITE = "#FFFFFF"
COLOR_TEXT_MAIN = "#0F172A"      # Slate escuro para máxima legibilidade
COLOR_TEXT_MUTED = "#64748B"     # Cinza para timestamps e subtítulos
COLOR_BORDER = "#CBD5E1"         # Borda sutil e elegante
COLOR_BORDER_FOCUS = "#3B82F6"   # Borda ao focar

# Cores temáticas das 3 colunas
COLUMNS = {
    "fazer": {
        "title": "Fazer",
        "badge": "📌 A Fazer",
        "color": "#2563EB",          # Azul Royal
        "badge_bg": "#EFF6FF",
        "border": "#BFDBFE"
    },
    "fazendo": {
        "title": "Fazendo",
        "badge": "⚡ Fazendo",
        "color": "#D97706",          # Âmbar / Laranja
        "badge_bg": "#FFFBEB",
        "border": "#FDE68A"
    },
    "feito": {
        "title": "Feito",
        "badge": "✅ Feito",
        "color": "#16A34A",          # Verde
        "badge_bg": "#F0FDF4",
        "border": "#BBF7D0"
    }
}

# Configurações Padrão de Tempo
DEFAULT_INTERVAL_MINUTES = 15     # Intervalo padrão de 15 minutos
MINUTES_OPTIONS = [5, 10, 15, 20, 30, 45, 60]

# Dimensões da Janela
WINDOW_WIDTH = 1050
WINDOW_HEIGHT = 650

