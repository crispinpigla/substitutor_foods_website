"""This module allows the validation of products and the creation of data to
be inserted into the database. """


class Validations:
    """This class is that of objects that sort products and create data to
    be inserted into the database.. """

    def __init__(self):
        """Init."""
        self.products_stores = []
        self.products_categories = []
        self.rows_products = []
        self.rows_stores = []
        self.rows_categories = []
        self.rows_products_categories = []
        self.rows_products_stores = []

    def sort_build(self, object_download):
        """This method makes it possible to sort the products and create the
        data to be inserted in the database. """
        # Construction of products
        list_products = []
        for list_product in object_download.rows_products:
            for product0 in list_product:
                try:
                    if (
                        (product0["categories"] != "")
                        and (product0["product_name"] != "")
                        and (product0["nutriscore_data"]["grade"] != "")
                    ):
                        list_products.append(product0)
                    else:
                        pass
                except Exception as e:
                    #print(product0['code'])
                    pass
        self.rows_products = list_products

        # Construction of product-stores and products-categories dictionaries
        list_products_store = []
        list_products_categories = []
        for product1 in self.rows_products:
            try:
                list_store = product1["stores"].split(",")
                try:
                    list_categorie = product1["categories"].split(",")
                    # Remove the empty catégories
                    for empty in range(list_categorie.count(" ")):
                        list_categorie.remove(" ")
                    list_products_store.append({product1["code"]: list_store})
                    list_products_categories.append({product1["code"]: list_categorie})
                except KeyError as e:
                    self.rows_products.remove(product1)
            except KeyError as e:
                pass

        self.products_stores = list_products_store
        self.products_categories = list_products_categories

        # Construction of categories to insert
        for dictionnary_product_categories in self.products_categories:
            for product in dictionnary_product_categories:
                for categorie in dictionnary_product_categories[product]:
                    if categorie[0] == " ":
                        categorie = categorie[1:]
                    if tuple([categorie]) not in self.rows_categories:
                        self.rows_categories.append(tuple([categorie]))

        # Construction of stores to insert
        for dictionnary_product_store in self.products_stores:
            for key in dictionnary_product_store:
                for store in dictionnary_product_store[key]:
                    if store != "":
                        if store[0] == " ":
                            store = store[1:]
                    if tuple([store]) not in self.rows_stores:
                        self.rows_stores.append(tuple([store]))

        # Construction of category-product
        for products in self.products_categories:
            for key in products:
                try:
                    for categorie in products[key]:
                        if categorie[0] == " ":
                            categorie = categorie[1:]
                        self.rows_products_categories.append((key, categorie))
                except Exception as e:
                    pass

        # Construction of products-stores
        for products in self.products_stores:
            for key in products:
                for store in products[key]:
                    if store != "":
                        if store[0] == " ":
                            store = store[1:]
                    self.rows_products_stores.append((key, store))
