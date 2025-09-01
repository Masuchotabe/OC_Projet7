# OC_Projet7

## installation
 install UV 
 
 ```shell 
 uv init
 uv run src/bruteforce.py
 uv run src/optimized.py
 ```
 

## Bruteforce 
### Complexité temporelle
Avec n = Le nombre d'actions total 
Parcours de toutes les solutions possibles -> O(2<sup>n</sup>)
Calcul du score pour une solution O(n)

Complexité temporelle : O(n*2<sup>n</sup>)

### Calcul de la complexité en mémoire
Grâce à la fonction `combination`, on ne stocke en mémoire que la combinaison courante et la meilleure. 

Au maximum, deux liste d'actions sont stockées en mémoire, on est donc sur de la complexité O(2n). 

Complexité en mémoire : O(n)

## Optimized

### Complexité 
n : Nombre d'actions
B : Budget maximal
#### Temporelle 
Calcul du profit : O(n) 
Calcul de chaque case du tableau : O(n*B) 
Calcul solution : O(n) 

Complexité temporelle : O(n\*B + 2n) = **O(n\*B)**

#### Mémoire
Liste des actions : O(n) 
Tableau de taille O([n+1][B+1]) 
Meilleure combinaison : O(n)

Complexité en mémoire : O((n+1)\*(B+1) + 2n) = **O(n\*B)**
