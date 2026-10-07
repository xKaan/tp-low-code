# Mini-dashboard de consultation — Niveau 2

Objectif du brief : permettre à l'équipe commerciale (5 personnes) et à la
direction (1 personne) de consulter la base **sans écrire dans Airtable**.
Solution retenue : des vues Airtable dédiées à la consultation (grid views en
lecture, partagées en lien public "en lecture seule"), pas de nouvel outil
(Softr) — suffisant pour la démo et sans coût ni compte supplémentaire.

## Vues à créer

### Table `Clients` — vue `Dashboard Clients`

- Tri : `Dernier échange` décroissant (les clients les plus récemment actifs
  en haut)
- Colonnes visibles, dans l'ordre : `Nom`, `Domaine email`, `Nb mails`,
  `Nb fichiers`, `Dernier échange`, `Contact principal`
- Filtre : aucun (vue globale) — sert de point d'entrée "quel client a
  bougé récemment, combien de documents lui sont rattachés"

### Table `Mails` — vue `Recherche par client`

- Groupement : par `Client`
- Tri intra-groupe : `Date` décroissant
- Colonnes visibles : `Sujet`, `Date`, `Expéditeur`, `Statut traitement`,
  `Nb fichiers`
- Répond au besoin du brief "retrouver le dernier devis envoyé à Carrasco" :
  ouvrir le groupe du client, le mail le plus récent est en tête.

### Table `Mails` — vue `Recherche par période`

- Tri : `Date` décroissant (vue plate, pas de groupement)
- Filtre optionnel activable par l'utilisateur dans l'UI Airtable (bouton
  Filtrer dispo même sur un lien partagé en lecture) sur `Date`
- Colonnes visibles : `Date`, `Client`, `Sujet`, `Statut traitement`

### Table `Fichiers` — vue `Documents par client`

- Groupement : par `Mail` → `Client` n'étant pas un lien direct de
  `Fichiers` (cf. [`airtable-schema.md`](airtable-schema.md), cascade
  volontaire), grouper par le champ lookup `Client` ajouté en complément
  (lookup simple depuis `Mail`, pas un lien — ne casse pas le modèle à 3
  tables du brief, juste un champ d'affichage)
- Colonnes visibles : `Nom du fichier`, `Type MIME`, `URL cloud`,
  `Statut upload`, `Date d'arrivée`
- Filtre : `Statut upload` ≠ vide (exclut les lignes en cours de
  traitement s'il y en a)
- Un clic sur `URL cloud` ouvre le fichier dans Drive — c'est la
  "recherche instantanée" demandée par le brief.

### Table `Fichiers` — vue `Échecs upload` (support / suivi d'erreurs)

- Filtre : `Statut upload` = `Échec`
- Colonnes visibles : `Nom du fichier`, `Mail`, `Erreur`, `Date d'arrivée`
- Vue de contrôle pour l'équipe : liste tout ce qui doit être ré-uploadé
  manuellement (cf. [`README.md`](../README.md#gestion-derreurs) et le
  mail d'alerte envoyé par le nœud `Notifier Échec Upload`).

## Partage

Pour chaque vue listée ci-dessus : bouton **Share view** → **Create a
shareable link for this view** → lecture seule (les utilisateurs ne
peuvent pas éditer depuis ce lien). Distribuer les 5 liens à l'équipe
commerciale et à la direction — pas de siège Airtable payant nécessaire
pour eux.

## Alternative Softr (si plus de temps)

Si le groupe veut aller au-delà d'un lien Airtable partagé : brancher
[Softr](https://www.softr.io/) sur la base (connecteur natif Airtable),
créer une page "Liste des clients" (source = vue `Dashboard Clients`) avec
une page de détail affichant les mails et fichiers liés. Non nécessaire
pour valider les critères du niveau 2, mais rend la soutenance plus
convaincante si le temps le permet.
