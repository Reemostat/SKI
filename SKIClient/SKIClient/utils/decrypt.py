import random, string
from cryptography.fernet import Fernet
import hashlib, json

VECTOR_SIZE = 256
BLOCK_SIZE = 8


class Helper:
    def __init__(self, key):
        self.__key = key
        self.__cipher_suite = Fernet(self.__key)

    def encrypt(self, data):
        return self.__cipher_suite.encrypt(data)

    def decrypt(self, data):
        return self.__cipher_suite.decrypt(data)

    @staticmethod
    def calculate_hash(data):
        md5_hash = hashlib.md5()
        md5_hash.update(data.encode('utf-8'))
        return md5_hash.hexdigest()


def decrypt(data, private_key):
    helper = Helper(private_key)
    vector = helper.decrypt(data['vector'].encode()).decode()

    # divide the vector into blocks of 8 bytes
    locations = [int(vector[i:i + BLOCK_SIZE]) for i in range(0, len(vector), BLOCK_SIZE)]

    # from data['data'], extract 10 bytes of data from each location in locations
    # and store it in a list
    text = data['data']
    extracted = []

    for i, location in enumerate(locations):
        l = location
        extracted.append(text[l:l + 10])
        # remove the extracted data from the text
        text = text[:l] + text[l + 10:]

    hash_val = helper.calculate_hash(''.join(extracted))
    hash_val = hash_val + hash_val[::-1]
    key = hash_val[:43] + '='
    key = key.encode()

    helper = Helper(key)
    return helper.decrypt(text.encode()).decode()
