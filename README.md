# TechDistri — Centralisation automatisée des emails (Niveau 1)

Centralisation automatique des emails clients (Airtable + n8n), avec
identification du client par domaine email.

## Livrables

- [`livrables/airtable-schema.md`](livrables/airtable-schema.md) — schéma Airtable
- [`livrables/techdistri-niveau1.json`](livrables/techdistri-niveau1.json) — workflow n8n
- [`livrables/test-plan.md`](livrables/test-plan.md) — jeu de test

## Mise en service

1. **n8n + serveur mail de test** : `docker compose up -d` → n8n sur [http://localhost:5678](http://localhost:5678)
2. **Airtable** : créer les tables selon [`livrables/airtable-schema.md`](livrables/airtable-schema.md), récupérer l'ID de la base et un Personal Access Token (scopes `data.records:read/write`)
3. **Import** : n8n → Import from File → `livrables/techdistri-niveau1.json`
4. **Config** : renseigner les credentials IMAP (voir ci-dessous) et Airtable sur les nœuds correspondants, remplacer `__AIRTABLE_BASE_ID__` par l'ID réel
5. **Activer** le workflow
6. **Tester** avec [`livrables/test-plan.md`](livrables/test-plan.md)

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
python3 scripts/send-test-mails.py        # les 5
python3 scripts/send-test-mails.py 1 2    # seulement #1 et #2
```
