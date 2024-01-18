from django.db import models
import string, random, hashlib


# Create your models here.
def generate_random_string(length):
    letters = string.ascii_uppercase
    return ''.join(random.choice(letters) for i in range(length))


class Message(models.Model):
    message_id = models.CharField(max_length=64, primary_key=True, default=generate_random_string(16))
    message = models.JSONField()
    key_hash = models.CharField(max_length=64)
    number_of_bad_requests = models.IntegerField(default=0)
    is_disposed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
