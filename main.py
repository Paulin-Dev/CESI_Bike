from serial import Serial, PARITY_EVEN, STOPBITS_ONE, SEVENBITS
import json
from datetime import datetime
from operators_status import get_items_in_production, check
from os import system


RESET = '\x1b[0m'
RED = '\x1b[1;31;40m'
BLUE = '\x1b[1;34;40m'
GREEN = '\x1b[1;32;40m'
YELLOW = '\x1b[1;33;40m'


# Il faut vérifier que les ports correspondent aux bons arduino

try:
    # arduino auto : poste 1 / poste 2 / poste 4 / poste 6
    serial_1 = Serial(port="COM6", timeout=1, baudrate=9600, parity=PARITY_EVEN, stopbits=STOPBITS_ONE, bytesize=SEVENBITS)
except:
    serial_1 = None

try:
    # arduino poste 5
    serial_2 = Serial(port="COM3", timeout=1, baudrate=9600, parity=PARITY_EVEN, stopbits=STOPBITS_ONE, bytesize=SEVENBITS)
except:
    serial_2 = None

try:  
    # arduino poste 3
    serial_3 = Serial(port="COM5", timeout=1, baudrate=9600, parity=PARITY_EVEN, stopbits=STOPBITS_ONE, bytesize=SEVENBITS)
except:
    serial_3 = None

# dictionnaire contenant l'heure de début de fabrication d'un sous-ensemble pour chaque poste
timers = {}

def reset_json():
    ''' réinitialise le contenu du fichier data.json '''
    with open("data.json", "w") as f:
        d = {"poste_1": {}, "poste_2": {}, "poste_3": {}, "poste_4": {}, "poste_5": {}, "poste_6": {}}
        json.dump(d, f, indent=1)

def clear_logs():
    ''' efface le contenu du fichier logs.txt '''
    with open("logs.txt", "w") as f:
        f.write("")

def add_to_json(data):
    ''' ajoute un sous-ensemble pour un certain poste dans le fichier data.json '''
    with open("data.json", "r+") as f:
        content = json.load(f)
        f.truncate(0)
        f.seek(0)
        count = len(content[f"poste_{data['poste']}"])+1
        content[f"poste_{data['poste']}"][f"sous_ensemble_{count}"] = data["time_elapsed"]
        json.dump(content, f, indent=1)


def filter_info(data):
    ''' si la led verte s'allume, ajout de l'heure de début pour un certain poste dans le dictionnaire timers
    si la led verte s'éteint, calcul du temps écoulé pendant la fabrication et ajout dans la base de données'''
    if data["color"] == "green":
        if data["state"] == "on":
            timers[data["poste"]] = datetime.now()
        else:
            add_to_json({"poste": data["poste"], "time_elapsed": (datetime.now()-timers[data["poste"]]).total_seconds()})


old_display = None
def data_treatment(data: dict):
    ''' transmission des actions à effectuer par les arduino '''
    global old_display
    # envoie le nombre d'encours sur le poste 4 à l'arduino auto pour qu'il l'affiche
    if data["display"] != old_display and data["display"]:
        if data["display"] < 0:
            data["display"] = 0
        to_send = f'{data["display"]}'
        send_data(serial_1, to_send)
        old_display = data["display"]

    # envoie 3 caracteres (numéro du poste, premiere lettre de la couleur de la led, futur état de la led : A (allumer) ou E (éteindre))
    # aux arduino afin de changer l'état des leds

    # Allumer led bleue
    if data["go_help"] is not None:
        if data["go_help"] == "poste_5":
            send_data(serial_2, "5BA")
        elif data["go_help"] == "poste_3":
            send_data(serial_3, "3BA")
        else:
            send_data(serial_1, f'{data["go_help"][-1]}BA')

    # Eteindre led bleue
    if data["stop_help"] is not None:
        if data["stop_help"] == "poste_5":
            send_data(serial_2, "5BE")
        elif data["stop_help"] == "poste_3":
            send_data(serial_3, "3BE")
        else:
            send_data(serial_1, f'{data["stop_help"][-1]}BE')
    
    # Allumer led rouge
    if data["need_help"] is not None:
        if data["need_help"] == "poste_5":
            send_data(serial_2, "5RA")      
        elif data["need_help"] == "poste_3":
            send_data(serial_3, "3RA")
        else:
            send_data(serial_1, f'{data["need_help"][-1]}RA')

    # Eteindre led rouge
    if data["no_need_help"] is not None:
        if data["no_need_help"] == "poste_5":
            send_data(serial_2, "5RE")    
        elif data["no_need_help"] == "poste_3":
            send_data(serial_3, "3RE")
        else:
            send_data(serial_1, f'{data["no_need_help"][-1]}RE')
            
        
def send_data(ser: Serial, string: str):
    ''' envoie un ou des caracteres à un arduino'''
    if ser is not None:
        ser.write(string.encode('utf-8'))
    else:
        print("Erreur: le port est occupé / non connecté")


reset_json()
clear_logs()
system('cls')

while True:
    # Récupération infinie des données envoyées par les arduino
    for ser in [serial_1, serial_2, serial_3]:
        if ser is not None:
            output = str(ser.readline())[2:-5]
            if output != "" and output != "{}":
                filter_info(json.loads(output))

    # Envoi de données losqu'un poste a besoin d'aide
    data_treatment(check())

    # Récupération du nombre de sous-ensembles pour chaque poste et affichage
    stocks = get_items_in_production()
    print(f'\rPoste 1: {YELLOW}{stocks["poste_1"]}{RESET}, Poste 2: {YELLOW}{stocks["poste_2"]}{RESET}, Poste 3: {YELLOW}{stocks["poste_3"]}{RESET}, Poste 4: {YELLOW}{stocks["poste_4"]}{RESET}, Poste 5: {YELLOW}{stocks["poste_5"]}{RESET}, Poste 6: {YELLOW}{stocks["poste_6"]}{RESET} ', end='')

