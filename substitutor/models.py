from django.db import models

# Create your models here.


class Categorie(models.Model):
    name = models.CharField(max_length=255)


class Store(models.Model):
    name = models.CharField(max_length=255)


class Product(models.Model):

    code = models.BigIntegerField(null=True)
    name = models.CharField(max_length=255)
    quantite = models.CharField(max_length=255)
    marque = models.TextField()
    nom_categories = models.TextField()
    nom_stores = models.TextField(null=True)
    labels = models.TextField()
    ingredients = models.TextField()
    nutriments = models.TextField(null=True)
    produits_provoqu_allergies = models.TextField()
    traces_eventuelles = models.TextField()
    nutriscore = models.CharField(max_length=255)
    lien_o_ff = models.TextField()
    url_image = models.TextField(blank=True)
    store = models.ManyToManyField(Store, related_name="product", blank=True)
    categorie = models.ManyToManyField(Categorie, related_name="product", blank=True)


class Account(models.Model):
    name = models.CharField(max_length=255)
    adresse_mail = models.EmailField(max_length=200)
    password = models.CharField(max_length=255)


class Favorite(models.Model):

    date_engistrement = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(
        Product, related_name="product", on_delete=models.CASCADE, null=True
    )
    substitut = models.ForeignKey(
        Product, related_name="substitut", on_delete=models.CASCADE
    )
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
