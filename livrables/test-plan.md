# Plan de test — Niveau 1

Conforme à l'exigence du brief : "Démo : envoyer 5 emails depuis 3
expéditeurs différents, vérifier la base."

## Jeu d'emails à envoyer (dans cet ordre, à la boîte de démo)

| # | Expéditeur | Domaine | Sujet | But du test |
|---|---|---|---|---|
| 1 | jean.dupont@carrasco.fr | carrasco.fr | Demande de devis vérins hydrauliques | Première fois que le domaine `carrasco.fr` apparaît → doit créer le Client `carrasco.fr` |
| 2 | contact@meca-nord.fr | meca-nord.fr | Commande n°4521 | Nouveau domaine → doit créer un 2e Client `meca-nord.fr` |
| 3 | marie.dupont@carrasco.fr | carrasco.fr | Relance devis vérins | Expéditeur différent, même domaine que #1 → NE DOIT PAS créer de doublon Client, doit lier au Client `carrasco.fr` existant |
| 4 | contact@meca-nord.fr | meca-nord.fr | Bon de livraison BL-9081 | Même expéditeur que #2 → doit lier au Client `meca-nord.fr` existant |
| 5 | achats@dupont-outillage.fr | dupont-outillage.fr | Réclamation commande n°4498 | 3e domaine → doit créer un 3e Client `dupont-outillage.fr` |

## Résultat attendu dans Airtable après les 5 emails

**Table Clients : exactement 3 enregistrements**
- `carrasco.fr` (créé à l'email #1, réutilisé à l'email #3)
- `meca-nord.fr` (créé à l'email #2, réutilisé à l'email #4)
- `dupont-outillage.fr` (créé à l'email #5)

**Table Mails : exactement 5 enregistrements**, chacun avec :
- Statut traitement = `Nouveau`
- Client correctement lié (vérifier notamment que les mails #1 et #3
  pointent bien vers le même enregistrement Client, pas deux enregistrements
  différents — c'est le test clé de la déduplication)

## Procédure de démo live (brief : 10 min démo + 8 min Q/R)

1. Montrer la base Airtable vide (ou avec les tables créées mais 0 ligne).
2. Envoyer les emails #1 et #2 depuis les boîtes de test préparées à l'avance.
3. Attendre le prochain cycle de polling IMAP (jusqu'à 5 min — prévoir ce
   temps mort dans le timing, ou déclencher une exécution manuelle du
   workflow dans n8n pour la démo si le timing est serré).
4. Montrer la création des 2 fiches Client + 2 fiches Mail dans Airtable.
5. Envoyer l'email #3 (même domaine que #1) en direct.
6. Montrer qu'aucun nouveau Client n'est créé, et que la fiche Mail #3 est
   liée au Client existant `carrasco.fr`.
7. Envoyer les emails #4 et #5, montrer le résultat final (3 Clients, 5 Mails).

## Plan B (recommandé par le brief)

Enregistrer une vidéo de ce scénario complet à l'avance, à montrer si la
démo live échoue (problème réseau, IMAP lent, etc.).
