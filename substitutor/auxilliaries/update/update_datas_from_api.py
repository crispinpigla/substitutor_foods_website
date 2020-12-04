"""update launch module."""


from . import download, validations


class Update:
    """docstring for update"""

    def __init__(self, product_model, store_model, categorie_model):
        """Init."""
        self.product_model = product_model
        self.store_model = store_model
        self.categorie_model = categorie_model

        # Downloading API data
        download0 = download.Download()
        download0.get_products_from_api()
        download0.rows_products = [download0.rows_products[0][:700]]

        # Construction and filtering of data to insert in the database
        validation0 = validations.Validations()
        validation0.sort_build(download0)

        self.validation = validation0

    def insertions(self):
        """Insertions"""

        product_to_insert = []
        store_to_insert = []
        categorie_to_insert = []


        # Inserting data into the table
        for product in self.validation.rows_products:

            product_to_insert.append(
                self.product_model.objects.create(
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

            if ((self.validation.rows_products.index(product)) % 100) == 0:
                print(
                    "Insertion des produits : ",
                    self.validation.rows_products.index(product),
                    "/",
                    len(self.validation.rows_products),
                )


        for store in self.validation.rows_stores:

            store_to_insert.append(self.store_model.objects.create(name=store[0]))

            if ((self.validation.rows_stores.index(store)) % 100) == 0:
                print(
                    "Insertion des magasins : ",
                    self.validation.rows_stores.index(store),
                    "/",
                    len(self.validation.rows_stores),
                )


        for categorie in self.validation.rows_categories:

            categorie_to_insert.append(
                self.categorie_model.objects.create(name=categorie[0])
            )

            if ((self.validation.rows_categories.index(categorie)) % 100) == 0:
                print(
                    "Insertion des catégories : ",
                    self.validation.rows_categories.index(categorie),
                    "/",
                    len(self.validation.rows_categories),
                )


        for product_store in self.validation.rows_products_stores:
            product0 = self.product_model.objects.get(code=int(product_store[0]))
            store0 = self.store_model.objects.get(name=product_store[1])
            product0.store.add(store0)
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
            product0 = self.product_model.objects.get(
                code=int(product_categorie[0])
            )
            categorie0 = self.categorie_model.objects.get(name=product_categorie[1])
            product0.categorie.add(categorie0)
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

        print("mise à jour terminée")
