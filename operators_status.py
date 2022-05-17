import json

# True : Active les logs, False : Desactive les logs
VERBOSE = True

def open_file() -> dict:
    ''' Ouvre le fichier data.json et renvoie son contenu dans un dictionnaire '''
    with open('data.json', 'r') as f:
        return json.load(f)

def add_to_logs(line: str) -> None:
    ''' ajoute une ligne de texte dans le fichier logs.txt '''
    with open('logs.txt', 'r+') as f:
        content = f.read()
        f.seek(0)
        f.truncate()
        content += f'\n{line}'
        f.write(content)

def get_items_in_production(data: dict = None) -> dict:
    ''' renvoie un dictionnaire avec comme clés les postes et comme valeurs le nombre total de sous-ensemble fabriqués '''
    if data is None:
        data = open_file()
    operators_items = {}
    for key, val in data.items():
        operators_items[key] = len(val)
    return dict(sorted(operators_items.items(), key = lambda x: operators_items[x[0]], reverse=True))

def get_mean(poste: dict) -> int:
    ''' renvoie la moyenne des valeurs d'un dictionnaire '''
    return sum(poste.values())/len(poste.values()) if len(poste.values()) != 0 else 0

def check_dependencies(operators_items: dict) -> tuple:
    ''' vérifie que le poste le plus rapide n'a pas besoin de fabriquer un nouveau sous-ensemble pour celui qui dépend de ce dernier,
    et qu'il peut donc aller aider le poste le plus lent 
    sinon, le 2eme plus rapide devient le plus rapide et ainsi de suite '''
    fastest_index = 0
    fastest_operator = (list(operators_items.keys())[fastest_index], list(operators_items.values())[fastest_index]) # tuple (operator number, items in prod)
    
    for i in range(3):
        if fastest_operator[0] == "poste_3" and get_stock_poste_4_from_3(operators_items) < 2:
            fastest_index += 1
            fastest_operator = (list(operators_items.keys())[fastest_index], list(operators_items.values())[fastest_index])
        elif fastest_operator[0] == "poste_2" and get_stock_poste_4_from_2(operators_items) < 2:
            fastest_index += 1
            fastest_operator = (list(operators_items.keys())[fastest_index], list(operators_items.values())[fastest_index])
        elif fastest_operator[0] == "poste_1" and get_stock_poste_2_from_1(operators_items) < 2:
            fastest_index += 1
            fastest_operator = (list(operators_items.keys())[fastest_index], list(operators_items.values())[fastest_index])
        elif fastest_operator[0] == "poste_4" and get_stock_poste_6_from_4(operators_items) < 2:
            fastest_index += 1
            fastest_operator = (list(operators_items.keys())[fastest_index], list(operators_items.values())[fastest_index])
        elif fastest_operator[0] == "poste_5" and get_stock_poste_6_from_5(operators_items) < 2:
            fastest_index += 1
            fastest_operator = (list(operators_items.keys())[fastest_index], list(operators_items.values())[fastest_index])
    return fastest_operator

def who_needs_help(data: dict, operators_items: dict) -> tuple:
    ''' compare le nombre de sous-ensembles entre le poste le plus rapide et le poste le plus lent,
    si la différence est trop importante ( >= 2)
    renvoie un tuple avec le nom du plus lent et le nom du plus rapide '''
    fastest_operator = check_dependencies(operators_items)
    operators_items = dict(sorted(operators_items.items(), key = lambda x: operators_items[x[0]]))
    slowest_operator = None
    for key, val in operators_items.items():
        if fastest_operator[1] - val >= 2 and val > 0:
            if slowest_operator is None or val == operators_items[slowest_operator] and get_mean(data[key]) > get_mean(data[slowest_operator]):
                slowest_operator = key
    return slowest_operator, fastest_operator[0]

already_helping = ()
def check():
    ''' fait appel à la fonction who_needs_help() et effectue des comparaisons pour savoir ce que doit faire chaque
    et renvoie un dictionnaire avec comme valeurs le nom des postes qui doivent effectuer une action sinon None :
    {
        "display": get_stock_poste_4_from_3(operators_and_items),       # pour afficher le nombre d'encours sur le poste 4 (demande spéciale)
        "go_help": go_help,                                             # nom du poste qui doit aller aider
        "stop_help": stop_help,                                         # nom du poste qui doit arreter d'aider
        "need_help": need_help,                                         # nom du poste  qui a besoin d'aide
        "no_need_help": no_need_help                                    # nom du poste qui n'a plus besoin d'aide
    } '''
    global already_helping
    data = open_file()
    operators_and_items = get_items_in_production(data)
    operators_needing_help = who_needs_help(data, operators_and_items)
    go_help = None
    stop_help = None
    need_help = None
    no_need_help = None
    if operators_needing_help[0] is None:
        if already_helping:
            stop_help = already_helping[1]
            no_need_help = already_helping[0]
            if VERBOSE:
                add_to_logs(f"Poste {already_helping[1][-1]} arrete d'aider, Poste {already_helping[0][-1]} n'a plus besoin d'aide")
            already_helping = ()
    
    if operators_needing_help[0] is not None:
        if not already_helping:
            go_help = operators_needing_help[1]
            need_help = operators_needing_help[0]
            if VERBOSE:
                add_to_logs(f"Poste {operators_needing_help[1][-1]} commence a aider Poste {operators_needing_help[0][-1]}")
            already_helping = operators_needing_help
        else:
            if already_helping[0] != operators_needing_help[0]:
                no_need_help = already_helping[0]
                need_help = operators_needing_help[0]
                if VERBOSE:
                    add_to_logs(f"Poste {operators_needing_help[1][-1]} arrete d'aider Poste {already_helping[0][-1]}, commence a aider Poste {operators_needing_help[0][-1]}")
                already_helping = operators_needing_help
            if already_helping[1] != operators_needing_help[1]:
                stop_help = already_helping[1]
                no_need_help = already_helping[0]
                go_help = operators_needing_help[1]
                need_help = operators_needing_help[0]
                if VERBOSE:
                    add_to_logs(f"Poste {already_helping[1][-1]} arrete d'aider Poste {already_helping[0][-1]}, Poste {operators_needing_help[1][-1]} commence a aider aider Poste {operators_needing_help[0][-1]}")
                already_helping = operators_needing_help

    return {"display": get_stock_poste_4_from_3(operators_and_items), "go_help": go_help, "stop_help": stop_help, "need_help": need_help, "no_need_help": no_need_help} 

def get_stock_poste_4_from_3(operators_and_items: dict) -> int:
    ''' renvoie le nombre d'encours sur le poste 4 fabriqués par le poste 3'''
    return operators_and_items["poste_3"] - operators_and_items["poste_4"]

def get_stock_poste_4_from_2(operators_and_items: dict) -> int:
    ''' renvoie le nombre d'encours sur le poste 4 fabriqués par le poste 2'''
    return operators_and_items["poste_2"] - operators_and_items["poste_4"]

def get_stock_poste_2_from_1(operators_and_items: dict) -> int:
    ''' renvoie le nombre d'encours sur le poste 2 fabriqués par le poste 1'''
    return operators_and_items["poste_1"] - operators_and_items["poste_2"]

def get_stock_poste_6_from_4(operators_and_items: dict) -> int:
    ''' renvoie le nombre d'encours sur le poste 6 fabriqués par le poste 4'''
    return operators_and_items["poste_4"] - operators_and_items["poste_6"]

def get_stock_poste_6_from_5(operators_and_items: dict) -> int:
    ''' renvoie le nombre d'encours sur le poste 6 fabriqués par le poste 5'''
    return operators_and_items["poste_5"] - operators_and_items["poste_6"]