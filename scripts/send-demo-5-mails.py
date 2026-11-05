#!/usr/bin/env python3
"""Envoie d'un coup 5 emails de démo, tous de expéditeurs et d'entreprises différents.

Pensé pour la démo live : 5 clients distincts, avec 0 à 3 pièces jointes
(PDF, PNG, CSV générés à la volée, rien à télécharger).

Attendu après passage du workflow :
  - 5 fiches Client (une par domaine), 5 fiches Mail ;
  - 6 fiches Fichier (0 + 1 + 2 + 1 + 2) et 4 dossiers Drive.

Chaque envoi a un Message-ID unique : on peut relancer le script sans que les
mails soient pris pour des doublons (les clients, eux, sont réutilisés).

Usage : python3 scripts/send-demo-5-mails.py
"""
import smtplib
import struct
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


# (expéditeur, sujet, corps, pièces jointes) : 5 entreprises, 5 domaines différents
MAILS = [
    (
        "Camille Roux <c.roux@aciers-roux.test>",
        "Demande de devis – tôles inox 304",
        "Bonjour,\n\nPouvez-vous nous faire un devis pour 200 tôles inox 304 (2 mm) ?\n\n"
        "Cordialement,\nCamille Roux\nAciers Roux",
        [],
    ),
    (
        "Nadia Benali <n.benali@hydro-lorraine.test>",
        "Bon de commande BC-26140",
        "Bonjour,\n\nVeuillez trouver ci-joint notre bon de commande BC-26140.\n\n"
        "Bien à vous,\nNadia Benali\nHydro Lorraine",
        [("BC-26140.pdf", "application/pdf", pdf("Bon de commande BC-26140"))],
    ),
    (
        "Pierre Vasseur <p.vasseur@vasseur-transports.test>",
        "Réclamation livraison BL-79012",
        "Bonjour,\n\nLa livraison BL-79012 est arrivée endommagée, photo et bon de livraison joints.\n\n"
        "Merci de revenir vers nous rapidement.\nPierre Vasseur\nVasseur Transports",
        [
            ("BL-79012.pdf", "application/pdf", pdf("Bon de livraison BL-79012")),
            ("photo-palette.png", "image/png", png((150, 90, 60))),
        ],
    ),
    (
        "Sandrine Moreau <s.moreau@electro-ouest.test>",
        "Facture FA-2026-0388 – demande de copie",
        "Bonjour,\n\nPourriez-vous nous renvoyer la facture FA-2026-0388 ?\n\n"
        "Merci,\nSandrine Moreau\nElectro Ouest",
        [("FA-2026-0388.pdf", "application/pdf", pdf("Facture FA-2026-0388"))],
    ),
    (
        "Julien Faure <j.faure@faure-batiment.test>",
        "Appel d'offres – chantier entrepôt Lyon",
        "Bonjour,\n\nVoici les pièces de notre appel d'offres pour l'entrepôt de Lyon.\n\n"
        "Cordialement,\nJulien Faure\nFaure Bâtiment",
        [
            ("cahier-des-charges.pdf", "application/pdf", pdf("Cahier des charges entrepôt")),
            ("quantitatif.csv", "text/csv", csv([["Référence", "Quantité"], ["IPE-200", 48], ["HEA-160", 30]])),
        ],
    ),
]

with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp:
    for expediteur, sujet, corps, pieces in MAILS:
        msg = EmailMessage()
        msg["From"] = expediteur
        msg["To"] = DESTINATAIRE
        msg["Subject"] = sujet
        msg["Message-ID"] = make_msgid(domain="techdistri.local")
        msg.set_content(corps)
        for nom, mime, contenu in pieces:
            principal, secondaire = mime.split("/")
            msg.add_attachment(contenu, maintype=principal, subtype=secondaire, filename=nom)
        smtp.send_message(msg)
        print(f"envoyé : {expediteur} → {sujet} ({len(pieces)} PJ)")

print(f"\n{len(MAILS)} mails envoyés à {DESTINATAIRE}")
