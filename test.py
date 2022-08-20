s = input(int("enter a number"))
print(s)
'''from cryptography.fernet import Fernet

key = Fernet.generate_key()
f = Fernet(key)
test = "123456"
test1 = test.encode()
test1 = f.encrypt(test1)
#test1 = test1.decode()
print(test1)
#test1 = test1.encode()
test1 = f.decrypt(test1)
test1 = test1.decode()
print(test1)

test2 = test.encode()
test2 = f.encrypt(test2)
#test2 = test2.decode()
print(test2)
#test2 = test1.encode()
test2 = f.decrypt(test2)
test2 = test2.decode()
print(test2)'''