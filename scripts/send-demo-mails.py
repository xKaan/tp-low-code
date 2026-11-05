#!/usr/bin/env python3
"""Envoie un jeu de données fictif (8 emails réalistes) au serveur GreenMail local, pour la démo.

Mélange de clients déjà présents dans Airtable (Carrasco Industrie, Industries Garcia)
et de nouveaux domaines, dont un qui écrit deux fois (pour montrer qu'il n'est pas dupliqué).

Usage : python3 scripts/send-demo-mails.py [numéros...]   (ex : 1 2, défaut : tous)
"""
import smtplib
import sys
from email.message import EmailMessage
from email.utils import make_msgid

SMTP_HOST, SMTP_PORT = "localhost", 3025
DESTINATAIRE = "demo@techdistri.local"

MAILS = {
    1: (
        "Sophie Lemaire <s.lemaire@carrasco-indus.test>",
        "Demande de devis – 40 vérins hydrauliques VH-200",
        "Bonjour,\n\nPourriez-vous nous transmettre un devis pour 40 vérins hydrauliques "
        "VH-200, livraison souhaitée avant fin novembre à notre site de Lyon ?\n\n"
        "Merci d'avance,\nSophie Lemaire\nAcheteuse – Carrasco Industrie",
    ),
    2: (
        "Thomas Girard <t.girard@atelier-vauban.test>",
        "Première commande – roulements à billes 6204",
        "Bonjour,\n\nNous sommes un nouvel atelier de maintenance à Besançon. Nous souhaitons "
        "commander 200 roulements 6204-2RS. Pouvez-vous nous ouvrir un compte client ?\n\n"
        "Cordialement,\nThomas Girard\nAtelier Vauban",
    ),
    3: (
        "Carlos Garcia <c.garcia@ind-garcia.test>",
        "Bon de commande BC-25890",
        "Bonjour,\n\nVeuillez trouver ci-joint notre bon de commande BC-25890 "
        "(courroies trapézoïdales, réf. SPZ-1250, 60 unités).\n\nBien à vous,\n"
        "Carlos Garcia\nIndustries Garcia",
    ),
    4: (
        "Léa Fontaine <lea.fontaine@hydro-sud.test>",
        "Demande de catalogue 2027",
        "Bonjour,\n\nPourriez-vous m'envoyer votre catalogue 2027 ainsi que vos conditions "
        "tarifaires pour les distributeurs ?\n\nMerci,\nLéa Fontaine\nHydro Sud",
    ),
    5: (
        "Thomas Girard <t.girard@atelier-vauban.test>",
        "Re: Première commande – délai de livraison ?",
        "Bonjour,\n\nPetite relance concernant notre commande de roulements : pouvez-vous "
        "nous confirmer un délai de livraison ?\n\nMerci,\nThomas Girard\nAtelier Vauban",
    ),
    6: (
        "Service achats <achats@meca-precision.test>",
        "Réclamation – pièces non conformes (BL-7712)",
        "Bonjour,\n\nSur la livraison BL-7712, 12 pignons présentent un défaut d'usinage. "
        "Merci de nous indiquer la procédure de retour.\n\nService achats\nMéca Précision",
    ),
    7: (
        "Marc Dubois <m.dubois@carrasco-indus.test>",
        "Facture F-2026-1184 – question",
        "Bonjour,\n\nLa facture F-2026-1184 mentionne 45 vérins au lieu de 40. "
        "Pouvez-vous vérifier et nous renvoyer une facture corrigée ?\n\n"
        "Marc Dubois\nComptabilité – Carrasco Industrie",
    ),
    8: (
        "Nadia Benali <n.benali@hydro-sud.test>",
        "Rendez-vous commercial",
        "Bonjour,\n\nSuite à la demande de catalogue de ma collègue Léa Fontaine, "
        "seriez-vous disponible pour un rendez-vous la semaine prochaine ?\n\n"
        "Nadia Benali\nDirectrice commerciale – Hydro Sud",
    ),
}

numeros = [int(n) for n in sys.argv[1:]] or sorted(MAILS)

with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp:
    for n in numeros:
        expediteur, sujet, corps = MAILS[n]
        msg = EmailMessage()
        msg["From"] = expediteur
        msg["To"] = DESTINATAIRE
        msg["Subject"] = sujet
        msg["Message-ID"] = make_msgid(domain="techdistri.test")
        msg.set_content(corps)
        smtp.send_message(msg)
        print(f"#{n} envoyé : {expediteur} → {sujet}")
