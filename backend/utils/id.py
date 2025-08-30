import random

def generate_id(prefix=""):
    charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    random_id = prefix
    for _ in range(12):
        random_id += random.choice(charset)

    return random_id