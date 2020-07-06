import os, json, requests, pprint, random, time # Importation de diverses librairies
from dotenv import load_dotenv                  # Importation de dotenv pour gérer les fichiers .env
load_dotenv()                                   # Chargement du fichier .env
token = os.getenv('TOKEN')                      # Stockage dans 'token' de la valeur de 'TOKEN' présent dans le fichier .env
url = 'http://192.168.1.22'                     # Url pour les requêtes à l'APi (@IP du Philips Hue Bridge)
BulbsID = []                                    # Déclaration d'un array où seront stockés les ID des ampoules choisies

class bulb:                                     # Définition d'une classe 'Bulb'
    bulbType = 'filament bulb'                  # Définition d'un attribut de classe 'BulbType'
    def __init__(self,someInteger):             # Définition des attributs uniques à chaque objet de classe 'Bulb' (un paramètre ID sera requis lors de l'instanciation de l'objet)
        self.numId = someInteger                # Chaque objet aura un id défini par l'ID envoyé en paramètre       
        self.name = self.getName()              # Chaque objet aura un nom récupéré grâce à la méthode de class 'Bulb' GetName()
    def getName(self):                                                   # Définition de la méthode de classe 'Bulb' GetName()
        r = requests.get(f'{url}/api/{token}/lights/{self.numId}')       # Requête HTTP GET à l'API pour récupérer les infos de l'ampoule suivant son ID unique
        response = json.loads(r.content)                                 # Utilisation de la librairie JSON pour convertir le json en dictionnaire python
        self.name = response.get('name')                                 # Le nom de l'ampoule est égal à la valeur de la clé 'name' renvoyé par le json
        return self.name                                                 # Retourne la valeur de self.name (à destination de l'attribut name)
    def setBrightness(self,brightnessLevel):                                        # Définition de la méthode de classe 'Bulb' SetBrightness(), permet de modifier la valeur du champ 'bri' de chaque ampoule, nécessite une valeur de luminosité en paramètre
        data = {'bri' : brightnessLevel}                                            # Stockage dans data du body de la requête POST
        requests.put(f'{url}/api/{token}/lights/{self.numId}/state', json=data)     # Exécution de la requête POST
    def powerOn(self):                                                              # Définition de la méthode de classe 'Bulb' PowerOn()
        data = {'on' : True}                                                        # Stockage dans data du body de la requête POST
        requests.put(f'{url}/api/{token}/lights/{self.numId}/state', json=data)     # Exécution de la requête POST
    def powerOff(self):                                                             # Définition de la méthode de classe 'Bulb' PowerOff()
        data = {'on' : False}                                                       # Stockage dans data du body de la requête POST
        requests.put(f'{url}/api/{token}/lights/{self.numId}/state', json=data)     # Exécution de la requête POST
    def getState(self):                                                             # Définition de la méthode de classe 'Bulb' GetState(), permet de connaitre état on/off de l'ampoule
        r = requests.get(f'{url}/api/{token}/lights/{self.numId}')                  # Requête HTTP GET à l'API pour récupérer les infos de l'ampoule suivant son ID unique
        response = json.loads(r.content)                                            # Utilisation de la librairie JSON pour convertir le json en dictionnaire python
        self.state = response.get('state').get('on')                                # L'état de l'ampoule est égal à la valeur de la clé 'on', dans la clé 'state' (renvoie un Booléen)
        return self.state                                                           # Retourne le booléen
    def candle(self):                                                               # Définition de la méthode de classe 'Bulb' Candle()
        randomTimer = round(random.uniform(0.1,3), 1)                               # Définition d'un float aléatoire à une décimale
        randomBrightnessLevel = random.randint(1,100)                               # Définition d'une luminosité aléatoire entre 1 et 100
        print(f'{self.name} : luminosité à {randomBrightnessLevel} pour {randomTimer} secondes.')
        bulbObject.setBrightness(randomBrightnessLevel)                             # Appel de la méthode de classe 'Bulb' SetBrightness() pour régler la luminosité de l'ampoule
        time.sleep(randomTimer)                                                     # Pause pour simuler temps de variation de la flamme

def displayBulbs():                                 # Fonction qui affiche les ampoules de type 'filament'
    name = 'name'
    r = requests.get(f'{url}/api/{token}/lights')   # requête à l'API de type GET pour récupérer la liste des ampoules
    response = json.loads(r.content)                # Utilisation de la librairie JSON pour convertir le json en dictionnaire python
    #pprint.pprint(response)
    for key, value in response.items():             # Pour chaque élément du dictionnaire
        if 'filament' in value.get('productname'):  # Si la string 'filament' est présente dans le nom du produit,
            print(f'{key} : {value.get(name)}')     # affichage de l'ampoule et de son ID

def choiceOfBulbs():            # Fonction qui permet de choisir les ampoules à intégrer dans le cycle
    global BulbsID              # L'ID des ampoules sera stocké dans un array
    print('Choisir les ampoules à inclure (laisser vide pour quitter) :')
    choice = input()
    if choice:                  # Si une ampoule est choisie,
        BulbsID.append(choice)  # Stockage de l'ID dans l'array BulbsID
        return choiceOfBulbs()  # Fonction itérative, elle s'appelle elle - même tant qu'une ampoule est choisie, fin de l'itération si rien n'est entré dans l'input

def bulbsInit(ListOfBulbs):         # Fonction d'instanciation des objets de classe 'Bulb'
    result = []                     # Les objets seront stockés localement dans un array
    for bulbID in ListOfBulbs:      # Pour chaque ID stocké dans l'array en paramètre
       result.append(bulb(bulbID))  # Instanciation d'un objet de classe 'Bulb' dont l'ID est l'ID itéré
    return result                   # On retourne l'array avec les objets stockés

    ###### Début Algo ######

displayBulbs()                      # Affichage des ampoules de type filament
choice = choiceOfBulbs()            # Choix des ampoules, fonction itérative pour sélectionner une ou plusieurs ampoules (permet d'éviter l'emploi d'une boucle)
listOfObjects = bulbsInit(BulbsID)  # Instanciation des objets de type bulb puis stockage des objets dans listOfObjects


for bulbObject in listOfObjects:    # On récupère l'état de l'ampoule de classe 'bulb' avec la méthode GetState() et on allume les bougies avec PowerOn() si elles sont éteintes
    if not bulbObject.getState():   # Si GetState() est Falsy
        bulbObject.powerOn()        # Appel de la méthode de classe 'Bulb' powerOn()
        print(f'Allumage de {bulbObject.name}')

try :                                                       # Utilisation de try/except pour gérer la sortie manuelle de la boucle
    while True:                                             # Création d'une boucle infinie
        for bulbObject in listOfObjects:                    # Pour chaque objet de classe 'Bulb' stocké dans l'array
            bulbObject.candle()                             # Utilisation de la méthode de classe 'Bulb' Candle()
except KeyboardInterrupt:                                   # Ctrl + C génère une exception de type 'KeyboardInterrupt' et sort de la boucle
    for bulbObject in listOfObjects:                        # Pour chaque objet de classe 'bulb' stocké dans l'array,
        bulbObject.powerOff()                               # Appel de la méthode de classe 'Bulb' PowerOff() pour éteindre l'ampoule
    print('Extinction des bougies ...')

    ###### Fin Algo ######
            



    
