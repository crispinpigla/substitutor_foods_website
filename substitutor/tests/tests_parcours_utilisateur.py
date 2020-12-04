import os, time

from django.test import LiveServerTestCase, RequestFactory

from ..models import Categorie, Store, Product, Account, Favorite

from ..auxilliaries.installation import download, validations
from . import products_data

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from selenium import webdriver

from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.keys import Keys


class TestsParcoursUsers(LiveServerTestCase):
    """docstring for TestsParcoursUsers"""

    def setUp(self):
        """Setup"""
        # binary = FirefoxBinary('./geckodriver-v0.28.0-linux32/geckodriver')
        super().setUpClass()

        #  support of request
        self.factory = RequestFactory()

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
                    id=(self.validation.rows_products.index(product)) + 1,
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

        user = Account.objects.create(name="a1", adresse_mail="a1@a1.a1", password="a1")

        favorite = Favorite.objects.create(
            product=product_to_insert[0], substitut=product_to_insert[1], user=user
        )

        PATH = "substitutor/tests/geckodriver/geckodriver"
        options = webdriver.firefox.options.Options()
        options.add_argument("-headless")
        #self.driver = webdriver.Firefox(executable_path=PATH, firefox_options=options)
        self.driver = FirefoxBinary(executable_path=PATH, firefox_options=options)
        FirefoxBinary
        if os.environ.get("ENV") == "PRODUCTION":
            self.domain = "http://purebeurre0.herokuapp.com"
        else:
            self.domain = self.live_server_url
        self.driver.maximize_window()
        self.driver.get(self.domain)

        self.waiteur = WebDriverWait(self.driver, 30)

    def tearDown(self):
        """Teardown"""
        self.driver.quit()

    def test_recherche(self):
        """Test detail"""

        # Acceuil - recherche
        print("Test du parcour acceuil - recherche")
        search_input = self.driver.find_element_by_name("search_input")
        search_input.send_keys("nutella")
        search_input.submit()
        element = self.waiteur.until(
            EC.presence_of_element_located((By.CLASS_NAME, "conteneur_produit"))
        )
        noms_produits = self.driver.find_elements_by_link_text("Voir plus de detail")
        self.assertTrue(len(noms_produits) > 0)

    def test_detail(self):
        """Test detail"""

        # Acceuil - recherche - detail du produit - acceuil
        print("Test du parcour acceuil - recherche - detail du produit")
        search_input = self.driver.find_element_by_name("search_input")
        search_input.send_keys("nutella")
        search_input.submit()
        element = self.waiteur.until(
            EC.presence_of_element_located((By.CLASS_NAME, "conteneur_produit"))
        )
        noms_produits = self.driver.find_elements_by_link_text("Voir plus de detail")
        first_prod = noms_produits[0]
        first_prod.click()
        contain_detail = self.driver.find_elements_by_class_name("detail_content")
        self.assertEqual(len(contain_detail), 1)

    def test_record_fail(self):
        """Test two"""

        # Acceuil - recherche - tentative d'enregistrement de favori ( hors connexion )
        print(
            "Test du parcour acceuil - recherche - tentative d'enregistrement de favori ( hors connexion )"
        )
        search_input = self.driver.find_element_by_name("search_input")
        search_input.send_keys("nutella")
        search_input.submit()
        element = self.waiteur.until(
            EC.presence_of_element_located((By.CLASS_NAME, "un_suscribe_off"))
        )
        subscription = self.driver.find_elements_by_class_name("un_suscribe_off")
        first_prod = subscription[0]
        first_prod.click()
        element = self.waiteur.until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "contain_header_disconnected")
            )
        )
        self.assertEqual(
            self.driver.current_url,
            self.domain + "/substitutor/home/?home_status=connexion",
        )

    def test_favori_unconnected(self):
        """Test three"""

        # Acceuil - favoris ( hors connexion )
        print("Test du parcour acceuil - favoris ( hors connexion )")
        self.driver.get(self.domain + "/substitutor/favoris/")
        self.assertEqual(self.driver.current_url, self.domain + "/substitutor/home/")

    def test_deconnexion(self):
        """Test three"""

        # Acceuil - connexion - deconnexion
        print("Test du parcour acceuil - connexion - deconnexion")
        self.driver.get(self.domain + "/substitutor/home/?home_status=connexion")
        mail_input = self.driver.find_element_by_name("email")
        password_input = self.driver.find_element_by_name("password")
        mail_input.send_keys("a1@a1.a1")
        password_input.send_keys("a1")
        password_input.submit()
        element = self.waiteur.until(
            EC.presence_of_element_located((By.CLASS_NAME, "disconnected_button"))
        )
        disconnected_button = self.driver.find_element_by_css_selector(
            ".disconnected_button"
        )
        disconnected_button.click()
        self.assertEqual(
            self.driver.current_url,
            self.domain + "/substitutor/home/?home_status=make_disconnection",
        )

    def test_inscription(self):
        """Test three"""

        # Acceuil - Inscription
        print("Test du parcour acceuil - inscription")
        self.driver.get(self.domain + "/substitutor/home/?home_status=inscription")
        users_before_inscription = len(Account.objects.all())
        name_input = self.driver.find_element_by_name("name")
        mail_input = self.driver.find_element_by_name("email")
        password_input = self.driver.find_element_by_name("password")
        name_input.send_keys("a2")
        mail_input.send_keys("a2@a2.a2")
        password_input.send_keys("a2")
        password_input.submit()
        element = self.waiteur.until(
            EC.presence_of_element_located((By.CLASS_NAME, "disconnected_button"))
        )
        self.assertEqual(users_before_inscription + 1, len(Account.objects.all()))

    def test_add_delete_substitut(self):
        """Test three"""

        # Acceuil - connexion - recherche - enregistrement de substitut - suppression de substitut - Acceuil
        print("Test du parcour acceuil - connexion - recherche - enregistrement de substitut - suppression de substitut")
        self.driver.get(self.domain + "/substitutor/home/?home_status=connexion")
        mail_input = self.driver.find_element_by_name("email")
        password_input = self.driver.find_element_by_name("password")
        mail_input.send_keys("a1@a1.a1")
        password_input.send_keys("a1")
        password_input.submit()
        element = self.waiteur.until(
            EC.presence_of_element_located((By.CLASS_NAME, "disconnected_button"))
        )
        search_input = self.driver.find_element_by_name("search_input")
        search_input.send_keys("nutella")
        search_input.submit()
        element = self.waiteur.until(
            EC.presence_of_element_located((By.CLASS_NAME, "un_suscribe_off"))
        )
        favorite_before = len(Favorite.objects.all())
        subscription = self.driver.find_elements_by_class_name("un_suscribe_off")
        first_prod = subscription[0]
        first_prod.click()
        self.assertEqual(favorite_before + 1, len(Favorite.objects.all()))
        subscription = self.driver.find_elements_by_class_name("un_suscribe_off")
        first_prod = subscription[0]
        first_prod.click()
        self.assertEqual(favorite_before, len(Favorite.objects.all()))

    def test_delete_favori(self):
        """Test three"""

        # Acceuil - connexion - favoris - suppression de favori - Acceuil
        print("Test du parcour acceuil - connexion - favoris - suppression de favori")
        self.driver.get(self.domain + "/substitutor/home/?home_status=connexion")
        wait = WebDriverWait(self.driver, 10)
        mail_input = self.driver.find_element_by_name("email")
        password_input = self.driver.find_element_by_name("password")
        mail_input.send_keys("a1@a1.a1")
        password_input.send_keys("a1")
        password_input.submit()
        element = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "contain_header_connected"))
        )
        self.driver.get(self.domain + "/substitutor/favoris/")
        favorite_before = len(Favorite.objects.all())
        element = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "un_suscribe_favorites"))
        )
        delete_favorite_subscription = self.driver.find_elements_by_class_name(
            "un_suscribe_favorites"
        )
        first_prod = delete_favorite_subscription[0]
        first_prod.click()
        self.assertEqual(favorite_before - 1, len(Favorite.objects.all()))

    def test_account(self):
        """Test three"""

        # Acceuil - connexion - compte - Acceuil
        print("Test du parcour acceuil - connexion - compte")
        self.driver.get(self.domain + "/substitutor/home/?home_status=connexion")
        wait = WebDriverWait(self.driver, 10)
        mail_input = self.driver.find_element_by_name("email")
        password_input = self.driver.find_element_by_name("password")
        mail_input.send_keys("a1@a1.a1")
        password_input.send_keys("a1")
        password_input.submit()
        element = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "contain_header_connected"))
        )
        self.driver.get(self.domain + "/substitutor/account/")
        element = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "contain_account"))
        )
        account = self.driver.find_elements_by_class_name("contain_account")
        self.assertEqual(len(account), 1)
