# Plan de test — Niveau 2 (pièces jointes)

Complète [`test-plan.md`](test-plan.md) (niveau 1, toujours valide). Ce plan
couvre les critères spécifiques au niveau 2 : upload cloud, organisation par
dossier, fiche Fichier, formules en cascade, gestion d'erreurs.

## Pré-requis avant de tester

1. Table `Fichiers` créée selon [`airtable-schema.md`](airtable-schema.md),
   avec les champs cascade (`Nb fichiers` sur `Mails`, `Nombre d'emails` /
   `Dernier échange` / `Nb fichiers` sur `Clients`).
2. Workflow [`techdistri-niveau2.json`](techdistri-niveau2.json) importé,
   credentials Airtable + IMAP + Google Drive + SMTP configurées, `__AIRTABLE_BASE_ID__`
   et `__GDRIVE_ROOT_FOLDER_ID__` remplacés par les vraies valeurs.
3. Un dossier Drive racine créé à l'avance (ex. `TechDistri - Pièces jointes`),
   son ID copié dans `__GDRIVE_ROOT_FOLDER_ID__` sur les deux nœuds Drive
   concernés (`Drive - Chercher Dossier Client`, `Drive - Créer Dossier Client`).
4. Workflow activé (ou déclenché manuellement pour la démo).

## Jeu d'emails à envoyer

`python3 scripts/send-test-mails-pj.py` envoie 4 emails réels du jeu de
données (avec vraies PJ) à la boîte de démo :

| Clé | Email | Expéditeur | PJ | Vérifie |
|---|---|---|---|---|
| `0pj` | #001 Carrasco | j.carrasco@carrasco-indus.test | 0 | Le cas "sans PJ" ne casse pas le workflow (`Extraire Pièces Jointes` renvoie 0 item, branche Drive non exécutée, fiche Mail créée normalement) |
| `1pj` | #011 Industries Garcia | c.garcia@ind-garcia.test | 1 (`BC_BC-25471.xlsx`) | Cas nominal : dossier Drive `ind-garcia.test` créé (1er passage) ou réutilisé, 1 fiche Fichier créée, liée au Mail |
| `2pj` | #033 Atelier Mécanique 38 | l.dupont@atelier-meca38.test | 2 (fiches techniques PDF) | La boucle gère bien N>1 PJ sur un même mail (2 fiches Fichier, même `Mail` lié) |
| `5pj` | #040 Euromag Distribution | m.granet@euromag-distri.test | 5 (PDF + PNG mélangés) | Cas piégeux explicitement cité par le brief : 5 fiches Fichier créées, aucune perdue, types MIME variés gérés |

Envoyer un sous-ensemble : `python3 scripts/send-test-mails-pj.py 1pj 5pj`

## Résultat attendu après les 4 emails

**Table `Fichiers` : exactement 1 + 1 + 2 + 5 = 9 enregistrements**, chacun
avec `Statut upload = Uploadé`, une `URL cloud` valide, et un lien `Mail`
non vide.

**Google Drive** : 3 dossiers clients créés sous le dossier racine
(`carrasco-indus.test` n'en a pas puisque #001 n'a pas de PJ) —
`ind-garcia.test`, `atelier-meca38.test`, `euromag-distri.test` — chacun
contenant les fichiers du bon client, pas de mélange entre dossiers.

**Table `Mails`** : `Nb fichiers` = 0 / 1 / 2 / 5 sur les 4 mails
respectivement.

**Table `Clients`** : pour chacun des 3 clients avec PJ, `Nb fichiers`
cascade correctement depuis `Mails.Nb fichiers` ; `Nombre d'emails` et
`Dernier échange` se mettent à jour pour les 4 clients (y compris Carrasco
qui n'a pas de PJ mais a bien 1 mail de plus).

## Simulation d'un échec d'upload (gestion d'erreurs)

Le brief demande explicitement : *"que se passe-t-il si l'upload cloud
échoue ?"*. Pour le démontrer en démo sans dépendre d'une vraie panne Drive :

1. Dans le nœud `Drive - Upload Fichier`, remplacer temporairement
   `folderId` par un ID de dossier invalide (ex. `ID_INVALIDE_TEST`), ou
   révoquer temporairement l'accès OAuth du credential Drive.
2. Envoyer `python3 scripts/send-test-mails-pj.py 1pj`.
3. Observer :
   - Le nœud retente 3 fois (`retryOnFail`, `waitBetweenTries: 2000`) avant
     de basculer sur la sortie erreur.
   - Une fiche `Fichiers` est quand même créée, avec `Statut upload = Échec`,
     `URL cloud` vide et `Erreur` renseignée — **aucune perte de traçabilité**,
     contrairement à un plantage silencieux.
   - Un email d'alerte arrive sur `demo@techdistri.local` (visible dans le
     webmail Roundcube, [http://localhost:8025](http://localhost:8025)),
     envoyé par le nœud `Notifier Échec Upload` via le SMTP GreenMail local —
     cela prouve que le circuit d'alerte fonctionne de bout en bout sans
     dépendre d'un vrai Slack/service externe.
   - Le mail d'origine (table `Mails`) reste traité normalement : une PJ en
     échec ne bloque jamais la création de la fiche Mail (elle a lieu avant
     la branche pièces jointes dans le workflow).
4. Remettre le `folderId` / credential valides et renvoyer le même email
   pour montrer le chemin nominal juste après.

## Procédure de démo live

1. Dérouler d'abord le plan de test niveau 1 (5 emails, 3 expéditeurs).
2. Enchaîner avec `0pj`, `1pj` : montrer la création du dossier Drive et de
   la fiche Fichier, cliquer sur `URL cloud` pour prouver que le fichier
   est bien accessible.
3. Envoyer `5pj` : montrer les 5 fiches Fichier créées d'un coup.
4. Montrer la vue `Dashboard Clients` ([`dashboard.md`](dashboard.md)) :
   `Nombre d'emails` / `Nb fichiers` / `Dernier échange` à jour sans action
   manuelle.
5. Dérouler le scénario d'échec ci-dessus pour montrer la gestion d'erreurs.

## Plan B

Même recommandation que le niveau 1 : enregistrer une vidéo de ce
scénario complet (y compris la simulation d'échec) avant la soutenance.
