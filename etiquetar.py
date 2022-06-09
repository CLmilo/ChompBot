from telethon import TelegramClient
import requests

with open('.token') as file:
    token = file.readlines()
    file.close()

lista_usuarios_id =[]
lista_usuarios_nombre =[]
TOKEN = token[0].rstrip("\n")
api_id = token[1].rstrip("\n")
api_hash = token[2].rstrip("\n")
grupo_id_publico = token[3].rstrip("\n")
grupo_id_numerico = token[4].rstrip("\n")

client = TelegramClient('owo', api_id, api_hash).start()

users = client.iter_participants(grupo_id_publico)

for user in users:
    if str(user.bot).strip() == "False":
        lista_usuarios_id.append(user.id)
        lista_usuarios_nombre.append(user.first_name)
        print(str(user.id) + user.first_name)

texto = ""
for i in range(len(lista_usuarios_id)):
    texto = texto + "["+lista_usuarios_nombre[i]+"](tg://user?id="+str(lista_usuarios_id[i])+") "
url = "https://api.telegram.org/bot"+TOKEN+"/sendMessage"
parameters = {
    "chat_id": grupo_id_numerico,
    "text": texto,
    "parse_mode": "MarkdownV2"
}
requests.get(url, data = parameters) 