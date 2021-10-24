from django.db import models

class Audio(models.Model):
    audiofile = models.FileField("Аудиофайл", upload_to="audiofiles")

    def __str__(self):
        return(str(self.audiofile))
    
    
