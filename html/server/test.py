import hashlib

m = hashlib.md5()
print(m.update("HELLO".encode('utf-8')))
md5string = m.digest()
print(md5string)