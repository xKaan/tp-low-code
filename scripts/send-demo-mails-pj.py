#!/usr/bin/env python3
"""Envoie au serveur GreenMail local 4 emails fictifs avec de vraies pièces jointes (niveau 2).

Couvre les cas du plan de test niveau 2 (0, 1, 2 et 5 PJ) avec les entreprises
du jeu de données de démo (scripts/send-demo-mails.py). Les fichiers (PDF, PNG,
CSV) sont générés à la volée, rien à télécharger.

Usage : python3 scripts/send-demo-mails-pj.py [clés...]   (ex : 1pj 5pj, défaut : toutes)

Chaque envoi reçoit un Message-ID unique (un nouvel envoi n'est donc jamais pris
pour un doublon). Clé spéciale `doublon` : envoie 2 fois le même mail avec le
même Message-ID, pour tester la déduplication (1 seule fiche Mail attendue).
Clé spéciale `nouveau-client` : envoie 2 mails d'un domaine jamais vu (généré à
chaque lancement) : le 1er crée le Client, le 2e doit le réutiliser (1 seul Client).
"""
import smtplib
import time
import struct
import sys
import zlib
from email.message import EmailMessage
from email.utils import make_msgid

SMTP_HOST, SMTP_PORT = "localhost", 3025
DESTINATAIRE = "demo@techdistri.local"


def pdf(titre):
    """PDF d'une page contenant un titre."""
    texte = titre.encode("latin-1", "replace")
    contenu = b"BT /F1 24 Tf 72 720 Td (" + texte + b") Tj ET"
    objets = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Contents 4 0 R "
        b"/Resources << /Font << /F1 5 0 R >> >> >>",
        b"<< /Length " + str(len(contenu)).encode() + b" >>\nstream\n" + contenu + b"\nendstream",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    ]
    out, offsets = b"%PDF-1.4\n", []
    for i, obj in enumerate(objets, 1):
        offsets.append(len(out))
        out += f"{i} 0 obj\n".encode() + obj + b"\nendobj\n"
    xref = len(out)
    out += f"xref\n0 {len(objets) + 1}\n0000000000 65535 f \n".encode()
    out += b"".join(f"{o:010d} 00000 n \n".encode() for o in offsets)
    out += f"trailer\n<< /Size {len(objets) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode()
    return out


def png(couleur, taille=64):
    """Image PNG unie de taille x taille pixels."""
    ligne = b"\x00" + bytes(couleur) * taille
    brut = zlib.compress(ligne * taille)

    def bloc(type_, data):
        return struct.pack(">I", len(data)) + type_ + data + struct.pack(">I", zlib.crc32(type_ + data))

    return (b"\x89PNG\r\n\x1a\n" + bloc(b"IHDR", struct.pack(">IIBBBBB", taille, taille, 8, 2, 0, 0, 0))
            + bloc(b"IDAT", brut) + bloc(b"IEND", b""))


def csv(lignes):
    return ("\n".join(";".join(map(str, l)) for l in lignes) + "\n").encode("utf-8")


# clé -> (expéditeur, sujet, corps, [(nom, type MIME, contenu)])
MAILS = {
    "0pj": (
        "Sophie Lemaire <s.lemaire@carrasco-indus.test>",
        "Question sur le délai des vérins VH-200",
        "Bonjour,\n\nPouvez-vous me confirmer le délai de livraison des vérins VH-200 ?\n\n"
        "Merci,\nSophie Lemaire\nCarrasco Industrie",
        [],
    ),
    "1pj": (
        "Carlos Garcia <c.garcia@ind-garcia.test>",
        "Bon de commande BC-26012",
        "Bonjour,\n\nVeuillez trouver ci-joint notre bon de commande BC-26012.\n\n"
        "Bien à vous,\nCarlos Garcia\nIndustries Garcia",
        [("BC-26012.pdf", "application/pdf", pdf("Bon de commande BC-26012"))],
    ),
    "2pj": (
        "Thomas Girard <t.girard@atelier-vauban.test>",
        "Plans pour devis – arbre de transmission",
        "Bonjour,\n\nCi-joint le plan et une photo de la pièce à reproduire.\n\n"
        "Cordialement,\nThomas Girard\nAtelier Vauban",
        [
            ("plan-arbre-transmission.pdf", "application/pdf", pdf("Plan arbre de transmission")),
            ("photo-piece.png", "image/png", png((120, 120, 130))),
        ],
    ),
    "5pj": (
        "Léa Fontaine <lea.fontaine@hydro-sud.test>",
        "Dossier complet – appel d'offres station de pompage",
        "Bonjour,\n\nVoici le dossier complet de l'appel d'offres (5 documents).\n\n"
        "Merci,\nLéa Fontaine\nHydro Sud",
        [
            ("cahier-des-charges.pdf", "application/pdf", pdf("Cahier des charges")),
            ("planning-travaux.pdf", "application/pdf", pdf("Planning des travaux")),
            ("quantitatif.csv", "text/csv", csv([["Référence", "Quantité"], ["VH-200", 12], ["SPZ-1250", 40]])),
            ("plan-site.png", "image/png", png((40, 90, 160))),
            ("photo-installation.png", "image/png", png((60, 140, 70))),
        ],
    ),
}

# Cas piégeux : envoyés uniquement à la demande (pas dans le lot par défaut)
CAS_PIEGEUX = {
    # Deux TPE différentes sur le même domaine grand public : 2 clients distincts
    "gmail1": (
        "Henri Petit <h.petit.btp@gmail.test>",
        "Devis rénovation salle de bain",
        "Bonjour,\n\nPouvez-vous me faire un devis pour une rénovation ?\n\nHenri Petit\nPetit BTP",
        [],
    ),
    "gmail2": (
        "Mathieu Atelier <mathieu.atelier@gmail.test>",
        "Demande de prix – outillage",
        "Bonjour,\n\nJe souhaite un prix sur une perceuse à colonne.\n\nMathieu\nAtelier Mathieu",
        [],
    ),
    # Expéditeur automatique : doit être ignoré (ni Client ni Mail)
    "noreply": (
        "TechDistri Notif <noreply@techdistri-portail.test>",
        "[AUTO] Récapitulatif quotidien commandes",
        "Ceci est un email automatique.\n\nNe pas répondre à cet email.",
        [],
    ),
    # Reply avec citations profondes : seul le message utile doit être gardé
    "citations": (
        "Antoine Martin <a.martin@construc-tech.test>",
        "Re: Re: Re: Devis DV-2026-0145 - questions",
        "Bonjour,\n\nMerci pour le retour. OK pour ce prix.\n\nA. Martin\n\n"
        "> Le 14/03/2026, TechDistri a écrit :\n"
        "> Bonjour M. Martin, voici notre meilleure offre : remise 8%.\n"
        ">\n"
        "> > Le 13/03/2026, vous avez écrit :\n"
        "> > Pouvez-vous faire un geste sur le prix ?\n"
        "> >\n"
        "> > > Le 12/03/2026, TechDistri a écrit :\n"
        "> > > Bonjour, voici le devis joint.\n",
        [],
    ),
}
MAILS_PAR_CLE = {**MAILS, **CAS_PIEGEUX}

cles = sys.argv[1:] or list(MAILS)
MESSAGE_ID_DOUBLON = "<test-doublon-1pj@techdistri.local>"

with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp:
    for cle in cles:
        # `doublon` = le mail 1pj envoyé 2 fois avec le même Message-ID
        envois = [("1pj", MESSAGE_ID_DOUBLON)] * 2 if cle == "doublon" else [(cle, None)]
        if cle == "nouveau-client":
            # domaine unique par lancement : garantit la branche "Client à créer"
            domaine = f"nouveau-{int(time.time())}.test"
            envois = [(("nc1", domaine), None), (("nc2", domaine), None)]
        for vraie_cle, message_id in envois:
            if isinstance(vraie_cle, tuple):
                numero, domaine = vraie_cle
                expediteur = f"Contact Achats <achats@{domaine}>"
                sujet = f"Demande de devis ({numero[-1]}/2) - {domaine}"
                corps = f"Bonjour,\n\nMerci de nous faire un devis.\n\nCordialement,\n{domaine}"
                pieces = [] if numero == "nc1" else [("demande.pdf", "application/pdf", pdf(f"Demande {domaine}"))]
            else:
                expediteur, sujet, corps, pieces = MAILS_PAR_CLE[vraie_cle]
            msg = EmailMessage()
            msg["From"] = expediteur
            msg["To"] = DESTINATAIRE
            msg["Subject"] = sujet
            msg["Message-ID"] = message_id or make_msgid(domain="techdistri.local")
            msg["Message-ID"] = make_msgid(domain="techdistri.test")msg.set_content(corps)
            for nom, mime, contenu in pieces:
                principal, secondaire = mime.split("/")
                msg.add_attachment(contenu, maintype=principal, subtype=secondaire, filename=nom)
            smtp.send_message(msg)
            print(f"{cle} envoyé : {expediteur} → {sujet} ({len(pieces)} PJ) {msg['Message-ID']}")
