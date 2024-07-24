from django import forms
from . import constances as c 


class InitToken(forms.Form):
    id = forms.CharField(required=True)
    email = forms.CharField(required=True)
    password = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super(InitToken, self).__init__(*args, **kwargs)

    def clean(self):
        return self.cleaned_data

class getToken(forms.Form):
    email = forms.CharField(required=True)
    password = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super(getToken, self).__init__(*args, **kwargs)

    def clean(self):
        return self.cleaned_data

class verifytoken(forms.Form):
    access = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super(verifytoken, self).__init__(*args, **kwargs)

    def clean(self):
        return self.cleaned_data
    
class setPassword(forms.Form):
    email = forms.CharField(required=True)
    newpassword = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super(setPassword, self).__init__(*args, **kwargs)

    def clean(self):
        return self.cleaned_data






class InitClient(forms.Form):
    id = forms.CharField(required=False)
    nom = forms.CharField(required=True)
    prenom = forms.CharField(required=True)
    email = forms.CharField(required=True)
    password = forms.CharField(required=True)
    photo = forms.CharField(required=True)
    sexe = forms.CharField(required=True)
    cni = forms.CharField(required=True)
    telephone = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super(InitClient, self).__init__(*args, **kwargs)

    def clean(self):
        return self.cleaned_data
class InitAdmin(forms.Form):
    id = forms.CharField(required=False)
    id_entite= forms.CharField(required=True)
    nom = forms.CharField(required=True)
    prenom = forms.CharField(required=True)
    email = forms.CharField(required=True)
    password = forms.CharField(required=True)
    # photo = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super(InitAdmin, self).__init__(*args, **kwargs)

    def clean(self):
        return self.cleaned_data
class InitSuperadmin(forms.Form):
    id = forms.CharField(required=False)
    nom = forms.CharField(required=True)
    prenom = forms.CharField(required=True)
    email = forms.CharField(required=True)
    password = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super(InitSuperadmin, self).__init__(*args, **kwargs)

    def clean(self):
        return self.cleaned_data
class InitChambre(forms.Form):
    id = forms.CharField(required=False)
    capacite = forms.CharField(required=True)
    nom = forms.CharField(required=True)
    entite = forms.CharField(required=True)
    prix = forms.IntegerField(required=True)

    def __init__(self, *args, **kwargs):
        super(InitChambre, self).__init__(*args, **kwargs)

    def clean(self):
        return self.cleaned_data


class checkAvailability(forms.Form):
    date_debut = forms.IntegerField(required=True)
    chambre = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super(checkAvailability, self).__init__(*args, **kwargs)

    def clean(self):
        return self.cleaned_data


class InitReservation(forms.Form):
    id = forms.CharField(required=False)
    id_client= forms.CharField(required=True)
    date_debut = forms.IntegerField(required=True)
    date_fin = forms.IntegerField(required=True)
    prix = forms.IntegerField(required=True)
    nbre_personnes = forms.IntegerField(required=True)
    items = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super(InitReservation, self).__init__(*args, **kwargs)

    def clean(self):
        return self.cleaned_data

class InitReservationNoAccount(forms.Form):
    id_entite= forms.CharField(required=True)
    pays_client= forms.CharField(required=True)
    nom_client= forms.CharField(required=True)
    prenom_client= forms.CharField(required=True)
    telephone_client= forms.CharField(required=True)
    email_client= forms.CharField(required=True)
    id_entite= forms.CharField(required=True)
    date_debut = forms.IntegerField(required=True)
    date_fin = forms.IntegerField(required=True)
    prix = forms.IntegerField(required=True)
    nbre_personnes = forms.IntegerField(required=True)
    chambre = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super(InitReservationNoAccount, self).__init__(*args, **kwargs)

    def clean(self):
        return self.cleaned_data
    

class InitEntite(forms.Form):
    id = forms.CharField(required=False)
    nom = forms.CharField(required=True)
    email = forms.CharField(required=True)
    password = forms.CharField(required=True)
    photo = forms.CharField(required=True)
    description = forms.CharField(required=True)
    adresse = forms.CharField(required=True)
    telephone = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super(InitEntite, self).__init__(*args, **kwargs)

    def clean(self):
        return self.cleaned_data
class InitPhoto(forms.Form):
    id = forms.CharField(required=False)
    id_chambre= forms.CharField(required=True)
    id_entite= forms.CharField(required=True)
    url= forms.CharField(required=True)
    def __init__(self, *args, **kwargs):
        super(InitPhoto, self).__init__(*args, **kwargs)

    def clean(self):
        return self.cleaned_data

class SettUserPasword(forms.Form):
    oldpassword = forms.CharField(required=True)
    newpassword = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super(SettUserPasword, self).__init__(*args, **kwargs)

    def clean(self):
        return self.cleaned_data

class setUserphoto(forms.Form):
    id = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super(setUserphoto, self).__init__(*args, **kwargs)

    def clean(self):
        return self.cleaned_data

class getUser(forms.Form):
    id = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super(getUser, self).__init__(*args, **kwargs)

    def clean(self):
        return self.cleaned_data

class getUserwithemail(forms.Form):
    email = forms.CharField(required=True)
    password = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super(getUserwithemail, self).__init__(*args, **kwargs)

    def clean(self):
        return self.cleaned_data


class getUsersFromId(forms.Form):
    ids = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super(getUser, self).__init__(*args, **kwargs)

    def clean(self):
        return self.cleaned_data
    
class getObject(forms.Form):
    id = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super(getObject, self).__init__(*args, **kwargs)

    def clean(self):
        return self.cleaned_data
    
class setObjectStatut(forms.Form):
    id = forms.CharField(required=True)
    statut = forms.CharField(required=True)
    object = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super(setObjectStatut, self).__init__(*args, **kwargs)

    def clean(self):
        return self.cleaned_data
class InitPhoto(forms.Form):
    id = forms.CharField(required=False)
    id_chambre = forms.CharField(required=False)
    id_entite = forms.CharField(required=False)
    url = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super(InitPhoto, self).__init__(*args, **kwargs)

    def clean(self):
        return self.cleaned_data


