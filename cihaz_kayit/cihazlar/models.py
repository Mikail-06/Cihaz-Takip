from django.db import models
from django.utils import timezone

class Cihaz(models.Model):
    marka = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    destek_durumu = models.CharField(max_length=50)
    aciklama = models.TextField(blank=True, null=True)
    musteri = models.CharField(max_length=100, blank=True, null=True)
    test_durumu = models.CharField(max_length=50, blank=True, null=True)
    platform = models.CharField(max_length=100, blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    supported_features = models.TextField(blank=True, null=True)
    model_note = models.TextField(blank=True, null=True)
    kaynak_dosya = models.CharField(max_length=100, blank=True, null=True)
    visibility = models.BooleanField(default=True)
    eklenme_tarihi = models.DateField(auto_now_add=True) 
    son_degistirilme = models.DateTimeField(auto_now=True)  
    detay = models.TextField(blank=True, null=True)  

    def __str__(self):
        return f"{self.marka} {self.model}"

    def save(self, *args, **kwargs):
        # Aynı marka/model ve farklı destek durumu olan cihazları bul
        diger_cihazlar = Cihaz.objects.filter(marka=self.marka, model=self.model).exclude(pk=self.pk)
        conflict = None
        for cihaz in diger_cihazlar:
            if cihaz.destek_durumu != self.destek_durumu:
                conflict = cihaz
                break

        if conflict:
            self.detay = f"Bu cihaz ({conflict.id}) numaralı cihaz ile çakışıyor. Lütfen kontrol edin!"
        else:
            self.detay = ""

        super().save(*args, **kwargs)
