from network_sec import *
import os

def file_read(cipher):
    with open(f"./test_files/{cipher}_text.txt") as f:
        plain_text= f.read()
        f.close()

    print(f"Plain text: {plain_text}")
    return plain_text
def file_write(cipher,text):
    with open(f"./cipher_files/{cipher}_cipher.txt", "a+") as f:
        f.write("\n"+text)
        f.close()
def file_delete():
    [open(os.path.join("./cipher_files", file), 'w').close() for file in os.listdir("./cipher_files")]

   
if __name__ == "__main__":
    file_delete() # to clear previous cipher runs

    encryptions= ["Ceaser's","Playfair", "Hill","Vigenere","Vernam"]
    encs_dict={
        1:"ceaser",
        2:"playfair",
        3:"hill",
        4:"vigenere",
        5:"vernam"
    }
    choice = 1
    while(choice!=0):
        for i,enc in enumerate(encryptions):
            print(f"{i+1}) {enc}")
        print("0) Exit")
        choice  = int(input("Pick the desired encryption\n"))
        if(choice == 1):
            print("------------------------------")
            keys=[3,6,12]
            plain_text=file_read("ceaser")
            for key in keys:
                    print(f"Cipher text (Key : {key}): {ceaser(plain_text,key)}")
                    file_write("ceaser",ceaser(plain_text,key))
            print("------------------------------")
        if (choice == 2):
            print("------------------------------")
            keys=["rats", "archangel"]
            plain_text=file_read("playfair")
            for key in keys:
                print(f"Cipher text (Key : {key}): {playfair(key,plain_text)}")
                file_write("playfair",playfair(key,plain_text))

            print("------------------------------")
        if (choice == 3):
            print("------------------------------")
            keys=["[[5,17],[8,3]]", "[[2,4,12],[9,1,6],[7,5,3]]"]
            plain_text=file_read("hill")
            for i,key in enumerate(keys):
                    print(f"Cipher text (Key : {key}): {hill(plain_text,key=i+1)}")
                    file_write("hill",hill(plain_text,key=i+1))

            print("------------------------------")

        if (choice == 4):
            print("------------------------------")
            keys=["pie (repeating mode)", "aether (auto mode)"]
            plain_text=file_read("vigenere")
            print(f"Cipher text (Key : {keys[0]}): {vigenere('pie',plain_text)}")
            file_write("vigenere",vigenere('pie',plain_text))
            print(f"Cipher text (Key : {keys[1]}): {vigenere('aether',plain_text,True)}")
            file_write("vigenere",vigenere('aether',plain_text,True))
            print("------------------------------")
        if (choice == 5):
            print("------------------------------")
            plain_text=file_read("vernam")
            print(f"Cipher text (Key : SPARTANS): {vernam('SPARTANS',plain_text)}")
            file_write("vernam",vigenere("SPARTANS",plain_text))
            print("------------------------------")
