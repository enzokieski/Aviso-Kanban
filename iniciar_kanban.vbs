Option Explicit

Dim WshShell, fso, strPath, mainPy, exeFile, distExeFile
Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

strPath = fso.GetParentFolderName(WScript.ScriptFullName)
WshShell.CurrentDirectory = strPath

mainPy = strPath & "\main.py"
exeFile = strPath & "\KanbanFlutuante.exe"
distExeFile = strPath & "\dist\KanbanFlutuante\KanbanFlutuante.exe"

' 1. Verifica se o script está sendo rodado de uma pasta temporária (ex: direto do navegador/zip sem extrair)
If InStr(LCase(strPath), "microsoftedgedownloads") > 0 Or InStr(LCase(strPath), "\temp\") > 0 Then
    If Not fso.FileExists(mainPy) And Not fso.FileExists(exeFile) And Not fso.FileExists(distExeFile) Then
        MsgBox "O Kanban não pode ser iniciado direto do navegador ou de dentro do arquivo ZIP sem extrair." & vbCrLf & vbCrLf & _
               "Por favor, extraia a pasta inteira para seus Documentos ou Área de Trabalho antes de abrir.", _
               16, "Aviso - Extrair Arquivos"
        WScript.Quit
    End If
End If

' 2. Tenta executar via executável standalone se existir
If fso.FileExists(exeFile) Then
    WshShell.Run """" & exeFile & """", 0, False
    WScript.Quit
End If

If fso.FileExists(distExeFile) Then
    WshShell.Run """" & distExeFile & """", 0, False
    WScript.Quit
End If

' 3. Se houver o main.py, tenta rodar com Python
If fso.FileExists(mainPy) Then
    On Error Resume Next
    ' Tenta pythonw
    WshShell.Run "pythonw.exe """ & mainPy & """", 0, False
    If Err.Number = 0 Then WScript.Quit
    Err.Clear

    ' Tenta pyw (Python Launcher padrão do Windows)
    WshShell.Run "pyw.exe """ & mainPy & """", 0, False
    If Err.Number = 0 Then WScript.Quit
    Err.Clear

    ' Tenta python
    WshShell.Run "python.exe """ & mainPy & """", 0, False
    If Err.Number = 0 Then WScript.Quit
    Err.Clear
    On Error GoTo 0

    ' Se falhou em encontrar o Python
    MsgBox "O Python não foi encontrado neste computador." & vbCrLf & vbCrLf & _
           "Para rodar este aplicativo nesta máquina:" & vbCrLf & _
           "1. Instale o Python (marcando a opção 'Add Python to PATH'), OU" & vbCrLf & _
           "2. Use a versão executável (KanbanFlutuante.exe).", _
           48, "Python Não Encontrado"
    WScript.Quit
End If

' 4. Se não encontrou nem main.py nem o executável
MsgBox "Arquivos do projeto não foram encontrados nesta pasta." & vbCrLf & _
       "Certifique-se de que todos os arquivos foram descompactados juntos.", _
       16, "Erro ao Iniciar"
