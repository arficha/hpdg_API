from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .constances import forms
from .constances import constances  as c
import datetime
import json,base64
import logging
from PIL import Image
#import pandas as pd
import random
#import numpy as np
import requests
from django.core.files.storage import FileSystemStorage
from collections import Counter
from secrets import token_hex
from django.http import QueryDict
from .views import *

User_END_POINT = "http://hpdg.steps4u.net/auth/users/"

logger = logging.getLogger('db')

def chat_box(request, chat_box_name):
    # we will get the chatbox name from the url
    return render(request, "chatbox.html", {"chat_box_name": chat_box_name})

@csrf_exempt
def home(request):
    return render(request,template_name='index.html')


@csrf_exempt
def admin(request):
    return render(request,template_name='admin.html')


@csrf_exempt
def inscription_c(request):
    return render(request,template_name='incrisption_c.html')

@csrf_exempt
def connexion_c(request):
    return render(request,template_name='connexion_c.html')

@csrf_exempt
def consulter_dispo(request):
    return render(request,template_name='consulter_dispo.html')

@csrf_exempt
def effectuer_reservation(request):
    return render(request,template_name='effectuer_reservation.html')


@csrf_exempt
def connexion_a(request):
    return render(request,template_name='connexion_a.html')

@csrf_exempt
def inscription_a(request):
    return render(request,template_name='inscription_a.html')

@csrf_exempt
def profil_a(request):
    return render(request,template_name='profil_a.html')

@csrf_exempt
def profil_c(request):
    return render(request,template_name='profil_c.html')

@csrf_exempt
def home_a(request):
    return render(request,template_name='home_a.html')

@csrf_exempt
def home_sp(request):
    return render(request,template_name='home_sp.html')

@csrf_exempt
def downloadPage(request):
    return render(request,template_name='download_example.html')

#CRUD views for Token Model
@csrf_exempt
def createToken(request):
    data = {
        "error": True,
        "code": -4,
    }
    status = 400
    if  request.method == 'POST':
        body={
            'id':request.POST.get("id",''),
            'email':request.POST.get("email",''),
            'password':request.POST.get("password",''),
        }
        payload = json.dumps(body)
        payload = json.loads(payload)
        form = forms.InitToken(payload)
        if form.is_valid() :
            password = form.cleaned_data["password"]
            email = form.cleaned_data["email"]
            try:
                usr = Token()
                usr.id=email
                usr.password = password
                usr.email = email
                usr.save() 
                data["error"] = False
                data["code"] = 0
                data["data"] = {
                            "id":usr.id,
                            "password" : usr.password,
                            "email" : usr.email,
                            "creation_date" : usr.creation_date,
                            }
                status = 200
            except Exception as e :
                data["error"] = True
                data["code"] = -1
                data['description'] = 'Database Writing error occured :' + str(e)
                logger.exception(data["description"])
                status = 300
        elif not form.is_valid():
            status = 400
            data['code'] = -2
            data['error'] = True
            data['description'] = 'Bad datas given '+form.errors.as_text()
            logger.exception(data["description"])
        else:
            status = 400
            data['code'] = -3
            data['error'] = True
            data['description'] = 'Bad Authorization'
            logger.exception(data["description"])
    
    else:
        status = 400
        data['code'] = -4
        data['error'] = True
        data['description'] = 'Unauthorized method '
        logger.exception(data["description"])
    return JsonResponse(data, status=status)

@csrf_exempt
def refreshToken(request):
    data = {
        "error": True,
        "code": -4,
    }
    status = 400
    if request.method == 'PUT' or request.method == 'POST':
        payload = json.loads(request.body)
        form = forms.getToken(payload)
        ip = ''
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        if form.is_valid():
            password = form.cleaned_data["password"]
            email = form.cleaned_data["email"]
            usr = Token.objects.filter(email=email).filter(password=password)
            if len(usr)>0:
                usr=usr[0]
                sessions = Session.objects.filter(email=email).filter(ip=ip)
                if len(sessions)==0 or sessions[0].end_time < datetime.datetime.now().timestamp():
                    session = Session()
                    codefin = datetime.datetime.now().timestamp()
                    session.id = str(uuid.uuid4()) + ":"+str(codefin)
                    session.access = token_hex(100)
                    session.refresh = token_hex(100)
                    session.ip = ip
                    session.email = email
                    now=floor(datetime.datetime.now().timestamp())
                    end_time = (now + (3600*24*30))
                    session.end_time = end_time
                    session.save()
                else :
                    session=sessions[0]

                data["error"] = False
                data["code"] = 0
                data["access"] = session.access
                data["refresh"] = session.refresh
                data["role"] = usr.role
                status = 200
            else:
                data["error"] = True
                data["code"] = -1
                data['description'] = 'No matching Credentials'
                status = 300
        else:
            status = 400
            data['code'] = -2
            data['error'] = True
            data['description'] = 'Bad datas given '+form.errors.as_text()
            logger.exception(data["description"])
    else:
        status = 400
        data['code'] = -4
        data['error'] = True
        data['description'] = 'Unauthorized method '
        logger.exception(data["description"])
    return JsonResponse(data, status=status)

@csrf_exempt
def verifyToken(request):
    data = {
        "error": True,
        "code": -4,
    }
    status = 400
    if request.method == 'PUT' or request.method == 'POST': 
        payload = json.loads(request.body)
        ip = ''
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        form = forms.verifytoken(payload)
        if form.is_valid() :
            access = form.cleaned_data["access"]
            usr = Token.objects.filter(access=access)
            if len(usr)>0:
                usr=usr[0] 
                if ip in usr.ips.split('#'):
                    data["error"] = False
                    data["code"] = 0
                    data["data"] = {
                            "id":usr.id,
                            "email" : usr.email,
                            "end_time" : usr.end_time,
                            }
                    status = 200
                else:
                    data["error"] = True
                    data["code"] = -1
                    data['description'] = 'No matching Credentials'
                    status = 300
            else:
                data["error"] = True
                data["code"] = -1
                data['description'] = 'No matching Credentials'
                status = 300
        elif not form.is_valid():
                status = 400
                data['code'] = -2
                data['error'] = True
                data['description'] = 'Bad datas given '+form.errors.as_text()
                logger.exception(data["description"])
    else:
        status = 405
        data['code'] = -4
        data['error'] = True
        data['description'] = 'Unauthorized method'
        logger.exception(data["description"])
    return JsonResponse(data, status=status)

@csrf_exempt
def signOut(request):
    data = {
        "error": True,
        "code": -4,
    }
    status = 400
    if request.method == 'GET':
        payload = json.dumps(request.GET.dict())
        payload = json.loads(payload)
        ip = ''
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        form = forms.verifytoken(payload)
        if form.is_valid() :
            access = form.cleaned_data["access"]
            usr = Token.objects.filter(access=access)
            if len(usr)>0:
                usr=usr[0]
                ips=usr.ips.split('#')
                if ip in usr.ips.split('#'):
                    ips.remove(ip)
                    ips_str = ''
                    for i in range(len(ips)):
                        if i == len(ips)-1:
                            ips_str += ips[i]
                        else :
                            ips_str += ips[i] + '#'
                    usr.ips=ips_str
                    usr.save()
                    data["error"] = False
                    data["code"] = 0
                    data["data"] = ip + ' logged out successfully'
                    logger.info(data["data"])
                    status = 200
                else:
                    data["error"] = True
                    data["code"] = -1
                    data['description'] = 'No matching Credentials'
                    status = 300
            else:
                data["error"] = True
                data["code"] = -1
                data['description'] = 'No matching Credentials'
                status = 300
        elif not form.is_valid():
            status = 400
            data['code'] = -2
            data['error'] = True
            data['description'] = 'Bad datas given '+form.errors.as_text()
            logger.exception(data["description"])
        else:
            status = 400
            data['code'] = -3
            data['error'] = True
            data['description'] = 'Bad Authorization'
            logger.exception(data["description"])
    else:
        status = 405
        data['code'] = -4
        data['error'] = True
        data['description'] = 'Unauthorized method'
        logger.exception(data["description"])
    return JsonResponse(data, status=status)

@csrf_exempt
def setPassword(request):
    data = {
        "error": True,
        "code": -4,
    }
    status = 400
    if request.method == 'GET':
        payload = json.dumps(request.GET.dict())
        payload = json.loads(payload)
        form = forms.verifytoken(payload)
        if form.is_valid() :
            email = form.cleaned_data["email"]
            newpassword = form.cleaned_data["newpassword"]
            usr = Token.objects.filter(email=email)
            if len(usr)>0:
                usr=usr[0]
                usr.password=newpassword
                usr.save()
                data["error"] = False
                data["code"] = 0
                data["data"] = ' password out successfully'
                logger.info(data["data"])
                status = 200
            else:
                data["error"] = True
                data["code"] = -1
                data['description'] = 'No matching Credentials'
                status = 300
        else:
            status = 400
            data['code'] = -3
            data['error'] = True
            data['description'] = 'Not Authorized to perform this action'
            logger.exception(data["description"] +' tried by Token '+token)
    else:
        status = 405
        data['code'] = -4
        data['error'] = True
        data['description'] = 'Unauthorized method PUT'
        logger.exception(data["description"])
    return JsonResponse(data, status=status)

def verifyTokenIn(token,request):
    #print('verifying user : ' + token)
    ip = ''
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    toks = Session.objects.filter(access=token.replace('Bearer ',''))
    if len(toks)>0:
        usr=toks[0]
        #print(ip+' ----- '+usr.ips)
        if ip == usr.ip:
            return True
        else:
            return False
    else :
        return False 


#CRUD views for Client Model
@csrf_exempt
def createClient(request):
    data = {
        "error": True,
        "code": -4,
    }
    status = 400
    if request.method == 'PUT' or request.method == 'POST':
        
        ip = ''
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        try:
            payload = json.loads(request.body)
            form = forms.InitClient(payload)
            if form.is_valid() :
                nom = form.cleaned_data["nom"]
                prenom = form.cleaned_data["prenom"]
                email = form.cleaned_data["email"]
                password = form.cleaned_data["password"]
                photo = form.cleaned_data["photo"]
                sexe = form.cleaned_data["sexe"]
                cni = form.cleaned_data["cni"]
                telephone = form.cleaned_data["telephone"]
                try:
                    token = Token()
                    token.id=email
                    token.password = password
                    token.email = email
                    token.role = 'client'
                    token.save() 
                    
                    session = Session()
                    codefin = datetime.datetime.now().timestamp()
                    session.id = str(uuid.uuid4()) + ":"+str(len(Client.objects.filter(creation_date=codefin)))
                    session.access = token_hex(100)
                    session.refresh = token_hex(100)
                    session.ip = ip
                    session.email = email
                    now=floor(datetime.datetime.now().timestamp())
                    end_time = (now + (3600*24*30))
                    session.end_time = end_time
                    session.save()
                    
                    usr = Client()
                    usr.id=id
                    print(floor(datetime.datetime.now().timestamp()))
                    codefin = datetime.datetime.now().timestamp()
                    usr.id = str(uuid.uuid4()) + ":"+str(len(Client.objects.filter(creation_date=codefin)))
                    usr.nom = nom
                    usr.prenom = prenom
                    usr.email = email
                    usr.photo = photo
                    usr.sexe = sexe
                    usr.cni = cni
                    usr.telephone = telephone
                    usr.save() 
                    data["error"] = False
                    data["code"] = 0
                    data["data"] = {
                                "id":usr.id,
                                "nom" : usr.nom,
                                "prenom" : usr.prenom,
                                "email" : usr.email,
                                "photo" : usr.photo,
                                "sexe" : usr.sexe,
                                "cni" : usr.cni,
                                "telephone" : usr.telephone,
                                }
                    status = 200
                    logger.info('New Client created successfully')
                except Exception as e :
                    data["error"] = True
                    data["code"] = -1
                    data['description'] = 'Database Writing error occured :' + str(e)
                    status = 302
                    logger.exception(e)
            elif not form.is_valid():
                status = 400
                data['code'] = -2
                data['error'] = True
                data['description'] = 'Bad datas given '+ form.errors.as_text()
                logger.exception(data['description'])
        except  Exception as e:
            status = 500
            data['code'] = -4
            data['error'] = True
            data['description'] = str(e)
            logger.exception(e)
    else:
        status = 400
        data['code'] = -4
        data['error'] = True
        data['description'] = 'Unauthorized method GET'
        logger.exception(data['description'])
    return JsonResponse(data, status=status)

@csrf_exempt
def updateClient(request):
    data = {
        "error": True,
        "code": -4,
    }
    status = 400
    if request.method == 'PUT' or request.method == 'POST':
        token=request.META['HTTP_AUTHORIZATION']
        payload = json.loads(request.body)
        form = forms.InitClient(payload)
        #print(token)
        if verifyTokenIn(token=token,request=request) and form.is_valid():

            nom = form.cleaned_data["nom"]
            prenom = form.cleaned_data["prenom"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            photo = form.cleaned_data["photo"]
            sexe = form.cleaned_data["sexe"]
            cni = form.cleaned_data["cni"]
            telephone = form.cleaned_data["telephone"]
            try:
                usr = Client.objects.get(id=id)
                usr.nom = nom
                usr.prenom = prenom
                usr.email = email
                usr.photo = photo
                usr.sexe = sexe
                usr.cni = cni
                usr.telephone = telephone
                usr.save() 
                data["error"] = False
                data["code"] = 0
                data["data"] = {
                                "id":usr.id,
                                "nom" : usr.nom,
                                "prenom" : usr.prenom,
                                "email" : usr.email,
                                "photo" : usr.photo,
                                "sexe" : usr.sexe,
                                "cni" : usr.cni,
                                "telephone" : usr.telephone,
                            "creation_date" : usr.creation_date,
                            }
                data['error']= False
                status = 200
                logger.info('New Client updated successfully')
            except Exception as e :
                data["error"] = True
                data["code"] = -1
                data['description'] = 'Database Writing error occured :' + str(e)
                status = 300
                logger.exception(data["description"])
        elif not form.is_valid():
            status = 400
            data['code'] = -2
            data['error'] = True
            data['description'] = 'Bad datas given '+form.errors.as_text()
            logger.exception(data["description"])
        else:
            status = 400
            data['code'] = -3
            data['error'] = True
            data['description'] = 'Bad Authorization'
            logger.exception(data["description"])
    else:
        status = 400
        data['code'] = -4
        data['error'] = True
        data['description'] = 'Unauthorized method GET'
        logger.exception(data["description"])
    return JsonResponse(data, status=status)

@csrf_exempt
def getClient(request):
    data = {
        "error": True,
        "code": -4,
    }
    status = 400
    if request.method == 'GET':
        token=request.META['HTTP_AUTHORIZATION']  
        payload = json.dumps(request.GET.dict())
        payload = json.loads(payload)
        print(payload)
        form = forms.getObject(payload)
        if verifyTokenIn(token=token,request=request) and form.is_valid() :
            id = form.cleaned_data["id"]
            usr = Client.objects.get(id=id)
            
            data["error"] = False
            data["code"] = 0
            data["data"] = {
                                "id":usr.id,
                                "nom" : usr.nom,
                                "prenom" : usr.prenom,
                                "email" : usr.email,
                                "photo" : usr.photo,
                                "sexe" : usr.sexe,
                                "cni" : usr.cni,
                                "telephone" : usr.telephone,
                                "statut" : usr.statut,
                    "creation_date" : usr.creation_date,
                    }
            status = 200
        elif not form.is_valid():
                status = 400
                data['code'] = -2
                data['error'] = True
                data['description'] = 'Bad datas given '+form.errors.as_text()
                logger.exception(data["description"])
        else:
            status = 400
            data['code'] = -3
            data['error'] = True
            data['description'] = 'Bad Authorization'
            logger.exception(data["description"])
    else:
        status = 405
        data['code'] = -4
        data['error'] = True
        data['description'] = 'Unauthorized method PUT'
        logger.exception(data["description"])
    return JsonResponse(data, status=status)

@csrf_exempt
def getClients(request):
    data = {
        "error": True,
        "code": -4,
    }
    status = 400
    if request.method == 'GET':
        token=request.META['HTTP_AUTHORIZATION']
        if verifyTokenIn(token=token,request=request) :
            pres = Client.objects.all()
            res = []
            for usr in pres:
                if usr.id!="":
                    res.append({
                                "id":usr.id,
                                "nom" : usr.nom,
                                "prenom" : usr.prenom,
                                "email" : usr.email,
                                "photo" : usr.photo,
                                "sexe" : usr.sexe,
                                "cni" : usr.cni,
                                "telephone" : usr.telephone,
                                "statut" : usr.statut,
                    "creation_date" : usr.creation_date,
                    })
            data["error"] = False
            data["code"] = 0
            data["data"] = res
            status = 200
            logger.info('inscriptions fetched successfully')
        else:
            status = 400
            data['code'] = -3
            data['error'] = True
            data['description'] = 'Bad Authorization'
            logger.exception(data["description"])
    else:
        status = 405
        data['code'] = -4
        data['error'] = True
        data['description'] = 'Unauthorized method'
        logger.exception(data["description"])
    return JsonResponse(data, status=status)


@csrf_exempt
def getClientWithEmailandPwd(request):
    data = {
        "error": True,
        "code": -4,
    }
    status = 400
    if request.method == 'GET':
        token=request.META['HTTP_AUTHORIZATION']  
        payload = json.dumps(request.GET.dict())
        payload = json.loads(payload)
        print(payload)
        form = forms.getUserwithemail(payload)
        if verifyTokenIn(token=token,request=request) and form.is_valid() :
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            try:
                usr = Client.objects.get(email=email)
                data["error"] = False
                data["code"] = 0
                data["data"] = {
                                "id":usr.id,
                                "nom" : usr.nom,
                                "prenom" : usr.prenom,
                                "email" : usr.email,
                                "photo" : usr.photo,
                                "sexe" : usr.sexe,
                                "cni" : usr.cni,
                                "telephone" : usr.telephone,
                                "statut" : usr.statut,
                             "creation_date" : usr.creation_date,
                        }
                status = 200
            except Exception as e:
                status = 300
                data['code'] = -1
                data['error'] = True
                data['description'] = 'No matching account found '+ str(e)
                print(str(e))
                logger.exception(data["description"])

        elif not form.is_valid():
                status = 400
                data['code'] = -2
                data['error'] = True
                data['description'] = 'Bad datas given '+form.errors.as_text()
                logger.exception(data["description"])
        else:
            status = 400
            data['code'] = -3
            data['error'] = True
            data['description'] = 'Bad Authorization'
            logger.exception(data["description"])
    else:
        status = 405
        data['code'] = -4
        data['error'] = True
        data['description'] = 'Unauthorized method PUT'
        logger.exception(data["description"])
    return JsonResponse(data, status=status)

@csrf_exempt
def deleteClient(request):
    data = {
        "error": True,
        "code": -4,
    }
    status = 400
    if request.method == 'GET':
        token=request.META['HTTP_AUTHORIZATION']  
        payload = json.dumps(request.GET.dict())
        payload = json.loads(payload)
        print(payload)
        form = forms.getObject(payload)
        if verifyTokenIn(token=token,request=request) and form.is_valid() :
            id = form.cleaned_data["id"]
            Client.objects.delete(id=id)
            data["error"] = False
            data["code"] = 0
            data["data"] = id + ' deleted successfully'
            status = 200
        elif not form.is_valid():
                status = 400
                data['code'] = -2
                data['error'] = True
                data['description'] = 'Bad datas given '+form.errors.as_text()
                logger.exception(data["description"])
        else:
            status = 400
            data['code'] = -3
            data['error'] = True
            data['description'] = 'Bad Authorization'
            logger.exception(data["description"])
    else:
        status = 405
        data['code'] = -4
        data['error'] = True
        data['description'] = 'Unauthorized method PUT'
        logger.exception(data["description"])
    return JsonResponse(data, status=status)

@csrf_exempt
def deleteClients(request):
    data = {
        "error": True,
        "code": -4,
    }
    status = 400
    if request.method == 'GET':
        token=request.META['HTTP_AUTHORIZATION'] 
        if c.verifyTokenSuperUsers(token=token):
            try:
                Client.objects.delete()
                data["error"] = False
                data["code"] = 0
                data["data"] ='Client table cleaned successfully'
                logger.info(data["data"])
                status = 200
            except Exception as e :
                data["error"] = True
                data["code"] = -1
                data['description'] = 'Database exception occured :' + e
                logger.exception(data["description"])
                status = 300
        else:
            status = 400
            data['code'] = -3
            data['error'] = True
            data['description'] = 'Not Authorized to perform this action'
            logger.exception(data["description"] +' tried by Token '+token)
    else:
        status = 405
        data['code'] = -4
        data['error'] = True
        data['description'] = 'Unauthorized method PUT'
        logger.exception(data["description"])
    return JsonResponse(data, status=status)


#CRUD views for Admin Model
@csrf_exempt
def createAdmin(request):
    data = {
        "error": True,
        "code": -4,
    }
    status = 400
    if request.method == 'PUT' or request.method == 'POST':
        token=request.META['HTTP_AUTHORIZATION']
        payload = json.loads(request.body)
        form = forms.InitAdmin(payload)
        ip = ''
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        if verifyTokenIn(token=token,request=request) and form.is_valid():
            id = form.cleaned_data["id"]
            id_entite = form.cleaned_data["id_entite"]
            nom = form.cleaned_data["nom"]
            prenom = form.cleaned_data["prenom"]
            photo = form.cleaned_data["photo"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            try:
                token = Token()
                token.id=email
                token.password = password
                token.email = email
                token.role = 'admin'
                token.save() 
                
                session = Session()
                codefin = datetime.datetime.now().timestamp()
                session.id = str(uuid.uuid4()) + ":"+str(len(Client.objects.filter(creation_date=codefin)))
                session.access = token_hex(100)
                session.refresh = token_hex(100)
                session.ip = ip
                session.email = email
                now=floor(datetime.datetime.now().timestamp())
                end_time = (now + (3600*24*30))
                session.end_time = end_time
                session.save()
                    
                usr = Admin()
                usr.id=id
                usr.id_entite=id_entite
                codefin = floor(datetime.datetime.now().timestamp())
                usr.id = str(uuid.uuid4()) + ":" + str(codefin)
                usr.nom = nom
                usr.prenom = prenom
                usr.email = email
                usr.photo=photo
                usr.save() 
                data["error"] = False
                data["code"] = 0
                data["data"] = {
                            "id":usr.id,
                            "nom" : usr.nom,
                            "prenom" : usr.prenom,
                            "email" : usr.email,
                            "photo" : usr.photo,
                            }
                status = 200
            except Exception as e :
                data["error"] = True
                data["code"] = -1
                data['description'] = 'Database Writing error occured :' + str(e)
                logger.exception(data["description"])
                status = 300
        elif not form.is_valid():
            status = 400
            data['code'] = -2
            data['error'] = True
            data['description'] = 'Bad datas given '+form.errors.as_text()
            logger.exception(data["description"])
        else:
            status = 400
            data['code'] = -3
            data['error'] = True
            data['description'] = 'Bad Authorization'
            logger.exception(data["description"])
    
    else:
        status = 400
        data['code'] = -4
        data['error'] = True
        data['description'] = 'Unauthorized method '
        logger.exception(data["description"])
    return JsonResponse(data, status=status)

@csrf_exempt
def updateAdmin(request):
    data = {
        "error": True,
        "code": -4,
    }
    status = 400
    if request.method == 'PUT' or request.method == 'POST':
        token=request.META['HTTP_AUTHORIZATION']
        payload = json.loads(request.body)
        form = forms.InitAdmin(payload)
        #print(token)
        if verifyTokenIn(token=token,request=request) and form.is_valid():
            nom = form.cleaned_data["nom"]
            prenom = form.cleaned_data["prenom"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            photo = form.cleaned_data["photo"]
            try:
                usr = Admin.objects.get(id=id)
                usr.nom = nom
                usr.prenom = prenom
                usr.email = email
                usr.photo = photo
                usr.save() 
                data["error"] = False
                data["code"] = 0
                data["data"] = {
                            "id":usr.id,
                            "id_entite":usr.id_entite,
                            "nom" : usr.nom,
                            "prenom" : usr.prenom,
                            "email" : usr.email,
                            "photo" : usr.photo,
                            "creation_date" : usr.creation_date,
                            }
                status = 200
            except Exception as e :
                data["error"] = True
                data["code"] = -1
                data['description'] = 'Database Writing error occured :' + str(e)
                status = 300
        elif not form.is_valid():
            status = 400
            data['code'] = -2
            data['error'] = True
            data['description'] = 'Bad datas given '+form.errors.as_text()
            logger.exception(data["description"])
        else:
            status = 400
            data['code'] = -3
            data['error'] = True
            data['description'] = 'Bad Authorization'
            logger.exception(data["description"])
    else:
        status = 400
        data['code'] = -4
        data['error'] = True
        data['description'] = 'Unauthorized method '
        logger.exception(data["description"])
    return JsonResponse(data, status=status)

@csrf_exempt
def getAdmin(request):
    data = {
        "error": True,
        "code": -4,
    }
    status = 400
    if request.method == 'GET':
        token=request.META['HTTP_AUTHORIZATION']  
        payload = json.dumps(request.GET.dict())
        payload = json.loads(payload)
        print(payload)
        form = forms.getObject(payload)
        if verifyTokenIn(token=token,request=request) and form.is_valid() :
            usr = Admin.objects.get(id=id)
            data["error"] = False
            data["code"] = 0
            data["data"] = {
                    "id":usr.id,
                    "id_entite":usr.id_entite,
                    "nom" : usr.nom,
                    "prenom" : usr.prenom,
                    "email" : usr.email,
                    "photo" : usr.photo,
                    "creation_date" : usr.creation_date,
                    }
            status = 200
        elif not form.is_valid():
                status = 400
                data['code'] = -2
                data['error'] = True
                data['description'] = 'Bad datas given '+form.errors.as_text()
                logger.exception(data["description"])
        else:
            status = 400
            data['code'] = -3
            data['error'] = True
            data['description'] = 'Bad Authorization'
            logger.exception(data["description"])
    else:
        status = 405
        data['code'] = -4
        data['error'] = True
        data['description'] = 'Unauthorized method'
        logger.exception(data["description"])
    return JsonResponse(data, status=status)

@csrf_exempt
def getAdminWithEmailandPwd(request):
    data = {
        "error": True,
        "code": -4,
    }
    status = 400
    if request.method == 'GET':
        token=request.META['HTTP_AUTHORIZATION']  
        payload = json.dumps(request.GET.dict())
        payload = json.loads(payload)
        print(payload)
        form = forms.getUserwithemail(payload)
        if verifyTokenIn(token=token,request=request) and form.is_valid() :
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            try:
                usr = Admin.objects.get(email=email)
                data["error"] = False
                data["code"] = 0
                data["data"] = {
                                
                    "id":usr.id,
                    "id_entite":usr.id_entite,
                    "nom" : usr.nom,
                    "prenom" : usr.prenom,
                    "email" : usr.email,
                    "photo" : usr.photo,
                    "creation_date" : usr.creation_date,
                      }
                status = 200
            except Exception as e:
                status = 300
                data['code'] = -1
                data['error'] = True
                data['description'] = 'No matching account found '+ str(e)
                print(str(e))
                logger.exception(data["description"])

        elif not form.is_valid():
                status = 400
                data['code'] = -2
                data['error'] = True
                data['description'] = 'Bad datas given '+form.errors.as_text()
                logger.exception(data["description"])
        else:
            status = 400
            data['code'] = -3
            data['error'] = True
            data['description'] = 'Bad Authorization'
            logger.exception(data["description"])
    else:
        status = 405
        data['code'] = -4
        data['error'] = True
        data['description'] = 'Unauthorized method PUT'
        logger.exception(data["description"])
    return JsonResponse(data, status=status)

@csrf_exempt
def getAdmins(request):
    data = {
        "error": True,
        "code": -4,
    }
    status = 400
    if request.method == 'GET':
        token=request.META['HTTP_AUTHORIZATION']
        if verifyTokenIn(token=token,request=request) :
            pres = Admin.objects.all()
            res = []
            for usr in pres:
                if usr.id!="":
                    res.append({
                              "id":usr.id,
                              "id_entite":usr.id_entite,
                              "nom" : usr.nom,
                              "prenom" : usr.prenom,
                              "email" : usr.email,
                              "photo" : usr.photo,
                              "creation_date" : usr.creation_date,
                    })
            data["error"] = False
            data["code"] = 0
            data["data"] = res
            status = 200
            logger.info('Admins fetched successfully')
        else:
            status = 400
            data['code'] = -3
            data['error'] = True
            data['description'] = 'Bad Authorization'
            logger.exception(data["description"])
    else:
        status = 405
        data['code'] = -4
        data['error'] = True
        data['description'] = 'Unauthorized method'
        logger.exception(data["description"])
    return JsonResponse(data, status=status)

@csrf_exempt
def deleteAdmin(request):
    data = {
        "error": True,
        "code": -4,
    }
    status = 400
    if request.method == 'GET':
        token=request.META['HTTP_AUTHORIZATION']  
        payload = json.dumps(request.GET.dict())
        payload = json.loads(payload)
        print(payload)
        form = forms.getObject(payload)
        if verifyTokenIn(token=token,request=request) and form.is_valid() :
            Admin.objects.delete(id=id)
            data["error"] = False
            data["code"] = 0
            data["data"] = id + ' deleted successfully'
            logger.info(data["data"])
            status = 200
        elif not form.is_valid():
            status = 400
            data['code'] = -2
            data['error'] = True
            data['description'] = 'Bad datas given '+form.errors.as_text()
            logger.exception(data["description"])
        else:
            status = 400
            data['code'] = -3
            data['error'] = True
            data['description'] = 'Bad Authorization'
            logger.exception(data["description"])
    else:
        status = 405
        data['code'] = -4
        data['error'] = True
        data['description'] = 'Unauthorized method'
        logger.exception(data["description"])
    return JsonResponse(data, status=status)


    data = {
        "error": True,
        "code": -4,
    }
    status = 400
    if request.method == 'GET':
        token=request.META['HTTP_AUTHORIZATION'] 
        if c.verifyTokenSuperUser(token=token):
            try:
                Inscription.objects.delete()
                data["error"] = False
                data["code"] = 0
                data["data"] ='Inscription table cleaned successfully'
                logger.info(data["data"])
                status = 200
            except Exception as e :
                data["error"] = True
                data["code"] = -1
                data['description'] = 'Database exception occured :' + e
                logger.exception(data["description"])
                status = 300
        else:
            status = 400
            data['code'] = -3
            data['error'] = True
            data['description'] = 'Not Authorized to perform this action'
            logger.exception(data["description"] +' tried by Token '+token)
    else:
        status = 405
        data['code'] = -4
        data['error'] = True
        data['description'] = 'Unauthorized method PUT'
        logger.exception(data["description"])
    return JsonResponse(data, status=status)



#CRUD views for Superadmin Model
@csrf_exempt
def createSuperadmin(request):
    data = {
        "error": True,
        "code": -4,
    }
    status = 400
    if request.method == 'PUT' or request.method == 'POST':
        
        ip = ''
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        try:
            payload = json.loads(request.body)
            form = forms.InitSuperadmin(payload)
            if form.is_valid() :
                nom = form.cleaned_data["nom"]
                prenom = form.cleaned_data["prenom"]
                email = form.cleaned_data["email"]
                password = form.cleaned_data["password"]
                try:
                    token = Token()
                    token.id=email
                    token.password = password
                    token.email = email
                    token.save() 
                    
                    session = Session()
                    codefin = datetime.datetime.now().timestamp()
                    session.id = str(uuid.uuid4()) + ":"+str(len(Client.objects.filter(creation_date=codefin)))
                    session.access = token_hex(100)
                    session.refresh = token_hex(100)
                    session.ip = ip
                    session.email = email
                    now=floor(datetime.datetime.now().timestamp())
                    end_time = (now + (3600*24*30))
                    session.end_time = end_time
                    session.save()
                    
                    usr = Superadmin()
                    usr.id=id
                    print(floor(datetime.datetime.now().timestamp()))
                    codefin = datetime.datetime.now().timestamp()
                    usr.id = str(uuid.uuid4()) + ":"+str(len(Client.objects.filter(creation_date=codefin)))
                    usr.nom = nom
                    usr.prenom = prenom
                    usr.email = email
                    usr.save() 
                    data["error"] = False
                    data["code"] = 0
                    data["data"] = {
                                "id":usr.id,
                                "nom" : usr.nom,
                                "prenom" : usr.prenom,
                                "email" : usr.email,
                                }
                    status = 200
                    logger.info('New Superadmin created successfully')
                except Exception as e :
                    data["error"] = True
                    data["code"] = -1
                    data['description'] = 'Database Writing error occured :' + str(e)
                    status = 302
                    logger.exception(e)
            elif not form.is_valid():
                status = 400
                data['code'] = -2
                data['error'] = True
                data['description'] = 'Bad datas given '+ form.errors.as_text()
                logger.exception(data['description'])
        except  Exception as e:
            status = 500
            data['code'] = -4
            data['error'] = True
            data['description'] = str(e)
            logger.exception(e)
    else:
        status = 400
        data['code'] = -4
        data['error'] = True
        data['description'] = 'Unauthorized method GET'
        logger.exception(data['description'])
    return JsonResponse(data, status=status)

@csrf_exempt
def updateSuperadmin(request):
    data = {
        "error": True,
        "code": -4,
    }
    status = 400
    if request.method == 'PUT' or request.method == 'POST':
        token=request.META['HTTP_AUTHORIZATION']
        payload = json.loads(request.body)
        form = forms.InitSuperadmin(payload)
        #print(token)
        if verifyTokenIn(token=token,request=request) and form.is_valid():

            nom = form.cleaned_data["nom"]
            prenom = form.cleaned_data["prenom"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            photo = form.cleaned_data["photo"]
            try:
                usr = Superadmin.objects.get(id=id)
                usr.nom = nom
                usr.prenom = prenom
                usr.email = email
                usr.save() 
                data["error"] = False
                data["code"] = 0
                data["data"] = {
                                "id":usr.id,
                                "nom" : usr.nom,
                                "prenom" : usr.prenom,
                                "email" : usr.email,
                            "creation_date" : usr.creation_date,
                            }
                data['error']= False
                status = 200
                logger.info('New Superadmin updated successfully')
            except Exception as e :
                data["error"] = True
                data["code"] = -1
                data['description'] = 'Database Writing error occured :' + str(e)
                status = 300
                logger.exception(data["description"])
        elif not form.is_valid():
            status = 400
            data['code'] = -2
            data['error'] = True
            data['description'] = 'Bad datas given '+form.errors.as_text()
            logger.exception(data["description"])
        else:
            status = 400
            data['code'] = -3
            data['error'] = True
            data['description'] = 'Bad Authorization'
            logger.exception(data["description"])
    else:
        status = 400
        data['code'] = -4
        data['error'] = True
        data['description'] = 'Unauthorized method GET'
        logger.exception(data["description"])
    return JsonResponse(data, status=status)

@csrf_exempt
def getSuperadmin(request):
    data = {
        "error": True,
        "code": -4,
    }
    status = 400
    if request.method == 'GET':
        token=request.META['HTTP_AUTHORIZATION']  
        payload = json.dumps(request.GET.dict())
        payload = json.loads(payload)
        print(payload)
        form = forms.getObject(payload)
        if verifyTokenIn(token=token,request=request) and form.is_valid() :
            id = form.cleaned_data["id"]
            usr = Superadmin.objects.get(id=id)
            
            data["error"] = False
            data["code"] = 0
            data["data"] = {
                                "id":usr.id,
                                "nom" : usr.nom,
                                "prenom" : usr.prenom,
                                "email" : usr.email,
                    "creation_date" : usr.creation_date,
                    }
            status = 200
        elif not form.is_valid():
                status = 400
                data['code'] = -2
                data['error'] = True
                data['description'] = 'Bad datas given '+form.errors.as_text()
                logger.exception(data["description"])
        else:
            status = 400
            data['code'] = -3
            data['error'] = True
            data['description'] = 'Bad Authorization'
            logger.exception(data["description"])
    else:
        status = 405
        data['code'] = -4
        data['error'] = True
        data['description'] = 'Unauthorized method PUT'
        logger.exception(data["description"])
    return JsonResponse(data, status=status)

@csrf_exempt
def getSuperadminWithEmailandPwd(request):
    data = {
        "error": True,
        "code": -4,
    }
    status = 400
    if request.method == 'GET':
        token=request.META['HTTP_AUTHORIZATION']  
        payload = json.dumps(request.GET.dict())
        payload = json.loads(payload)
        print(payload)
        form = forms.getUserwithemail(payload)
        if verifyTokenIn(token=token,request=request) and form.is_valid() :
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            try:
                usr = Superadmin.objects.get(email=email)
                data["error"] = False
                data["code"] = 0
                data["data"] = {
                                "id":usr.id,
                                "nom" : usr.nom,
                                "prenom" : usr.prenom,
                                "email" : usr.email,
                    "creation_date" : usr.creation_date,
                      }
                status = 200
            except Exception as e:
                status = 300
                data['code'] = -1
                data['error'] = True
                data['description'] = 'No matching account found '+ str(e)
                print(str(e))
                logger.exception(data["description"])

        elif not form.is_valid():
                status = 400
                data['code'] = -2
                data['error'] = True
                data['description'] = 'Bad datas given '+form.errors.as_text()
                logger.exception(data["description"])
        else:
            status = 400
            data['code'] = -3
            data['error'] = True
            data['description'] = 'Bad Authorization'
            logger.exception(data["description"])
    else:
        status = 405
        data['code'] = -4
        data['error'] = True
        data['description'] = 'Unauthorized method PUT'
        logger.exception(data["description"])
    return JsonResponse(data, status=status)

@csrf_exempt
def getSuperadmins(request):
    data = {
        "error": True,
        "code": -4,
    }
    status = 400
    if request.method == 'GET':
        token=request.META['HTTP_AUTHORIZATION']
        if verifyTokenIn(token=token,request=request) :
            pres = Superadmin.objects.all()
            res = []
            for usr in pres:
                if usr.id!="":
                    res.append({
                                "id":usr.id,
                                "nom" : usr.nom,
                                "prenom" : usr.prenom,
                                "email" : usr.email,
                    "creation_date" : usr.creation_date,
                    })
            data["error"] = False
            data["code"] = 0
            data["data"] = res
            status = 200
            logger.info('inscriptions fetched successfully')
        else:
            status = 400
            data['code'] = -3
            data['error'] = True
            data['description'] = 'Bad Authorization'
            logger.exception(data["description"])
    else:
        status = 405
        data['code'] = -4
        data['error'] = True
        data['description'] = 'Unauthorized method'
        logger.exception(data["description"])
    return JsonResponse(data, status=status)


@csrf_exempt
def deleteSuperadmin(request):
    data = {
        "error": True,
        "code": -4,
    }
    status = 400
    if request.method == 'GET':
        token=request.META['HTTP_AUTHORIZATION']  
        payload = json.dumps(request.GET.dict())
        payload = json.loads(payload)
        print(payload)
        form = forms.getObject(payload)
        if verifyTokenIn(token=token,request=request) and form.is_valid() :
            id = form.cleaned_data["id"]
            Superadmin.objects.delete(id=id)
            data["error"] = False
            data["code"] = 0
            data["data"] = id + ' deleted successfully'
            status = 200
        elif not form.is_valid():
                status = 400
                data['code'] = -2
                data['error'] = True
                data['description'] = 'Bad datas given '+form.errors.as_text()
                logger.exception(data["description"])
        else:
            status = 400
            data['code'] = -3
            data['error'] = True
            data['description'] = 'Bad Authorization'
            logger.exception(data["description"])
    else:
        status = 405
        data['code'] = -4
        data['error'] = True
        data['description'] = 'Unauthorized method PUT'
        logger.exception(data["description"])
    return JsonResponse(data, status=status)

@csrf_exempt
def deleteSuperadmins(request):
    data = {
        "error": True,
        "code": -4,
    }
    status = 400
    if request.method == 'GET':
        token=request.META['HTTP_AUTHORIZATION'] 
        if c.verifyTokenSuperUsers(token=token):
            try:
                Superadmin.objects.delete()
                data["error"] = False
                data["code"] = 0
                data["data"] ='Client table cleaned successfully'
                logger.info(data["data"])
                status = 200
            except Exception as e :
                data["error"] = True
                data["code"] = -1
                data['description'] = 'Database exception occured :' + e
                logger.exception(data["description"])
                status = 300
        else:
            status = 400
            data['code'] = -3
            data['error'] = True
            data['description'] = 'Not Authorized to perform this action'
            logger.exception(data["description"] +' tried by Token '+token)
    else:
        status = 405
        data['code'] = -4
        data['error'] = True
        data['description'] = 'Unauthorized method PUT'
        logger.exception(data["description"])
    return JsonResponse(data, status=status)



#CRUD views for Entite Model
@csrf_exempt
def createEntite(request):
    data = {
        "error": True,
        "code": -4,
    }
    status = 400
    if request.method == 'PUT' or request.method == 'POST':
        
        ip = ''
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        try:
            payload = json.loads(request.body)
            form = forms.InitEntite(payload)
            if form.is_valid() :
                nom = form.cleaned_data["nom"]
                email = form.cleaned_data["email"]
                password = form.cleaned_data["password"]
                photo = form.cleaned_data["photo"]
                description = form.cleaned_data["description"]
                adresse = form.cleaned_data["adresse"]
                telephone = form.cleaned_data["telephone"]
                try:
                    token = Token()
                    token.id=email
                    token.password = password
                    token.email = email
                    token.role = 'entite'
                    token.save() 
                    
                    session = Session()
                    codefin = datetime.datetime.now().timestamp()
                    session.id = str(uuid.uuid4()) + ":"+str(len(Client.objects.filter(creation_date=codefin)))
                    session.access = token_hex(100)
                    session.refresh = token_hex(100)
                    session.ip = ip
                    session.email = email
                    now=floor(datetime.datetime.now().timestamp())
                    end_time = (now + (3600*24*30))
                    session.end_time = end_time
                    session.save()
                    
                    usr = Entite()
                    usr.id=id
                    print(floor(datetime.datetime.now().timestamp()))
                    codefin = datetime.datetime.now().timestamp()
                    usr.id = str(uuid.uuid4()) + ":"+str(len(Client.objects.filter(creation_date=codefin)))
                    usr.nom = nom
                    usr.email = email
                    usr.photo = photo
                    usr.description = description
                    usr.adresse = adresse
                    usr.telephone = telephone
                    usr.save() 
                    data["error"] = False
                    data["code"] = 0
                    data["data"] = {
                                "id":usr.id,
                                "nom" : usr.nom,
                                "email" : usr.email,
                                "photo" : usr.photo,
                                "description" : usr.description,
                                "adresse" : usr.adresse,
                                "telephone" : usr.telephone,
                                }
                    status = 200
                    logger.info('New Client created successfully')
                except Exception as e :
                    data["error"] = True
                    data["code"] = -1
                    data['description'] = 'Database Writing error occured :' + str(e)
                    status = 302
                    logger.exception(e)
            elif not form.is_valid():
                status = 400
                data['code'] = -2
                data['error'] = True
                data['description'] = 'Bad datas given '+ form.errors.as_text()
                logger.exception(data['description'])
        except  Exception as e:
            status = 500
            data['code'] = -4
            data['error'] = True
            data['description'] = str(e)
            logger.exception(e)
    else:
        status = 400
        data['code'] = -4
        data['error'] = True
        data['description'] = 'Unauthorized method GET'
        logger.exception(data['description'])
    return JsonResponse(data, status=status)

@csrf_exempt
def updateEntite(request):
    data = {
        "error": True,
        "code": -4,
    }
    status = 400
    if request.method == 'PUT' or request.method == 'POST':
        token=request.META['HTTP_AUTHORIZATION']
        payload = json.loads(request.body)
        form = forms.InitEntite(payload)
        #print(token)
        if verifyTokenIn(token=token,request=request) and form.is_valid():

            nom = form.cleaned_data["nom"]
            prenom = form.cleaned_data["prenom"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            photo = form.cleaned_data["photo"]
            description = form.cleaned_data["description"]
            adresse = form.cleaned_data["adresse"]
            telephone = form.cleaned_data["telephone"]
            try:
                usr = Entite.objects.get(id=id)
                usr.nom = nom
                usr.email = email
                usr.photo = photo
                usr.description = description
                usr.adresse = adresse
                usr.telephone = telephone
                usr.save() 
                data["error"] = False
                data["code"] = 0
                data["data"] = {
                                "id":usr.id,
                                "nom" : usr.nom,
                                "email" : usr.email,
                                "photo" : usr.photo,
                                "description" : usr.description,
                                "adresse" : usr.adresse,
                                "telephone" : usr.telephone,
                            "creation_date" : usr.creation_date,
                            }
                data['error']= False
                status = 200
                logger.info('New Client updated successfully')
            except Exception as e :
                data["error"] = True
                data["code"] = -1
                data['description'] = 'Database Writing error occured :' + str(e)
                status = 300
                logger.exception(data["description"])
        elif not form.is_valid():
            status = 400
            data['code'] = -2
            data['error'] = True
            data['description'] = 'Bad datas given '+form.errors.as_text()
            logger.exception(data["description"])
        else:
            status = 400
            data['code'] = -3
            data['error'] = True
            data['description'] = 'Bad Authorization'
            logger.exception(data["description"])
    else:
        status = 400
        data['code'] = -4
        data['error'] = True
        data['description'] = 'Unauthorized method GET'
        logger.exception(data["description"])
    return JsonResponse(data, status=status)

@csrf_exempt
def getEntite(request):
    data = {
        "error": True,
        "code": -4,
    }
    status = 400
    if request.method == 'GET':
        token=request.META['HTTP_AUTHORIZATION']  
        payload = json.dumps(request.GET.dict())
        payload = json.loads(payload)
        print(payload)
        form = forms.getObject(payload)
        if verifyTokenIn(token=token,request=request) and form.is_valid() :
            id = form.cleaned_data["id"]
            usr = Entite.objects.get(id=id)
            
            data["error"] = False
            data["code"] = 0
            data["data"] = {
                                "id":usr.id,
                                "nom" : usr.nom,
                                "email" : usr.email,
                                "photo" : usr.photo,
                                "description" : usr.description,
                                "adresse" : usr.adresse,
                                "telephone" : usr.telephone,
                                "statut" : usr.statut,
                    "creation_date" : usr.creation_date,
                    }
            status = 200
        elif not form.is_valid():
                status = 400
                data['code'] = -2
                data['error'] = True
                data['description'] = 'Bad datas given '+form.errors.as_text()
                logger.exception(data["description"])
        else:
            status = 400
            data['code'] = -3
            data['error'] = True
            data['description'] = 'Bad Authorization'
            logger.exception(data["description"])
    else:
        status = 405
        data['code'] = -4
        data['error'] = True
        data['description'] = 'Unauthorized method PUT'
        logger.exception(data["description"])
    return JsonResponse(data, status=status)

@csrf_exempt
def getEntiteWithEmailandPwd(request):
    data = {
        "error": True,
        "code": -4,
    }
    status = 400
    if request.method == 'GET':
        token=request.META['HTTP_AUTHORIZATION']  
        payload = json.dumps(request.GET.dict())
        payload = json.loads(payload)
        print(payload)
        form = forms.getUserwithemail(payload)
        if verifyTokenIn(token=token,request=request) and form.is_valid() :
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            try:
                usr = Entite.objects.get(email=email)
                data["error"] = False
                data["code"] = 0
                data["data"] = {
                                "id":usr.id,
                                "nom" : usr.nom,
                                "email" : usr.email,
                                "photo" : usr.photo,
                                "description" : usr.description,
                                "adresse" : usr.adresse,
                                "telephone" : usr.telephone,
                                "statut" : usr.statut,
                    "creation_date" : usr.creation_date,
                      }
                status = 200
            except Exception as e:
                status = 300
                data['code'] = -1
                data['error'] = True
                data['description'] = 'No matching account found '+ str(e)
                print(str(e))
                logger.exception(data["description"])

        elif not form.is_valid():
                status = 400
                data['code'] = -2
                data['error'] = True
                data['description'] = 'Bad datas given '+form.errors.as_text()
                logger.exception(data["description"])
        else:
            status = 400
            data['code'] = -3
            data['error'] = True
            data['description'] = 'Bad Authorization'
            logger.exception(data["description"])
    else:
        status = 405
        data['code'] = -4
        data['error'] = True
        data['description'] = 'Unauthorized method PUT'
        logger.exception(data["description"])
    return JsonResponse(data, status=status)

@csrf_exempt
def getEntites(request):
    data = {
        "error": True,
        "code": -4,
    }
    status = 400
    if request.method == 'GET':
        token=request.META['HTTP_AUTHORIZATION']
        if verifyTokenIn(token=token,request=request) :
            pres = Entite.objects.all()
            res = []
            for usr in pres:
                if usr.id!="":
                    res.append({
                                "id":usr.id,
                                "nom" : usr.nom,
                                "email" : usr.email,
                                "photo" : usr.photo,
                                "description" : usr.description,
                                "adresse" : usr.adresse,
                                "telephone" : usr.telephone,
                                "statut" : usr.statut,
                    "creation_date" : usr.creation_date,
                    })
            data["error"] = False
            data["code"] = 0
            data["data"] = res
            status = 200
            logger.info('inscriptions fetched successfully')
        else:
            status = 400
            data['code'] = -3
            data['error'] = True
            data['description'] = 'Bad Authorization'
            logger.exception(data["description"])
    else:
        status = 405
        data['code'] = -4
        data['error'] = True
        data['description'] = 'Unauthorized method'
        logger.exception(data["description"])
    return JsonResponse(data, status=status)

@csrf_exempt
def deleteEntite(request):
    data = {
        "error": True,
        "code": -4,
    }
    status = 400
    if request.method == 'GET':
        token=request.META['HTTP_AUTHORIZATION']  
        payload = json.dumps(request.GET.dict())
        payload = json.loads(payload)
        print(payload)
        form = forms.getObject(payload)
        if verifyTokenIn(token=token,request=request) and form.is_valid() :
            id = form.cleaned_data["id"]
            Entite.objects.delete(id=id)
            data["error"] = False
            data["code"] = 0
            data["data"] = id + ' deleted successfully'
            status = 200
        elif not form.is_valid():
                status = 400
                data['code'] = -2
                data['error'] = True
                data['description'] = 'Bad datas given '+form.errors.as_text()
                logger.exception(data["description"])
        else:
            status = 400
            data['code'] = -3
            data['error'] = True
            data['description'] = 'Bad Authorization'
            logger.exception(data["description"])
    else:
        status = 405
        data['code'] = -4
        data['error'] = True
        data['description'] = 'Unauthorized method PUT'
        logger.exception(data["description"])
    return JsonResponse(data, status=status)

@csrf_exempt
def deleteEntites(request):
    data = {
        "error": True,
        "code": -4,
    }
    status = 400
    if request.method == 'GET':
        token=request.META['HTTP_AUTHORIZATION'] 
        if c.verifyTokenSuperUsers(token=token):
            try:
                Entite.objects.delete()
                data["error"] = False
                data["code"] = 0
                data["data"] ='Client table cleaned successfully'
                logger.info(data["data"])
                status = 200
            except Exception as e :
                data["error"] = True
                data["code"] = -1
                data['description'] = 'Database exception occured :' + e
                logger.exception(data["description"])
                status = 300
        else:
            status = 400
            data['code'] = -3
            data['error'] = True
            data['description'] = 'Not Authorized to perform this action'
            logger.exception(data["description"] +' tried by Token '+token)
    else:
        status = 405
        data['code'] = -4
        data['error'] = True
        data['description'] = 'Unauthorized method PUT'
        logger.exception(data["description"])
    return JsonResponse(data, status=status)


#CRUD views for Chambre Model
@csrf_exempt
def createChambre(request):
    data = {
        "error": True,
        "code": -4,
    }
    status = 400
    if request.method == 'PUT' or request.method == 'POST':
        
        ip = ''
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        try:
            payload = json.loads(request.body)
            form = forms.InitChambre(payload)
            if form.is_valid() :
                nom = form.cleaned_data["nom"]
                capacite = form.cleaned_data["capacite"]
                prix = form.cleaned_data["prix"]
                try:
                    
                    usr = Chambre()
                    usr.id=id
                    print(floor(datetime.datetime.now().timestamp()))
                    codefin = datetime.datetime.now().timestamp()
                    usr.id = str(uuid.uuid4()) + ":"+str(len(Client.objects.filter(creation_date=codefin)))
                    usr.nom = nom
                    usr.capacite = capacite
                    usr.save() 
                    data["error"] = False
                    data["code"] = 0
                    data["data"] = {
                                "id":usr.id,
                                "nom" : usr.nom,
                                "capacite" : usr.capacite,
                                "prix" : usr.prix,
                                }
                    status = 200
                    logger.info('New Client created successfully')
                except Exception as e :
                    data["error"] = True
                    data["code"] = -1
                    data['description'] = 'Database Writing error occured :' + str(e)
                    status = 302
                    logger.exception(e)
            elif not form.is_valid():
                status = 400
                data['code'] = -2
                data['error'] = True
                data['description'] = 'Bad datas given '+ form.errors.as_text()
                logger.exception(data['description'])
        except  Exception as e:
            status = 500
            data['code'] = -4
            data['error'] = True
            data['description'] = str(e)
            logger.exception(e)
    else:
        status = 400
        data['code'] = -4
        data['error'] = True
        data['description'] = 'Unauthorized method GET'
        logger.exception(data['description'])
    return JsonResponse(data, status=status)

@csrf_exempt
def updateChambre(request):
    data = {
        "error": True,
        "code": -4,
    }
    status = 400
    if request.method == 'PUT' or request.method == 'POST':
        token=request.META['HTTP_AUTHORIZATION']
        payload = json.loads(request.body)
        form = forms.InitChambre(payload)
        #print(token)
        if verifyTokenIn(token=token,request=request) and form.is_valid():

            nom = form.cleaned_data["nom"]
            capacite = form.cleaned_data["capacite"]
            prix = form.cleaned_data["prix"]
            try:
                usr = Chambre.objects.get(id=id)
                usr.nom = nom
                usr.capacite = capacite
                usr.prix = prix
                usr.save() 
                data["error"] = False
                data["code"] = 0
                data["data"] = {
                                "id":usr.id,
                                "nom" : usr.nom,
                                "capacite" : usr.capacite,
                                "prix" : usr.prix,
                            "creation_date" : usr.creation_date,
                            }
                data['error']= False
                status = 200
                logger.info('New Client updated successfully')
            except Exception as e :
                data["error"] = True
                data["code"] = -1
                data['description'] = 'Database Writing error occured :' + str(e)
                status = 300
                logger.exception(data["description"])
        elif not form.is_valid():
            status = 400
            data['code'] = -2
            data['error'] = True
            data['description'] = 'Bad datas given '+form.errors.as_text()
            logger.exception(data["description"])
        else:
            status = 400
            data['code'] = -3
            data['error'] = True
            data['description'] = 'Bad Authorization'
            logger.exception(data["description"])
    else:
        status = 400
        data['code'] = -4
        data['error'] = True
        data['description'] = 'Unauthorized method GET'
        logger.exception(data["description"])
    return JsonResponse(data, status=status)

@csrf_exempt
def getChambre(request):
    data = {
        "error": True,
        "code": -4,
    }
    status = 400
    if request.method == 'GET':
        token=request.META['HTTP_AUTHORIZATION']  
        payload = json.dumps(request.GET.dict())
        payload = json.loads(payload)
        print(payload)
        form = forms.getObject(payload)
        if verifyTokenIn(token=token,request=request) and form.is_valid() :
            id = form.cleaned_data["id"]
            usr = Chambre.objects.get(id=id)
            
            data["error"] = False
            data["code"] = 0
            data["data"] = {
                                "id":usr.id,
                                "nom" : usr.nom,
                                "capacite" : usr.capacite,
                                "prix" : usr.prix,
                                "statut" : usr.statut,
                                "creation_date" : usr.creation_date,
                    }
            status = 200
        elif not form.is_valid():
                status = 400
                data['code'] = -2
                data['error'] = True
                data['description'] = 'Bad datas given '+form.errors.as_text()
                logger.exception(data["description"])
        else:
            status = 400
            data['code'] = -3
            data['error'] = True
            data['description'] = 'Bad Authorization'
            logger.exception(data["description"])
    else:
        status = 405
        data['code'] = -4
        data['error'] = True
        data['description'] = 'Unauthorized method PUT'
        logger.exception(data["description"])
    return JsonResponse(data, status=status)

@csrf_exempt
def getChambres(request):
    data = {
        "error": True,
        "code": -4,
    }
    status = 400
    if request.method == 'GET':
        token=request.META['HTTP_AUTHORIZATION']
        if verifyTokenIn(token=token,request=request) :
            pres = Chambre.objects.all()
            res = []
            for usr in pres:
                if usr.id!="":
                    res.append({
                                "id":usr.id,
                                "nom" : usr.nom,
                                "capacite" : usr.capacite,
                                "prix" : usr.prix,
                                "statut" : usr.statut,
                    "creation_date" : usr.creation_date,
                    })
            data["error"] = False
            data["code"] = 0
            data["data"] = res
            status = 200
            logger.info('inscriptions fetched successfully')
        else:
            status = 400
            data['code'] = -3
            data['error'] = True
            data['description'] = 'Bad Authorization'
            logger.exception(data["description"])
    else:
        status = 405
        data['code'] = -4
        data['error'] = True
        data['description'] = 'Unauthorized method'
        logger.exception(data["description"])
    return JsonResponse(data, status=status)

@csrf_exempt
def getChambresFromEntity(request):
    data = {
        "error": True,
        "code": -4,
    }
    status = 400
    if request.method == 'GET':
        token=request.META['HTTP_AUTHORIZATION']
        payload = json.dumps(request.GET.dict())
        payload = json.loads(payload)
        print(payload)
        form = forms.getObject(payload)
        if verifyTokenIn(token=token,request=request) and  form.is_valid() :
            id = form.cleaned_data["id"]
            pres = Chambre.objects.filter(entite=id).exclude(status='5')
            now=floor(datetime.datetime.now().timestamp())
            res = []
            for usr in pres:
                if usr.id!="":
                    res.append({
                                "id":usr.id,
                                "nom" : usr.nom,
                                "capacite" : usr.capacite,
                                "availability" : usr.capacite - len(Reservation.objects.filter(items__contains=usr.id).filter(date_debut__gt=now) |
                                                                    Reservation.objects.filter(items__contains=usr.id).filter(date_fin__lt=now)),
                                "prix" : usr.prix,
                                "statut" : usr.statut,
                    "creation_date" : usr.creation_date,
                    })
            data["error"] = False
            data["code"] = 0
            data["data"] = res
            status = 200
            logger.info('inscriptions fetched successfully')
        else:
            status = 400
            data['code'] = -3
            data['error'] = True
            data['description'] = 'Bad Authorization'
            logger.exception(data["description"])
    else:
        status = 405
        data['code'] = -4
        data['error'] = True
        data['description'] = 'Unauthorized method'
        logger.exception(data["description"])
    return JsonResponse(data, status=status)

@csrf_exempt
def deleteChambre(request):
    data = {
        "error": True,
        "code": -4,
    }
    status = 400
    if request.method == 'GET':
        token=request.META['HTTP_AUTHORIZATION']  
        payload = json.dumps(request.GET.dict())
        payload = json.loads(payload)
        print(payload)
        form = forms.getObject(payload)
        if verifyTokenIn(token=token,request=request) and form.is_valid() :
            id = form.cleaned_data["id"]
            Chambre.objects.delete(id=id)
            data["error"] = False
            data["code"] = 0
            data["data"] = id + ' deleted successfully'
            status = 200
        elif not form.is_valid():
                status = 400
                data['code'] = -2
                data['error'] = True
                data['description'] = 'Bad datas given '+form.errors.as_text()
                logger.exception(data["description"])
        else:
            status = 400
            data['code'] = -3
            data['error'] = True
            data['description'] = 'Bad Authorization'
            logger.exception(data["description"])
    else:
        status = 405
        data['code'] = -4
        data['error'] = True
        data['description'] = 'Unauthorized method PUT'
        logger.exception(data["description"])
    return JsonResponse(data, status=status)

@csrf_exempt
def deleteChambres(request):
    data = {
        "error": True,
        "code": -4,
    }
    status = 400
    if request.method == 'GET':
        token=request.META['HTTP_AUTHORIZATION'] 
        if c.verifyTokenSuperUsers(token=token):
            try:
                Chambre.objects.delete()
                data["error"] = False
                data["code"] = 0
                data["data"] ='Client table cleaned successfully'
                logger.info(data["data"])
                status = 200
            except Exception as e :
                data["error"] = True
                data["code"] = -1
                data['description'] = 'Database exception occured :' + e
                logger.exception(data["description"])
                status = 300
        else:
            status = 400
            data['code'] = -3
            data['error'] = True
            data['description'] = 'Not Authorized to perform this action'
            logger.exception(data["description"] +' tried by Token '+token)
    else:
        status = 405
        data['code'] = -4
        data['error'] = True
        data['description'] = 'Unauthorized method PUT'
        logger.exception(data["description"])
    return JsonResponse(data, status=status)


#CRUD views for Reservation Model
@csrf_exempt
def createReservation(request):
    data = {
        "error": True,
        "code": -4,
    }
    status = 400
    if request.method == 'PUT' or request.method == 'POST':
        
        ip = ''
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        try:
            payload = json.loads(request.body)
            form = forms.InitReservation(payload)
            if form.is_valid() :
                nom = form.cleaned_data["nom"]
                id_client = form.cleaned_data["id_client"]
                id_entite = form.cleaned_data["id_entite"]
                prix = form.cleaned_data["prix"]
                date_debut = form.cleaned_data["date_debut"]
                date_fin = form.cleaned_data["date_fin"]
                items = form.cleaned_data["items"]
               
                try:
                    
                    usr = Reservation()
                    usr.id=id
                    print(floor(datetime.datetime.now().timestamp()))
                    codefin = datetime.datetime.now().timestamp()
                    usr.id = str(uuid.uuid4()) + ":"+str(len(Client.objects.filter(creation_date=codefin)))
                    usr.entite = Entite.objects.get(id=id_entite)
                    usr.date_debut = date_debut
                    usr.date_fin = date_fin
                    usr.prix = prix
                    usr.items = items
                    usr.client = Client.objects.get(email=id_client)


                    usr.save() 
                    data["error"] = False
                    data["code"] = 0
                    data["data"] = {
                                "id":usr.id,
                                "client": str(usr.client),
                                "entite": str(usr.entite),
                                "date_debut":usr.date_debut,
                                "date_fin":usr.date_fin,
                                "prix":usr.prix,
                                "items":usr.items,
                                }
                    status = 200
                    logger.info('New Client created successfully')
                except Exception as e :
                    data["error"] = True
                    data["code"] = -1
                    data['description'] = 'Database Writing error occured :' + str(e)
                    status = 302
                    logger.exception(e)
            elif not form.is_valid():
                status = 400
                data['code'] = -2
                data['error'] = True
                data['description'] = 'Bad datas given '+ form.errors.as_text()
                logger.exception(data['description'])
        except  Exception as e:
            status = 500
            data['code'] = -4
            data['error'] = True
            data['description'] = str(e)
            logger.exception(e)
    else:
        status = 400
        data['code'] = -4
        data['error'] = True
        data['description'] = 'Unauthorized method GET'
        logger.exception(data['description'])
    return JsonResponse(data, status=status)

@csrf_exempt
def updateReservation(request):
    data = {
        "error": True,
        "code": -4,
    }
    status = 400
    if request.method == 'PUT' or request.method == 'POST':
        token=request.META['HTTP_AUTHORIZATION']
        payload = json.loads(request.body)
        form = forms.InitReservation(payload)
        #print(token)
        if verifyTokenIn(token=token,request=request) and form.is_valid():
            
            id = form.cleaned_data["id"]
            id_client = form.cleaned_data["id_client"]
            prix = form.cleaned_data["prix"]
            date_debut = form.cleaned_data["date_debut"]
            date_fin = form.cleaned_data["date_fin"]
            items = form.cleaned_data["items"]
            try:
                usr = Reservation.objects.get(id=id)
                
                usr.id_client = id_client
                usr.date_debut = date_debut
                usr.date_fin = date_fin
                usr.prix = prix
                usr.items = items
                usr.save() 
                data["error"] = False
                data["code"] = 0
                data["data"] = {
                                "id":usr.id,
                                "id_client" : usr.id_client,
                            "creation_date" : usr.creation_date,
                            }
                data['error']= False
                status = 200
                logger.info('New Client updated successfully')
            except Exception as e :
                data["error"] = True
                data["code"] = -1
                data['description'] = 'Database Writing error occured :' + str(e)
                status = 300
                logger.exception(data["description"])
        elif not form.is_valid():
            status = 400
            data['code'] = -2
            data['error'] = True
            data['description'] = 'Bad datas given '+form.errors.as_text()
            logger.exception(data["description"])
        else:
            status = 400
            data['code'] = -3
            data['error'] = True
            data['description'] = 'Bad Authorization'
            logger.exception(data["description"])
    else:
        status = 400
        data['code'] = -4
        data['error'] = True
        data['description'] = 'Unauthorized method GET'
        logger.exception(data["description"])
    return JsonResponse(data, status=status)

@csrf_exempt
def getReservation(request):
    data = {
        "error": True,
        "code": -4,
    }
    status = 400
    if request.method == 'GET':
        token=request.META['HTTP_AUTHORIZATION']  
        payload = json.dumps(request.GET.dict())
        payload = json.loads(payload)
        print(payload)
        form = forms.getObject(payload)
        if verifyTokenIn(token=token,request=request) and form.is_valid() :
            id = form.cleaned_data["id"]
            usr = Reservation.objects.get(id=id)
            
            data["error"] = False
            data["code"] = 0
            data["data"] = {
                                "id":usr.id,
                                "id_client":usr.client.id,
                                "clientName":str(usr.client),
                                "date_debut":usr.date_debut,
                                "date_fin":usr.date_fin,
                                "prix":usr.prix,
                                "items":usr.items,
                                "statut" : usr.statut,
                    "creation_date" : usr.creation_date,
                    }
            status = 200
        elif not form.is_valid():
                status = 400
                data['code'] = -2
                data['error'] = True
                data['description'] = 'Bad datas given '+form.errors.as_text()
                logger.exception(data["description"])
        else:
            status = 400
            data['code'] = -3
            data['error'] = True
            data['description'] = 'Bad Authorization'
            logger.exception(data["description"])
    else:
        status = 405
        data['code'] = -4
        data['error'] = True
        data['description'] = 'Unauthorized method PUT'
        logger.exception(data["description"])
    return JsonResponse(data, status=status)

@csrf_exempt
def getReservations(request):
    data = {
        "error": True,
        "code": -4,
    }
    status = 400
    if request.method == 'GET':
        token=request.META['HTTP_AUTHORIZATION']
        if verifyTokenIn(token=token,request=request) :
            pres = Reservation.objects.all()
            res = []
            for usr in pres:
                if usr.id!="":
                    res.append({
                                "id":usr.id,
                                "client": str(usr.client),
                                "entite": str(usr.entite),
                                "date_debut":usr.date_debut,
                                "date_fin":usr.date_fin,
                                "prix" : usr.prix,
                                "items" : usr.items,
                                "statut" : usr.statut,
                                "creation_date" : usr.creation_date,
                    })
            data["error"] = False
            data["code"] = 0
            data["data"] = res
            status = 200
            logger.info('inscriptions fetched successfully')
        else:
            status = 400
            data['code'] = -3
            data['error'] = True
            data['description'] = 'Bad Authorization'
            logger.exception(data["description"])
    else:
        status = 405
        data['code'] = -4
        data['error'] = True
        data['description'] = 'Unauthorized method'
        logger.exception(data["description"])
    return JsonResponse(data, status=status)

@csrf_exempt
def getReservationsFromEntity(request):
    data = {
        "error": True,
        "code": -4,
    }
    status = 400
    if request.method == 'GET':
        token=request.META['HTTP_AUTHORIZATION']
        payload = json.dumps(request.GET.dict())
        payload = json.loads(payload)
        print(payload)
        form = forms.getObject(payload)
        if verifyTokenIn(token=token,request=request) and form.is_valid() :
            id = form.cleaned_data["id"]
        if verifyTokenIn(token=token,request=request) :
            pres = Reservation.objects.filter(entite = id)
            res = []
            for usr in pres:
                if usr.id!="":
                    res.append({
                                "id":usr.id,
                                "client": str(usr.client),
                                "date_debut":usr.date_debut,
                                "date_fin":usr.date_fin,
                                "prix" : usr.prix,
                                "items" : usr.items,
                                "statut" : usr.statut,
                                "creation_date" : usr.creation_date,
                    })
            data["error"] = False
            data["code"] = 0
            data["data"] = res
            status = 200
            logger.info('inscriptions fetched successfully')
        else:
            status = 400
            data['code'] = -3
            data['error'] = True
            data['description'] = 'Bad Authorization'
            logger.exception(data["description"])
    else:
        status = 405
        data['code'] = -4
        data['error'] = True
        data['description'] = 'Unauthorized method'
        logger.exception(data["description"])
    return JsonResponse(data, status=status)

@csrf_exempt
def deleteReservation(request):
    data = {
        "error": True,
        "code": -4,
    }
    status = 400
    if request.method == 'GET':
        token=request.META['HTTP_AUTHORIZATION']  
        payload = json.dumps(request.GET.dict())
        payload = json.loads(payload)
        print(payload)
        form = forms.getObject(payload)
        if verifyTokenIn(token=token,request=request) and form.is_valid() :
            id = form.cleaned_data["id"]
            Reservation.objects.delete(id=id)
            data["error"] = False
            data["code"] = 0
            data["data"] = id + ' deleted successfully'
            status = 200
        elif not form.is_valid():
                status = 400
                data['code'] = -2
                data['error'] = True
                data['description'] = 'Bad datas given '+form.errors.as_text()
                logger.exception(data["description"])
        else:
            status = 400
            data['code'] = -3
            data['error'] = True
            data['description'] = 'Bad Authorization'
            logger.exception(data["description"])
    else:
        status = 405
        data['code'] = -4
        data['error'] = True
        data['description'] = 'Unauthorized method PUT'
        logger.exception(data["description"])
    return JsonResponse(data, status=status)

@csrf_exempt
def deleteReservations(request):
    data = {
        "error": True,
        "code": -4,
    }
    status = 400
    if request.method == 'GET':
        token=request.META['HTTP_AUTHORIZATION'] 
        if c.verifyTokenSuperUsers(token=token):
            try:
                Reservation.objects.delete()
                data["error"] = False
                data["code"] = 0
                data["data"] ='Client table cleaned successfully'
                logger.info(data["data"])
                status = 200
            except Exception as e :
                data["error"] = True
                data["code"] = -1
                data['description'] = 'Database exception occured :' + e
                logger.exception(data["description"])
                status = 300
        else:
            status = 400
            data['code'] = -3
            data['error'] = True
            data['description'] = 'Not Authorized to perform this action'
            logger.exception(data["description"] +' tried by Token '+token)
    else:
        status = 405
        data['code'] = -4
        data['error'] = True
        data['description'] = 'Unauthorized method PUT'
        logger.exception(data["description"])
    return JsonResponse(data, status=status)


#CRUD views for Photo Model
@csrf_exempt
def createPhoto(request):
    data = {
        "error": True,
        "code": -4,
    }
    status = 400
    if request.method == 'PUT' or request.method == 'POST':
        token=request.META['HTTP_AUTHORIZATION']
        payload = json.loads(request.body)
        form = forms.InitPhoto(payload)
        #print(token)
        if verifyTokenIn(token=token,request=request) and form.is_valid():
            id_chambre = form.cleaned_data[" id_chambre"]
            id_entite = form.cleaned_data["  id_entite"]
            url = form.cleaned_data["url"]

            try:
                usr = Photo()
                codefin = floor(datetime.datetime.now().timestamp())
                usr.id = str(uuid.uuid4()) + ":" + str(codefin)
                usr. id_chambre =  id_chambre
                usr. id_entite =  id_entite
                usr. url =  url
                usr.save() 
                data["error"] = False
                data["code"] = 0
                data["data"] = {
                            "id":usr.id,
                            "creation_date" : usr.creation_date,
                            }
                status = 200
            except Exception as e :
                data["error"] = True
                data["code"] = -1
                data['description'] = 'Database Writing error occured :' + str(e)
                logger.exception(data["description"])
                status = 300
        elif not form.is_valid():
            status = 400
            data['code'] = -2
            data['error'] = True
            data['description'] = 'Bad datas given '+form.errors.as_text()
            logger.exception(data["description"])
        else:
            status = 400
            data['code'] = -3
            data['error'] = True
            data['description'] = 'Bad Authorization'
            logger.exception(data["description"])
    else:
        status = 400
        data['code'] = -4
        data['error'] = True
        data['description'] = 'Unauthorized method'
        logger.exception(data["description"])
    return JsonResponse(data, status=status)

@csrf_exempt
def updatePhoto(request):
    data = {
        "error": True,
        "code": -4,
    }
    status = 400
    if request.method == 'PUT' or request.method == 'POST':
        token=request.META['HTTP_AUTHORIZATION']
        payload = json.loads(request.body)
        form = forms.InitPhoto(payload)
        #print(token)
        if verifyTokenIn(token=token,request=request) and form.is_valid():
            id = form.cleaned_data["id"]
            id_chambre = form.cleaned_data["id_chambre"]
            id_entite = form.cleaned_data["id_entite"]
            url = form.cleaned_data["url"]
            try:
                usr = Photo.objects.get(id=id)
                usr. id_chambre =  id_chambre
                usr. id_entite =  id_entite
                usr. url =  url
                usr.save() 
                data["error"] = False
                data["code"] = 0
                data["data"] = {
                            "id":usr.id,
                            "creation_date" : usr.creation_date,
                            }
                status = 200
            except Exception as e :
                data["error"] = True
                data["code"] = -1
                data['description'] = 'Database Writing error occured :' + str(e)
                logger.exception(data["description"])
                status = 300
        elif not form.is_valid():
            status = 400
            data['code'] = -2
            data['error'] = True
            data['description'] = 'Bad datas given '+form.errors.as_text()
            logger.exception(data["description"])
        else:
            status = 400
            data['code'] = -3
            data['error'] = True
            data['description'] = 'Bad Authorization'
            logger.exception(data["description"])
    else:
        status = 400
        data['code'] = -4
        data['error'] = True
        data['description'] = 'Unauthorized method'
        logger.exception(data["description"])
    return JsonResponse(data, status=status)

@csrf_exempt
def getPhoto(request):
    data = {
        "error": True,
        "code": -4,
    }
    status = 400
    if request.method == 'GET':
        token=request.META['HTTP_AUTHORIZATION']  
        payload = json.dumps(request.GET.dict())
        payload = json.loads(payload)
        print(payload)
        form = forms.getObject(payload)
        if verifyTokenIn(token=token,request=request) and form.is_valid() :
            id = form.cleaned_data["id"]
            try:
                usr = Photo.objects.get(id=id)
                data["error"] = False
                data["code"] = 0
                data["data"] = {
                                "id":usr.id,
                                 "id_chambre" : usr.id_chambre,
                                 "id_entite" :  usr.id_entite,
                                 "url" : usr.url,
                                "creation_date" : usr.creation_date,
                                 }
                status = 200
            except Exception as e :
                data["error"] = True
                data["code"] = -1
                data['description'] = 'Database Writing error occured :' + str(e)
                logger.exception(data["description"])
                status = 300
        elif not form.is_valid():
            status = 400
            data['code'] = -2
            data['error'] = True
            data['description'] = 'Bad datas given '+form.errors.as_text()
            logger.exception(data["description"])
        else:
            status = 400
            data['code'] = -3
            data['error'] = True
            data['description'] = 'Bad Authorization'
            logger.exception(data["description"])
    else:
        status = 405
        data['code'] = -4
        data['error'] = True
        data['description'] = 'Unauthorized method'
        logger.exception(data["description"])
    return JsonResponse(data, status=status)

@csrf_exempt
def getPhotos(request):
    data = {
        "error": True,
        "code": -4,
    }
    status = 400
    if request.method == 'GET':
        token=request.META['HTTP_AUTHORIZATION']
        if verifyTokenIn(token=token,request=request):
            pres = Photo.objects.exclude(statut='5')
            res = []
            for usr in pres:
                if usr.id!="":
                    res.append({
                                "id":usr.id,
                                 "id_chambre" : usr.id_chambre,
                                 "id_entite" :  usr.id_entite,
                                 "url" : usr.url, 
                                "creation_date" : usr.creation_date,
                    })
            data["error"] = False
            data["code"] = 0
            data["data"] = res
            status = 200
        else:
            status = 400
            data['code'] = -3
            data['error'] = True
            data['description'] = 'Bad Authorization'
            logger.exception(data["description"])
    else:
        status = 405
        data['code'] = -4
        data['error'] = True
        data['description'] = 'Unauthorized method'
        logger.exception(data["description"])
    return JsonResponse(data, status=status)

@csrf_exempt
def deletePhoto(request):
    data = {
        "error": True,
        "code": -4,
    }
    status = 400
    if request.method == 'GET':
        token=request.META['HTTP_AUTHORIZATION']  
        payload = json.dumps(request.GET.dict())
        payload = json.loads(payload)
        print(payload)
        form = forms.getObject(payload)
        if verifyTokenIn(token=token,request=request) and form.is_valid() :
            id = form.cleaned_data["id"]
            try:
                usr = Photo.objects.get(id=id)
                usr.statut = '5'
                usr.save()
                data["error"] = False
                data["code"] = 0
                data["data"] = id + ' deleted successfully'
                logger.info(data["data"])
                status = 200
            except Exception as e :
                data["error"] = True
                data["code"] = -1
                data['description'] = 'Database Writing error occured :' + str(e)
                logger.exception(data["description"])
                status = 300
        elif not form.is_valid():
                status = 400
                data['code'] = -2
                data['error'] = True
                data['description'] = 'Bad datas given '+form.errors.as_text()
                logger.exception(data["description"])
        else:
            status = 400
            data['code'] = -3
            data['error'] = True
            data['description'] = 'Bad Authorization'
            logger.exception(data["description"])
    else:
        status = 405
        data['code'] = -4
        data['error'] = True
        data['description'] = 'Unauthorized method'
        logger.exception(data["description"])
    return JsonResponse(data, status=status)


#files management
def save_file(request_file,ext):
    fs = FileSystemStorage()
    file = fs.save('files/'+token_hex(8)+'_'+str(int(datetime.datetime.now().timestamp()))
                    +'.'+ext, request_file)
    # the fileurl variable now contains the url to the file. This can be used to serve the file when needed.
    fileurl = fs.url(file)
    return fileurl

def save_image(request_file,ext):
    fs = FileSystemStorage()
    file = fs.save('images/'+token_hex(8)+'_'+str(int(datetime.datetime.now().timestamp()))
                    +'.'+ext, request_file)
    # the fileurl variable now contains the url to the file. This can be used to serve the file when needed.
    fileurl = fs.url(file)
    return fileurl

@csrf_exempt
def upload_file(request):
    data = {
        "error": True,
        "code": -4,
    }
    status = 400
    if request.method == 'POST':
        token=request.META['HTTP_AUTHORIZATION']
        # if the PUT request has a file under the input name 'document', then save the file.
        request_file = request.FILES['document'] if 'document' in request.FILES else None
        if verifyTokenIn(token=token,request=request) and request_file:
            fileurl = save_file(request_file,request.POST.get("ext",'pdf'))
            status=200
            data['code'] = 0
            data['error'] = False
            data["data"] = {
                            "fileurl":fileurl
                            }
            logger.exception(data["data"])
        elif not request_file:
            status = 400
            data['code'] = -2
            data['error'] = True
            data['description'] = 'No file found in request'
            logger.exception(data["description"])
        else:
            status = 400
            data['code'] = -3
            data['error'] = True
            data['description'] = 'Bad Authorization'
            logger.exception(data["description"])
    return JsonResponse(data, status=status)

@csrf_exempt
def upload_image(request):
    data = {
        "error": True,
        "code": -4,
    }
    status = 400
    if request.method == 'POST':
        token=request.META['HTTP_AUTHORIZATION']
        # if the PUT request has a file under the input name 'document', then save the file.
        request_file = request.FILES['image'] if 'image' in request.FILES else None
        print(request.POST.get("ext",'jpg'))
        
        if verifyTokenIn(token=token,request=request) and request_file:
            fileurl = save_image(request_file,request.POST.get("ext",'jpg'))
            status=200
            data['code'] = 0
            data['error'] = False
            data["data"] = {
                            "fileurl":fileurl
                            }
            logger.exception(data["data"])
        elif not request_file:
            status = 400
            data['code'] = -2
            data['error'] = True
            data['description'] = 'No file found in request'
            logger.exception(data["description"])
        else:
            status = 400
            data['code'] = -3
            data['error'] = True
            data['description'] = 'Bad Authorization'
            logger.exception(data["description"])
    return JsonResponse(data, status=status)

