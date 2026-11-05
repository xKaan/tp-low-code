# Mini-dashboard de consultation — Niveau 2

Objectif du brief : permettre à l'équipe commerciale (5 personnes) et à la
direction (1 personne) de consulter la base **sans écrire dans Airtable**.

Deux niveaux de consultation, tous deux dans Airtable (pas d'outil
supplémentaire, pas de coût) :

1. **Interface `TechDistri - Dashboard`** (Airtable Interface Designer) :
   le dashboard principal, en lecture seule.
2. **Vues de consultation** dans chaque table, partageables en lien
   lecture seule.

## Interface `TechDistri - Dashboard`

Onglet **Interfaces** de la base. Quatre pages, toutes en lecture seule
(actions « Modifier / Ajouter / Supprimer les entrées » désactivées sur
chaque liste).

### Page `Vue d'ensemble`

- Indicateurs : nombre de **Clients**, de **Mails**, de **Fichiers** et de
  **Fichiers en échec** (`Statut upload` = `Échec`)
- Graphique en barres **Mails par client**
- Graphique **Fichiers par type MIME**
- Liste **Mails les plus récents** (Sujet, Expéditeur, Date, Client), triée
  par date décroissante

### Page `Clients`

- Liste triée par `Dernier échange` décroissant : `Nom`, `Domaine email`,
  `Nombre d'emails`, `Nb fichiers`, `Dernier échange`
- Clic sur un client → page détail avec ses mails et leurs fichiers

### Page `Mails`

- Liste groupée par `Client`, triée par `Date` décroissante
- Menus déroulants de filtre par **Client** et par **Date** (recherche par
  client et par période demandée par le brief)
- Répond au besoin « retrouver le dernier devis envoyé à Carrasco » : filtrer
  sur le client, le mail le plus récent est en tête.

### Page `Fichiers`

- Liste groupée par `Client` : `Nom du fichier`, `Type MIME`, `URL cloud`,
  `Statut upload`, `Date d'arrivée`
- Un clic sur `URL cloud` ouvre le fichier dans Drive.

## Vues de consultation (tables)

| Table | Vue | Configuration |
|---|---|---|
| `Clients` | `Dashboard Clients` | Tri `Dernier échange` décroissant ; colonnes `Nom`, `Domaine email`, `Contact principal`, `Nombre d'emails`, `Dernier échange`, `Nb fichiers` |
| `Mails` | `Recherche par client` | Groupé par `Client`, tri `Date` décroissant ; colonnes `Sujet`, `Expéditeur`, `Date`, `Statut traitement`, `Fichiers`, `Nb fichiers` |
| `Mails` | `Recherche par période` | Vue plate, tri `Date` décroissant ; colonnes `Sujet`, `Expéditeur`, `Date`, `Statut traitement`, `Client`, `Nb fichiers` |
| `Fichiers` | `Documents par client` | Groupé par `Client` ; colonnes `Nom du fichier`, `Type MIME`, `URL cloud`, `Date d'arrivée`, `Statut upload`, `Mail` |
| `Fichiers` | `Échecs upload` | Filtre `Statut upload` = `Échec` — liste ce qui doit être ré-uploadé à la main (cf. [`README.md`](../README.md#gestion-derreurs)) |

`Fichiers` n'est pas lié directement à `Clients` (cf.
[`airtable-schema.md`](airtable-schema.md)) : le groupement par client
utilise un champ **Recherche** `Client` (lookup `Mail` → `Client`), un simple
champ d'affichage qui ne change pas le modèle à 3 tables.

## Partage

- **Interface** : bouton **Publier**, puis **Partager l'interface** et
  inviter l'équipe avec un rôle lecture seule.
- **Vues** : **Partager et synchroniser** → lien partagé de la vue, en
  lecture seule — pas de siège Airtable nécessaire pour le consulter.
