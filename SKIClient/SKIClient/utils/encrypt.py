import random
import string
from cryptography.fernet import Fernet
import hashlib
import requests
import json

VECTOR_SIZE = 256
BLOCK_SIZE = 8
P_KEY = b'CL7I3mtrZXlCKod6KL77k_UU5wMNjDt1qB69380GFoo='
TOKEN = "a31c2ff90debf04cead036391d5e2cec4a957230"


# pt = """
# Creating
# """


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


def get_random_location(text):
    locs = random.sample(
        range(int(len(text) * .05), len(text) - int(len(text) * .05)), 32)
    locs.sort()
    return locs


class Encryptor:
    @staticmethod
    def generate_random_string(length):
        """
        Generate a random string of fixed length
        """
        letters = list(string.ascii_lowercase) + list(string.ascii_uppercase) + list(string.digits) + ['-', '_']
        return ''.join(random.choice(letters) for i in range(length))

    @staticmethod
    def generate_random_string_set(size):
        data = []
        for i in range(size):
            data.append(Encryptor.generate_random_string(10))
        return data

    @staticmethod
    def stuff_random_characters(data, random_string_set, locs):
        text = data
        for i, loc in enumerate(locs):
            l = loc + (i * 10)
            print(loc, l)
            left, right = text[:l], text[l:]
            text = left + random_string_set[i] + right
            print(len(text))
        return text

    @staticmethod
    def generate_key(data):
        c_data = ''.join(data)
        hash_val: str = Helper.calculate_hash(c_data)
        hash_val = hash_val + hash_val[::-1]
        key = hash_val[:43] + '='
        return key.encode('utf-8')

    @staticmethod
    def calculate_vector(locs, blocks, private_key):
        vector = ''
        for i in range(blocks):
            l = str(locs[i])
            vector += l.zfill(BLOCK_SIZE)
        h = Helper(private_key)
        return h.encrypt(vector.encode('utf-8')).decode('utf-8')

    def encrypt(self, data, private_key):
        vector = '_' * VECTOR_SIZE
        blocks = VECTOR_SIZE // BLOCK_SIZE
        # select 32 unique random location from the plaintext
        random_string_set = self.generate_random_string_set(blocks)
        data_key = self.generate_key(random_string_set)
        helper = Helper(data_key)
        enc_data = helper.encrypt(data.encode('utf-8')).decode('utf-8')
        locs = get_random_location(enc_data)
        stuffed_enc_data = self.stuff_random_characters(
            enc_data, random_string_set, locs).encode('utf-8')
        vector = self.calculate_vector(locs, blocks, private_key)
        return {
            "data": stuffed_enc_data.decode('utf-8'),
            "vector": vector
        }


def encrypt(data, private_key):
    encryptor = Encryptor()
    return encryptor.encrypt(data, private_key)

# response = requests.post('http://127.0.0.1:8000/api/message/', data=json.dumps({
#     "message": message,
#     "hash": Helper.calculate_hash(PRIVATE_KEY.decode('utf-8'))
# }), headers={
#     "Authorization": f"Token {TOKEN}",
#     "Content-Type": "application/json"
# })

# print(response.json())
