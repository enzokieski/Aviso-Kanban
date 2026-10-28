# 💬 Kanban Flutuante em Balões de Mensagens (Sistema de Avisos)

Um sistema nativo para Windows projetado para produtividade sem distrações: ele exibe um quadro **Kanban transparente** diretamente na sua tela, com suas tarefas organizadas no formato de **balões de mensagens** (estilo chat/mensageiro).

O fundo da tela é **totalmente transparente**, permitindo que você continue enxergando seus códigos, navegadores ou papéis de parede, enquanto os balões de tarefas possuem **fundo branco sólido** para garantir leitura nítida e confortável.

---

## ✨ Funcionalidades Principais

- 📌 **3 Colunas Kanban Essenciais**:
  - **Fazer** (`#2563EB` Azul Royal)
  - **Fazendo** (`#D97706` Âmbar/Laranja)
  - **Feito** (`#16A34A` Verde Esmeralda)
- 💬 **Visual em Balões de Mensagens**:
  - Cada tarefa é apresentada como um balão de conversa com rabicho lateral, horário de registro e botões de avanço e retrocesso (`◀ Voltar`, `Avançar ▶`, `Feito ✅`).
- 🪟 **Transparência Inteligente com Fundo Branco**:
  - O fundo da janela é invisível/transparente.
  - Apenas as partes escritas (a barra superior, os cabeçalhos das colunas e os balões de cada tarefa) têm fundo branco sólido de alto contraste.
- ⏰ **Aviso Automático a cada 15 Minutos**:
  - A aplicação não precisa ficar fixa na sua tela o tempo todo: ao pressionar `ESC` ou clicar em `Ocultar`, ela minimiza para segundo plano.
  - A cada 15 minutos (configurável para 5, 10, 15, 20, 30, 45 ou 60 min), a tela se sobrepõe automaticamente com suas tarefas, emitindo um aviso sonoro suave e notificação balão na barra de tarefas.
- 🔄 **Aba de Aplicações em Segundo Plano (Bandeja do Windows / System Tray)**:
  - Fica quieto ao lado do relógio do Windows com ícone próprio.
  - **1 clique** ou **duplo clique**: Abre o Kanban na hora.
  - **Botão direito**: Menu de contexto rápido com opções para *Abrir Kanban*, *Nova Tarefa*, *Ocultar*, *Configurar Tempo* e *Sair*.
  - O indicador de hover exibe a contagem regressiva para o próximo aviso: `Kanban - Próximo aviso em 14:32`.
- 💾 **Persistência Automática em JSON**:
  - Todas as tarefas, colunas, prioridades e até a posição arrastada na tela são salvas imediatamente no arquivo `kanban_data.json`.
- 🖐️ **Arrastável pela Tela**:
  - Clique e arraste na barra superior branca para posicionar o Kanban onde preferir no seu monitor. A posição fica salva automaticamente.

---

## 🚀 Como Iniciar

### 1. Início Rápido (Sem janela preta de terminal)
Dê um duplo clique no arquivo:
👉 **`iniciar_kanban.vbs`**

Ele inicializa o sistema silenciosamente em segundo plano via `pythonw`. O ícone aparecerá instantaneamente na bandeja do sistema (ao lado do relógio) e o quadro Kanban abrirá sobre sua tela.

### 2. Início via Prompt / Batch
Se preferir visualizar logs no terminal:
👉 **`iniciar_kanban.bat`**

### 3. Iniciar Automaticamente com o Windows
Para que o sistema ligue junto com o seu computador:
👉 Execute **`configurar_inicializacao_windows.bat`** e digite a opção `1`.

---

## ⌨️ Atalhos e Controles

| Ação | Como Fazer |
| :--- | :--- |
| **Ocultar para segundo plano** | Pressione `ESC` ou clique em `👁️ Ocultar (ESC)` |
| **Criar nova tarefa** | Pressione `Ctrl + N` ou clique em `➕ Nova Tarefa` |
| **Avançar coluna** | Clique no botão `Avançar ▶` ou `Feito ✅` dentro do balão |
| **Voltar coluna** | Clique no botão `◀ Voltar` dentro do balão |
| **Editar tarefa** | Clique no ícone de lápis `✏️` |
| **Excluir tarefa** | Clique no ícone de lixeira `🗑️` |
| **Limpar tarefas concluídas** | Clique em `🧹 Limpar Feitos` no cabeçalho da coluna Feito |
| **Mover a janela** | Clique e arraste na barra superior branca |
| **Alterar tempo de aviso** | Clique no botão `⚙️ 15 min` na barra superior |

---

## 📂 Estrutura dos Arquivos

```text
Sistema de avisos/
├── config.py                         # Configurações de cores, transparência, dimensões e tempos
├── storage.py                        # Gerenciamento de tarefas e persistência em kanban_data.json
├── tray_manager.py                   # Integração nativa com a bandeja do Windows (System Tray Win32)
├── bubble_widgets.py                 # Componentes visuais dos balões de mensagens e modais
├── kanban_app.py                     # Aplicação gráfica principal, timer e motor de transparência
├── main.py                           # Ponto de entrada com proteção de instância única
├── icon.ico                          # Ícone estilizado do Kanban
├── iniciar_kanban.vbs                # Inicializador invisível (sem janela CMD)
├── iniciar_kanban.bat                # Inicializador alternativo .bat
├── configurar_inicializacao_windows.bat # Configurador para iniciar com o Windows
└── kanban_data.json                  # Banco de dados local das suas tarefas (criado automaticamente)
```

