# StudyPilot Local (PyQt5)

Application locale (pas de cloud) pour étudiants du secondaire (16–18 ans).  
**Premium UI**, **écran de chargement**, **multi‑utilisateur**, **onglets**.

## Installation (sans .exe)
> Nécessite Python 3.9+ (avec `pip`) et les droits d'installation de paquets utilisateurs.

```bash
# 1) (Optionnel) Crée un environnement virtuel
python -m venv .venv && . .venv/Scripts/activate  # Windows
# ou
python3 -m venv .venv && source .venv/bin/activate # macOS/Linux

# 2) Installer
pip install --upgrade pip
pip install -r requirements.txt
pip install .   # installe le paquet et le raccourci console "studypilot"
```

## Lancer
```bash
studypilot
```
ou
```bash
python -m studypilot
```

## Données locales
- Windows: `%APPDATA%/StudyPilotLocal`
- macOS: `~/Library/Application Support/StudyPilotLocal`
- Linux: `~/.local/share/StudyPilotLocal`

Chaque **utilisateur** a son dossier séparé. Les mots de passe sont **hachés (PBKDF2-SHA256)**.  
Les données ne sont pas chiffrées par défaut (option “Chiffrage” à venir).

## Fonctionnalités
- Connexion **Master Password** + sélecteur d’utilisateur (créer/supprimer depuis l’écran d’accueil).
- **Onglets**: Agenda, Horaire (1–9), Devoirs/Examens, Matières, Outils, Import, Paramètres.
- **Clic droit** dans l’agenda/horaire pour ajouter: note, absence, devoir, examen (récurrence jour de cycle).
- **Styles premium** (QSS sombre), **splash** animé.
- **Sauvegarde/Import JSON** (localStorage-like), ICS/CSV import (léger).

## Créer un raccourci (Windows)
1. Clic droit sur le bureau → Nouveau → Raccourci.
2. Cible: `C:\\Users\\…\\.venv\\Scripts\\pythonw.exe -m studypilot` (ou `studypilot` si ajouté au PATH)
3. Nom: `StudyPilot` → OK. Icône personnalisable depuis `studypilot/assets/logo.ico` (à créer).

Bon succès! 🎓
