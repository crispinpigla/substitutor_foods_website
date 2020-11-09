"""Test auxilliaries modules"""

from django.test import TestCase

from ..models import Categorie, Store, Product, Account, Favorite

from ..auxilliaries.installation import download, validations

# Create your tests here.


# 	Auxilliaries home

# 	pass


# 	Si l'inscription réussi verifier qu'un nouvel utilisateur est ajouté dans la base de données

# 	Si l'inscription echoue vérifier qu'aucun nouvel utilisateur a été ajouté à la base de donnée et que
# 	le user_id n'es pas définit


# 	Vérifier le user_id si le compte auquel l'utilisateur veut se connecté existe

# 	Vérifier le user_id si le compte auquel l'utilisateur veut se connecté existe


# 	Vérifier que le user_id vaut False après la déconnexion


# 	Auxilliaries favorite

# 	Vérifier que le résultat est une liste


# 	Auxilliaries substitute


# 	Si aucun résultat n'est trouvé vérifier que le résultat_product_page est une liste

# 	Si au moins un résultat est trouvé vérifier que le reésultat est une liste contenant de(s) liste(s) de deux caractères numérique


class TestAuxilliaries(TestCase):
    """docstring for TestAuxilliaries"""

    def setUp(self):
        """Initialize database test"""
        pass
