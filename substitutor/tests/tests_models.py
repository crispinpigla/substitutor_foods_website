from django.test import TestCase

from ..models import Categorie, Store, Product, Account, Favorite

from ..auxilliaries.installation import download, validations
from . import products_data
# Create your tests here.


class TestsModels(TestCase):
    """docstring for TestsSubstitutor"""

    def setUp(self):
        """Initilize database test"""
        download0 = download.Download()
        download0.rows_products = products_data.PRODUCTS

        # Construction and filtering of data to insert in the database
        validation0 = validations.Validations()
        validation0.sort_build(download0)
        self.validation = validation0

        product_to_insert = []
        store_to_insert = []
        categorie_to_insert = []
        for product in self.validation.rows_products:
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

        for store in self.validation.rows_stores:
            store_to_insert.append(Store.objects.create(name=store[0]))

        for categorie in self.validation.rows_categories:
            categorie_to_insert.append(Categorie.objects.create(name=categorie[0]))

        for product_store in self.validation.rows_products_stores:
            product0 = Product.objects.get(code=int(product_store[0]))
            store0 = Store.objects.get(name=product_store[1])
            product0.store.add(store0)

        for product_categorie in self.validation.rows_products_categories:
            product0 = Product.objects.get(code=int(product_categorie[0]))
            categorie0 = Categorie.objects.get(name=product_categorie[1])
            product0.categorie.add(categorie0)

        user = Account.objects.create(name="a1", adresse_mail="a1@a1.a1", password="a0")

        favorite = Favorite.objects.create(
            product=product_to_insert[0], substitut=product_to_insert[1], user=user
        )

    def test_models_categorie(self):
        """Test models modele categorie"""

        # Test that objects receive to the database are Categorie's objects
        print('\nTest du model categorie')
        result_categorie = True
        categories = Categorie.objects.all()
        for categorie in categories:
            if not isinstance(categorie, Categorie):
                result_categorie = False
        self.assertTrue(result_categorie)

    def test_models_store(self):
        """Test modele store"""

        # Test that objects receive to the database are Store's objects
        print('\nTest du model store')
        result_store = True
        stores = Store.objects.all()
        for store in stores:
            if not isinstance(store, Store):
                result_store = False
        self.assertTrue(result_store)

    def test_models_produit(self):
        """Test modele produit"""

        # Test that objects receive to the database are Product's objects
        print('\nTest du model produit')
        result_product = True
        products = Product.objects.all()
        for product in products:
            if not isinstance(product, Product):
                result_product = False
        self.assertTrue(result_product)

    def test_models_account(self):
        """Test modele account"""

        # Test that objects receive to the database are Account's objects
        print('\nTest du model account')
        result_account = True
        accounts = Account.objects.all()
        for account in accounts:
            if not isinstance(account, Account):
                result_account = False
        self.assertTrue(result_account)

    def test_models_favorite(self):
        """Test modele favorite"""

        # Test that objects receive to the database are Favorite's objects
        print('\nTest du model favorite')
        result_favorite = True
        favorites = Favorite.objects.all()
        for favorite in favorites:
            if not isinstance(favorite, Favorite):
                result_favorite = False
        self.assertTrue(result_favorite)
