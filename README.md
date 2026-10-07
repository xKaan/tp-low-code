# TechDistri — Centralisation automatisée des emails (Niveau 2)

Centralisation automatique des emails clients (Airtable + n8n), avec
identification du client par domaine email, extraction des pièces jointes
vers le cloud et formules de synthèse en cascade dans la table `Clients`.

## Livrables

- [`livrables/airtable-schema.md`](livrables/airtable-schema.md) — schéma Airtable (3 tables + cascade)
- [`livrables/techdistri-niveau1.json`](livrables/techdistri-niveau1.json) — workflow n8n niveau 1 (archivé, toujours valide)
- [`livrables/techdistri-niveau2.json`](livrables/techdistri-niveau2.json) — workflow n8n niveau 2 (à importer, remplace le niveau 1 en usage)
- [`livrables/test-plan.md`](livrables/test-plan.md) — jeu de test niveau 1
- [`livrables/test-plan-niveau2.md`](livrables/test-plan-niveau2.md) — jeu de test niveau 2 (PJ, erreurs)
- [`livrables/dashboard.md`](livrables/dashboard.md) — vues de consultation

## Mise en service

1. **n8n + serveur mail de test** : `docker compose up -d` → n8n sur [http://localhost:5678](http://localhost:5678)
2. **Airtable** : créer les tables selon [`livrables/airtable-schema.md`](livrables/airtable-schema.md) (ordre important : `Clients` → `Mails` → `Fichiers`, puis ajouter les champs Count/Rollup une fois les liens en place), récupérer l'ID de la base et un Personal Access Token (scopes `data.records:read/write`)
3. **Google Drive** : créer un dossier racine dédié (ex. `TechDistri - Pièces jointes`), noter son ID (dans l'URL du dossier), créer une credential OAuth2 Google Drive dans n8n (scope `drive.file` suffit)
4. **Import** : n8n → Import from File → `livrables/techdistri-niveau2.json`
5. **Config** : renseigner les credentials IMAP, Airtable, Google Drive et SMTP (voir ci-dessous) sur les nœuds correspondants, remplacer `__AIRTABLE_BASE_ID__` et `__GDRIVE_ROOT_FOLDER_ID__` par les valeurs réelles
6. **Activer** le workflow
7. **Tester** avec [`livrables/test-plan.md`](livrables/test-plan.md) puis [`livrables/test-plan-niveau2.md`](livrables/test-plan-niveau2.md)
8. **Consulter** via les vues décrites dans [`livrables/dashboard.md`](livrables/dashboard.md)

## Gestion d'erreurs

Le nœud `Drive - Upload Fichier` retente 3 fois (`retryOnFail`, 2 s entre
essais) avant de basculer sur sa sortie d'erreur (`onError:
continueErrorOutput`) — un échec d'upload ne fait jamais planter le reste
du workflow ni la fiche Mail, déjà créée avant la branche pièces jointes.
En cas d'échec définitif :

- une fiche `Fichiers` est quand même créée, avec `Statut upload = Échec`,
  `URL cloud` vide et le message d'erreur dans `Erreur` — rien n'est perdu
  silencieusement ;
- le nœud `Notifier Échec Upload` envoie un email d'alerte (via le SMTP
  GreenMail local pour la démo, un vrai SMTP/Slack en production) listant
  le fichier et le mail concernés, pour qu'un humain relance l'upload.

Voir le scénario de simulation détaillé dans
[`livrables/test-plan-niveau2.md`](livrables/test-plan-niveau2.md#simulation-dun-échec-dupload-gestion-derreurs).

## Serveur mail de test (GreenMail)

Le service `mail` du `docker-compose.yml` fournit SMTP + IMAP en local,
sans authentification (toute adresse devient une boîte). Les mails sont
gardés en mémoire : `docker compose restart mail` vide toutes les boîtes.

Webmail (Roundcube) : [http://localhost:8025](http://localhost:8025) — se
connecter avec `demo@techdistri.local` / n'importe quel mot de passe.

Credential IMAP à créer dans n8n :

| Champ | Valeur |
|---|---|
| User | `demo@techdistri.local` |
| Password | n'importe quoi (ex. `demo`) |
| Host | `mail` |
| Port | `3143` |
| SSL/TLS | désactivé |

Envoyer les emails du plan de test :

```bash
python3 scripts/send-test-mails.py        # les 5 emails niveau 1 (sans PJ)
python3 scripts/send-test-mails.py 1 2    # seulement #1 et #2

python3 scripts/send-test-mails-pj.py         # 4 emails niveau 2 avec vraies PJ (0/1/2/5)
python3 scripts/send-test-mails-pj.py 5pj     # seulement le cas à 5 PJ
```
