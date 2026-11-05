# Démarrage rapide — Workflow TechDistri (Niveau 2)

Les étapes pour faire tourner `techdistri-niveau2.json` en local, de zéro à
la base remplie. Il faut compter environ 20 minutes la première fois, puis
2 minutes pour les fois suivantes (étape 6 seulement).

**Prérequis** : Docker Desktop démarré, Python 3, un compte Airtable et un
compte Google.

---

## 1. Démarrer les services

```bash
docker compose up -d        # depuis la racine du repo
```

| Service | URL / accès |
|---|---|
| n8n | http://localhost:5678 (compte local créé au premier lancement) |
| Webmail Roundcube | http://localhost:8025 — `demo@techdistri.local` / n'importe quel mot de passe |
| GreenMail (serveur mail de test) | SMTP `localhost:3025`, IMAP `localhost:3143`, sans authentification |

## 2. Préparer Airtable (une seule fois)

Créer une base avec les 3 tables décrites dans
[`airtable-schema.md`](airtable-schema.md), **dans cet ordre** :
`Clients` → `Mails` → `Fichiers`, puis les champs Count/Rollup.

Vérifier qu'on a bien les champs ajoutés pour les cas piégeux :

| Table | Champ | Type |
|---|---|---|
| `Clients` | `Adresses connues` | Long text |
| `Clients` | `À vérifier` | Checkbox |
| `Mails` | `Statut traitement` | Single select : `Nouveau`, `Automatique`, `Interne` |
| `Mails` | `Origine` | Single select : `Direct`, `Transfert interne`, `Formulaire site` |

Récupérer ensuite :
- **l'ID de la base** : il commence par `app…` et se trouve dans l'URL Airtable ;
- **un Personal Access Token** (https://airtable.com/create/tokens), avec
  les scopes `data.records:read` et `data.records:write`, et un accès à la base.

## 3. Préparer Google Drive (une seule fois)

Créer un dossier racine, par exemple `TechDistri - Pièces jointes`, et noter
son **ID** (la fin de l'URL du dossier). La création de la credential OAuth2
est détaillée pas à pas dans [`tuto-google-drive.md`](tuto-google-drive.md).

## 4. Importer et configurer le workflow

1. n8n → **Workflows** → **Import from File** → `livrables/techdistri-niveau2.json`
2. Créer les 4 credentials (menu **Credentials** → **Add credential**), puis
   les sélectionner sur les nœuds :

| Credential | Paramètres | Nœuds concernés |
|---|---|---|
| **IMAP** | User `demo@techdistri.local`, Password `demo`, Host `mail`, Port `3143`, SSL/TLS **désactivé** | `IMAP - Mails entrants` |
| **Airtable Personal Access Token** | le token de l'étape 2 | les 5 nœuds `Airtable - …` |
| **Google Drive OAuth2** | voir [`tuto-google-drive.md`](tuto-google-drive.md) | les 3 nœuds `Drive - …` |
| **SMTP** | Host `mail`, Port `3025`, sans utilisateur ni mot de passe, SSL/TLS **désactivé** | `Notifier Échec Upload` |

3. Remplacer les deux valeurs factices du workflow (7 occurrences en tout) :
   - `__AIRTABLE_BASE_ID__` → l'ID de la base `app…`, sur les nœuds Airtable ;
   - `__GDRIVE_ROOT_FOLDER_ID__` → l'ID du dossier Drive, sur `Drive - Chercher Dossier Client` et `Drive - Créer Dossier Client`.

   Astuce : on peut aussi les remplacer dans le fichier JSON **avant** l'import :
   ```bash
   sed -e 's/__AIRTABLE_BASE_ID__/appXXXXXXXXXXXXXX/g' \
       -e 's/__GDRIVE_ROOT_FOLDER_ID__/1AbCdEf.../g' \
       livrables/techdistri-niveau2.json > /tmp/techdistri-niveau2-config.json
   ```
   puis importer `/tmp/techdistri-niveau2-config.json`.
4. **Save**, puis activer le toggle **Active** en haut à droite.

## 5. Envoyer des emails de test

Le nœud IMAP relève la boîte **toutes les 5 minutes**. Pour ne pas attendre,
on peut ouvrir le workflow et cliquer sur **Execute workflow**.

```bash
# Jeu de données officiel (50 emails, dont les cas piégeux)
python3 scripts/send-dataset-mails.py                     # les 50
python3 scripts/send-dataset-mails.py 042 043 044 048     # seulement certains

# Jeux de démo plus courts
python3 scripts/send-demo-mails.py        # 8 emails sans pièce jointe
python3 scripts/send-demo-mails-pj.py     # 4 emails avec 0, 1, 2 et 5 pièces jointes
```

Ensuite, vérifier :
- n8n → onglet **Executions** : toutes les exécutions sont en vert ;
- Airtable : les tables `Clients`, `Mails` et `Fichiers`, et les compteurs
  de la table `Clients` ;
- Drive : un sous-dossier par client, plus un dossier `_Interne` pour les
  mails automatiques.

Ce qui est attendu pour chaque cas est décrit dans [`test-plan.md`](test-plan.md)
et [`test-plan-niveau2.md`](test-plan-niveau2.md).

## 6. Repartir de zéro (avant une démo)

1. Vider les 3 tables Airtable (sélectionner toutes les lignes → **Delete**).
2. Vider les dossiers clients dans Drive.
3. Vider la boîte mail :
   ```bash
   docker compose restart mail
   ```

Les workflows et les credentials n8n sont conservés : ils sont stockés dans
le volume `n8n_data`.

Pour tout arrêter : `docker compose down`. Ne **pas** ajouter `-v`, sinon le
volume est supprimé et on perd la configuration n8n.

---

## Dépannage

| Symptôme | Cause probable / solution |
|---|---|
| Aucun mail traité | Le workflow n'est pas activé, ou la credential IMAP pointe vers `localhost` au lieu de `mail` (n8n tourne dans Docker). |
| `Connection refused` sur l'IMAP ou le SMTP | Le service mail est arrêté : `docker compose ps`, puis `docker compose up -d`. |
| Erreur Airtable `UNKNOWN_FIELD_NAME` | Un champ manque ou a un nom différent : comparer avec l'étape 2 (accents compris : `À vérifier`, `Date création`…). |
| Erreur Airtable `INVALID_MULTIPLE_CHOICE_OPTIONS` | Une option manque dans `Statut traitement` ou `Origine` : l'ajouter dans Airtable. |
| Erreur Airtable `NOT_FOUND` / 403 | L'ID de la base est mauvais, ou le token n'a pas accès à cette base ou n'a pas les scopes requis. |
| Erreur Drive 404 sur le dossier | `__GDRIVE_ROOT_FOLDER_ID__` n'a pas été remplacé, ou le compte OAuth n'a pas accès au dossier. |
| Mail retraité mais pas de doublon | C'est normal : la déduplication par `Message-ID` saute les mails déjà présents. |
| Mot de passe n8n oublié | `docker compose exec n8n n8n user-management:reset`, puis recharger la page et recréer le compte. |
