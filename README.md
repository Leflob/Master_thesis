# Master Thesis: Systematic Analysis of Accident Reports with LLMs

## 1. Installation
Um alle benötigten Pakete zu installieren, führe den folgenden Befehl aus:

```bash
pip install -r requirements.txt
```


## 2. Run the Streamlit App
1. Erstelle einen Ordner im Python Projekt "API_keys" mit einer Textdatei "my_openai_key.txt". In der Datei muss ein gültiger API-Key hinterlegt sein
2.  cmd / Konsole / Eingabeaufforderung öffnen
3. Navigiere in das Verzeichnis in dem das Python project gespeichert ist
4. Führe folgenden Befehl aus : "streamlit run gui.py"
5. Die Webapp sollte sich automatisch im Browser öffnen und direkt funktionieren


## 3. Where are the prompt and function calls? 
```bash
auto_eval_preprocessing.py
```
- Enthält alle prompts.

```bash
call.py
```
- Führt alles zu einem API Call zusammen

```bash
gui.py
```
- Streamlit Oberfläche

```bash
validator.py
```
- enthält den Validator
- Generiert die Functions mit dem pydantic package

