from bs4 import BeautifulSoup
from lxml import etree
import telegram
from telegram.ext import Updater, CommandHandler
import requests
import os
from datetime import datetime
import random

players_id_steam = { 'milo' : '76561198263879968',
                    'rasec' : '76561198019779413',
                    'pandita' : '76561199147714259',
                    'totti' : '76561198357625562',
                    'pio' : '76561198154629927',
                    'chris_smurf': '76561198951101503',
                    'chris_main' : '76561198088535072',
                    'rodrigo' : '76561199101841724',
                    'ItzyMidzyFlyHigh' : '76561198136076124',
                    'gianchanco' : '76561198219036947',
                    'diunlen' : '76561198268193098',
                    'pip' : '76561198281207106',
                    'huron_main' : '76561198337466376',
                    'huron_smurf' : '76561198973768345',
                    'cubito' : '76561198183606259'
           }

players_id_telegram = { '1457371380' : 'cubito',
                        '1411835674' : 'ItzyMidzyFlyHigh',
                        '1269814292' : 'chris_main',
                        '880584052' : 'milo',
                        '708266414' : 'huron_main',
                        '5212301885' : 'totti',
                        '1512302118' : 'gianchanco',
                        '1422908273' : 'pandita',
                        '689540859' : 'rasec',
                        '1512250438' : 'diunlen',
                        '1530257544' : 'pip'
}

lista_rangos = {    '1' : 'plata 1',
                    '2' : 'plata 2',
                    '3' : 'plata 3',
                    '4' : 'plata 4',
                    '5' : 'plata 5',
                    '6' : 'plata 6',
                    '7' : 'nova 1',
                    '8' : 'nova 2',
                    '9' : 'nova 3',
                    '10' : 'nova 4',
                    '11' : 'ak pelada',
                    '12' : 'ak laurel',
                    '13' : 'ak cruzada',
                    '14' : 'chapa',
                    '15' : 'águila desplumada',
                    '16' : 'águila laurel',
                    '17' : 'supreme',
                    '18' : 'global',
                    '19' : 'sin rango agg mrd'
           }

with open('.token') as file:
    token = file.readlines()
    file.close()

TOKEN = token[0].rstrip("\n")
grupo_id_numerico = token[4].rstrip("\n")


def sendMessage(chat_id, text):
    url = "https://api.telegram.org/bot"+TOKEN+"/sendMessage"
    parameters = {
    "chat_id": chat_id,
        "text": text
    }
    requests.get(url, data = parameters) 

def Etiquetar_a_todos(update,context):
    os.system('python3 ./etiquetar.py')

def Kbro_del_dia(update,context):
    now = datetime.now()
    semilla = int(str(now.year) + str(now.month) + str(now.day) + str(1))
    random.seed(semilla)
    lista_usuarios = list(players_id_telegram.items())
    numero = int(random.random()*len(lista_usuarios))
    if numero == len(lista_usuarios):
        numero -= 1
    Kbro_escogido = lista_usuarios[numero]
    nombre_escogido = Kbro_escogido[1]
    sendMessage(grupo_id_numerico,"El Rosquete del día es: "+nombre_escogido)

def Obtener_Stats(numero_partidas=-1):
    with open("data.txt","r") as data:
        soup = BeautifulSoup(data, 'lxml')
        data.close()
    dom = etree.HTML(str(soup))
    kills = dom.xpath('//tr[@class="p-row js-link"]/td[7]')
    muertes = dom.xpath('//tr[@class="p-row js-link"]/td[8]')
    headshots = dom.xpath('//tr[@class="p-row js-link"]/td[11]')
    adr = dom.xpath('//tr[@class="p-row js-link"]/td[12]')
    mapas = dom.xpath('//tr[@class="p-row js-link"]/td[3]/img/@alt')
    try:
        rango = lista_rangos[str(dom.xpath('//tr[@class="p-row js-link"][1]/td[5]/img/@src')[0])[41:43]]
    except:
        rango = lista_rangos['19']
    suma_kd=0
    suma_adr=0
    suma_headshots=0
    if numero_partidas == -1:
        numero_partidas = len(kills)
    for i in range(numero_partidas):
        if (int(muertes[i].text) == 0):
            muerte = 1
        else:
            muerte = int(muertes[i].text)
        suma_kd = suma_kd + int(kills[i].text)/muerte
        suma_adr = suma_adr + int(adr[i].text)
        suma_headshots = suma_headshots + int(headshots[i].text)

    kd_stat = round(float((suma_kd/numero_partidas)),2)
    adr_stat = int((suma_adr/numero_partidas))
    headshot_stat = int((suma_headshots/numero_partidas))
    mapa_mas_jugado = max(set(mapas), key=mapas.count)
    stats = "\nkd: "+str(kd_stat) + "\nadr: "+str(adr_stat)+"\nhs: "+str(headshot_stat)+"\nrango: "+rango+"\nmapa main: "+mapa_mas_jugado
    return stats

def CrearCreatorjs(user_id):
    string1 = """
    var page = require("webpage").create();
    page.open("""
    url = "https://csgostats.gg/player/"+user_id+"#/matches"
    string2 = """
        , function(status){
        if (status == "success") {
            console.log("The title of the page is: "+ page.title);
            var data = page.content
            console.log(data)

        }page.close();
        phantom.exit();
    })"""
    with open("creator.js","w") as file:
        file.write(string1+'"'+url+'"'+string2)

def Mostrar_stats(update,context):
    bandera = 0
    try:
        usuario = str(update.message["text"].split(" ")[1])
        bandera = 1
    except:
        usuario = players_id_telegram[str(update.effective_user["id"])]
        user_id = players_id_steam[players_id_telegram[str(update.effective_user["id"])]]
        sendMessage(grupo_id_numerico,"Obteniendo estadísticas de: "+usuario)
    if bandera ==1:
        try: 
            user_id = players_id_steam[usuario]
            bandera = 0
        except:
            sendMessage(grupo_id_numerico,"No busques mamadas Mary Jane.jpg")
            bandera = 1
    if bandera ==0:    
        CrearCreatorjs(user_id)
        os.system('echo $SLIMERJSLAUNCHER > prueba.txt')
        os.system('./slimerjs_folder/slimerjs --headless creator.js > data.txt')
        try:
            p_numero_partidas = int(update.message["text"].split(" ")[2])
            text = usuario+" stats: "+Obtener_Stats(p_numero_partidas)
        except:
            text = usuario+" stats: "+Obtener_Stats()
    
        sendMessage(grupo_id_numerico,text)

if __name__ == "__main__":
    my_bot = telegram.Bot(token = TOKEN)

updater = Updater(my_bot.token, use_context=True)

dp = updater.dispatcher


#Creamos los manejadores
dp.add_handler(CommandHandler("stats", Mostrar_stats))
dp.add_handler(CommandHandler("all", Etiquetar_a_todos))
dp.add_handler(CommandHandler("kbro", Kbro_del_dia))

updater.start_polling()

updater.idle()
