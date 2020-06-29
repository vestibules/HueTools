import os, json, requests
from dotenv import load_dotenv
load_dotenv()
token = os.getenv('TOKEN')
url = 'http://192.168.1.22'

def displayLights():
    name = 'name'
    r = requests.get(f'{url}/api/{token}/lights')
    response = json.loads(r.content)
    print(response)
    print('Liste des éléments disponibles :')
    for k in response.keys():
        state = response.get(k).get('state')
        power = state.get('on')
        bright = state.get('bri')
        if power:
            stateMsg = 'Allumée'
        else:
            stateMsg = 'Eteinte'
        print(f'{k} : {response.get(k).get(name)}. {stateMsg}. Luminosité : {bright}.')

def selectBulb():
    print('Choisir quelle ampoule ?')
    idBulb = input()
    return idBulb

def menuBulb(bulb):
    print('Que souhaitez vous faire ?')
    print(f'''1 : Allumer l'ampoule.
2 : Eteindre l'ampoule. 
3 : Changer la luminosité.''')
    choice = input()
    if choice == '1':
        return switchOnLight(bulb)
    elif choice == '2':
        return switchOffLight(bulb)
    else:
        return setBrightness(bulb)
def switchOffLight(bulb):
    data = {'on' : False}
    response = requests.put(f'{url}/api/{token}/lights/{bulb}/state', json=data)
    print(response.json())

def switchOnLight(bulb):
    data = {'on' : True}
    response = requests.put(f'{url}/api/{token}/lights/{bulb}/state', json=data)
    print(response.json())

def setBrightness(bulb):
    print('Entrer un niveau de luminosité (1 - 254) :')
    brightness = int(input())
    data = {'bri' : brightness}
    response = requests.put(f'{url}/api/{token}/lights/{bulb}/state', json=data)
    print(response.json())


displayLights()
bulb = selectBulb()
action = menuBulb(bulb)
