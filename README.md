# INSTALLATION NECESSAIRE  
## Version de Python  
Il est obligatoire d'utiliser une verison Python 3.x.x. De plus, afin d'avoir un meilleur rendu 3D, il est fortement 
recommandé d'utiliser la version Python 3.11.  

## Imports nécessaires  
La liste suivante donne les imports nécessaires et obligatoires pour le bon fonctionnement du logiciel :
1) NumPy pour tous les calculs ;
2) MatPlotLib pour tous les affichages.

# UTILISATION
## Interface utilisateur
Afin de lancer la procédure demandée dans le cahier des charges, il suffit d'exécuter le fichier Python ```user.py```. 
Celui-ci demande alors de renseigner les paramètres du robot et les deux points dans l'espace pour réaliser un segment de droite.
Aucune vérification n'est faite lors de la saisie, cependant le programme se ferme avec un message d'erreur si le segment
renseigné n'est pas réalisable par le robot.

Une fois les paramètres saisis, les figures devraient apparaître dans l'ordre suivant :
1) Absisse curviligne et ses dérivées (loi de commande) ;
2) Trajectoire opérationnelle sur chaque composante en fonction du temps et ses dérivées ;
3) theta en fonction du temps ;
4) Trajectoire opérationnelle dans l'espace cartésien 3D ;
5) Vitesses des composantes du point O5 calculées et comparaison avec les attendues ;
6) qi en fonction du temps ;
7) dqi en fonction du temps ;
8) Visualisation avec le visualiseur 3D du résultat de la fonction traj.

Il est nécessaire de fermer une figure pour faire apparaître la suivante.

## Visualiseur MGD
Il est possible de visualiser le MGD (modèle géométrique direct) en 3D de manière intéractive en appelant les lignes de code suivantes :
```python
mgd = MGD(H, L, [[0., 2 * np.pi], [0., 2 * np.pi], [-5., 5.], [0., 2 * np.pi]])
mgd.plot3D()
```

Il faut bien sûr au préalable initialiser les paramètres.

## Visualiseur G-code
Une fonctionnalité de visualiseur de G-code a été implémentée (ne supporte que les commandes de G0 à G3). Pour cela, il 
suffit de placer le fichier G-code dans le dossier ```/input``` et d'appeler le viewer avec les lignes de code suivantes :
```python
interpreter = GcodeInterpreter(law, H, L, V, 'input/upssitech.gcode')
interpreter.read_lines()
interpreter.get_commands()
t, M = interpreter.get_M()
q, q_bis = interpreter.get_Q(t, M, theta)
g = GcodePath(law, H, L)
g.plot3D_M(t, M, theta)
g.plot3D_Q(t, M, q, q_bis, step=25)
```

Il faut bien sûr au préalable initialiser les paramètres.

## Autre
Le fichier ```main.py``` permet de montrer toutes les fonctionnalités du projet.