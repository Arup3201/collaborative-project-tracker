import random

def generate_id(prefix="", size=12):
    charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    random_id = prefix
    for _ in range(size):
        random_id += random.choice(charset)

    return random_id