import json,hashlib

try:
    with open("data.json", "x") as f:
        json.dump(
            {"users": [
                {
                    "id": 1,
                    "username": "admin",
                    "password": "4b1b8aa3608a26da451ae0630d75b60ab1bc2dd229c41a80838fc7993e835c46",
                    "full_name": "admin",
                    "role": "admin"
                }
            ]
            }, f)

except FileExistsError:
    pass

f = open("data.json","r+")
y = json.loads(f.read())

username  = input("Please enter the username: ")
password  = input("Please enter the password: ")


for user in y["users"] :
    if user["username"] == username :
        if user["password"] == hashlib.sha256(password.encode()).hexdigest():
            print("Succesful")
            break
        else:
            print("Wrong password")
            break
    else:
        print("User not found")

