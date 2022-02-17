from django.conf import settings
from django.db import models


class Profile(models.Model):
    class Meta:
        verbose_name = "Telegram profil"
        verbose_name_plural = "Telegram profillar"

    tg_id = models.CharField(max_length=16, unique=True, verbose_name="ID")
    tg_username = models.CharField(max_length=255, null=True, blank=True, verbose_name="Telegram nomi (@username)")
    first_name = models.CharField(max_length=255, null=True, blank=True, verbose_name="Ismi")
    last_name = models.CharField(max_length=255, null=True, blank=True, verbose_name="Familiyasi")
    step = models.CharField(max_length=255, default="")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.tg_id or ""


class City(models.Model):
    class Meta:
        verbose_name = "Shahar/Tuman"
        verbose_name_plural = "Shaharlar/Tumanlar"

    title = models.CharField(max_length=255, verbose_name="Shahar/tuman nomi")
    mfys_count = models.IntegerField(default=0, verbose_name="MFYlar soni")

    def __str__(self):
        return self.title or ""


class MFY(models.Model):
    class Meta:
        verbose_name = "Mahalla fuqarolar yig'ini"
        verbose_name_plural = "Mahalla fuqarolar yig'inlari"

    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255, verbose_name="MFY nomi")
    inspector = models.CharField(max_length=255, null=True, blank=True, verbose_name="IIB inspektori FISH")
    inspector_phone = models.CharField(max_length=255, null=True, blank=True, verbose_name="Telefon nomeri")
    rais = models.CharField(max_length=255, null=True, blank=True, verbose_name="MFY raisi FISH")
    rais_phone = models.CharField(max_length=255, null=True, blank=True, verbose_name="Telefon nomeri")
    helper = models.CharField(max_length=255, null=True, blank=True, verbose_name="Xokim yordamchisi FISH")
    helper_phone = models.CharField(max_length=255, null=True, blank=True, verbose_name="Telefon nomeri")
    leader = models.CharField(max_length=255, null=True, blank=True, verbose_name="Yoshlar yetakchisi FISH")
    leader_phone = models.CharField(max_length=255, null=True, blank=True, verbose_name="Telefon nomeri")

    def __str__(self):
        return self.title or ""


class Feedback(models.Model):
    class Meta:
        verbose_name = "Murojaat"
        verbose_name_plural = "Murojaatlar"

    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    text = models.TextField(verbose_name="Murojaat")


class HelperInfographic(models.Model):
    class Meta:
        verbose_name = "Hokim yordamchisi infogrfikasi"
        verbose_name_plural = "Hokim yordamchisi infogrfikalari"
    
    image = models.ImageField(verbose_name="Rasm")

    @property
    def full_url(self):
        return "{}{}".format(settings.BASE_URL, self.image.url)


class LeaderInfographic(models.Model):
    class Meta:
        verbose_name = "Yoshlar yetakchisi infografikasi"
        verbose_name_plural = "Yoshlar yetakchisi infografikalari"
    
    image = models.ImageField(verbose_name="Rasm")

    @property
    def full_url(self):
        return "{}{}".format(settings.BASE_URL, self.image.url)


class TelegramChannel(models.Model):
    class Meta:
        verbose_name = "Obuna telegram kanal"
        verbose_name_plural = "Obuna telegram kanallar"
    
    title = models.CharField(max_length=255, verbose_name="Kanal nomi")
    chat_id = models.CharField(max_length=255, verbose_name="ID")
    url = models.TextField(default="", verbose_name="Havola")

    def __str__(self):
        return self.title or "-"