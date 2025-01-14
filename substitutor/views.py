"""Vue"""

import pdb
import traceback

from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponse, Http404
from django.shortcuts import redirect

from .forms import InscriptionForm, ConnexionForm, SearchForm
from .models import Categorie, Store, Product, Account, Favorite, Comment

from .auxilliaries.home import AuxillariesHome
from .auxilliaries.substitute import AuxilliarySubstitute
from .auxilliaries.favorite import AuxilliariesFavorites
from .auxilliaries.installation.installation import Installation


# Create your views here.

def home(request):
    # request ...
    try:
        user_id = request.session["user_id"]
    except (KeyError, AttributeError):
        # print(traceback.format_exc())
        user_id = False
    home_status = request.GET.get("home_status")
    auxilliary_home = AuxillariesHome()
    # print('home_status: ', home_status)
    if home_status == "make_inscription":
        context = auxilliary_home.make_inscription(request, user_id)
    elif home_status == "make_connexion":
        context = auxilliary_home.make_connexion(request, user_id)
    elif home_status == "make_disconnection":
        context = auxilliary_home.make_disconnexion(request)
    elif home_status == "connexion":
        form0 = ConnexionForm()
        form1 = SearchForm()
        context = {"user_id": user_id, "home_status": home_status, "form0": form0, "form1": form1}
    elif home_status == "inscription":
        form0 = InscriptionForm()
        form1 = SearchForm()
        context = {"user_id": user_id, "home_status": home_status, "form0": form0, "form1": form1}
    else:
        #installation0 = Installation(Product, Store, Categorie)
        #installation0.insertions()
        form = SearchForm()
        context = {"user_id": user_id, "home_status": home_status, "form1": form}
    return render(request, "home.html", context)


def substitute(request):
    # request ...
    try:
        user_id = request.session["user_id"]
    except (KeyError, AttributeError):
        user_id = False
    auxilliary_substitute = AuxilliarySubstitute()
    id_substitut = request.GET.get("un_suscribe_substitute_id")
    id_product = request.GET.get("id_product")
    if id_substitut:
        #     Ajout suppression substitut
        if user_id:
            context = auxilliary_substitute.get_context_subscription(
                request, user_id, id_product, id_substitut
            )
            return render(request, "souscription_favorite.html", context)
        else:
            return HttpResponse("not_connected")
    else:
        #     Liste des substituts d'une recherche
        # Récupération de produit
        context = auxilliary_substitute.build_context_substitutes(request, user_id)
        return render(request, "substitute.html", context)


def detail(request, product_id):
    try:
        user_id = request.session["user_id"]
    except (KeyError, AttributeError):
        user_id = False
    product = Product.objects.get(pk=product_id)
    comments = Comment.objects.filter(product__id=product.id, validation_status='t')
    product_stores = product.store.all()
    product_categories = product.categorie.all()
    post_nutriments = product.nutriments
    nutriments = post_nutriments[1:-1].split(", ")
    nutriments_100g = []
    for count in range(len(nutriments)):
        nutriments[count] = nutriments[count].split(":")
        nutriments[count][0] = nutriments[count][0][1:-1]
        if nutriments[count][0][-5:] == "_100g":
            nutriments_100g.append([nutriments[count][0][:-5], [nutriments[count][1]]])
    form = SearchForm()
    context = {
        "user_id": user_id,
        "product": product,
        "stores": product_stores,
        "categories": product_categories,
        "nutriments_100g": nutriments_100g,
        "form": form,
        "comments":comments,
    }
    return render(request, "detail.html", context)

def comments(request):
    # commentaires ...
    try:
        user_id = request.session["user_id"]
    except (KeyError, AttributeError):
        user_id = False
    id_produit = request.GET.get("id_product_comments")
    contenu_text = request.GET.get("comment_text")
    if user_id:
        comment = Comment.objects.create(
                contenu_text=contenu_text,
                commentator=Account.objects.get(pk=request.session["user_id"]),
                product=Product.objects.get(pk=id_produit),
            )
        return HttpResponse( "done" )
    else:
        return HttpResponse("not_connected")



def favoris(request):
    # request ...
    try:
        user_id = request.session["user_id"]
    except (KeyError, AttributeError):
        user_id = False
    auxilliary_favorite = AuxilliariesFavorites()
    # favoris_status = request.GET.get("favorite_status")
    if user_id:
        context = auxilliary_favorite.get_context_favorites(request, user_id)
        return render(request, "favoris.html", context)
    else:
        return redirect("/substitutor/home/")


def account(request):
    # request ...
    try:
        user_id = request.session["user_id"]
    except (KeyError, AttributeError):
        user_id = False
    if user_id:
        form = SearchForm()
        account = Account.objects.get(pk=user_id)
        context = {"user_id": user_id, "account": account, "form": form}
        return render(request, "account.html", context)
    else:
        return redirect("/substitutor/home/")


def redirect_home(request):
    """Redirect vers home"""
    return redirect("/substitutor/home/")



def delete(request):
    """ Delete """

    Product.objects.all().delete()
    Store.objects.all().delete()
    Categorie.objects.all().delete()
    Account.objects.all().delete()
    Favorite.objects.all().delete()
    print('Nombre de produits : ', len(Product.objects.all()))
    print('Nombre de magasins : ', len(Store.objects.all()))
    print('Nombre de categories : ', len(Categorie.objects.all()))
    print('Nombre de comptes : ', len(Account.objects.all()))
    print('Nombre de favoris : ', len(Favorite.objects.all()))

    return HttpResponse('data deleted')


def errorrr_404(request, var):
    """errorrr"""
    raise Http404()
    #raise Exception('Erreur 404')
