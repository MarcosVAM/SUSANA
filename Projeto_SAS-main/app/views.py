from multiprocessing import context
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404

from django.contrib.auth.decorators import login_required


from django.urls import reverse_lazy

from app.models import Rua, Festival, Participante
from app.form import RuaForm, FestivalForm

from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.models import User

from customauth.models import MyUser
from customauth.forms import UserChangeForm

#bot e grafico
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import codecs
import os

# Create your views here.

#grafico

# parte do código do gráfico 
def grafico(request):
    pacote = {}
    vetor = []
    a = 0
    for i in range(27):
        for mes in range(12):
            df = pd.read_csv(f'C:/Users/marco/Documents/GitHub/susana-bot/teste/EstadosFinal/estado{i+1}/hipertensao_diabetes/mes'+str(mes+1)+'.csv', encoding="mbcs") 
            df2 = df.max()
            df3 = df2.max()
            dff = df3[-2::]
            vetor.append (dff)
            a  += 1
    pacote = {"chave": vetor}
    print(len(vetor))
    return render(request, 'grafico.html', pacote)

#funções do bot
def estados(nome,driver):
    botao =  driver.find_element("name", nome)
    botao.click()

def seleciona(request):
    return render(request, "selecionar.html")

def campo(id, index,driver):
    select_element = driver.find_element(By.ID,id)
    select_object = Select(select_element)
    select_object.select_by_index(index)


#selecionando o conteudo das tabelas
def selecionador(id, index, deselect,driver):
    select_element = driver.find_element(By.ID,id)
    select_object = Select(select_element)
    select_object.select_by_index(index)
#caso o select seja multiple colocar true
    if deselect:
       select_object.deselect_by_index(0)


#selecionar tabelade acordo com o index(so precisa mudar os numeros para mudar o conteudo baixado)


#clicar no botao


def clicker_by_name(nome,driver):    
    botao =  driver.find_element("name", nome)
    botao.click()


def bot(request, v1, v2):
    driver = webdriver.Chrome("chromedriver.exe")
    driver.get("https://datasus.saude.gov.br/acesso-a-informacao/hipertensao-e-diabetes-hiperdia/")
    for i in range(v2-v1):
        estados("radiobutton",driver)
        campo("mySelect", v1+i,driver)
        for col in range (3):
            if i == 3 or i == 22:
                break
            for con in range (4):
                for mes in range (12):
                    selecionador("L", 0, False,driver)
                    selecionador("C", (col+1), False,driver)       
                    if con == 0:   
                        selecionador("I", (con), False,driver) 
                    else:
                        selecionador("I", (con), True,driver)
                    if i+v1 == 1 or i+v1 == 4 or i+v1 == 17 or i+v1 == 20 or i+v1 == 22:
                        selecionador("A", (27+mes), True,driver)
                    elif i+v1 == 7:
                        selecionador("A", (7+mes), True,driver)
                    elif i+v1 == 23:
                        selecionador("A", (26+mes), True,driver)
                    else:
                        selecionador("A", (28+mes), True,driver)

                    time.sleep(1)   
                    clicker_by_name("mostre",driver)
                    time.sleep(1)
                    while True:
                        try:
                            driver.find_element(By.XPATH,"//tbody//tr//td[@class='botao_opcao']").click()
                            time.sleep(1)
                            break
                        except:
                            time.sleep(10)
                            driver.refresh()
                    time.sleep(4)
                    time.sleep(4)
                    driver.back()
                    driver.refresh()
        driver.get("https://datasus.saude.gov.br/acesso-a-informacao/hipertensao-e-diabetes-hiperdia/")



def home(request, LoginRequiredMixin):
    return render(request, LoginRequiredMixin, "index.html")


def Equipe(request):
    return render(request, "nossotime.html")
    

# VIEWS DE USUARIO (READ, CREATE, UPDATE, DELETE)#

def Lista_Ruas(request):    

    parametros = {"Ruas": Rua.objects.all()}

    return render(request, "TelaRuas.html", parametros)

@login_required(login_url='auth.login')
def Create_Ruas(request):   
    formRua = RuaForm(request.POST or None)
    form = {"FormRua": formRua}

    if formRua.is_valid():
        formRua.save()
        return redirect("/Ruas")
    
    return render(request, "FormRuas.html", form)

def Update_Ruas(request, pk):
    rua = Rua.objects.get(pk=pk)
    formRua = RuaForm(request.POST or None, instance=rua)

    if formRua.is_valid():
        formRua.save()
        return redirect('url_ruas')
        
    form = {"FormRua": formRua, "rua": rua}

    return render(request, 'FormRuas.html', form)

def Delete_Ruas(request, pk):
    rua = Rua.objects.get(pk=pk)
    rua.delete()
    return redirect('url_ruas')

def index (request):
    return render(request,'index.html')


def Lista_Festivais(request):    
    festivais = Festival.objects.all()
    participantes = Participante.objects.all()
    n_participantes = {}
    count = 0    
    for festival in festivais:        
        aux = 0
        for participante in participantes:
            if participante.festival.pk == festival.pk:
                aux += 1
        n_participantes[festival.nome] = aux
        count += 1

    parametros = {"Festivais": festivais, "participantes":participantes, "n_participantes":n_participantes}
    
    return render(request, "TelaFestivais.html", parametros)

@login_required(login_url='auth.login')
def Create_Festivais(request):   
    formFestival = FestivalForm(request.POST or None)
    form = {"FormFestival": formFestival}    
    if formFestival.is_valid():
        formFestival.instance.user = request.user
        formFestival.save()
        return redirect("/Festivais")
    
    return render(request, "FormFestivais.html", form)

@login_required(login_url='auth.login')
def Update_Festivais(request, pk):
    festival = Festival.objects.get(pk=pk)
    if festival.user.id != request.user.id:
        return redirect('url_festivais')
    formFestival = FestivalForm(request.POST or None, instance=festival)

    if formFestival.is_valid():
        formFestival.save()
        return redirect('url_festivais')
        
    form = {"FormFestival": formFestival, "festival": festival}

    return render(request, 'FormFestivais.html', form)

@login_required(login_url='auth.login')
def Delete_Festivais(request, pk):
    festival = Festival.objects.get(pk=pk)    
    if festival.user.id != request.user.id:
        return redirect('url_festivais')    
    festival.delete()
    return redirect('url_festivais')

@login_required(login_url='auth.login')
def Add_Participante(request, pk_festival):
    participante = Participante.objects.filter(user=request.user, festival=pk_festival)    
    if not participante:
        festival = Festival.objects.get(pk=pk_festival)
        if request.user != festival.user:
            novo_participante = Participante.objects.create(user=request.user, festival=festival)

            novo_participante.save()
            print(participante)
        
    return redirect('url_festivais')

@login_required(login_url='auth.login')
def edit_profile(request, pk):
    user = MyUser.objects.get(pk=pk)
    if user.id == request.user.id:
        form = UserChangeForm(request.POST or None, instance=user)
        if form.is_valid():
            form.save()
            return redirect('index')
        
        return render(request, 'edit_profile.html', {'form': form})
    return redirect('index')
    
        
