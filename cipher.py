# Shit Cipher
 
def encrypt(text, password):
    encrypted = ""
    password_new = ""
    for letter in password:
        password_new += str(ord(letter))
    password = int(password_new)
 
    for letter in text:
        encrypted += str(ord(letter) + password) + " "
    return encrypted
 
def decrypt(text, password):
    decrypted = ""
    password_new = ""
    for letter in password:
        password_new += str(ord(letter))
    password = int(password_new)
   
    text = text.split(" ")
    for number in text:
        decrypted += str(unichr(int(number) - int(password)))
    return decrypted
       
question = raw_input("Would you like to encrypt or decrypt? ")
 
if question == "encrypt":
    data = raw_input("Please enter the data you wish to encrypt: ")
    password = raw_input("Password: ")
    print "Encrypted Data: " + encrypt(data, password)
 
elif question == "decrypt":
    data = raw_input("Please enter the data you wish to decrypt: ")
    password = raw_input("Password: ")
    print "Decrypted Data: " + decrypt(data, password)
 
else:
    print "Unknown option: " + question
 
# check out my blog at https://www.revealed.xyz
