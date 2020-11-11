"""Auxillaries home"""
from ..forms import InscriptionForm, SearchForm, ConnexionForm
from ..models import Account


class AuxillariesHome:
    """docstring for AuxillariesHome"""

    def __init__(self):
        """"""
        pass

    def register_account(self, account, request):
        """Register account"""
        if len(account) == 0:
            form = SearchForm()
            user = Account.objects.create(
                name=request.POST.get("name"),
                adresse_mail=request.POST.get("email"),
                password=request.POST.get("password"),
            )
            request.session["user_id"] = user.id
            user_id = request.session["user_id"]
            context = {"user_id": user_id, "home_status": None, "form": form}
        else:
            home_status = "inscription"
            form = InscriptionForm()
            message_to_user = "Un compte possédant cet e-mail existe déja"
            context = {
                "user_id": None,
                "home_status": home_status,
                "form": form,
                "message_to_user": message_to_user,
            }
        return context

    def make_inscription(self, request, user_id):
        """Make inscription"""
        if user_id:
            form = SearchForm()
            context = {"user_id": user_id, "home_status": None, "form": form}
        else:
            post_form = InscriptionForm(request.POST)
            if post_form.is_valid():
                account = Account.objects.filter(adresse_mail=request.POST.get("email"))
                context = self.register_account(account, request)
            else:
                home_status = "inscription"
                form = InscriptionForm()
                context = {
                    "user_id": user_id,
                    "home_status": home_status,
                    "form": form,
                    "message_to_user": "",
                }
                context["errors"] = post_form.errors.items()
        return context

    def make_connexion(self, request, user_id):
        """Make connexion"""
        form = SearchForm()
        account = Account.objects.filter(
            adresse_mail=request.POST.get("email"),
            password=request.POST.get("password"),
        )
        if len(account) == 0:
            home_status = "connexion"
            form = ConnexionForm()
            message_to_user = "Adresse ou mot de passe incorrect"
            context = {
                "user_id": user_id,
                "home_status": home_status,
                "form": form,
                "message_to_user": message_to_user,
            }
        else:
            request.session["user_id"] = account[0].id
            user_id = request.session["user_id"]
            context = {"user_id": user_id, "home_status": None, "form": form}
        return context

    def make_disconnexion(self, request):
        """ Make disconnection """
        form = SearchForm()
        try:
            del request.session["user_id"]
        except Exception as e:
            pass
        user_id = None
        context = {"user_id": user_id, "home_status": None, "form": form}
        return context
