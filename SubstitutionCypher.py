import random
import string


chars = list(string.punctuation + string.digits + string.ascii_letters)

key = chars.copy()

random.shuffle(key)

#ENCRYPT:
plaintext = input("Enter text to encrypt:\n")
encrypted = ''

for letter in plaintext:
    index = chars.index(letter)
    encrypted += key[index]

print("OG text:\n" + plaintext)
print("Encrypted text:\n" + encrypted)