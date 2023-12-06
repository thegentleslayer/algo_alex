import random
from hashlib import sha256

# Fonction pour générer une clé aléatoire de longueur b
def generer_cle(b):
    # Liste de caractères possibles
    caracteres = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                  'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                  'u', 'v', 'w', 'x', 'y', 'z']

    majuscules = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
                  'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                  'U', 'V', 'W', 'X', 'Y', 'Z']

    chiffres = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    caracteres_speciaux = ['&', '#', '@', '$', '%', '.', '?', '!']
    
    # Liste combinée de tous les caractères possibles
    ensemble_caracteres = caracteres + majuscules + chiffres + caracteres_speciaux

    # Générer une chaîne aléatoire en choisissant des caractères dans l'ensemble
    cle = ''.join(random.choice(ensemble_caracteres) for _ in range(b))
    return cle

# Fonction pour effectuer la substitution des caractères
def substitution(caracteres):
    # Initialiser une nouvelle chaîne vide pour le résultat
    nouvelle_chaine = ""

    for s, char in enumerate(caracteres):
        # Déterminer la liste de caractères appropriée en fonction de la catégorie du caractère
        if char in lettres_minuscules:
            liste_caracteres = lettres_minuscules
        elif char in majuscules:
            liste_caracteres = majuscules
        elif char in chiffres:
            liste_caracteres = chiffres
        elif char in caracteres_speciaux:
            liste_caracteres = caracteres_speciaux
        else:
            # Si le caractère n'est pas dans une catégorie connue, le conserver tel quel
            nouvelle_chaine += char
            continue

        # Effectuer une substitution en faisant tourner la liste de caractères
        index = liste_caracteres.index(char)
        nouvelle_chaine += liste_caracteres[(index + len(caracteres) - s) % len(liste_caracteres)]

    return nouvelle_chaine

# Fonction pour calculer le haché SHA-256 d'une chaîne
def calculer_hash_sha256(chaine):
    hash_sha256 = sha256(chaine.encode('utf-8')).hexdigest()
    return hash_sha256

# Fonction pour obtenir le haché SHA-256 sous forme de bytes
def hash_en_bytes(chaine):
    hash_bytes = sha256(chaine.encode('utf-8')).digest()
    return hash_bytes

# Fonction pour chiffrer un fichier
def chiffrement(fichier_entree, fichier_sortie, cle_substitution):
    with open(fichier_entree, 'rb') as fichier_entree:
        with open(fichier_sortie, 'wb') as fichier_sortie:
            # Convertir le haché en séquence binaire de bits
            sequence_cle = ''.join(format(x, '08b') for x in hash_en_bytes(cle_substitution))
            compteur = 0

            while fichier_entree.peek():
                octet = ord(fichier_entree.read(1))
                indice_cle = compteur % len(hash_en_bytes(cle_substitution))
                octet_chiffre = bytes([octet ^ hash_en_bytes(cle_substitution)[indice_cle]])
                fichier_sortie.write(octet_chiffre)
                compteur += 1

# Fonction pour déchiffrer un fichier
def dechiffrement(fichier_chiffre, fichier_sortie, cle_substitution):
    with open(fichier_chiffre, 'rb') as fichier_chiffre:
        with open(fichier_sortie, 'wb') as fichier_sortie:
            # Convertir le haché en séquence binaire de bits
            sequence_cle = ''.join(format(x, '08b') for x in hash_en_bytes(cle_substitution))
            compteur = 0

            while fichier_chiffre.peek():
                octet_chiffre = ord(fichier_chiffre.read(1))
                indice_cle = compteur % len(hash_en_bytes(cle_substitution))
                octet_dechiffre = octet_chiffre ^ hash_en_bytes(cle_substitution)[indice_cle]
                fichier_sortie.write(bytes([octet_dechiffre]))
                compteur += 1

# Générer une clé aléatoire
cle = generer_cle(5)

# Effectuer la substitution des caractères dans la clé
cle_substitution = substitution(cle)

# Calculer le haché SHA-256 de la clé d'origine
hash_cle = calculer_hash_sha256(cle)

print("Clé d'origine : ", cle)
print("Clé après substitution : ", cle_substitution)
print("Haché SHA-256 de la clé d'origine : ", hash_cle)

# Chiffrer un fichier avec la clé substituée
chiffrement("msg.txt", "msg_ch.txt", cle_substitution)

# Déchiffrer le fichier chiffré avec la clé substituée
dechiffrement("msg_ch.txt", "msg_dch.txt", cle_substitution)
