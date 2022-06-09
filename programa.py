#from bs4 import BeautifulSoup
#import undetected_chromedriver as uc
from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager


service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

#driver = uc.Chrome()
owo = driver.get('https://csgostats.gg/player/76561198263879968#/matches')

#html = driver.page_source
print(owo)


def ObtenerKD():
    kills = []
    with open("kills.txt","r") as archivo:
        for linea in archivo:
            kills.append(linea)
    archivo.close()
    muertes = []
    with open("muertes.txt","r") as archivo:
        for linea in archivo:
            muertes.append(linea)
    archivo.close()
    contador = 0
    suma = 0
    for i in range(len(kills)):
        #print(int(kills[i])/int(muertes[i]))
        suma += int(kills[i])/int(muertes[i])
        contador +=1
        if contador ==29:
            break
    print(suma/30)
