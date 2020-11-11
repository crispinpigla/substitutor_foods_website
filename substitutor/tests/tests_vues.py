"""Test of view's functions"""


from django.http import HttpResponseRedirect

from django.test import TestCase, RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware


from ..models import Categorie, Store, Product, Account, Favorite
from ..auxilliaries.installation import download, validations
from ..views import home, substitute, detail, favoris, account

# Create your tests here.


class TestsModels(TestCase):
    """docstring for TestsSubstitutor"""

    def setUp(self):
        """Setup"""
        self.factory = RequestFactory()

        download0 = download.Download()
        download0.get_products_from_api()

        # resizing
        download0.rows_products = [download0.rows_products[0][:10]]

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
            if ((self.validation.rows_products.index(product)) % 500) == 0:
                print(
                    "Insertion des produits : ",
                    self.validation.rows_products.index(product),
                    "/",
                    len(self.validation.rows_products),
                )

        for store in self.validation.rows_stores:
            store_to_insert.append(Store.objects.create(name=store[0]))
            if ((self.validation.rows_stores.index(store)) % 500) == 0:
                print(
                    "Insertion des magasins : ",
                    self.validation.rows_stores.index(store),
                    "/",
                    len(self.validation.rows_stores),
                )

        for categorie in self.validation.rows_categories:
            categorie_to_insert.append(Categorie.objects.create(name=categorie[0]))
            if ((self.validation.rows_categories.index(categorie)) % 500) == 0:
                print(
                    "Insertion des catégories : ",
                    self.validation.rows_categories.index(categorie),
                    "/",
                    len(self.validation.rows_categories),
                )

        for product_store in self.validation.rows_products_stores:
            product0 = Product.objects.get(code=int(product_store[0]))
            store0 = Store.objects.get(name=product_store[1])
            product0.store.add(store0)
            if ((self.validation.rows_products_stores.index(product_store)) % 500) == 0:
                print(
                    "Insertion des produits-magasins : ",
                    self.validation.rows_products_stores.index(product_store),
                    "/",
                    len(self.validation.rows_products_stores),
                )

        for product_categorie in self.validation.rows_products_categories:
            product0 = Product.objects.get(code=int(product_categorie[0]))
            categorie0 = Categorie.objects.get(name=product_categorie[1])
            product0.categorie.add(categorie0)
            if (
                (self.validation.rows_products_categories.index(product_categorie))
                % 500
            ) == 0:
                print(
                    "Insertion des produits-categories : ",
                    self.validation.rows_products_categories.index(product_categorie),
                    "/",
                    len(self.validation.rows_products_categories),
                )

        user = Account.objects.create(name="a1", adresse_mail="a1@a1.a1", password="a0")

        favorite = Favorite.objects.create(
            product=product_to_insert[0], substitut=product_to_insert[1], user=user
        )

    def tests_vues(self):
        """Test vues"""

        # Teste la vue home
        request = self.factory.post("/substitutor/home/")
        response = home(request)
        self.assertEqual(response.status_code, 200)

        # Teste l'enregistrement d'un substitut si l'utilisateur est connecté
        request = self.factory.get(
            "/substitutor/substitute/",
            {
                "un_suscribe_substitute_id": 2,
                "id_product": 1,
                "search_input": "nutella",
            },
        )
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.session["user_id"] = 1
        response = substitute(request)
        self.assertEqual(response.status_code, 200)

        # Teste la reponse renvoyée si l'utilisateur n'est pas connecté et souhaite enregistrer un favori
        request = self.factory.get(
            "/substitutor/substitute/",
            {"un_suscribe_substitute_id": 2, "id_product": 1},
        )
        response = substitute(request)
        self.assertEqual(response.content, b"not_connected")

        # Teste la page de détail d'un substitut
        request = self.factory.get("/substitutor/")
        response = detail(request, 1)
        self.assertEqual(response.status_code, 200)

        # Teste la restitution des favoris
        request = self.factory.get("/substitutor/favoris/")
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.session["user_id"] = 1
        response = favoris(request)
        self.assertEqual(response.status_code, 200)

        # Teste la redirection de l'utilisateur s'il n'est pas connecté et souhaite acceder aux favoris
        request = self.factory.get("/substitutor/favoris/")
        response = favoris(request)
        self.assertTrue(isinstance(response, HttpResponseRedirect))
        self.assertEqual(response.url, "/substitutor/home")

        # Teste l'accession aux informations du compte
        request = self.factory.get("/substitutor/account/")
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.session["user_id"] = 1
        response = account(request)
        self.assertEqual(response.status_code, 200)
