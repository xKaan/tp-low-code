# TechDistri — Centralisation automatisée des emails (Niveau 1)

Centralisation automatique des emails clients (Airtable + n8n), avec
identification du client par domaine email.

## Livrables

- [`livrables/airtable-schema.md`](livrables/airtable-schema.md) — schéma Airtable
- [`livrables/techdistri-niveau1.json`](livrables/techdistri-niveau1.json) — workflow n8n
- [`livrables/test-plan.md`](livrables/test-plan.md) — jeu de test

## Mise en service

1. **n8n** : `docker compose up -d` → [http://localhost:5678](http://localhost:5678) (ou n8n cloud)
2. **Airtable** : créer les tables selon [`livrables/airtable-schema.md`](livrables/airtable-schema.md), récupérer l'ID de la base et un Personal Access Token (scopes `data.records:read/write`)
3. **Import** : n8n → Import from File → `livrables/techdistri-niveau1.json`
4. **Config** : renseigner les credentials IMAP et Airtable sur les nœuds correspondants, remplacer `__AIRTABLE_BASE_ID__` par l'ID réel
5. **Activer** le workflow
6. **Tester** avec [`livrables/test-plan.md`](livrables/test-plan.md)
