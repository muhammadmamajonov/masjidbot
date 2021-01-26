from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import NamozVaqti, Maruzalar, HaftaKunlari, Mavzu, Dars
import json
from rest_framework import authentication, permissions




############################ ma'lumotlar yozish #############################
############################ Namoz vaqti #############################
########################### Namoz vaqti qo'shish #############################
def namoz_vaqti_qoshish(request):
    if request.method == "POST":
        sana = request.POST['sana']
        hk = request.POST['hk']
        tong = request.POST['tong']
        quyosh = request.POST['quyosh']
        peshin = request.POST['peshin']
        asr = request.POST['asr']
        shom =request.POST['shom']
        xufton = request.POST['xufton']

        hk = HaftaKunlari.objects.get(id = hk)
        NamozVaqti.objects.create(sana=sana, hafta_kuni=hk, tong=tong, quyosh=quyosh, peshin=peshin, asr = asr, shom = shom, xufton = xufton)

    return redirect('/api/malumotlar-qoshish')
########################### /Namoz vaqti qo'shish #############################

################ namoz vaqti o'chirish ############################
def nvo(request):
    if request.method == 'POST':
        nvid = request.POST['nvid']
        okbnv = NamozVaqti.objects.get(id = nvid)
        okbnv.delete()
################ /namoz vaqti o'chirish  ############################

def MalumotYozish(request):
    hkunlari = HaftaKunlari.objects.all()
    namoz_vaqtlari = NamozVaqti.objects.all()
    return render(request, 'malumot_joylash.html', {'hkunlar':hkunlari, 'namoz_vaqtlari':namoz_vaqtlari})

########################### Maruzalar #############################
def maruzalar(request):
    if request.method == 'POST':
        mn = request.POST['mn']
        muallif = request.POST['muallif']
        maruza_audio = request.POST['maruza_audio']

        Maruzalar.objects.create(maruza_nomi=mn, muallif=muallif, maruza_audio=maruza_audio)
        return redirect('/api/maruzalar/')
    
    mar = Maruzalar.objects.all()
    return render(request, 'maruzalar.html', {'maruzalar':mar})

####################### maruzalar o'chirish  #######################################

def maruza_ochirish(request):
    if request.method == 'POST':
        mid = request.POST['mid']

        maruza = Maruzalar.objects.get(id=mid)
        maruza.delete()
        return redirect('/api/maruzalar/')
####################### /Malumot yozish  ########################################

####################### Darslar  ########################################
def darslar(request):
    if request.method == 'POST':
        dn = request.POST['dn']
        muallif = request.POST['muallif']
        dars_audio = request.POST['dars_audio']
        mavzu = request.POST['mavzu']

        mavzu = Mavzu.objects.get(id=mavzu)
        Dars.objects.create(muallif = muallif, dars_nomi= dn, qaysi_mavzu=mavzu, audio = dars_audio)
    mavzular = Mavzu.objects.all()
    darslar = Dars.objects.all()
    return render(request, 'darslar.html', {'mavzular':mavzular, 'darslar':darslar})


def ymq(request):
    if request.method == "POST":
        mn = request.POST['mavn']
        Mavzu.objects.create(mavzu=mn)
    return redirect('/api/darslar/')

####################### Darslar o'chirish ########################################

def darslar_ochirish(request):
    if request.method == 'POST':
        did = request.POST['did']

        d=Dars.objects.get(id = did)
        d.delete()
    return redirect('/api/darslar/')
####################### /Darslar  ########################################

####################### API  ########################################
####################### Namoz vaqti API  ########################################
class GetList(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        d = []
        for i in NamozVaqti.objects.all():
            b = {
                'sana':i.sana,
                'hafta_kuni':i.hafta_kuni.nomi,
                'tong':i.tong,
                'quyosh':i.quyosh,
                'peshin':i.peshin,
                'asr':i.asr,
                'shom':i.shom,
                'xufton':i.xufton
            }
            d.append(b)
        data = {
            'd':d,
        }
        return Response(data)


    def post(self, request):
        pass
####################### /Namoz vaqti API  ########################################

####################### Maruzalar API  ########################################
class MaruzalarApiView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        d = []
        maruzalar =  Maruzalar.objects.all()
       
        for i in maruzalar:
            m = {
                'maruza_nomi': i.maruza_nomi,
                'muallif': i.muallif,
                'maruza_audio':i.maruza_audio.url
            }
            d.append(m)
        data = {
            'd':d,
        }
        return Response(data)

####################### Mavzular API  ########################################
class MavzularApiView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        d = []
        mavzular = Mavzu.objects.all()
        for i in mavzular:
        
            m = {
                'id':i.id,
                'mavzu':i.mavzu,
            }
          
            d.append(m)
        data = {
            'd':d,
            
        }
        return Response(data)



####################### /darslar API  ########################################

class DarslarApiView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        darslar = Dars.objects.all()
        d = []
        print("darslar pip ")
        for i in darslar:
            m = {
                'qaysi_mavzu_id':i.qaysi_mavzu.id,
                'audio':i.audio.url,
            }
          
            d.append(m)
        data = {
            'd':d, 
        }
        return Response(data)




