# Schéma Airtable — TechDistri

## Table `Clients`

| Champ | Type |
|---|---|
| Nom | Single line text |
| Domaine email | Single line text |
| Adresse | Single line text |
| Contact principal | Single line text |
| Date création | Date |
| Nombre d'emails *(Niveau 2)* | Count — compte les enregistrements liés dans `Mails` |
| Dernier échange *(Niveau 2)* | Rollup sur `Mails` → champ `Date`, agrégation `MAX(values)` |
| Nb fichiers *(Niveau 2)* | Rollup sur `Mails` → champ `Nb fichiers`, agrégation `SUM(values)` |

## Table `Mails`

| Champ | Type |
|---|---|
| Sujet | Single line text |
| Expéditeur | Email |
| Date | Date |
| Corps | Long text |
| Message-ID | Single line text |
| Statut traitement | Single select (`Nouveau`) |
| Client | Link to `Clients` |
| Fichiers *(Niveau 2)* | Link to `Fichiers` (généré automatiquement, voir ci-dessous) |
| Nb fichiers *(Niveau 2)* | Count — compte les enregistrements liés dans `Fichiers` |

Créer `Clients` avant `Mails` : le champ `Client` (link) génère
automatiquement le champ inverse `Mails` dans `Clients`.

## Table `Fichiers` *(Niveau 2)*

| Champ | Type |
|---|---|
| Nom du fichier | Single line text |
| Type MIME | Single line text |
| Taille (octets) | Number |
| URL cloud | URL |
| Date d'arrivée | Date |
| Statut upload | Single select (`Uploadé`, `Échec`) |
| Erreur | Long text (vide si succès, message d'erreur sinon) |
| Mail | Link to `Mails` |

Créer `Fichiers` après `Mails` : le champ `Mail` (link) génère
automatiquement le champ inverse `Fichiers` dans `Mails`, nécessaire au
champ `Nb fichiers` de `Mails`.

## Ordre de création et formules en cascade

1. `Clients`, puis `Mails` (niveau 1) — voir ci-dessus.
2. `Fichiers`, avec son champ `Mail` lié à `Mails` → fait apparaître le
   champ inverse `Fichiers` dans `Mails`.
3. Dans `Mails`, ajouter le champ **Count** `Nb fichiers` sur le lien
   `Fichiers`.
4. Dans `Clients`, ajouter :
   - **Count** `Nombre d'emails` sur le lien `Mails`
   - **Rollup** `Dernier échange` = `MAX(values)` du champ `Date` de `Mails`
   - **Rollup** `Nb fichiers` = `SUM(values)` du champ `Nb fichiers` de
     `Mails` (rollup de rollup : chaque mail compte ses fichiers, le
     client somme sur tous ses mails — c'est la cascade demandée par le
     brief)

Airtable ne permet pas un rollup sur deux niveaux de liaison en une
seule étape (`Clients` ne peut pas lire `Fichiers` directement puisqu'ils
ne sont pas liés). La cascade `Fichiers → Mails.Nb fichiers → Clients.Nb
fichiers` est le contournement standard et évite de dupliquer un lien
`Client` sur `Fichiers`, ce qui garderait le modèle conforme au schéma du
brief (3 tables, `Fichiers` lié uniquement à `Mails`).
