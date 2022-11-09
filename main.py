import json
import requests
import random
import threading

register_url = 'http://localhost:3001/register'

def getrandomfromfile(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        return random.choice(lines)


def generate_random_user():
    name = str(getrandomfromfile('firstnames.txt')).strip()
    lastname = str(getrandomfromfile('lastnames.txt')).strip().capitalize()
    email = str(name + lastname.lower() + getrandomfromfile('domains.txt')).strip()
    user = {
        "account_id": str(random.randint(10000000000, 99999999999)),  # 11 digit random number (TCKN in Turkey)
        "password": str(random.randint(10000000, 99999999)),  # 8 digit random number
        "name": name,
        "surname": lastname,
        "email": email
    }
    return user


def create_to_backend():
    user = generate_random_user()
    print("Creating user: " + user['name'] + " " + user['surname'], end=" ")
    r = requests.post(register_url, json=user)
    if r.status_code == 200:
        print(" - OK")
    else:
        print(" - Failed: " + str(r.status_code + " " + r.text))


# thread pooled loop
def thread_loop(num):
    for i in range(num):
        create_to_backend()
        
# main
if __name__ == '__main__':
    for i in range(50):
        t = threading.Thread(target=thread_loop, args=(100,))
        t.start()
