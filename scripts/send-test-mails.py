#!/usr/bin/env python3
"""Envoie les 5 emails du plan de test (livrables/test-plan.md) au serveur GreenMail local.

Usage : python3 scripts/send-test-mails.py [numéros...]   (ex : 1 2, défaut : tous)
"""
import smtplib
import sys
from email.message import EmailMessage

SMTP_HOST, SMTP_PORT = "localhost", 3025
DESTINATAIRE = "demo@techdistri.local"

MAILS = {
    1: ("jean.dupont@carrasco-indus.test", "Demande de devis vérins hydrauliques"),
    2: ("contact@meca-nord.fr", "Commande n°4521"),
    3: ("marie.dupont@carrasco-indus.test", "Relance devis vérins"),
    4: ("contact@meca-nord.fr", "Bon de livraison BL-9081"),
    5: ("achats@dupont-outillage.fr", "Réclamation commande n°4498"),
}

numeros = [int(n) for n in sys.argv[1:]] or sorted(MAILS)

with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp:
    for n in numeros:
        expediteur, sujet = MAILS[n]
        msg = EmailMessage()
        msg["From"] = expediteur
        msg["To"] = DESTINATAIRE
        msg["Subject"] = sujet
        msg.set_content(f"Bonjour,\n\nCeci est l'email de test #{n}.\n\nCordialement,\n{expediteur}")
        smtp.send_message(msg)
        print(f"#{n} envoyé : {expediteur} → {sujet}")
