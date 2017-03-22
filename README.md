Constitution de l'équipe:
-Raphael BARRAUD
-Thomas COQUEREAU
-Omar DIOUF
-Quentin MAISONNEUVE
-Etienne MARTIN
-Jean PORTALIS

Guide d'utilisation de 

I. Fonctionnement global du programme
 Nous avons mplementer la méthode de résolution débutante du cube
 Voici les principaux sous-programmes de ce programme:
  - Résolution de la croix sur la face du haut
  - Résolution de la première couronne 
  - Résolution de la deuxième couronne
  - Résolution de la croix sur la face du bas
  - Resolution de la face du bas
  - Résolution finale du cube grace au bon positionnement des arêtes et des coins
  
 II. Utilisation du programme

  Pour résoudre son cube, l'utilisateur devra entrer la composition de son cube, pour cela il entrera les 56 couleurs comme ceux,ci:
	
				                       1  2  3
				                       4  U  6
				                       7  8  9
	                          10 11 12 13 14 15 16 17 18 19 20 21
                              22 L  24 25 F  27 28 R  30 31 B  33
                              34 35 36 37 38 39 40 41 42 43 44 45
                                       46 47 48
                                       49 D  51
                                       52 53 54
Avec U=La face du haut
     D=La face du bas
     L=La face de gauche
     R=La face de droite
     F=La face avant
     B=La face arrière

Exemple d'entré du programme:
#solve("RYYWWBWWRGRRBOGYWGOGWBGYRRWGBBYORORRBOBOOOBBGYGYGYYWOW")

(la fonction se trouve dans poqb.py)

III.Résultat

Après avoir entré ces 56 caractères, le programme voit renvoyer en sortie une chaine de caractère de mouveement à appliquer pour que le cube soit résolu.
Il existe 6 mouvements principaux : U,F,R,L,B,D. De plus il existe des variantes de ces mouvements qui sont par exemple pour le mouvement U : U' et U2
Ces mouvement représente:

- U est la rotation d'1/4 de tour dans le sens horaire de la face du haut, lorque l'on a cette face en face de nous. 
 U' représente la rotation d'1/4 de tour dans le sens anti-horaire de cette face. Et U2 représente la rotation d'1/2 tour l=dde la face du haut.
- De même que pour la rotation U, D c'est pour la face du bas, L la face de gauche, R la face de droite, B la face arrière et F la face avant.

!!! ATTENTION : Lors de l'application des mouvements pour résoudre le cube, il faut toujour tenir le cube de la même manière.    