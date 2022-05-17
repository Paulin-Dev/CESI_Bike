# Projet CESI Bike

### Simulation d'une chaîne de production

![Maquette de la chaine de montage](https://media.discordapp.net/attachments/918983715143684137/974684928727990322/IMG_4619.jpg?width=884&height=663)


Deux types d'opérateurs : 

- Manuel
- Automatique


## Manuel :
- Une pression sur le bouton vert (avec la led verte éteinte) simule le début de fabrication d'un sous-ensemble (la led verte s'allume alors)
- Une pression sur le bouton vert (avec la led verte allumée) simule la fin de fabrication d'un sous-ensemble (la led verte s'éteint alors)
- La led bleue s'allume automatiquement si le poste doit aller aider un autre poste
- La led rouge s'allume automatiquement si le poste a besoin d'aide

*Amélioration : La led jaune s'allume automatiquement si le poste a besoin de matériel*

## Automatique :

- Toutes les leds s'allument automatiquement après une première pression sur le bouton vert 


**Les temps de fabrication par poste et par sous-ensemble sont visibles dans data.json**
**Les actions d'entraide sont visibles dans le fichier logs.txt**

Étudiants : Lucas & Antoine & Mohamad & Paulin
Intervenants : Cédric
