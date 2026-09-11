# Atelier Git avancé & collaboratif — Séance 1

Dépôt du bloc DevOps (séance 1). Application minimale Python pour exercer
rebase, conflits, cherry-pick, bisect, pull requests et protections GitHub.

## Stratégie de branches : trunk-based

Nous utilisons une **stratégie trunk-based** (et non Git Flow).

Pourquoi ce choix : l'étape 6 impose un **historique linéaire** sur `main`.
Git Flow s'appuie sur des merge commits longue durée (`develop`, `release/*`),
ce qui contredit cette contrainte. Trunk-based + branches courtes + squash
(ou rebase) produit un historique lisible et linéaire, cohérent avec les
protections de `main`.

### Convention de nommage

| Type | Branche | Exemple |
| --- | --- | --- |
| Fonctionnalité | `feat/<sujet>` | `feat/greet-message` |
| Correctif | `fix/<sujet>` | `fix/add-overflow` |
| Urgent (à cherry-pick) | `hotfix/<sujet>` | `hotfix/greet-empty-name` |
| Maintenance | `chore/<sujet>` | `chore/gitignore` |

Une branche vit le temps d'une PR (heures, pas des jours). Pas de branche
`develop` longue durée.

### Règle de merge

- **Interdiction** de pousser directement sur `main`.
- Toute modification arrive par **pull request**.
- Merge autorisé : **squash merge** uniquement (historique linéaire).
- Rebase / merge commit désactivés sur GitHub.
- Une PR n'est mergée qu'après **revue du Code Owner** de la zone touchée.
- Messages de commit au format [Conventional Commits](https://www.conventionalcommits.org/) :
  `type(scope): description` (`feat`, `fix`, `chore`, `docs`, `hotfix`).

### Collaborateurs

Tous les membres du groupe doivent être **Collaborators** du dépôt GitHub
dès l'étape 1 (Settings → Collaborators), sinon les PR et protections de
l'étape 6 bloquent le travail.

> À compléter : identifiants GitHub des membres du groupe.

## Structure

```
src/app.py          # code Python (zone CODEOWNERS)
docs/               # documentation (zone CODEOWNERS)
.github/CODEOWNERS  # propriétaires par zone (étape 5)
```

## Lancer l'application

```bash
python -c "from src.app import greet, add; print(greet('DevOps'), add(2, 3))"
```
