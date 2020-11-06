from django import forms


class InscriptionForm(forms.Form):
    """Inscription form"""

    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class ConnexionForm(forms.Form):
    """Inscription form"""

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class SearchForm(forms.Form):
    """Search form"""

    search_input = forms.CharField(
        label="", widget=forms.TextInput(attrs={"class": "col-12"})
    )
