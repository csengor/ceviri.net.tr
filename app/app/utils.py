import random
import string

def generate_secret():
    return ''.join(random.choices(string.ascii_uppercase, k=8))
