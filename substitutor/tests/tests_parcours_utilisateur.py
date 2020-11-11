
import os, time

from django.test import LiveServerTestCase

from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.keys import Keys




class TestsParcoursUsers(LiveServerTestCase):
	"""docstring for TestsParcoursUsers"""
	

	def setUp(self):
		"""Setup"""
		#binary = FirefoxBinary('./geckodriver-v0.28.0-linux32/geckodriver')
		PATH='substitutor/tests/geckodriver/geckodriver'
		self.driver = webdriver.Firefox(executable_path=PATH)
		self.driver.maximize_window()
		if os.environ.get("ENV") == "PRODUCTION":
		    self.domain = "http://purebeurre0.herokuapp.com"
		else:
		    self.domain = "localhost:8000"
		self.driver.get(self.domain + '/substitutor/home/')
		

	def tearDown(self):
		"""Teardown"""
		pass
		

	def test_a(self):
		"""Test one"""
		
		# Acceuil - recherche - detail du produit
		search_input = self.driver.find_element_by_name('search_input')
		time.sleep(2)
		search_input.send_keys("nutella")
		time.sleep(5)
		search_input.submit()
		time.sleep(5)
		noms_produits = self.driver.find_elements_by_link_text('Voir plus de detail')
		first_prod = noms_produits[0]
		first_prod.click()
		time.sleep(5)
		self.driver.quit()


	def test_b(self):
		"""Test two"""

		# Acceuil - recherche - tentative d'enregistrement de favori ( hors connexion )
		search_input = self.driver.find_element_by_name('search_input')
		time.sleep(2)
		search_input.send_keys("nutella")
		time.sleep(5)
		search_input.submit()
		time.sleep(5)
		subscription = self.driver.find_elements_by_class_name('un_suscribe_off')
		first_prod = subscription[0]
		first_prod.click()
		time.sleep(5)
		self.driver.quit()


	def test_c(self):
		"""Test three"""

		# Acceuil - favoris ( sans connexion )
		time.sleep(2)
		self.driver.get(self.domain + '/substitutor/favoris/')
		time.sleep(5)
		self.driver.quit()


	def test_d(self):
		"""Test three"""
		
		# Acceuil - connexion - deconnexion
		time.sleep(2)
		self.driver.get(self.domain + '/substitutor/home/?home_status=connexion')
		time.sleep(2)
		mail_input = self.driver.find_element_by_name('email')
		password_input = self.driver.find_element_by_name('password')
		mail_input.send_keys("aa0@aa0.aa0")
		time.sleep(2)
		password_input.send_keys("crispin")
		time.sleep(2)
		password_input.submit()
		time.sleep(2)
		disconnected_button = self.driver.find_element_by_css_selector('.disconnected_button')
		disconnected_button.click()
		time.sleep(5)
		self.driver.quit()
		

	def test_e(self):
		"""Test three"""
		
		# Acceuil - Inscription
		time.sleep(2)
		self.driver.get(self.domain + '/substitutor/home/?home_status=inscription')
		time.sleep(2)
		name_input = self.driver.find_element_by_name('name')
		mail_input = self.driver.find_element_by_name('email')
		password_input = self.driver.find_element_by_name('password')
		name_input.send_keys("aa3")
		time.sleep(2)
		mail_input.send_keys("aa3@aa3.aa3")
		time.sleep(2)
		password_input.send_keys("crispin")
		time.sleep(2)
		password_input.submit()
		time.sleep(2)
		self.driver.quit()


	def test_f(self):
		"""Test three"""
		
		# Acceuil - connexion - recherche - enregistrement de favori - suppression de favori - Acceuil
		time.sleep(2)
		self.driver.get(self.domain + '/substitutor/home/?home_status=connexion')
		time.sleep(2)
		mail_input = self.driver.find_element_by_name('email')
		password_input = self.driver.find_element_by_name('password')
		mail_input.send_keys("aa0@aa0.aa0")
		time.sleep(2)
		password_input.send_keys("crispin")
		time.sleep(2)
		password_input.submit()
		time.sleep(2)
		search_input = self.driver.find_element_by_name('search_input')
		time.sleep(2)
		search_input.send_keys("nutella")
		time.sleep(2)
		search_input.submit()
		time.sleep(5)
		subscription = self.driver.find_elements_by_class_name('un_suscribe_off')
		first_prod = subscription[0]
		first_prod.click()
		time.sleep(5)
		subscription = self.driver.find_elements_by_class_name('un_suscribe_off')
		first_prod = subscription[0]
		first_prod.click()
		time.sleep(2)
		self.driver.get(self.domain + '/substitutor/home/')
		time.sleep(2)
		self.driver.quit()

	def test_g(self):
		"""Test three"""
		
		# Acceuil - connexion - favoris - suppression de favori - Acceuil
		time.sleep(2)
		self.driver.get(self.domain + '/substitutor/home/?home_status=connexion')
		time.sleep(2)
		mail_input = self.driver.find_element_by_name('email')
		password_input = self.driver.find_element_by_name('password')
		mail_input.send_keys("aa0@aa0.aa0")
		time.sleep(2)
		password_input.send_keys("crispin")
		time.sleep(2)
		password_input.submit()
		time.sleep(2)
		self.driver.get(self.domain + '/substitutor/favoris/')
		time.sleep(5)
		delete_favorite_subscription = self.driver.find_elements_by_class_name('un_suscribe_favorites')
		first_prod = delete_favorite_subscription[0]
		first_prod.click()
		time.sleep(5)
		self.driver.get(self.domain + '/substitutor/home/')
		time.sleep(2)
		self.driver.quit()



	def test_h(self):
		"""Test three"""
		
		# Acceuil - connexion - compte - Acceuil 
		time.sleep(2)
		self.driver.get(self.domain + '/substitutor/home/?home_status=connexion')
		time.sleep(2)
		mail_input = self.driver.find_element_by_name('email')
		password_input = self.driver.find_element_by_name('password')
		mail_input.send_keys("aa0@aa0.aa0")
		time.sleep(2)
		password_input.send_keys("crispin")
		time.sleep(2)
		password_input.submit()
		time.sleep(2)
		self.driver.get(self.domain + '/substitutor/account/')
		time.sleep(8)
		self.driver.get(self.domain + '/substitutor/home/')
		time.sleep(2)
		self.driver.quit()