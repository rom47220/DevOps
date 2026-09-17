# Atelier Git — Séance 1

[![CI](https://github.com/rom47220/DevOps/actions/workflows/ci.yml/badge.svg)](https://github.com/rom47220/DevOps/actions/workflows/ci.yml)

Repo : https://github.com/rom47220/DevOps

Mini app Python pour l'atelier DevOps (séance 1).

## Pipeline CI

Le pipeline se lance sur les push vers `main` et sur toutes les pull requests. Il vérifie
le style avec flake8, puis exécute les tests et génère un rapport de couverture avec
Python 3.10, 3.11 et 3.12.

## Strategie

On fait du **Git Flow**.
- `main` : prod
- `dev` : developpement
- `test` : recette
- features : `feat/<sujet>`, `fix/<sujet>`, `hotfix/<sujet>` (depuis `dev`)

## Merge

Pas de push direct sur `main`.
`feat/*` -> `dev` -> `test` -> `main`.
Commits en Conventional Commits (`feat`, `fix`, `chore`, `docs`).

Membre GitHub : [rom47220](https://github.com/rom47220)

## Lancer les tests

```bash
cd starter-app2
python -m pip install -r requirements.txt
python -m flake8 .
python -m pytest -v --cov=app --cov-report=html
```
