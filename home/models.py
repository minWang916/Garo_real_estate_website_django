from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
import PIL.Image

class user(models.Model):
    name = models.CharField(max_length=264, blank= False)
    email = models.EmailField(blank= False) 
    password = models.CharField(max_length=50, blank=False)
    address = models.TextField()
    phone = models.CharField(max_length=264, blank= False)
    description = RichTextUploadingField(blank=True)
    image = models.ImageField(upload_to='', default='default.png', blank = True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = PIL.Image.open(self.image.path)
        width, height = img.size
        left = (width - 300)/2
        top = (height - 300)/2
        right = (width + 300)/2
        bottom = (height + 300)/2

        img = img.crop((left, top, right, bottom))
        img = img.resize((300,300))

        img.save(self.image.path)

class home(models.Model):
    name = models.CharField(max_length=200, blank = True)
    price = models.FloatField(blank = True)
    status = models.CharField(max_length=20, default="For sale")
    area = models.FloatField(blank = True)
    bedrooms = models.IntegerField(blank = True, default = 1)
    bathrooms = models.IntegerField(blank = True, default = 1)
    garage = models.IntegerField(blank = True, default = 1)
    garden = models.IntegerField(blank = True, default = 1)
    description = RichTextUploadingField(blank=True)
    thumbnail = models.ImageField(upload_to='', default='default.png', blank = True)
    owner = models.ForeignKey(user, on_delete=models.PROTECT)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = PIL.Image.open(self.thumbnail.path)
        img = img.resize((304,248))
        img.save(self.thumbnail.path)


class Image(models.Model):
    home = models.ForeignKey(home, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='', default='default.png', blank = True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = PIL.Image.open(self.image.path)
        img = img.resize((850, 570))
        img.save(self.image.path)

