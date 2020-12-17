"""update launch module."""

import os
import django

from substitutor.models import Categorie, Favorite, Product, Store
from substitutor.auxilliaries.installation import download, validations


os.environ['DJANGO_SETTINGS_MODULE'] = 'pure_beurre_django.settings'

django.setup()



class Update:
    """docstring for update"""

    def __init__(self):
        """Init."""
        
        self.products_to_protect = []
        self.stores_to_protect = []
        self.categories_to_protect = []


        # Downloading API data
        download0 = download.Download()
        download0.get_products_from_api()
        download0.rows_products = [download0.rows_products[0][:700]]

        # Construction and filtering of data to insert in the database
        
        validation0 = validations.Validations()
        validation0.sort_build(download0)

        self.validation = validation0

    def _build_data_to_protect(self):
        """Build data to protect"""
        
        favorites = Favorite.objects.all()
        for favorite in favorites:
            product = favorite.product
            substitut = favorite.substitut
            if product not in self.products_to_protect :
                self.products_to_protect.append(product)
            if substitut not in self.products_to_protect :
                self.products_to_protect.append(substitut)

        for product0 in self.products_to_protect:
            for store in product0.store.all():
                if store not in self.stores_to_protect :
                    self.stores_to_protect.append(store)
            for categorie in product0.categorie.all():
                if categorie not in self.categories_to_protect :
                    self.categories_to_protect.append(categorie)
        print('produits protégés : ', self.products_to_protect)
        print('magasins protégés : ', self.stores_to_protect)
        print('categories protégés : ', self.categories_to_protect)


    def _suppression_protegee(self):
        """Suppression protegée"""

        for store in Store.objects.all():
            if store not in self.stores_to_protect:
                store.delete()

        for categorie in Categorie.objects.all():
            if categorie not in self.categories_to_protect:
                categorie.delete()

        for product in Product.objects.all():
            if product not in self.products_to_protect:
                product.delete()

        print('suppression protégée effectuée')



    def _insertions(self):
        """Insertions"""

        product_to_insert = []
        store_to_insert = []
        categorie_to_insert = []


        # Inserting data into the table
        for product in self.validation.rows_products:

            liste_codes_produits_favoris = []

            product0 = Product.objects.filter(code=product["code"])

            if len(product0) == 0 :
                # Insertions
                product_to_insert.append(
                    Product.objects.create(
                        code=product["code"],
                        name=product["product_name"],
                        quantite=product.get("quantity", ""),
                        marque=product.get("brands", ""),
                        nom_categories=product.get("categories", ""),
                        labels=product.get("labels", ""),
                        ingredients=product.get("ingredients_text", ""),
                        nutriments=product["nutriments"],
                        produits_provoqu_allergies=product["allergens_tags"],
                        traces_eventuelles=product["traces_tags"],
                        nutriscore=product["nutriscore_data"]["grade"],
                        lien_o_ff=product.get("url", ""),
                        url_image=product.get("image_url", ""),
                    )
                )
            elif len(product0) == 1 :
                # mise à jour
                product0 = Product.objects.get(code=product["code"])
                product0.name = product["product_name"]
                product0.quantite = product.get("quantity", "")
                product0.marque = product.get("brands", "")
                product0.nom_categories = product.get("categories", "")
                product0.labels = product.get("labels", "")
                product0.ingredients = product.get("ingredients_text", "")
                product0.nutriments = product["nutriments"]
                product0.produits_provoqu_allergies = product["allergens_tags"]
                product0.traces_eventuelles = product["traces_tags"]
                product0.nutriscore = product["nutriscore_data"]["grade"]
                product0.lien_o_ff = product.get("url", "")
                product0.url_image = product.get("image_url", "")
            else:
                print('Problème : nombre de produit identique dans la base différent de 0 et 1')

            if ((self.validation.rows_products.index(product)) % 100) == 0:
                print(
                    "Insertion des produits : ",
                    self.validation.rows_products.index(product),
                    "/",
                    len(self.validation.rows_products),
                )

        for store in self.validation.rows_stores:
            if len(Store.objects.filter(name=store[0])) == 0 :
                # Insertion
                store_to_insert.append(Store.objects.create(name=store[0]))

                if ((self.validation.rows_stores.index(store)) % 100) == 0:
                    print(
                        "Insertion des magasins : ",
                        self.validation.rows_stores.index(store),
                        "/",
                        len(self.validation.rows_stores),
                    )
        for categorie in self.validation.rows_categories:
            if len( Categorie.objects.filter(name=categorie[0])) == 0  :
                # Insertion
                categorie_to_insert.append(
                    Categorie.objects.create(name=categorie[0])
                )

                if ((self.validation.rows_categories.index(categorie)) % 100) == 0:
                    print(
                        "Insertion des catégories : ",
                        self.validation.rows_categories.index(categorie),
                        "/",
                        len(self.validation.rows_categories),
                    )


        for product_store in self.validation.rows_products_stores:
            product1 = Product.objects.filter(code=int(product_store[0]))
            store0 = Store.objects.filter(name=product_store[1])
            if (len( product1 ) != 0) and (len( store0 ) != 0) :
                product1[0].store.add(store0[0])
            if (
                (self.validation.rows_products_stores.index(product_store)) % 100
            ) == 0:
                print(
                    "Insertion des produits-magasins : ",
                    self.validation.rows_products_stores.index(product_store),
                    "/",
                    len(self.validation.rows_products_stores),
                )

        for product_categorie in self.validation.rows_products_categories:
            product2 = Product.objects.filter(
                code=int(product_categorie[0])
            )
            categorie0 = Categorie.objects.filter(name=product_categorie[1])
            if (len( product2 ) != 0) and (len( categorie0 ) != 0) :
                product2[0].categorie.add(categorie0[0])

            if (
                (self.validation.rows_products_categories.index(product_categorie))
                % 100
            ) == 0:
                print(
                    "Insertion des produits-categories : ",
                    self.validation.rows_products_categories.index(
                        product_categorie
                    ),
                    "/",
                    len(self.validation.rows_products_categories),
                )
        print('Nouvelle insertion effectuée')



    def update(self):
        """Upadate"""
        self._build_data_to_protect()
        self._suppression_protegee()
        self._insertions()
        print("mise à jour terminée")



update0 = Update()
update0.update()
