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

## Comparaison des images Docker

Mesures réalisées avec `docker images devops-flask` :

- Image naïve (`python:3.12`) : 1,64 Go sur disque, 423 Mo de contenu.
- Image multi-stage (`python:3.12-slim`) : 219 Mo sur disque, 53 Mo de contenu.
- Réduction du contenu : environ 87 %.

L'image finale utilise un build multi-stage, Gunicorn et un utilisateur non-root.

## Application Docker

### Construire l'image

    docker build -t devops-flask:multistage ./starter-app

### Lancer les services

    docker compose -f starter-app/docker-compose.yml up -d --build

Endpoints disponibles :

- http://localhost:5000/health
- http://localhost:5000/status
- http://localhost:5000/visits

Pour arrêter :

    docker compose -f starter-app/docker-compose.yml down

### Image publiée

    docker pull ghcr.io/rom47220/devops-flask:1.0.0

Package : https://github.com/users/rom47220/packages/container/package/devops-flask
