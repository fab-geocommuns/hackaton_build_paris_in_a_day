# Hackathon IGN : Paris en un jour
Projet de hackaton 2026 sur la reconstruction 3D de Paris.
L'idée est de construire des itinéraires optimaux pour faire le tour complet de Paris en vélo en 1 jour afin de prendre en photos toute la capitale. Ensuite, les photos seront exploitées pour créer une reconstruction de Paris virtuelle.

## Getting started
```{bash}
git clone https://github.com/fab-geocommuns/hackaton_build_paris_in_a_day
cd hackaton_build_paris_in_a_day
uv sync
```

## Lancer un notebook

- Ouvrir la Command Palette avec Ctrl+Shift+P (Windows/Linux) ou Cmd+Shift+P (Mac)  
- Chercher et cliquer sur >Python: Select Interpreter  
- Choisir Enter interpreter path… et entrer : /home/onyxia/work/hackaton_build_paris_in_a_day/.venv/bin/python

## Faire tourner la pipeline des données

```
uv run python main.py
```