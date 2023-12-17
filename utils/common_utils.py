import random
import string
import random

def generate_random_password(length=8):
    # Generate a random password of the specified length
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def generate_username(first_name, last_name):
    # Generate a username based on the first name and last name
    username = (first_name.lower() + '.' + last_name.lower()).replace(' ', '') + str(random.randint(0, 1000))
    return username