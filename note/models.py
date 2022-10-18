
from enum import unique
from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User
import uuid

from cryptography.fernet import Fernet
class Note(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    title = models.BinaryField(null=True, blank=True, unique=True)
    content = models.BinaryField(null=True, blank=True, unique=True)
    date_posted = models.DateTimeField(default=timezone.now)
    key = models.BinaryField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE) 


def decrypt_note(notes, user):
    notelist = []
    for note in notes:
        key = bytes(note.key)# convert the memoryview type to bytes
        f = Fernet(key)

        dec_title = f.decrypt(bytes(note.title)).decode()
        dec_content = f.decrypt(bytes(note.content)).decode()
        final_dec_note = {'id':note.id, 'title':dec_title, 'content': dec_content, 'date_posted': note.date_posted, 'user_id': user }
        notelist.append(final_dec_note)
    return notelist

def decrypt_single_note(note, user):
    key = bytes(note.key)# convert the memoryview type to bytes
    f = Fernet(key)
    dec_title = f.decrypt(bytes(note.title)).decode()# convert the memoryview type to bytes and decrypt it and decode the byte to string
    dec_content = f.decrypt(bytes(note.content)).decode()
    final_dec_note = {'id':note.id, 'title':dec_title, 'content': dec_content, 'date_posted': note.date_posted, 'user_id': user }
    return final_dec_note
