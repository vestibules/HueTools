import os, json, requests, time, random
from dotenv import load_dotenv
load_dotenv()
token = os.getenv('TOKEN')
weatherToken = os.getenv('WEATHER_TOKEN')
url = 'http://192.168.1.22'
units = 'metric'
cityName = 'pau,fr'

switcher = {
300 : [0.31,0.31,100],  # Drizzle 	light intensity drizzle 
301 : [0.31,0.31,100],  # Drizzle 	drizzle 
302 : [0.31,0.31,100],  # Drizzle 	heavy intensity drizzle 
310 : [0.31,0.31,100],  # Drizzle 	light intensity drizzle rain 
311 : [0.31,0.31,100],  # Drizzle 	drizzle rain 
312 : [0.31,0.31,100],  # Drizzle 	heavy intensity drizzle rain 
313 : [0.31,0.31,100],  # Drizzle 	shower rain and drizzle 
314 : [0.31,0.31,100],  # Drizzle 	heavy shower rain and drizzle 
321 : [0.31,0.31,100],  # Drizzle 	shower drizzle 
500 : [0.31,0.31,70],   # Rain 	light rain 
501 : [0.31,0.31,70],   # Rain 	moderate rain 
502 : [0.31,0.31,70],   # Rain 	heavy intensity rain 
503 : [0.31,0.31,70],   # Rain 	very heavy rain 
504 : [0.31,0.31,70],   # Rain 	extreme rain 
511 : [0.31,0.31,70],   # Rain 	freezing rain 
520 : [0.31,0.31,70],   # Rain 	light intensity shower rain 
521 : [0.31,0.31,70],   # Rain 	shower rain 
522 : [0.31,0.31,70],   # Rain 	shower rain 
531 : [0.31,0.31,70],   # Rain 	ragged shower rain 
800 : [0.32,0.18,224],  # Clear 	clear sky 
801 : [0.26,0.32,150],  # Clouds 	few clouds: 11-25% 
802 : [0.31,0.31,150],  # Clouds 	scattered clouds: 25-50% 
803 : [0.31,0.31,100],  # Clouds 	broken clouds: 51-84% 
804 : [0.31,0.31,70]    # Clouds 	overcast clouds: 85-100% 
}

def getWeather():
    r = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={cityName}&appid={weatherToken}&units={units}")
    response = json.loads(r.content)
    print(response)
    currentWeather = response.get('weather')[0].get('main')
    currentDescription = response.get('weather')[0].get('description')
    weatherID = response.get('weather')[0].get('id')
    print(f'Météo en cours : {currentWeather} {currentDescription}.')
    if 'thunderstorm' in currentWeather.lower():
        return 'thunderstorm'
    else:
        return weatherID

def setThunder():
    print('Orage')
    x = 0.42
    y = 0.42
    number = random.randint(1,224)
    numberSleep = random.randint(1,10)
    color = {'xy' : [x,y]}
    brightness = {'bri' : number}
    response = requests.put(f'{url}/api/{token}/lights/5/state', json=color)
    print(response)
    response = response = requests.put(f'{url}/api/{token}/lights/5/state', json=brightness)
    print(response)
    time.sleep(numberSleep)

def setColor():
    if weather == 'thunderstorm':
        setThunder()
    else:
        if weather in switcher.keys():
            x = switcher.get(weather)[0]
            y = switcher.get(weather)[1]
            bri = switcher.get(weather)[2]
            color = {'xy' : [x,y]}
            brightness = {'bri' : bri}
            response = requests.put(f'{url}/api/{token}/lights/5/state', json=color)
            response = response = requests.put(f'{url}/api/{token}/lights/5/state', json=brightness)
            print(response)
            time.sleep(300)
        else:
            print('Météo non reconnue')


while True:
    weather = getWeather()
    setColor()

