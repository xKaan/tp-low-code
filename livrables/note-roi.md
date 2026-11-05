# Note ROI : centralisation des emails TechDistri

Projet NoCode, niveau 2. Novembre 2026.

## Contexte et hypothèses

TechDistri compte 3 000 clients professionnels et reçoit entre 8 000 et 10 000 emails par mois. Pour les calculs, nous avons retenu 9 000 emails par mois. Le système sera utilisé par 6 personnes : 5 commerciaux et la direction. Le coût horaire chargé d'un commercial est estimé à 35 €.

## Temps gagné

Aujourd'hui, retrouver un échange ou un document client prend en moyenne 12 minutes, et la recherche échoue une fois sur quatre. Avec la base, il suffit de filtrer la vue sur le client, ce qui prend environ une minute. Si chaque commercial fait 6 recherches par jour, cela représente 630 recherches par mois (5 personnes sur 21 jours ouvrés). Avec 11 minutes gagnées à chaque fois, on arrive à environ 115 heures par mois.

Il faut ajouter le classement manuel des pièces jointes dans les dossiers Windows. Nous l'estimons à une minute par mail pour environ 1 000 mails par mois, soit 17 heures, qui disparaissent puisque l'upload vers le dossier du client est automatique.

Au total, le système fait gagner environ 130 heures par mois, ce qui correspond à près de 0,8 équivalent temps plein, ou 2,6 minutes par client et par mois. Cela représente environ 4 550 € par mois, soit 55 000 € par an. Nous n'avons pas compté le coût des 160 recherches qui échouent chaque mois (devis refait, client relancé), le chiffre réel est donc probablement plus élevé.

## Risques couverts

Le premier risque est la perte d'information. Chaque mail est désormais enregistré avec son Message-ID et rattaché à sa fiche client. L'historique ne dépend plus de la mémoire de l'équipe, ce qui protège aussi l'entreprise en cas de départ d'un commercial. Les pièces jointes sont rangées automatiquement dans un dossier par client et chaque fichier a sa fiche avec le lien cloud. Le rapprochement par domaine évite les doublons : jean@carrasco.fr et marie@carrasco.fr sont rattachés au même client Carrasco. Enfin, si un upload échoue après trois tentatives, une fiche « Échec » est créée et un email d'alerte est envoyé, donc rien ne se perd sans laisser de trace.

Quelques limites restent à traiter : les adresses sur des domaines génériques comme gmail.com ou orange.fr, qu'il faudra rapprocher par adresse complète, le délai de 5 minutes lié à la relève IMAP, et l'historique antérieur à la mise en service, qui n'est pas repris.

## Coût d'exploitation mensuel

Au volume de TechDistri, le système crée environ 14 000 fiches par mois (mails et fichiers), soit 170 000 par an, et environ 3 Go de pièces jointes par mois. Nous avons comparé deux options.

| Poste | Option A : auto-hébergée | Option B : outils SaaS (démo) |
|---|---|---|
| n8n | Serveur VPS : 15 € | n8n Cloud Pro : 60 € |
| Base de données | NocoDB sur le même serveur : 0 € | Airtable Business, 2 éditeurs : 90 € |
| Stockage | OneDrive inclus dans Microsoft 365 : 0 € | Google Workspace 2 To : 14 € |
| Maintenance | 2 h par mois : 100 € | 2 h par mois : 100 € |
| **Total** | **115 €** | **265 €** |

Nous recommandons l'option A pour la production. L'offre Airtable Business est limitée à 125 000 enregistrements par base, une limite qui serait atteinte en 9 mois environ. Le workflow n8n reste le même, seuls les nœuds de la base de données changent.

## Conclusion

Avec un gain de 4 550 € par mois pour un coût de 115 à 265 €, le gain net est d'environ 4 300 à 4 400 € par mois. La mise en place, estimée à 5 jours (2 500 €), est remboursée en moins d'un mois. Même si le gain réel était trois fois plus faible, le projet serait rentable dès le deuxième mois. Les tarifs indiqués sont hors taxes et à vérifier au moment du déploiement.
