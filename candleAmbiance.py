import os, json, requests, pprint, random, time
from dotenv import load_dotenv
load_dotenv()
token = os.getenv('TOKEN')
url = 'http://192.168.1.22'
BulbsID = []

class bulb:
    bulbType = 'filament bulb'
    def __init__(self,someInteger):
        self.numId = someInteger
        self.name = self.getName()
        self.state = self.getState()
        self.brightness = self.getBrightness()
    def getName(self):
        r = requests.get(f'{url}/api/{token}/lights/{self.numId}')
        response = json.loads(r.content)
        self.name = response.get('name')
        return self.name
    def getState(self):
        r = requests.get(f'{url}/api/{token}/lights/{self.numId}')
        response = json.loads(r.content)
        self.state = response.get('state').get('on')
        return self.state
    def getBrightness(self):
        r = requests.get(f'{url}/api/{token}/lights/{self.numId}')
        response = json.loads(r.content)
        self.brightness = response.get('state').get('bri')
        return self.brightness
    def setBrightness(self,brightnessLevel):
        data = {'bri' : brightnessLevel}
        requests.put(f'{url}/api/{token}/lights/{self.numId}/state', json=data)
    def powerOn(self):
        data = {'on' : True}
        requests.put(f'{url}/api/{token}/lights/{self.numId}/state', json=data)
    def powerOff(self):
        data = {'on' : False}
        requests.put(f'{url}/api/{token}/lights/{self.numId}/state', json=data)

def displayBulbs():
    name = 'name'
    r = requests.get(f'{url}/api/{token}/lights')
    response = json.loads(r.content)
    pprint.pprint(response)
    for key, value in response.items():
        if 'filament' in value.get('productname'):
            print(f'{key} : {value.get(name)}')

def choiceOfBulbs():
    global BulbsID
    print('Choisir les ampoules à inclure (laisser vide pour quitter) :')
    choice = input()
    if choice:
        BulbsID.append(choice)
        return choiceOfBulbs()

def bulbsInit(ListOfBulbs):
    result = []
    for bulbID in ListOfBulbs:
       result.append(bulb(bulbID))
    return result


displayBulbs() # Affichage des ampoules de type filament
choice = choiceOfBulbs() # Choix des ampoules puis envoi dans un array
listOfObjects = bulbsInit(BulbsID) # Instanciation des objets de type bulb


for bulbObject in listOfObjects: # On récupère l'état de l'ampoule avec la méthode GetState() et on allume les bougies avec PowerOn() si elles sont éteintes
    if not bulbObject.getState():
        bulbObject.powerOn()
        print(f'Allumage de {bulbObject.name}')

try :
    while True: 
        for bulbObject in listOfObjects:
            randomTimer = round(random.uniform(0.1,3), 1)
            randomBrightnessLevel = random.randint(1,100)
            print(f'{bulbObject.name} : luminosité à {randomBrightnessLevel} pour {randomTimer} secondes.')
            bulbObject.setBrightness(randomBrightnessLevel)
            time.sleep(randomTimer)
except KeyboardInterrupt:
    for bulbObject in listOfObjects:
        bulbObject.powerOff()
    print('Extinction des bougies ...')
            



    
