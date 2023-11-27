import numpy as np
def text_preprocess(text):
    text=text.replace(" ","")
    text=text.lower()
    return text
def test(text,shift):
    cipher=""
    #97 -> 120
    text=text_preprocess(text)
    for i in text:
        # print(chr((ord(i)-97+shift)%26+97))
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
    text=text_preprocess(text)
    text=text.replace("i",i_j)
    text=text.replace("j",i_j)
    matrix=create_playfair_matrix(key,i_j)
    pairs = [(text[i], text[i + 1] if i + 1 < len(text) and text[i] != text[i + 1] else 'x') for i in range(0, len(text), 2)]
    print(pairs)
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

print(playfair("rats","hello world this is a test sentence j zk"))

