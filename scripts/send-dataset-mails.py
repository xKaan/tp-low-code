#!/usr/bin/env python3
"""Envoie les 50 .eml du jeu de données (techdistri/emails) au serveur GreenMail local.

Le script fourni (techdistri/envoi_emails.py) impose STARTTLS + login Gmail,
ce que GreenMail ne propose pas : celui-ci envoie en clair sur localhost:3025.

Usage : python3 scripts/send-dataset-mails.py [numéros...]   (ex : 043 044 048, défaut : tous)
"""
import email
import smtplib
import sys
import time
from email import policy
from pathlib import Path

SMTP_HOST, SMTP_PORT = "localhost", 3025
DESTINATAIRE = "demo@techdistri.local"
DOSSIER = Path(__file__).resolve().parent.parent / "techdistri" / "emails"

numeros = set(sys.argv[1:])
fichiers = sorted(f for f in DOSSIER.glob("*.eml") if not numeros or f.name[:3] in numeros)

with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp:
    for f in fichiers:
        with open(f, "rb") as fh:
            msg = email.message_from_binary_file(fh, policy=policy.default)
        del msg["To"]
        msg["To"] = DESTINATAIRE
        smtp.send_message(msg, to_addrs=[DESTINATAIRE])
        print(f"envoyé {f.name[:3]} — {msg['From']} — {msg['Subject']}")
        time.sleep(0.2)

print(f"{len(fichiers)} email(s) envoyé(s) à {DESTINATAIRE}")
