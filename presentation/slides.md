![](/presentation/img/mesure3DBUILDPARIS.gif)

# Hackathon IGN : Paris en un jour

But : photographier tout Paris en un jour.  

- Plusieurs vélo avec casque caméra embarquée  
- Itinéraire complet et optimisé (le moins de repassage, le plus de couverture) de Paris sur un jour  
- Reconstitution de Paris avec les photos récupérées  

-------
## L'itinéraire vélo

### Les données

#### Récupérer les données des voiries de Paris en vélo  

Voies cyclables de Paris (OSM), extraits avec le package `osmnx`
![](/presentation/img/paris_bois.png)

Et on exclu les bois de Boulogne et de Vincennes
![](/presentation/img/paris.png)

-------

#### Filtrer les petites impasses  
2e arrondissement de Paris, filtré des impasses
![](/presentation/img/paris2_impasse.png)

-------

#### Détecter les tronçons de connection de voies  
Tronçons de connection dans le 2e arrondissement de Paris
![](/presentation/img/paris2_connecteurs.png)

4. Pondérer les voies : pente, traffic  

### L'algorithme
1. Créer l'itinéraire pour un vélo qui traverse tout Paris  
2. Découper Paris en n secteurs et faire un itinéraire par secteur  
3. Trouver le n optimal pour avoir des secteurs équivalents  

![](/maps/trajet_multi.html)

![](/maps/trajet_velo_200km.html)

## La reconstitution des photos

Proof of concept sur Strasbourg
