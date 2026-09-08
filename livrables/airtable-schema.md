# Schéma Airtable — TechDistri Niveau 1

## Table `Clients`

| Champ | Type |
|---|---|
| Nom | Single line text |
| Domaine email | Single line text |
| Adresse | Single line text |
| Contact principal | Single line text |
| Date création | Date |

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

Créer `Clients` avant `Mails` : le champ `Client` (link) génère
automatiquement le champ inverse `Mails` dans `Clients`.
