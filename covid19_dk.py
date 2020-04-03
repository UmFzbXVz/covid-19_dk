#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import urllib.request
import time
import datetime
from datetime import date, datetime
import os
from bs4 import BeautifulSoup

class bcolors: #Class til farvning af tekst
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

headers = {'User-Agent': 'Mozilla/5.0'}
sst_url = 'https://www.sst.dk/da/corona/tal-og-overvaagning'
ssi_url = 'https://www.ssi.dk/aktuelt/sygdomsudbrud/coronavirus'
rapportsamling = 'https://www.ssi.dk/aktuelt/sygdomsudbrud/coronavirus/covid-19-i-danmark-epidemiologisk-overvaagningsrapport'

def getSoupFromURL(url):
    return BeautifulSoup(requests.get(url, headers = headers).text, "lxml")

def intify(input):
    if isinstance(input, int):
        return input
    return int(input.replace(u'\xa0', u'').replace('.',''))

def printStats(smittede, testede, doede, raske, tid):
    os.system('cls' if os.name == 'nt' else 'clear') #Laver "clear" command i Terminal
    print(bcolors.UNDERLINE + tid + bcolors.ENDC)
    print("Testet: \t", bcolors.BOLD + testede + bcolors.ENDC)
    print("Smittet: \t", bcolors.WARNING + bcolors.BOLD + smittede + bcolors.ENDC)
    print("Raske: \t\t", bcolors.OKGREEN + bcolors.BOLD + raske + bcolors.ENDC)
    print("Døde: \t\t", bcolors.FAIL + bcolors.BOLD + doede + bcolors.ENDC + "(" + str( round(intify(doede)/(intify(raske)+intify(doede))*100, 2) ) + "%)") #Divider døde med samlet antal afsluttede sygdomsforløb


def statens_seruminstitut():
    soup = getSoupFromURL(ssi_url)
    table = soup.find("div", {"class" : "table table-responsive table-striped table-hover table-borderless"}).find("tbody").findAll("tr")[0].findAll("td") #Table der indeholder data for Danmark
    personer_testet_i_danmark = table[1].find(text=True) #Antal testede i Danmark
    personer_smittet_i_danmark = table[2].find(text=True) #Antal smittede i Danmark
    personer_raske_i_danmark = table[3].find(text=True) #Antal raskmeldte i Danmark
    personer_doede_i_danmark = table[4].find(text=True) #Antal døde i Danmark
    #updateTimestamp = soup.findAll('p')[3].find(text=True) #Tidspunkt for sidste opdatering af hjemmesiden
    updateTimestamp = str(datetime.now().strftime("%d. %B kl. %H:%M"))

    printStats(personer_smittet_i_danmark, personer_testet_i_danmark, personer_doede_i_danmark, personer_raske_i_danmark, updateTimestamp + " " + dagligRapport())
    return

def dagligRapport():
    try:
        text = "(R)"
        dagligtLink = getSoupFromURL(rapportsamling).find('body', {'class': 'theme-rusty-red'}).find('div', {'id' : 'top'}).find('div', {'class:', 'main-content'}).find('section', {'class': 'rte w-max'}).find('blockquote', {'class': 'factbox'}).findAll('a', href=True)[1]['href']
        if requests.get(rapport_url, headers = headers).status_code == 200:
            return(f"\u001b]8;;{rapport_url}\u001b\\{text}\u001b]8;;\u001b\\") #Klikbart link til dagens rapport
        if date.today().strftime("%d%m%Y") in dagligtLink:
            return(f"\u001b]8;;{dagligtLink}\u001b\\{text}\u001b]8;;\u001b\\")
        else:
            return ''
    except:
        return ''

while True:
    starttime = time.time() #Bruges til at hente nyeste information hver 60. sekund
    rapport_url = 'https://files.ssi.dk/COVID19-overvaagningsrapport-' + date.today().strftime("%d%m%Y") #Opdaterer linket til DD når programmet kører fra før til efter midnat
    try:
        statens_seruminstitut() #Opdatér globale variable med nyeste statistikker
    except Exception as e:
        print(e)
        now = datetime.now()
        print("[!] " + str(now.hour).strip() + "." + str(now.minute).strip() + ": Kunne ikke hente statistikkerne. Prøver igen om lidt..")
    time.sleep(60.0 - ((time.time() - starttime) % 60.0)) #Re-download nyeste data efter 60 sekunder
