# Atelier Git — Séance 1

Repo : https://github.com/rom47220/DevOps

Mini app Python pour l'atelier DevOps (séance 1).

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
python -m pytest tests/
```
