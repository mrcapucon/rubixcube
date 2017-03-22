import copy
class Cube:


  

    # 0 si jamais la couleur n'a pas encore été indiquée
    
    def __init__(self, cube=None):

        #plages d'indexes de toutes les cases de chaque face
        # CF schéma dans madoc 

        self.idx=[["u",range(0,9)],["d",range(45,54)],["f",[12,13,14 ,24,25,26, 36,37,38]],["l",[9,10,11, 21,22,23, 33,34,35]],["r",[15,16,17 ,27,28,29, 39,40,41]],["b",[18,19,20 ,30,31,32, 42,43,44]]]
        
        #liste des noms des faces permet de faciliter les boucles for


        self.liFace=["u","l","f","b","r","d"]
        self.liFaceaff=["u","l","f","r","b","d"]


        #Vient du merge de Jean, a garder pour voir si il en a besoin
        #self.liFace=["u","l","f","r","b","d"]
        #self.liFaceaff=["u","l","f","r","b","d"]
 
        
        #Initialisation des faces à 0
        
        self.up=[0,0,0],[0,0,0],[0,0,0] 
        self.down=[0,0,0],[0,0,0],[0,0,0]
        self.front=[0,0,0],[0,0,0],[0,0,0]
        self.left=[0,0,0],[0,0,0],[0,0,0]
        self.right=[0,0,0],[0,0,0],[0,0,0]
        self.back=[0,0,0],[0,0,0],[0,0,0]

        

       

        
        #Liste des mouvements
        
        #explications de la structure de données :
        #Dans la case m[0] le trouve le nom de la face à faire tourner
        #la rotation de la face est gérée par la methode rotationFace
        
        #Le tableau m[1] decrit tout les subtitutions de cases entre chaque face
        #exemple si je fais tourner la face du dessus (up) j'utilise le mouvement self.U
        #la face "u" devra tourner sur elle meme puis
        #les cases 0,1,2 de la face 'l' se retrouve en position 0,1,2 sur la face'f'
        #les cases 0,1,2 de la face 'f' se retrouve en position 0,1,2 sur la face'r'
        #ainsi de suite
        
        #NB pour passer d'une coordonée 1D noté ("i" dans ce programme) en coordonnées 2D sur un tablea de taille n
        #coord x = partie entiere(i/n)
        #coord y = i modulo n
        
        # 0|1|2
        # 3|4|5
        # 6|7|8

         #sert aussi de liste des voisins dans cette ordre [u,r,d,l]
        
        self.D="d",[["f",[6,7,8]],["r",[6,7,8]],["b",[6,7,8]],["l",[6,7,8]]]
        self.U="u",[["b",[2,1,0]],["r",[2,1,0]],["f",[2,1,0]],["l",[2,1,0]]]
                
        self.R="r",[["u",[2,5,8]],["b",[6,3,0]],["d",[2,5,8]],["f",[2,5,8]]]
        self.L="l",[["u",[0,3,6]],["f",[0,3,6]],["d",[0,3,6]],["b",[8,5,2]]]
                
        self.B="b",[["u",[2,1,0]],["l",[0,3,6]],["d",[6,7,8]],["r",[8,5,2]]]
        self.F="f",[["u",[8,7,6]],["r",[6,3,0]],["d",[0,1,2]],["l",[2,5,8]]]


        #ordre de transposition des cases de la face qui tourne
        #explications de la structure de données :

        #Meme principe que pour la rotation des bords
        #si je fais tourner la face f
        #les cases de trans[0] (0,1,2) se retrouve en trans[1] (2,5,8)
        #sachant que les cases de trans[3] se retrouve en trans[0]
        self.trans=[0,1,2],[2,5,8],[8,7,6],[6,3,0]

        self.transInversed=[0,1,2],[6,3,0],[8,7,6],[2,5,8]
        self.liEdge=1,5,7,3
        self.liCorn=0,2,8,6




        #Si aucunes configuration de départ n'a été renseignée
        
        if(cube==None):
            return

        #origin stocke 
        self.origin=cube

        for x in self.idx:
            self.initFace(x)
        
    #change l'état d'une face par le tableau renseigné
    #face doit être une liste de liste 3x3
    def setFace(self,nameFace,face):
        if(nameFace=="u"):
            self.up=face
            return
            
        if(nameFace=="d"):
            self.down=face
            return 
            
        if(nameFace=="l"):
            self.left=face
            return
            
        if(nameFace=="r"):
            self.right=face
            return
            
        if(nameFace=="f"):
            self.front=face
            return
            
        if(nameFace=="b"):
            self.back=face
            return

        
        print("INVALID FACENAME")
        return -1
        
    def getStr(self,nameFace='u'):
        up=self.getFace(nameFace)
        down=self.getFace(self.getFaceInversed(nameFace))
        core=[]
        strresult=''
        for x in self.liFaceaff :
            if (x!=nameFace and x!=self.getFaceInversed(nameFace)):
                core+=[self.getFace(x)]
        for x in range(3):
            for y in range(3):
                strresult+=up[x][y]
        
        for x in range(3):
            for z in core:
                for y in range(3):
                    strresult+=z[x][y]

        for x in range(3):
            for y in range(3):
                strresult+=down[x][y]

        return strresult
        

    
    # Cette methode remplis chaque face avec les éléments qui lui correspondent 
    # et renseignés dans la listes idx ( cf __init__ )

    def initFace(self,idx):
        # on recupere la face à initialiser
        face=self.getFace(idx[0])
        i=0 
        j=0
        for val in idx[1]:

            face[j][i]=self.origin[val]
            #on passe à la case suivante   
            i=i+1

            # si on arrive à la fin d'une ligne
            # on passe à la suivante         
            if(i%3==0):   
                i=0
                j=j+1

        return face
        

    # cmd décrit l'action à operer sur le cube
    # rotation marche en deux parties
    # la rotation de la face puis la rotation des bords de la face
    # des verifications sur cmd sont faites au fur et à mesure #NeverTrustUser
    def rotation(self,cmd):

        # Si l'action demandée n'est pas conforme
        if(len(cmd)>2 or len(cmd)==0):
            print("COMMAND INVALID")
            return -1
        
        #si il s'agit d'une rotation "simple"
        if(len(cmd)==1):
            m=self.getMouv(cmd)
            self.rotationFace(m[0])
            self.rotationEdge(cmd)
            return
        
        #deuxième verification de l'argument
        if(cmd[1]!="'" and cmd[1]!="2"):
            print("COMMAND INVALID 2ND CHAR ISN'T ' OR 2 ")
            return -1
        m=self.getMouv(cmd[0])
        
        #si il s'agit d'une rotation inverse
        if(cmd[1]=="'"):
            self.rotationFace(m[0],True)
            self.rotationEdgeInv(cmd[0])
            return
        if(cmd[1]=="2"):
            self.rotationHalfFace(m[0])
            self.rotationEdge(cmd[0],True)
            return
        

    #Une rotation d'un demi consiste à echanger les parties droites / gauches et hautes / basses de la face qui tourne
    #On recupere donc ces dernières dans deux listes "group" et on échange les valeurs  
    def rotationHalfFace(self,face):
        f=self.getFace(face)
        groupa=[self.trans[0]]+[self.trans[2]]
        groupb=[self.trans[1]]+[self.trans[3]]
        
        
        #on crée une face "temporaire" pour stocker l'état de la face apres rotation
        tmp=[0,0,0],[0,0,0],[0,0,0]
        
        #le centre de la face est la seule case qui reste en place
        tmp[1][1]=f[1][1]
        
        for x in range(0,3):
            tmp[int(groupa[0][x]/3)][groupa[0][x]%3]=f[int(groupa[1][x]/3)][groupa[1][x]%3]
            tmp[int(groupa[1][x]/3)][groupa[1][x]%3]=f[int(groupa[0][x]/3)][groupa[0][x]%3]

            tmp[int(groupb[0][x]/3)][groupb[0][x]%3]=f[int(groupb[1][x]/3)][groupb[1][x]%3]
            tmp[int(groupb[1][x]/3)][groupb[1][x]%3]=f[int(groupb[0][x]/3)][groupb[0][x]%3]

        self.setFace(face,tmp)
    

    def rotationFace(self,face,inv=False):
        if(inv==True):
            tt=self.transInversed
        else:
            tt=self.trans
        f=self.getFace(face)

        #on crée une face "temporaire" pour stocker l'état de la face apres rotation
        tmp=[0,0,0],[0,0,0],[0,0,0]
        
        #le centre de la face est la seule case qui reste en place
        tmp[1][1]=f[1][1]
        
        for x in range(0,4):
            t=tt[x]
            s=tt[(x+1)%4]
            for y in range(0,3):
                
                # cf explication de self.trans
                tmp[int(s[y]/3)][s[y]%3]=f[int(t[y]/3)][t[y]%3]
                
        self.setFace(face,tmp)

        
    def getLiCase(self,nameFace,li):
        f=self.getFace(nameFace)
        ret = []
        for x in li:
            ret=ret+[f[int(x/3)][x%3]]
        return ret
    
    def rotationEdge(self,mouv,half=False):
        if(half==True):
            inc=2
        else:
            inc=1
        m=self.getMouv(mouv)
        tmp=[]
        for x in range(0,4):
            tmp=tmp +[self.getLiCase(m[1][x][0],m[1][x][1])]
        for x in range(0,4):
            f=self.getFace(m[1][(x+inc)%4][0])
            for y in range(0,3):
                i=m[1][(x+inc)%4][1][y]
                f[int(i/3)][i%3]=tmp[x][y]
                

    #Meme principe que pour edge mais en inversant l'ordre des faces 
    def rotationEdgeInv(self,mouv):
        m=self.getMouv(mouv)
        tmp=[]
        for x in range(0,4):
            tmp=tmp +[self.getLiCase(m[1][x][0],m[1][x][1])]
        for x in range(3,-1,-1):
            f=self.getFace(m[1][x][0])
            for y in range(0,3):
                i=m[1][x][1][y]
                f[int(i/3)][i%3]=tmp[(x+1)%4][y]

        
    
            


            
   
    # récupere la face renseignée par nameFace 
    def getFace(self,nameFace):
        if(nameFace=='u'):
            return self.up
        
        if(nameFace=='d'):
            return self.down

        if(nameFace=='f'):
            return self.front

        if(nameFace=='l'):
            return self.left

        if(nameFace=='r'):
            return self.right

        if(nameFace=='b'):
            return self.back
        
        print("INVALID FACENAME")
        return -1
    
    # verifie un pattern li sur une des faces
    # face est un nameFace et li une liste de coord 1D
    def checkPattern(self,face,li):

        f=self.getface(face)

        
        color=f[int(li[0])][li[0]%3]
        for x in li:
            if(f[int(li[0]/3)][li[0]%3]!=color):
                return False
        return True
            
    def getMouv(self,nameMouv):
        if(nameMouv=='R'):
            return self.R
        
        if(nameMouv=='L'):
            return self.L

        if(nameMouv=='U'):
            return self.U

        if(nameMouv=='D'):
            return self.D

        if(nameMouv=='B'):
            return self.B
        if(nameMouv=='F'):
            return self.F
        
        print("INVALID MOUVEMENT NAME")
        return -1

    # Verifie qu'une face est complete
    def faceFinished(self,nameFace):
        face=self.getFace(nameFace)
        color=face[0][0]
        for x in face:
            for y in x:
                if(y!=color):
                    return False
        
        return True

    # Verifie si un cube est terminé ou non 
    def cubeFinished(self):
        for x in self.liFace:
            if(self.faceFinished(x)==False):
                return False
        return True


    #methode d'affichage du cube
    def printCube(self):
        print("///////////////////////////////////")
        for x in self.liFace:
            print("-------",x,"--------")
            affTab(self.getFace(x))

    #Deuxieme méthode d'affichage du cube

        #Deuxieme méthode d'affichage du cube

    def displayCube(self,defaultFace='u'):
        up=self.getFace(defaultFace)
        down=self.getFace(self.getFaceInversed(defaultFace))
        core=[]
        for x in self.liFaceaff :
            if (x!=defaultFace and x!=self.getFaceInversed(defaultFace)):
                core+=[self.getFace(x)]
        for x in range(3):
            print("      " ,end='')
            for y in range(3):
                print(up[x][y]+" " ,end='')
            print("")
            
        for x in range(3):
            for z in core:
                for y in range(3):
                    print(z[x][y]+" " ,end='')
            print("")

        for x in range(3):
            print("      " ,end='')
            for y in range(3):
                print(down[x][y]+" " ,end='')
            print("")

    
    def getCentralColor(self,nameFace):
        f=self.getFace(nameFace)
        return f[1][1]


     # Permet d'obtenir le nom de la face opposé à celle dont le nom est nameFace

    def getFaceInversed(self,nameFace):
        self.liFace=["u","l","f","b","r","d"]
        if(nameFace not in self.liFace):
            print("getFaceInversed :INVALID NAMEFACE ")
            return -1
        idx=self.liFace.index(nameFace)
        return self.liFace[len(self.liFace)-(1+idx)]
    

    def checkColorSquare(self,nameFace,color,idx):
        f=self.getFace(nameFace)
        return f[int(idx/3)][idx%3]==color

        
    def getCase(self, nameFace, i):
        face=self.getFace(nameFace)
        return face[int(i/3)][i%3]



    # Cette fonction permet de trouver un cube ( coin ou tranche ) à l'intérieur même
    # du rubik cube. Elle prend en argument une tabcolor qui est la liste des couleur des faces qui composent
    # le cube recherché
    
    # NB : si le cube est un coin la liste sera de trois couleurs
    # si il s'agit d'une tranche deux couleurs doivent être renseignées
    
    # La fonction renvoit la structure de données suivante
    # tab[idx couleur] =[index sur la face, nom de la face]
    
    # ex : si on precise tabcolor='R','G'
    # et que R se trouve en 7 sur Up et g en 1 sur Front on aura
    # tab = [ 7,'u'],[1,'f'] ,
    # l'ordre d'index dans tabcolor definit l'ordre d'index dans la liste renvoyée
    
    # nameFace est une option qu'il faut préciser si on cherche un cube SEULEMENT sur une face
    # précise. Dans ce cas on précise le nom de la face dans cet argument  
    
    def findCube (self,tabcolor,nameFace=None):

        # si Tabcolor ne correspond pas
        if(len(tabcolor)!=2 and len(tabcolor)!=3):
            return -1
        
        # si il s'agit d'un coin ou d'une tranche le comportement de la fonction ets legerement différent
        # on regle ces différence dans ce bloc if else
        # tmpr est la structure de données renvoyées à la fin
        # sa taille depend du type de cube recherché
    
        if(len(tabcolor)==2):
            li=self.liEdge
            idx=1
            tmpr=[0]*2
            workingtab=self.liFace
        else:
            li=self.liCorn
            idx=0
            tmpr=[0]*3
            workingtab=self.liFace[0],self.liFace[5]

        if(nameFace!=None):
            workingtab=[nameFace]

        for i in workingtab :
            m=self.getMouv(i.upper())
 
            for idj,j in enumerate(li) :
                
                for idc1,c1 in enumerate(tabcolor) :
                    
                    # si on trouve une des couleurs on regardes les faces voisines
                    # pour savoir si on se trouve ou non sur le bon cube
                    
                    if self.checkColorSquare(i,c1,j):
                        tmpr[idc1]=[j,i]


                        j2=m[1][idj][1][idx]
                        f2=m[1][idj][0]



                        for idc2,c2 in enumerate(tabcolor) :
                            if self.checkColorSquare(f2,c2,j2):
                                tmpr[idc2]=[j2,f2]
                                
                                # si on a trouvé deux couleurs et que le cube recherché est
                                # une tranche on renvoit tmpr sinon on continue la recherche
                                if len(tabcolor)==2 :
                                    return tmpr
                                
                                j3=m[1][(idj+3)%4][1][2]
                                f3=m[1][(idj+3)%4][0]
                                for idc3,c3 in enumerate(tabcolor) :
                                    if self.checkColorSquare(f3,c3,j3) :
                                        tmpr[idc3]=[j3,f3]
                                        return tmpr
        
                            
        return -1                            
                            
                            
                                  
                                    
                            
                        
                               
        
                         
                
                    
            
   #methode d'affichage d'une table 2D
def affTab(tab):
    for x in tab:
        print(x)
