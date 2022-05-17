# Projet CESI Bike

### Simulation d'une chaîne de montage

<p align="center"><img alt="Image de la maquette" src="https://media.discordapp.net/attachments/918983715143684137/974684928727990322/IMG_4619.jpg?width=884&height=663" width=800 /></p> 
<p align="middle"><i> Maquette de la chaine de de montage </i></p>

Deux types d'opérateurs : 

- Manuel
- Automatique


## Manuel :
- Une pression sur le bouton vert (avec la led verte éteinte) simule le début de fabrication d'un sous-ensemble (la led verte s'allume alors)
- Une pression sur le bouton vert (avec la led verte allumée) simule la fin de fabrication d'un sous-ensemble (la led verte s'éteint alors)
- La led bleue s'allume automatiquement si le poste doit aller aider un autre poste
- La led rouge s'allume automatiquement si le poste a besoin d'aide

> Amélioration : La led jaune s'allume automatiquement si le poste a besoin de matériel

## Automatique :

- Toutes les leds s'allument automatiquement après une première pression sur le bouton vert 


> Les temps de fabrication par poste et par sous-ensemble sont visibles dans data.json  
> Les actions d'entraide sont visibles dans le fichier logs.txt

## Procédure
 
- Installer les modules nécessaires (voir `requirements.txt` pour la partie en Python)  
- Téléverser le programme `manuel.ino` (*à l'aide de l'IDE Arduino*) dans les arduino gérant les **postes manuels** en veillant bien à **modifier la variable** `POSTE`.  
- Téléverser le programme `automatique.ino` dans l'arduino gérant les **postes automatiques**
- Lancer le programme `main.py` sur le PC relié aux arduino

> Le nombre de sous-ensembles par poste devrait apparaître en temps réel dans la console
  
## Montage électrique

Pour les postes manuels :

<p align="center"><img alt="Image du montage electrique" src="https://media.discordapp.net/attachments/717747465805365330/976167174920089650/unknown.png?width=1010&height=663" width=500 /></p>  

Matériel :
  - 1 arduino uno  
  - 1 breadboard  
  - 4 boutons  
  - 4 leds (bleue, verte, jaune, rouge)  
  - 4 resistances 220Ω pour les leds  
  - 4 resistances 1kΩ pour les boutons  
  - fils électriques  


<br />  

Même principe pour les postes automatiques, à l'exception qu'il n'y a que des leds vertes (*un seul bouton peut également être utilisé pour commander les 4 postes*)
<br /><br /><br /><br />
  
<img alt="Logo CESI" src="https://ecole-ingenieurs.cesi.fr/wp-content/themes/cesi/static/logo/ecole-ingenieurs.svg" width="200" />  
  
Étudiants : Lucas, Antoine, Mohamad & Paulin  
Intervenant : Cédric
