![](/presentation/img/mesure3DBUILDPARIS.gif)

# Hackathon IGN : Paris en un jour

But : photographier tout Paris en un jour.  

- Plusieurs vélo avec casque caméra embarquée  
- Itinéraire complet et optimisé (le moins de repassage, le plus de couverture) de Paris réalisable en un jour  
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

4. Pondérer les voies : pente en récupérant les données d'élévation IGN, traffic avec les classification des voies par OSM (axe primaire, secondaire, tertiaire, résidentiel...) 

-------

### L'algorithme
1. Créer l'itinéraire pour un vélo qui traverse tout Paris (problème du Postier Chinois [1] [2] et parcours eulérien [3] en théorie des graphes)  
2. Découper Paris en n secteurs et faire un itinéraire par secteur    
3. A la place de découper Paris en n secteurs, trouver le n optimal pour avoir des secteurs équivalents en pondérant les voies en fonction des distances, des pentes et du traffic  

[Carte itinéraire 200km de trajet dans Paris](/maps/trajet_multi.html)

[Carte itinéraire avec 2 vélos](/maps/trajet_multi.html)

-------

## La reconstitution des photos

Proof of concept sur Strasbourg car bonne qualité de données

<img width="2455" height="1704" alt="Capture d’écran du 2026-06-23 16-40-56" src="https://github.com/user-attachments/assets/3bb948fa-e909-4641-9aa3-27ec2852fdf6" />

Récupération d'images sur un coin de rue:
<img width="2455" height="1704" alt="image" src="https://github.com/user-attachments/assets/7c92875e-f51a-4eb5-ad89-270e36706c7d" />

Entrainement d'un modèle de reconstitution 3D:

<img width="2455" height="1704" alt="image" src="https://github.com/user-attachments/assets/7a597728-5d0b-4e7c-b997-1f7540a86bc7" />

-------

## Bibliographie

1. **Problème du postier chinois** — Wikipédia  
   https://fr.wikipedia.org/wiki/Probl%C3%A8me_du_postier_chinois  
   Présentation du problème de couverture minimale d'un graphe par ses arêtes, directement applicable à la planification d'itinéraires couvrant l'ensemble du réseau routier.

2. van Ee, M., & Sitters, R. (2020).  
   *The Chinese Deliveryman Problem*.  
   4OR, 18, 341–356.  
   https://link.springer.com/article/10.1007/s10288-019-00420-2  
   Extension du problème du postier chinois visant à optimiser les temps de visite plutôt que la seule distance totale.

3. **Graphe eulérien** — Wikipédia  
   https://fr.wikipedia.org/wiki/Graphe_eul%C3%A9rien  
   Définition des parcours et circuits eulériens, fondement théorique des algorithmes de couverture de voirie.
