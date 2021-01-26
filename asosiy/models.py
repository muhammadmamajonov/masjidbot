from django.db import models

# Create your models here.

class HaftaKunlari(models.Model):
    nomi = models.CharField(max_length=50)

    def __str__(self):
        return self.nomi

class NamozVaqti(models.Model):
    sana = models.DateField()
    hafta_kuni = models.ForeignKey(HaftaKunlari, on_delete = models.CASCADE)
    tong = models.CharField(max_length=10)
    quyosh = models.CharField(max_length=10)
    peshin = models.CharField(max_length=10)
    asr = models.CharField(max_length=10)
    shom = models.CharField(max_length=10)
    xufton = models.CharField(max_length=10)
    
    def __str__(self):
        return self.hafta_kuni.nomi + ' | ' + str(self.sana)


class Maruzalar(models.Model):
    maruza_nomi = models.CharField(max_length=50)
    muallif = models.CharField(max_length=50)
    maruza_audio = models.FileField(upload_to='audio-maruzalar')

    def __str__(self):
        return self.maruza_nomi


class Mavzu(models.Model):
    mavzu = models.CharField(max_length=50)

    def __str__(self):
        return self.mavzu

class Dars(models.Model):
    dars_nomi = models.CharField(max_length=50)
    muallif = models.CharField(max_length=30)
    audio = models.FileField(upload_to='audio-darsliklar')
    qaysi_mavzu = models.ForeignKey(Mavzu, on_delete=models.CASCADE)

    def __str__(self):
        return self.dars_nomi + ' | ' + self.muallif
