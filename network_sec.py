import numpy as np
from preprocess import text_preprocess

def ceaser(text,shift):
    cipher=""
    text=text_preprocess(text)
    for i in text:
        cipher+=(chr((ord(i)-97+shift)%26+97))
    return cipher

def create_playfair_matrix(key,i_j):
    matrix =[]
    alphabet="abcdefghiklmnopqrstuvwxyz"
    alphabet=alphabet.replace("i",i_j)
    alphabet=alphabet.replace("j",i_j)

    for letter in key:
        alphabet=alphabet.replace(letter, '')
    key=key+alphabet
    for i in range (5):
        col = []
        for j in range(5):
            col.append(key[i * 5 + j])
        matrix.append(col)
    return matrix

def find_indices(matrix, char):
    indices = np.where(np.array(matrix) == char)
    return list(zip(indices[0], indices[1]))

def playfair(key,text,i_j = 'i'):
    cipher=""
    key = "".join(dict.fromkeys(key))
    text=text_preprocess(text)
    text=text.replace("i",i_j)
    text=text.replace("j",i_j)
    matrix=create_playfair_matrix(key,i_j)
    new_string = ''.join([char + 'x' if i < len(text) - 1 and char == text[i + 1] and i % 2 == 0 else char for i, char in enumerate(text)])

    pairs = [(new_string[i], new_string[i + 1] if i + 1 < len(new_string) else 'x') for i in range(0, len(new_string), 2)]

    results = []
    for pair in pairs:
        char1, char2 = pair
        index1 = find_index(matrix, char1)
        index2 = find_index(matrix, char2)
        if index1[0] == index2[0]:
            result = "Same Row"
            new_index1=(index1[0],(index1[1]+1)%5)
            new_index2=(index2[0],(index2[1]+1)%5)
        elif index1[1] == index2[1]:
            result = "Same Column"
            new_index1=((index1[0]+1)%5,index1[1])
            new_index2=((index2[0]+1)%5,index2[1])
        else:
            result = "Different Row and Column"
            new_index1=(index1[0],index2[1])
            new_index2=(index2[0],index1[1])
        new_pair=(new_index1,new_index2)
        results.append(new_pair)
    for pair in results:
        letter1 = matrix[pair[0][0]][pair[0][1]]
        letter2 = matrix[pair[1][0]][pair[1][1]]
        cipher+=letter1+letter2
    return cipher

def find_index(matrix, char):
    for i, row in enumerate(matrix):
        if char in row:
            return i, row.index(char)

def hill(text,key=2):
    cipher=""
    if key == 1:
        matrix = np.array([[5, 17],
                        [8, 3],])
        text=text_preprocess(text)
        tuples = []

        i = 0
        while i < len(text):
            if i + 1 < len(text):
                tup = (text[i], text[i+1])
            else :
                tup = (text[i],'x')
            if tup[0] == tup[1]:
                tup = (tup[0], 'x')
                i += 1
            else:
                i += 2
            tuples.append(tup)
        for pair in tuples:
            matrix_pair=np.array([[letter_to_index(pair[0]),letter_to_index(pair[1])]])
            enc=np.dot(matrix_pair,matrix)%26
            for i in enc:
                for j in i:
                    cipher+=(index_to_letter(j))

    if key==2:
        matrix = np.array([[2, 4, 12],
                    [9, 1, 6],
                    [7, 5, 3]])
        text=text_preprocess(text)
        triplets = []

        i = 0
        while i < len(text):
            if i + 2 < len(text):
                triplet = (text[i], text[i + 1], text[i + 2])
            else:
                triplet = (text[i], 'x', 'x')

            if triplet[1] == triplet[2]:
                triplet = (triplet[0], triplet[1] , 'x')
                i += 2 
            else:
                i += 3

            triplets.append(triplet)
        for pair in triplets:
            matrix_pair=np.array([[letter_to_index(pair[0]),letter_to_index(pair[1]),letter_to_index(pair[2])]])
            enc=np.dot(matrix_pair,matrix)%26
            for i in enc:
                for j in i:
                    cipher+=(index_to_letter(j))

    return cipher
def letter_to_index(letter):
    letter = letter.upper()
    return ord(letter) - ord('A')
def index_to_letter(index):
    return chr(index + ord('A') ).lower()
def vigenere(key,text,auto=False):
    cipher=""
    text=text_preprocess(text)
    text=text.upper()
    key=key.upper()
    if not auto:
        for i in range(len(text)):
            index = letter_to_index(text[i])
            k = letter_to_index(key[i % len(key)])
            cipher+=index_to_letter((index+k)%26)
    else:
        key = key+text
        key=key[:len(text)]
        for i in range(len(text)):
            index = letter_to_index(text[i])
            k = letter_to_index(key[i])
            cipher+=index_to_letter((index+k)%26)
    return cipher
def vernam(key,text):
    text = text_preprocess(text)
    text = text.upper()
    key = key.upper()
    cipher = ""
    for i in range(len(text)):
        index = letter_to_index(text[i])
        k = letter_to_index(key[i % len(key)])
        cipher+=index_to_letter((index^k)%26)
    return cipher
# print("ceaser: ",ceaser("Hello world",3))
# print("playfair: ",playfair("archangel","balloon worldt"))
# print("hill: ",hill("balloon world"))
# print("vigenere-repeat: ",vigenere("pie","Hello world"))
# print("vigenere-auto: ",vigenere("aether","Hello world",True))
# print("vernam: ",vernam("SPARTANS","abcdruas"))


# print("hill: ",hill("balloon world",key=1))
