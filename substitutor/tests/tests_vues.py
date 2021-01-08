"""Test of view's functions"""


from django.http import HttpResponseRedirect

from django.test import TestCase, RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware


from ..models import Categorie, Store, Product, Account, Favorite, Comment
from ..auxilliaries.installation import download, validations
from ..views import home, substitute, detail, favoris, account, comments
from . import products_data
# Create your tests here.


class TestsModels(TestCase):
    """docstring for TestsSubstitutor"""

    def setUp(self):
        """Setup"""
        self.factory = RequestFactory()

        download0 = download.Download()
        download0.rows_products = products_data.PRODUCTS

        # Construction and filtering of data to insert in the database
        validation0 = validations.Validations()
        validation0.sort_build(download0)
        self.validation = validation0

        self.product_to_insert = []
        self.store_to_insert = []
        self.categorie_to_insert = []
        for product in self.validation.rows_products:
            self.product_to_insert.append(
                Product.objects.create(
                    code=product["code"],
                    name=product["product_name"],
                    quantite=product.get("quantity", ""),
                    marque=product.get("brands", ""),
                    nom_categories=product.get("categories", ""),
                    nom_stores=product.get("store", ""),
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
                    "\nInsertion des produits : ",
                    self.validation.rows_products.index(product),
                    "/",
                    len(self.validation.rows_products),
                )

        for store in self.validation.rows_stores:
            self.store_to_insert.append(Store.objects.create(name=store[0]))
            if ((self.validation.rows_stores.index(store)) % 500) == 0:
                print(
                    "Insertion des magasins : ",
                    self.validation.rows_stores.index(store),
                    "/",
                    len(self.validation.rows_stores),
                )

        for categorie in self.validation.rows_categories:
            self.categorie_to_insert.append(Categorie.objects.create(name=categorie[0]))
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

        self.user = Account.objects.create(name="a1", adresse_mail="a1@a1.a1", password="a0")

        self.favorite = Favorite.objects.create(
            product=self.product_to_insert[0], substitut=self.product_to_insert[1], user=self.user
        )

    def tests_vues_home(self):
        """Test vues"""

        # Teste la vue home
        print('Test de la vue home')
        request = self.factory.post("/substitutor/home/")
        response = home(request)
        self.assertEqual(response.status_code, 200)

    def tests_vues_record_connected(self):
        """"""

        # Teste l'enregistrement d'un substitut si l'utilisateur est connecté
        print('Test de la vue substitute : enregistrement d\'un substitut si l\'utilisateur est connecté')
        request = self.factory.get(
            "/substitutor/substitute/",
            {
                "un_suscribe_substitute_id": self.product_to_insert[1].id,
                "id_product": self.product_to_insert[0].id,
                "search_input": "nutella",
            },
        )
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.session["user_id"] = self.user.id
        response = substitute(request)
        self.assertEqual(response.status_code, 200)

    def tests_vues_record_unconnected(self):
        """"""

        # Teste la reponse renvoyée si l'utilisateur n'est pas connecté et souhaite enregistrer un favori
        print('Test de la vue substitute: enregistrement d\'un substitut si l\'utilisateur n\'est pas connecté')
        request = self.factory.get(
            "/substitutor/substitute/",
            {"un_suscribe_substitute_id": 2, "id_product": 1},
        )
        response = substitute(request)
        self.assertEqual(response.content, b"not_connected")

    def tests_vues_detail_substitut(self):
        """"""

        print('Test de la vue detail')
        # Teste la page de détail d'un substitut
        request = self.factory.get("/substitutor/")
        response = detail(request, self.product_to_insert[0].id)
        self.assertEqual(response.status_code, 200)

    def tests_vues_comments_ajout_commentaire(self):
        """"""

        # Teste l'ajout dun commentaire lorsque l'utilisateur est connecté
        print('Test de l\'ajout dun commentaire lorsque l\'utilisateur est connecté')
        request = self.factory.get("/substitutor/", {"id_product_comments": self.product_to_insert[0].id, "comment_text": "ceci est un commentaire"})
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.session["user_id"] = self.user.id
        len_comments_before = len( Comment.objects.all() )
        response = comments(request)
        len_comments_after = len( Comment.objects.all() )
        self.assertEqual(len_comments_before + 1, len_comments_after)
        #self.assertEqual(response.content, b"done")

    def tests_vues_comments_redirection_ajout_commentaire(self):
        """"""
        # Teste la redirection après une tentative d'ajout de commentaire lorsque l'utilisateur n'est pas connecté
        print('Test de la redirection après une tentative d\'ajout de commentaire lorsque l\'utilisateur n\'est pas connecté')
        request = self.factory.get("/substitutor/")
        response = comments(request)
        self.assertEqual(response.content, b"not_connected")

    def tests_vues_get_favorites(self):
        """"""

        # Teste la restitution des favoris
        print('Test de la vue favorite : Si l\'utilisateur est connecté ')
        request = self.factory.get("/substitutor/favoris/")
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.session["user_id"] = self.user.id
        response = favoris(request)
        self.assertEqual(response.status_code, 200)

    def tests_vues_redirection(self):
        """"""

        # Teste la redirection de l'utilisateur s'il n'est pas connecté et souhaite acceder aux favoris
        print('Test de la vue favorite : Si l\'utilisateur n\'est pas connecté ')
        request = self.factory.get("/substitutor/favoris/")
        response = favoris(request)
        self.assertTrue(isinstance(response, HttpResponseRedirect))
        self.assertEqual(response.url, "/substitutor/home")

    def tests_vues_account(self):
        """"""

        # Teste l'accession aux informations du compte
        print('Test de la vue account')
        request = self.factory.get("/substitutor/account/")
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.session["user_id"] = self.user.id
        response = account(request)
        self.assertEqual(response.status_code, 200)
