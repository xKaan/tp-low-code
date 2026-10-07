#!/usr/bin/env python3
"""Envoie au serveur GreenMail local une sélection de vrais emails .eml du jeu
de données (ressources/techdistri/emails/), choisis pour couvrir les cas du
plan de test Niveau 2 (livrables/test-plan-niveau2.md) : 0, 1, 2 et 5 pièces
jointes, provenant de clients déjà présents dans clients_attendus.csv.

Contrairement à scripts/send-test-mails.py (emails synthétiques sans PJ), ce
script envoie les fichiers .eml tels quels : les pièces jointes réelles
(PDF/Excel/PNG/texte) sont donc préservées et atteignent l'IMAP du workflow.

Usage : python3 scripts/send-test-mails-pj.py [clés...]   (défaut : toutes)
  python3 scripts/send-test-mails-pj.py 0pj 5pj
"""
import smtplib
import sys
from email import policy
from email.parser import BytesParser
from pathlib import Path

SMTP_HOST, SMTP_PORT = "localhost", 3025
DESTINATAIRE = "demo@techdistri.local"
EMAILS_DIR = Path(__file__).resolve().parent.parent / "ressources" / "techdistri" / "emails"

# clé -> (fichier .eml, description du cas testé)
FICHIERS = {
    "0pj": ("001_j.carrasco_Demande_de_devis_-_plaques_aci.eml", "0 PJ — ne doit pas casser le workflow"),
    "1pj": ("011_c.garcia_Commande_BC-25471.eml", "1 PJ (BC_BC-25471.xlsx)"),
    "2pj": ("033_l.dupont_Documentation_produit.eml", "2 PJ (deux fiches techniques PDF)"),
    "5pj": ("040_m.granet_Dossier_complet_projet_Marseil.eml", "5 PJ — cas piégeux volume de la boucle d'upload"),
}

cles = sys.argv[1:] or list(FICHIERS)

with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp:
    for cle in cles:
        if cle not in FICHIERS:
            print(f"Clé inconnue : {cle} (choix possibles : {', '.join(FICHIERS)})")
            continue
        nom_fichier, description = FICHIERS[cle]
        chemin = EMAILS_DIR / nom_fichier
        with open(chemin, "rb") as f:
            msg = BytesParser(policy=policy.default).parse(f)

        expediteur = msg["From"]
        sujet = msg["Subject"]
        if "To" in msg:
            del msg["To"]
        msg["To"] = DESTINATAIRE

        smtp.send_message(msg, to_addrs=[DESTINATAIRE])
        print(f"[{cle}] envoyé : {expediteur} -> {sujet}  ({description})")
