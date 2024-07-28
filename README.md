# Master_thesis
Systematic analysis of accident reports with LLMs

Where are the prompt and function calls? 

auto_eval_preprocessing.py
- Enthält alle prompts.

call.py
- Führt alles zu einem API Call zusammen

gui.py
- Streamlit Oberfläche

validator.py
- enthält den Validator
- Generiert die Functions mit dem pydantic package


How to setup the Web-App?

0. Erstelle einen Ordner im Python Projekt "API_keys" mit einer Textdatei "my_openai_key.txt". In der Datei muss ein gültiger API-Key hinterlegt sein
1. cmd / Konsole / Eingabeaufforderung öffnen
2. Navigiere in das Verzeichnis in dem das Python project gespeichert ist
3. Führe folgenden Befehl aus : "streamlit run gui.py"
4. Die Webapp sollte sich automatisch im Browser öffnen und direkt funktionieren
