import string
import random


def generate_random_string(length, secure=True, chars=string.ascii_letters + string.digits + string.punctuation):
    if secure:
        choice_func = random.SystemRandom().choice
    else:
        choice_func = random.choice

    return ''.join(choice_func(chars) for _ in range(length))
