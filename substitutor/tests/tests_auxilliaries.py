"""Test auxilliaries modules"""

from django.test import TestCase, RequestFactory, Client

from ..models import Categorie, Store, Product, Account, Favorite

from django.contrib.sessions.middleware import SessionMiddleware

from ..auxilliaries.home import AuxillariesHome
from ..auxilliaries.favorite import AuxilliariesFavorites
from ..auxilliaries.substitute import AuxilliarySubstitute

from ..auxilliaries.installation import download, validations



class TestAuxilliaries(TestCase):
    """docstring for TestAuxilliaries"""

    def setUp(self):
        """Initialize database test"""

        #  support of request
        self.factory = RequestFactory()

        # print('nombre d\'utilisateur avant l\'insertion : ', self.user_before)
        # self.client = Client()

        download0 = download.Download()
        download0.get_products_from_api()

        # resizing
        download0.rows_products = [download0.rows_products[0][:500]]

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

    def test_auxilliaries(self):
        """docstring for test auxilliaries"""

        #  Teste la reussite de l'inscription d'un nouvel utilisateur
        request = self.factory.post(
            "/substitutor/home/",
            {
                "name": "user_name",
                "email": "user_mail@mail.com",
                "password": "user_password",
            },
        )
        # c = self.client.post('/substitutor/home/')
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        user_before = len(Account.objects.all())
        auxilliary_home = AuxillariesHome()
        auxilliary_home.make_inscription(request, None)
        self.assertEqual(len(Account.objects.all()), user_before + 1)

        #  Teste l'echec de l'inscription d'un nouvel utilisateur
        self.user_before = len(Account.objects.all())
        request = self.factory.post(
            "/substitutor/home/",
            {"name": "user_name", "email": "user_mail", "password": "user_password"},
        )
        auxilliary_home = AuxillariesHome()
        auxilliary_home.make_inscription(request, None)
        self.assertEqual(len(Account.objects.all()), self.user_before)

        #  Teste la reussite de la connexion d'un nouvel utilisateur
        request = self.factory.post(
            "/substitutor/home/",
            {"email": "user_mail@mail.com", "password": "user_password"},
        )
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        auxilliary_home = AuxillariesHome()
        context_connexion = auxilliary_home.make_connexion(request, None)
        self.assertTrue(isinstance(request.session["user_id"], int))

        #  Teste l'echec de la connexion d'un nouvel utilisateur
        request = self.factory.post(
            "/substitutor/home/",
            {"email": "another_user_mail@mail.com", "password": "user_password"},
        )
        auxilliary_home = AuxillariesHome()
        context_connexion = auxilliary_home.make_connexion(request, None)
        self.assertEqual(context_connexion["user_id"], None)

        #  Teste la deconnexion d'un utilisateur
        request = self.factory.post(
            "/substitutor/home/",
            {"email": "user_mail@mail.com", "password": "user_password"},
        )
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        auxilliary_home = AuxillariesHome()
        context_connexion = auxilliary_home.make_connexion(request, None)
        context_connexion = auxilliary_home.make_disconnexion(request)
        self.assertEqual(context_connexion["user_id"], None)

        #  Teste la recherche d'un substitut lorsques des résultats sont renvoyés
        request = self.factory.get(
            "/substitutor/substitute/", {"search_input": "nutella"}
        )
        substitute_auxilliary = AuxilliarySubstitute()
        context_find_substitute = substitute_auxilliary.build_context_substitutes(
            request, 1
        )
        counter_substitute = 0
        for prod in context_find_substitute["resultats_product_page"]:
            # print('prod : ', prod[1].name)
            counter_substitute += 1
        self.assertTrue(counter_substitute > 0)

        #  Teste la recherche d'un substitut lorsques des résultats ne sont pas renvoyés
        request = self.factory.get("/substitutor/substitute/", {"search_input": "aaa"})
        substitute_auxilliary = AuxilliarySubstitute()
        context_find_substitute = substitute_auxilliary.build_context_substitutes(
            request, 1
        )
        counter_substitute = 0
        for prod in context_find_substitute["resultats_product_page"]:
            # print('prod : ', prod[1].name)
            counter_substitute += 1
        self.assertTrue(counter_substitute == 0)

        #  Teste l'ajout d'un favori
        request = self.factory.get("/substitutor/substitute/")
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.session["user_id"] = 1
        substitute_before = len(Favorite.objects.all())
        substitute_auxilliary = AuxilliarySubstitute()
        context_add_substitute = substitute_auxilliary.get_context_subscription(
            request, 1, 3, 4
        )
        self.assertEqual(len(Favorite.objects.all()), substitute_before + 1)

        #  Teste la suppression d'un favori
        request = self.factory.get("/substitutor/substitute/")
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.session["user_id"] = 1
        substitute_auxilliary = AuxilliarySubstitute()
        substitute_before = len(Favorite.objects.all())
        context_add_substitute = substitute_auxilliary.get_context_subscription(
            request, 1, 3, 4
        )
        self.assertEqual(len(Favorite.objects.all()), substitute_before - 1)

        #  Teste la consultation de favoris
        request = self.factory.get("/substitutor/favorite/")
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.session["user_id"] = 1
        auxilliary_favorite = AuxilliariesFavorites()
        context_get_favorite = auxilliary_favorite.get_context_favorites(
            request, request.session["user_id"]
        )
        check_favorite = True
        for result in context_get_favorite["resultats"]:
            if isinstance(result[1], Favorite):
                check_favorite = False
        self.assertTrue(check_favorite)
