# StudyPilot Local (PyQt5)

Application locale (pas de cloud) avec **UI premium**, **splash**, **multi-utilisateur** et **onglets** (Agenda, Horaire 1–9, Devoirs/Examens, Matières, Outils, Import, Paramètres).

## Installer (sans .exe)
```bash
python -m venv .venv
# Windows
. .venv/Scripts/activate
# macOS/Linux
# source .venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
pip install .
```

## Lancer
```bash
studypilot
# ou
python -m studypilot
```

### BringStudy (agenda CLI)
```bash
bringstudy list            # lister les entrées
bringstudy add "Titre" 2024-06-01 -c exam -d "Description"
```

## Données locales par utilisateur
- Windows: %APPDATA%/StudyPilotLocal
- macOS: ~/Library/Application Support/StudyPilotLocal
- Linux: ~/.local/share/StudyPilotLocal
