import base64

encryptedpassword = base64.b64encode("password".encode("utf-8"))
print(encryptedpassword)

decryptedpassword = base64.b64decode("cGFzc3dvcmQ=").decode("utf-8")
print(decryptedpassword)
