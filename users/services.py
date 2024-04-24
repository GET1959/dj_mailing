import random


def generate_password(length):
    characters = list('abcdefghijklmnopqrstuvwxyz')
    characters.extend(list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))
    characters.extend(list('0123456789'))
    characters.extend(list('!@#$%^&()?><:;'))
    pass_word = ''
    for x in range(length):
        pass_word += random.choice(characters)
    return pass_word
