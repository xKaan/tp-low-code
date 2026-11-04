# Tuto — Brancher Google Drive sur n8n (niveau 2)

Le workflow niveau 2 envoie les pièces jointes dans Google Drive, un dossier
par client. Pour ça, n8n a besoin d'un accès OAuth à un compte Google.
Compter 10 minutes, gratuit, sans carte bancaire.

Ce qu'on récupère à la fin :

| Quoi | Où | Sert à |
|---|---|---|
| **Client ID** | Google Cloud Console | identifier l'app n8n auprès de Google |
| **Client Secret** | Google Cloud Console | va avec le Client ID |
| **ID du dossier racine** | adresse du dossier dans Drive | remplacer `__GDRIVE_ROOT_FOLDER_ID__` |

> ⚠️ Le Client Secret est un vrai secret : ne jamais le commit, ni le coller
> dans un fichier du repo ou dans une conversation. Il ne va que dans n8n.

---

## 1. Créer le projet Google Cloud

1. Aller sur [console.cloud.google.com](https://console.cloud.google.com).
2. En haut, sélecteur de projet → **Nouveau projet** → nom au choix
   (ex. `TechDistri`) → **Créer**.
3. Vérifier que ce projet est bien **sélectionné** en haut de la page avant
   de continuer. Toutes les étapes suivantes se font dans ce projet.

## 2. Activer l'API Google Drive

1. Menu **API et services → Bibliothèque**.
2. Chercher **Google Drive API** → **Activer**.

Sans ça, n8n se connecte mais chaque appel échoue avec
`Google Drive API has not been used in project … or it is disabled`.
L'activation peut mettre 1 à 2 minutes à s'appliquer.

## 3. Configurer l'écran de consentement

Menu **Google Auth Platform** (ancienne interface : **API et services →
Écran de consentement OAuth**).

1. **Branding** : nom de l'app (ex. `TPLowCode`), email d'assistance = ton
   email.
2. **Audience** : type **Externe**.
3. **Utilisateurs test → + Add users** : ajouter **l'adresse Gmail exacte**
   du compte qui contiendra les fichiers.

Ce dernier point est obligatoire : tant que l'app est en mode « Test »,
Google refuse tout compte qui n'est pas dans cette liste, même le tien,
avec le message *« Accès bloqué : … n'a pas terminé la procédure de
validation de Google »*.

## 4. Créer l'identifiant OAuth

1. Menu **Identifiants → Créer des identifiants → ID client OAuth**.
2. Type d'application : **Application Web**.
3. **URI de redirection autorisés → + Ajouter un URI** :

   ```
   http://localhost:5678/rest/oauth2-credential/callback
   ```

4. **Créer**. Google affiche le **Client ID** (finit par
   `.apps.googleusercontent.com`) et le **Client Secret** (commence par
   `GOCSPX-`). Les garder sous la main pour l'étape suivante.

## 5. Créer le credential dans n8n

1. Ouvrir [localhost:5678/home/credentials](http://localhost:5678/home/credentials)
   → **Create credential → Google Drive OAuth2 API**.
2. Coller le **Client ID** et le **Client Secret**.
3. Vérifier que l'**OAuth Redirect URL** affichée par n8n est exactement
   celle de l'étape 4.
4. **Sign in with Google** → choisir le compte ajouté en utilisateur test.
5. Écran *« Google n'a pas validé cette application »* : c'est normal pour
   une app en test → **Paramètres avancés → Accéder à … (non sécurisé)** →
   cocher l'accès à Drive → **Continuer**.
6. Le credential passe en « Account connected » → **Save**.

Les nœuds Google Drive du workflow utilisent ce credential
(`Drive - Chercher Dossier Client`, `Drive - Créer Dossier Client`,
`Drive - Upload Fichier`).

> Le credential Google Drive de n8n demande l'accès complet à Drive. Ne pas
> chercher à le restreindre au scope `drive.file` : avec ce scope, n8n ne
> verrait pas le dossier racine créé à la main dans Drive.

## 6. Créer le dossier racine et récupérer son ID

1. Dans [Google Drive](https://drive.google.com), créer un dossier, par
   exemple `TechDistri - Pièces jointes`.
2. L'ouvrir : l'ID est la fin de l'adresse.

   ```
   https://drive.google.com/drive/folders/1bk58f-kMmHvv2xsgO9Xa01RhO6k4cYqn
                                          └──────────── ID ────────────────┘
   ```

3. Dans le workflow importé, remplacer `__GDRIVE_ROOT_FOLDER_ID__` par cet
   ID, sur deux nœuds :
   - `Drive - Chercher Dossier Client` (dans la requête de recherche)
   - `Drive - Créer Dossier Client` (champ *Parent Folder*)

Les dossiers clients (`ind-garcia.test`, `hydro-sud.test`…) sont ensuite
créés automatiquement dedans, au premier fichier de chaque client.

## 7. Tester

```bash
python3 scripts/send-demo-mails-pj.py 1pj
```

Résultat attendu sous quelques secondes :
- un dossier `ind-garcia.test` dans le dossier racine, avec `BC-26012.pdf` ;
- une fiche dans la table Airtable `Fichiers`, statut `Uploadé`, avec le
  lien Drive et la taille.

Puis le jeu complet (0, 1, 2 et 5 pièces jointes) :

```bash
python3 scripts/send-demo-mails-pj.py
```

---

## Problèmes fréquents

| Message | Cause | Solution |
|---|---|---|
| *Accès bloqué : … n'a pas terminé la procédure de validation de Google* | compte absent des utilisateurs test | étape 3, ajouter l'adresse exacte, attendre 1 min, réessayer |
| *Google Drive API has not been used in project … or it is disabled* | API non activée | étape 2 |
| *redirect_uri_mismatch* | URI de redirection différente de celle de n8n | étape 4, copier l'URL affichée par n8n |
| La connexion marchait, puis plus rien après une semaine | en mode « Test », Google coupe l'accès au bout de **7 jours** | rouvrir le credential dans n8n → **Sign in with Google** (à faire juste avant la soutenance) |
| Plusieurs comptes Google ouverts, mauvais compte choisi | Google propose un autre compte | se connecter avec le compte ajouté en utilisateur test |

## Sécurité

- Le Client Secret ne doit exister que dans n8n (chiffré dans sa base).
- S'il a fuité (repo, capture, conversation) : **Identifiants → le client
  OAuth → Réinitialiser le secret**, puis recoller le nouveau dans n8n et
  refaire **Sign in with Google**.
