Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = "C:\Users\G Anirudh\.gemini\antigravity\scratch\genomedsl"
WshShell.Run "cmd /c ""C:\Users\G Anirudh\AppData\Local\Programs\Python\Python313\Scripts\streamlit.exe"" run genomedsl_app.py", 0, False
