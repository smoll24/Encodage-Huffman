#Project Encodage d'Huffman

#Importaiton des modules
import os
import csv


#creation de la structure arbre
class Noeud:
    """Un noeud ou une feuille d'un arbre binaire"""

    def __init__(self, valeur, gauche=None, droit=None):
        self.valeur = valeur
        self.gauche = gauche
        self.droit = droit

    def __str__(self):
        return f"[{self.valeur}, Cote Gauche: {self.gauche}, Cote Droite: {self.droit}]"


def get_frequency(phrase):
    #retourne dictionnaire avec frequence de chaque caractere
    occurences = {}
    for lettre in phrase:
        if lettre in occurences:
            occurences[lettre] += 1
        else:
            occurences[lettre] = 1
    return occurences

def liste_frequences(phrase):
    #cree une liste avec les frequences de chaque caractere dans une phrase
    liste = sorted(get_frequency(phrase).items(), key=lambda x: x[1])
    return liste


def somme(liste):
    #trouve somme de element 1 et element 2
    elt1 = liste[0][1]
    elt2 = liste[1][1]
    element = elt1 + elt2
    return element


def parcours_liste_lettre(arbre, letter, path=[]):
    #trouve le chemin a une liste en binaire
    if arbre is None or not arbre:
        return None

    if isinstance(arbre.gauche, tuple) and arbre.gauche[0] == letter:
        path.append(0)
        return path

    if isinstance(arbre.droit, tuple) and arbre.droit[0] == letter:
        path.append(1)
        return path

    if not isinstance(arbre.gauche, tuple):
        left_path = parcours_liste_lettre(arbre.gauche, letter, path + [0])
        if left_path:
            return left_path

    if not isinstance(arbre.droit, tuple):
        right_path = parcours_liste_lettre(arbre.droit, letter, path + [1])
        return right_path


def codes_binaires(arbre, phrase):
    #retourne dictionnaire avec les codes de chaque caractere
    liste = liste_frequences(phrase)
    codes = {}
    for el in liste:
        lettre = el[0]
        code = parcours_liste_lettre(arbre, lettre)
        codes[lettre] = code

    #aide https://stackoverflow.com/questions/5618878/how-to-convert-list-to-string
    for key, value in codes.items():
        codes[key] = ''.join(map(str, value))
    return codes


def compare(liste):
    #compare element 1 et element 2 et retourne tuple
    elt1 = liste[0]
    elt2 = liste[1]

    elt1_val = elt1[0] if isinstance(elt1[0], Noeud) else elt1
    elt2_val = elt2[0] if isinstance(elt2[0], Noeud) else elt2

    if elt1[1] > elt2[1]:
        return (elt2_val, elt1_val)
    else:
        return (elt1_val, elt2_val)


def liste_to_arbre(liste):
    #ajoute noeud dans la liste
    racine = Noeud(somme(liste), compare(liste)[0], compare(liste)[1])
    print('\nNoeud créé :', racine, '\n')
    for i in range(2):
        liste.pop(0)

    #insere le noeud dans la liste
    if len(liste) < 2 or racine.valeur > liste[-1][1]:
        liste.append((racine, racine.valeur))
        print('Liste :', liste, '\n')
        return None
    i = 0
    while liste[i][1] < racine.valeur:
        i += 1
    liste.insert(i, (racine, racine.valeur))
    print('Liste :', liste, '\n')


def construction_arbre(phrase):
    #construit l'arbre a partir d'un texte
    liste = liste_frequences(phrase)
    i = 0
    while len(liste) > 1:
        print('\n\u001b[34mEtape n', i + 1, ': \u001b[0m')
        liste_to_arbre(liste)
        i += 1
    return liste[0][0]


def phrase_binaire(phrase, codes):
    #transforme texte en str binaire
    binaire = []

    for lettre in phrase:
        if lettre in codes:
            binaire.append(codes[lettre])

    binaire_str = ''.join(binaire)
    return binaire_str


def phrase_lettres(binaire, codes):
    #transforme str binaire en texte
    n_zeros = int(codes['zeros'])
    codes.pop('zeros')
    lettres = {v: k for k, v in codes.items()}
    texte = []
    code = ""

    for bit in binaire[n_zeros:]:
        code += bit
        if code in lettres:
            texte.append(lettres[code])
            code = ""

    texte_str = ''.join(texte)
    return texte_str


def bits_to_bytes(binary_str):
    #transforme string de bits en bytes
    bytes_list = []
    for i in range(0, len(binary_str), 8):
        bytes_list.append(int(binary_str[i:i + 8], base=2))
    #https://www.programiz.com/python-programming/methods/built-in/bytes
    binary = bytes(bytes_list)
    return binary


def bytes_to_bits(binary):
    #transforme bytes en string de bits
    bytes_liste = []
    #https://stackoverflow.com/questions/10411085/converting-integer-to-binary-in-python
    #format(<the_integer>, "<0><width_of_string><format_specifier>")
    for byte in binary:
        bytes_liste.append(format(byte, '08b'))
    restored_binary_str = ''.join(bytes_liste)
    return restored_binary_str


def convert_text_binary(text):
    #https://www.askpython.com/python/examples/read-file-as-string-in-python
    with open(text, "r", encoding="utf-8") as f:
        text_to_str = f.read()

    #codage des caracteres
    print("\n------------------------------------------------\n")
    liste_frequence = liste_frequences(text_to_str)
    arbre = construction_arbre(text_to_str)
    codes = codes_binaires(arbre, text_to_str)
    print("\n------------------------------------------------\n")
    print("\u001b[32mListe des caractères:\n\n\u001b[0m", liste_frequence,
          "\n")
    print("\u001b[32mArbre final:\n\n\u001b[0m", arbre, "\n")
    print("\u001b[32mCodages des caractères:\n\n\u001b[0m", codes)
    print("\n------------------------------------------------\n")

    #binary to bytes -- first make binary_str length a multiple of 8
    binary_str = phrase_binaire(text_to_str, codes)
    n_zeros = 0
    while len(binary_str) % 8 != 0:
        binary_str = "0" + binary_str
        n_zeros += 1
    binary = bits_to_bytes(binary_str)
    codes['zeros'] = n_zeros

    #write binary to bin file
    #https://stackoverflow.com/questions/18367007/python-how-to-write-to-a-binary-file
    binary_file = open(str(text[:-4] + '_binary.bin'), "wb")
    binary_file.write(binary)
    binary_file.close()

    with open(str(text[:-4] + '_csv.csv'), 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['Character', 'Binary'])

        for key, value in codes.items():
            w.writerow([key, value])

    print("Fichier binaire saved to", str(text[:-4] + '_binary.bin'))
    print("Fichier csv saved to", str(text[:-4] + '_csv.csv'))

    text_size = os.path.getsize(text)
    bin_size = os.path.getsize(str(text[:-4] + '_binary.bin'))
    print("\nTaille du fichier texte :", text_size, "bytes =>",
          int(text_size / 1024), "megabytes")
    print("Taille du bicher binaire:", bin_size, "bytes =>",
          int(bin_size / 1024), "megabytes")
    print("\nLa taille du fichier binaire est",
          (float(bin_size) / float(text_size)), "fois le texte d'origine.")


def convert_binary_text(binaire, codes_csv):
    #https://stackoverflow.com/questions/8710456/reading-a-binary-file-with-python
    with open(binaire, mode='rb') as f:
        binary = f.read()

    with open(codes_csv, mode='r') as infile:
        reader = csv.reader(infile)
        with open(codes_csv, mode='r') as outfile:
            writer = csv.writer(outfile)
            codes = {rows[0]: rows[1] for rows in reader}

    #bytes back to binary back to text
    restored_binary_str = bytes_to_bits(binary)
    restored = phrase_lettres(restored_binary_str, codes)

    #write text to txt file
    #https://stackoverflow.com/questions/5214578/print-string-to-text-file
    text_file = open(str(binaire[:-11] + '_restored.txt'), "w")
    text_file.write(restored)
    text_file.close()

    print("Version reconstituée a partir du ficher binaire saved to",
          str(binaire[:-11] + '_restored.txt'))


def liste_fichiers(fin):
    #https://builtin.com/data-science/python-list-files-in-directory
    fichiers = [f for f in os.listdir() if f.endswith(fin)]
    return fichiers


def phrase_to_bin(text):
    text_to_str = text
    #codage des caracteres
    print("\n------------------------------------------------\n")
    liste_frequence = liste_frequences(text_to_str)
    arbre = construction_arbre(text_to_str)
    codes = codes_binaires(arbre, text_to_str)
    print("\n------------------------------------------------\n")
    print("\u001b[32mListe des caractères:\n\n\u001b[0m", liste_frequence,
          "\n")
    print("\u001b[32mArbre final:\n\n\u001b[0m", arbre, "\n")
    print("\u001b[32mCodages des caractères:\n\n\u001b[0m", codes)
    print("\n------------------------------------------------\n")
    return codes


def main():
    #Interface principale
    print("Compression de textes avec l'encodage d'Huffman\n")
    print("1. Compresser un fichier texte")
    print("2. Décompresser un fichier texte")
    print("3. Encoder une phrase")
    choix = input("\n\u001b[33mEntrez votre choix (1/3) : \u001b[0m")

    if choix == '1':
        #Choix de compression
        print("\nFichiers .txt disponibles : \n")
        txt_fichiers = liste_fichiers('.txt')
        for indice, file in enumerate(txt_fichiers):
            print(f"{indice+1}. {file}")

        indice_fichier = int(
            input(
                "\n\u001b[33mEntrez l'indice du fichier à compresser : \u001b[0m"
            )) - 1
        fichier = txt_fichiers[indice_fichier]

        convert_text_binary(fichier)

    elif choix == '2':
        #Choix de decompression
        print("\nFichiers .bin disponibles : \n")
        bin_fichiers = liste_fichiers('.bin')
        for indice, file in enumerate(bin_fichiers):
            print(f"{indice+1}. {file}")

        indice_fichier = int(
            input(
                "\n\u001b[33mEntrez l'indice du fichier à décompresser : \u001b[0m"
            )) - 1
        fichier = bin_fichiers[indice_fichier]

        print("\nFichiers .csv disponibles : \n")
        codes_csv = liste_fichiers('.csv')
        for indice, file in enumerate(codes_csv):
            print(f"{indice+1}. {file}")

        indice_csv = int(
            input(
                "\n\u001b[33mEntrez l'index du fichier csv pour décoder le fichier .bin : \u001b[0m"
            )) - 1
        csv = codes_csv[indice_csv]

        convert_binary_text(fichier, csv)

    elif choix == '3':
        phrase = input("Ecris votre phrase: ")
        codes = phrase_to_bin(phrase)
        print(f'{phrase} => {phrase_binaire(phrase, codes)}')


#-----------------
#APPEL DES FONCTIONS

main()
