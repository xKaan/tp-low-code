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

## Cas piégeux du jeu de données (Gmail perso, no-reply, citations)

Envoi à la demande : `python3 scripts/send-demo-mails-pj.py gmail1 gmail2 noreply citations`

| Clé | Ce que ça teste | Attendu |
|---|---|---|
| `gmail1` + `gmail2` | Deux TPE sur le même domaine grand public (`gmail.test`) | **2 Clients distincts**, identifiés par l'adresse complète (`h.petit.btp@gmail.test`, `mathieu.atelier@gmail.test`), nommés d'après le nom d'affichage. Jamais un client unique `gmail.test` |
| `noreply` | Expéditeur automatique (`noreply@`, sujet `[AUTO]`, en-tête `Auto-Submitted`) | **Ignoré** : aucune fiche Client ni Mail créée |
| `citations` | Reply avec citations imbriquées (`> > >`) | Le champ `Corps` ne contient que le message utile ("Merci pour le retour. OK pour ce prix. A. Martin"), sans les citations |

Règles appliquées (nœud `Extraire Champs Email`) :
- domaines grand public (gmail, wanadoo, hotmail, outlook, yahoo, orange, free, laposte, icloud) → la clé client est l'adresse complète ; sinon le domaine ;
- no-reply (`noreply`, `no-reply`, `donotreply`, `mailer-daemon`, `postmaster`, `bounce`), sujet commençant par `[AUTO]` ou en-tête `Auto-Submitted` ≠ `no` → mail ignoré ;
- corps : retrait des lignes citées (`>`), des blocs `Le … a écrit :` / `On … wrote:`, `Message d'origine`, des en-têtes `De/Envoyé/À/Objet` et de la signature (`-- `). Si tout est retiré, le texte brut est conservé ;
- dossier Drive d'un client grand public : nommé d'après l'adresse complète, pour ne pas mélanger les fichiers de deux clients Gmail.

Choix à défendre : un Gmail perso d'un contact d'un client B2B connu est traité comme un client à part entière (identifié par son adresse), pas rattaché au client B2B.

## Test "nouveau client" (branche `isNew = true`)

`python3 scripts/send-demo-mails-pj.py nouveau-client` envoie 2 mails d'un
domaine inédit (`nouveau-<timestamp>.test`, différent à chaque lancement) :

| Mail | PJ | Attendu |
|---|---|---|
| 1/2 | 0 | `Client Existe ?` → création : **1 fiche Client** `nouveau-….test`, 1 fiche Mail liée |
| 2/2 | 1 (`demande.pdf`) | Client trouvé (pas de 2e création), 1 fiche Mail liée au même Client, dossier Drive `nouveau-….test` créé, 1 fiche Fichier |

Au final : 1 Client, 2 Mails, 1 Fichier, 1 dossier Drive. Relancer la commande
crée un nouveau domaine, donc aucun nettoyage n'est nécessaire entre deux essais.

## Test de déduplication (Message-ID)

Vérifie que relancer un mail déjà traité ne crée rien en double.

1. Envoyer le même mail deux fois avec le même `Message-ID` :
   `python3 scripts/send-demo-mails-pj.py doublon`
2. Attendre le passage de l'IMAP (ou *Execute workflow*).
3. Attendu : **1 seule** fiche `Mails` (Message-ID `<test-doublon-1pj@techdistri.local>`),
   1 seule fiche `Fichiers`, 1 seul upload Drive. La 2e exécution passe par la
   branche `Mail Déjà Traité ?` = oui et enchaîne sur le mail suivant.
4. Les envois normaux (`1pj`, `2pj`…) ont chacun un Message-ID unique : ils ne
   doivent jamais être marqués "déjà traités", même renvoyés plusieurs fois.

Pour rejouer le test, supprimer d'abord la fiche `Mails` au Message-ID
`<test-doublon-1pj@techdistri.local>` dans Airtable.

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
