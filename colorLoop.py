import os, json, requests, time, random
from dotenv import load_dotenv
load_dotenv()
token = os.getenv('TOKEN')
url = 'http://192.168.1.22'

choiceList = []
colorBulbObjList = []

class colorBulb:
    bulbType = 'colorBulb'

    def __init__(self,listOfValues):
        self.numId = listOfValues[0]
        self.name = listOfValues[1]
        self.product = listOfValues[2]
        self.state = self.getState()

    def getState(self):
        r = requests.get(f'{url}/api/{token}/lights/{self.numId}')
        response = json.loads(r.content)
        self.state = response.get('state').get('on')
        return self.state


def displayColorLights():
    name = 'name'
    r = requests.get(f'{url}/api/{token}/lights')
    response = json.loads(r.content)
    print('Liste des ampoules à variation de couleur disponibles :')
    for k in response.keys():
        state = response.get(k).get('state')
        if 'xy' in state:
            print(f'id #{k} : {response.get(k).get(name)}')

def colorBulbChoice():
        global choiceList
        global colorBulbObjList
        x = 0
        print('Choisir une ampoule (laisser vide pour terminer)')
        choice = input()
        if choice:
            choiceList.append(choice)
            return colorBulbChoice()
        else:
            for i in choiceList:
                valueList = []
                r = requests.get(f'{url}/api/{token}/lights/{i}')
                response = json.loads(r.content)
                stateDic = response.get('state')
                bulbName = response.get('name')
                bulbProductName = response.get('productname')
                valueList.append(i)
                valueList.append(bulbName)
                valueList.append(bulbProductName)
                for v in stateDic.values():
                    valueList.append(v)
                colorBulbObjList.append(colorBulb(valueList))
                print(f'Ampoule {colorBulbObjList[x].name} créée !')
                x += 1

def checkIfAlive(listofObjects):
    for i in listofObjects:
        if not i.state:
            print(f'{i.name} est éteinte ... allumage en cours ...')
            data = {'on' : True}
            response = requests.put(f'{url}/api/{token}/lights/{i.numId}/state', json=data)
            print(response.json())

def colorLoop(listofObjects):
    print('A quel intervalle changer de couleur ? (minutes)')
    interval = int(input())
    for i in listofObjects:
        print(f'A partir de maintenant, {i.name} changera de teinte toutes les {interval} minutes.')
    interval = interval * 60
    #x = 0
    #y = 0
    while True:
        checkIfAlive(listofObjects)
        x = random.random() 
        y = random.random()
        data = {'xy' : [x,y]}
        for i in listofObjects:
            response = requests.put(f'{url}/api/{token}/lights/{i.numId}/state', json=data)
            print(response.json())
            time.sleep(interval)

def sequencedLoop(listofObjects):
    print('A quel intervalle changer de couleur ? (secondes)')
    interval = int(input())
    for i in listofObjects:
        print(f'A partir de maintenant, {i.name} changera de teinte toutes les {interval} secondes.')
    while True:
        checkIfAlive(listofObjects)
        for a in range(10):
            for b in range(10):
                x = 0 + (a/10)
                y = 0 + (b/10)
                x = round(x,1)
                y = round(y,1)
                data = {'xy' : [x,y]}
                for i in listofObjects:
                    response = requests.put(f'{url}/api/{token}/lights/{i.numId}/state', json=data)
                    print(response.json())
                time.sleep(interval)
            for b in range(10):
                y = 1 - (b/10)
                y = round(y,1)
                data = {'xy' : [x,y]}
                for i in listofObjects:
                    response = requests.put(f'{url}/api/{token}/lights/{i.numId}/state', json=data)
                    print(response.json())
                time.sleep(interval)
        for a in range(10):
            for b in range(10):
                x = 1 - (a/10)
                y = 1 - (b/10)
                x = round(x,1)
                y = round(y,1)
                data = {'xy' : [x,y]}
                for i in listofObjects:
                    response = requests.put(f'{url}/api/{token}/lights/{i.numId}/state', json=data)
                    print(response.json())
                time.sleep(interval)
            for b in range(10):
                y = 0 + (b/10)
                y = round(y,1)
                data = {'xy' : [x,y]}
                for i in listofObjects:
                    response = requests.put(f'{url}/api/{token}/lights/{i.numId}/state', json=data)
                    print(response.json())
                time.sleep(interval)

def modeChoice():
    print('Choisir un mode :')
    print('''1 : Varier aléatoirement.
2 : Varier de façon séquencée.
''')
    choice = input()
    if choice == '1':
        return colorLoop(colorBulbObjList)
    else:
        return sequencedLoop(colorBulbObjList)
        
displayColorLights()
choiceBulb = colorBulbChoice()
try:
    mode = modeChoice()
except KeyboardInterrupt:
    print('Equipement de retour en mode couleur statique.')
