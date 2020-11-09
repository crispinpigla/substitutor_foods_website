"""Auxilliary substitute"""

from ..models import Product, Favorite, Account
from ..forms import SearchForm
from django.core.paginator import Paginator


class SubstituteAuxilliary:
    """docstring for SubstituteAuxilliary"""

    def __init__(self):
        """Init"""
        pass

    def _query_to_product(self, request):
        """ query to product """
        # Récupération de produit
        caractere = request.GET.get("search_input")
        products_find = Product.objects.filter(name__icontains=caractere)
        try:
            product_to_treat = [products_find[0]]
        except Exception as e:
            product_to_treat = []
        return product_to_treat

    def _product_to_substitute(self, product_to_treat):
        """product to substitute"""
        # Récupération des substituts
        resultats = []
        for product in product_to_treat:
            for categorie in product.categorie.all():
                for substitute in categorie.product.filter(
                    nutriscore__lt=product.nutriscore
                ):
                    if substitute not in resultats:
                        resultats.append(substitute)
        if len(resultats) == 0:
            for product in product_to_treat:
                for categorie in product.categorie.all():
                    for substitute in categorie.product.filter(
                        nutriscore__lte=product.nutriscore
                    ).exclude(id=product.id):
                        if substitute not in resultats:
                            resultats.append(substitute)
        return resultats

    def _extract_page(self, request, resultats_product):
        """Extract page corresponding"""
        # extraction de la page
        paginator = Paginator(resultats_product, 9)
        page = request.GET.get("page")
        try:
            resultats_product_page = paginator.page(page)
        except Exception as e:
            resultats_product_page = paginator.page(1)
        return resultats_product_page

    def _favorite_resultat_template(self, request, resultats, product_to_treat):
        """ List of favorite and results use in the template """
        resultats_product = []
        for resultat in resultats:
            resultats_product.append([product_to_treat[0], resultat])
        try:
            favorite_user = Favorite.objects.filter(
                user__id=request.session["user_id"], product=product_to_treat[0]
            )
        except Exception as e:
            favorite_user = []
        list_product_favorite = []
        for favorite0 in favorite_user:
            list_product_favorite.append([favorite0.product, favorite0.substitut])
        return [resultats_product, list_product_favorite]

    def build_context_substitutes(self, request, user_id):
        """build context"""
        product_to_treat = self._query_to_product(request)
        caractere = request.GET.get("search_input")
        resultats = self._product_to_substitute(product_to_treat)
        form = SearchForm()
        if len(resultats) == 0:
            context = {
                "user_id": user_id,
                "caractere": caractere,
                "product_to_treat": product_to_treat,
                "resultats_product_page": [],
                "form": form,
            }
        else:
            favorite_resultat_template = self._favorite_resultat_template(
                request, resultats, product_to_treat
            )
            resultats_product = favorite_resultat_template[0]
            list_product_favorite = favorite_resultat_template[1]
            resultats_product_page = self._extract_page(request, resultats_product)
            context = {
                "list_product_favorite": list_product_favorite,
                "user_id": user_id,
                "caractere": caractere,
                "product_to_treat": product_to_treat,
                "resultats_product_page": resultats_product_page,
                "form": form,
            }
        return context

    def get_context_subscription(self, request, user_id, id_product, id_substitut):
        """Subscribe or delete a favorite"""
        favorite = Favorite.objects.filter(
            user__id=user_id, substitut__id=id_substitut, product__id=id_product
        )
        if len(favorite) == 0:
            user = Account.objects.get(pk=request.session["user_id"])
            substitut = Product.objects.get(pk=id_substitut)
            product = Product.objects.get(pk=id_product)
            new_favorite = Favorite.objects.create(
                product=product, user=user, substitut=substitut
            )
            context = {
                "reponse": "added",
                "id_product": id_product,
                "id_substitut": id_substitut,
            }
        else:
            favorite.delete()
            context = {
                "reponse": "deleted",
                "id_product": id_product,
                "id_substitut": id_substitut,
            }
        return context
