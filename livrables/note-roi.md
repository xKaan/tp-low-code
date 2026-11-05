# Note ROI — Centralisation automatisée des emails TechDistri (Niveau 2)

**Périmètre** : 3 000 clients B2B · 8 000 à 10 000 emails/mois (hypothèse retenue : **9 000**) · 6 utilisateurs.

## 1. Temps gagné

| Poste | Avant | Après | Calcul | Gain mensuel |
|---|---|---|---|---|
| Recherche d'un échange ou document client | 12 min, échec 1 fois sur 4 | ≈ 1 min (vue filtrée) | 6 recherches/jour/pers. × 5 pers. × 21 j = **630 recherches** × 11 min | **≈ 115 h** |
| Classement manuel des PJ | ≈ 1 min/mail (≈ 1 000 mails/mois) | 0 (upload auto) | 1 000 × 1 min | **≈ 17 h** |
| **Total** | | | | **≈ 130 h** |

Soit **≈ 0,8 ETP** libéré, ou **2,6 min par client et par mois** sur 3 000 clients. À 35 €/h chargé : **≈ 4 550 €/mois, ≈ 55 000 €/an**. Hypothèse prudente : le coût des ≈ 160 recherches ratées par mois (devis refait, client relancé) n'est pas valorisé.

## 2. Risques couverts

| Risque actuel | Couverture par le système |
|---|---|
| Information perdue (1 recherche sur 4) | Chaque mail archivé avec son `Message-ID`, traçable |
| Départ d'un commercial | Historique partagé dans la base, pas dans une tête |
| PJ introuvable ou mal classée | Dossier cloud par client + fiche `Fichiers` avec lien |
| Doublons clients | Rapprochement par domaine : `jean@carrasco.fr` et `marie@carrasco.fr` → un seul client |
| Échec silencieux d'un upload | 3 tentatives, puis fiche en `Échec` + email d'alerte |
| Pas de vision de l'activité client | Formules en cascade : nb mails, dernier échange, nb fichiers |

**Risques résiduels** : domaines génériques (`gmail.com`, `orange.fr`) à rapprocher par adresse complète ; latence de 5 min (IMAP) ; historique antérieur non repris.

## 3. Coût d'exploitation mensuel estimé

Volume généré : ≈ 9 000 fiches Mails + ≈ 5 000 fiches Fichiers par mois (≈ 170 000 enregistrements/an) et ≈ 3 Go de PJ par mois (≈ 35 Go/an).

| Poste | A — Production (auto-hébergé) | B — Stack SaaS de la démo |
|---|---|---|
| n8n | VPS 4 Go auto-hébergé : ≈ 15 € | n8n Cloud Pro (10 000 exécutions) : ≈ 60 € |
| Base de données | NocoDB / Baserow sur le même VPS : 0 € | Airtable Business, 2 éditeurs : ≈ 90 € |
| Stockage des PJ | OneDrive inclus dans Microsoft 365 : 0 € | Google Workspace 2 To : ≈ 14 € |
| Maintenance | 2 h × 50 € = 100 € | 2 h × 50 € = 100 € |
| **Total mensuel** | **≈ 115 €** | **≈ 265 €** |

Point d'attention : Airtable Business plafonne à 125 000 enregistrements par base, atteints en ≈ 9 mois. D'où le **scénario A recommandé** en production (même workflow n8n, seuls les nœuds de base changent).

## 4. Bilan

| | Scénario A | Scénario B |
|---|---|---|
| Gain / coût mensuel | ≈ 4 550 € / ≈ 115 € | ≈ 4 550 € / ≈ 265 € |
| **Gain net mensuel** | **≈ 4 400 €** | **≈ 4 300 €** |
| Mise en place (≈ 5 j × 500 € = 2 500 €) amortie en | **< 1 mois** | **< 1 mois** |

Même avec un gain divisé par trois (2 recherches/jour/commercial), le système est rentable dès le 2ᵉ mois. *Tarifs SaaS indicatifs (HT, 2025-2026), à confirmer au déploiement.*
