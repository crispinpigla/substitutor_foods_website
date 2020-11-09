"""This module allows you to manage the download of products."""

import json

import requests


class Download:
    """This class is the class of objects that download products."""

    def __init__(self):
        """Init."""
        self._rows_products = []

    def get_products_from_api(self):
        """This method downloads the data from the API."""
        with open(
            "substitutor/auxilliaries/installation/installation_status.json", "r"
        ) as installation_status:
            dictionnary_status = json.load(installation_status)
        print('----------------------------------------')
        print('Le code avant le if ')
        print('----------------------------------------')


        if dictionnary_status["status_installation"] == "not_installed":
            #dictionnary_status["status_installation"] = "installtion_in_progress"
            print('----------------------------------------')
            print('Le dictionnary status apres le if : ', dictionnary_status["status_installation"])
            print('----------------------------------------')
            with open(
                "substitutor/auxilliaries/installation/installation_status.json", "w"
            ) as file:
                json.dump(dictionnary_status, file)

            for number_page in range(10):
                request_products_api_open_food_facts = requests.get(
                    "https://fr.openfoodfacts.org/cgi/search.pl?action=process"
                    "&sort_by=unique_scans_n&page_size=1000&page= "
                    + str(number_page + 1)
                    + "&json=true&fields=product_name,stores,categories,code,"
                    "nutriscore_data,quantity,brands,labels, "
                    "allergens_tags,traces_tags,url,ingredients_text "
                )
                request_products_api_open_food_facts = json.loads(
                    request_products_api_open_food_facts.text
                )
                self._rows_products.append(
                    request_products_api_open_food_facts["products"]
                )
                print("Téléchargement des produits ", number_page + 1, "/", 10)

            #dictionnary_status["status_installation"] = "installed"
            #dictionnary_status["products"] = self._rows_products
            with open(
                "substitutor/auxilliaries/installation/installation_status.json", "w"
            ) as file:
                json.dump(dictionnary_status, file)

        elif dictionnary_status["status_installation"] == "installed":
            with open(
                "substitutor/auxilliaries/installation/installation_status.json", "r"
            ) as installation_status:
                dictionnary_status = json.load(installation_status)
            self._rows_products = dictionnary_status["products"]
            # print('Taille du row product : ', len(self._rows_products))

        elif dictionnary_status["status_installation"] == "installtion_in_progress":
            pass

    # getters
    @property
    def rows_products(self):
        return self._rows_products

    # setters
    @rows_products.setter
    def rows_products(self, valeur):
        self._rows_products = valeur
