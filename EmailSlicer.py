email = input("Enter your email: ")
index = email.index('@')
username = email[0:index]
domain=email[index+1:]
print(f"You username is {username}\nYou domain is {domain}")