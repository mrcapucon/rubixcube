#récupère le cube de départ entrée par l'utilisateur dans InterfaceIO
#et renvoie à InterfaceIO la résolution du cube

from Cube import *
class Resolution:

    def __init__(self,c):
        self.cube=c
        self.mouv = 0
        self.vr = 0
        self.br = 0
        self.bo = 0
        self.vo = 0
        self.a = 0
        self.b = 0
        
        
        # liste des indexes servant  à la croix
        self.liCross=1,5,7,3
        self.liCorner=0,2,8,6

        # liste des rotation effectué durant la résolution 
        self.liCmd=''
        self.nbCmd=0
        self.liRota='','2',"'"

        
    # Utiliser cette fonction permet de garder en mémoire les mouvements effectué durant la résolution
    def rotation(self,cmd):
        if(cmd=='' or cmd==' '):
            return 0
        if(len(cmd)!=1 and len(cmd)!=2):
            print("rotation : INVALID ROTATION NAME",cmd)
            return -1
        if(len(cmd)==2 and ( cmd[1]!="2" and cmd[1]!="'")):
            print("rotation : INVALID ROTATION NAME",cmd)
            return -1
        self.liCmd+=cmd
        self.nbCmd+=1
        #print(cmd,end='')
        self.cube.rotation(cmd)
        
    # Fonction qui renvoit l'inverse d'une rotation L2 => L2 L=>L' L'=>L        
    def getInvRot(self,cmd):
        if(len(cmd)!=1 and len(cmd)!=2):
            print("getInvRot : INVALID ROTATION NAME",cmd)
            return -1
        if(len(cmd)==1):
            return cmd+"'"
        if(cmd[1]=='2'):
            return cmd
        return cmd[0]
        
    # Cette fonction renvoit le type de rotation a éffectué
    # pour que le cube sur la face origin se retrouve sur la face
    # destination
    # la rotation doit etre une composante de la face rotatingF
    def getApproRot(self,origin,destination,rotatingF):
        if(origin == destination):
            return ''
        if(rotatingF==destination):
            return -2
        i=-1
        x=0
        m=self.cube.getMouv(rotatingF.upper())
        while(x<=6):
            if(origin==m[1][x%4][0]):
                i=0
            if(destination==m[1][x%4][0] and i!=-1):
                return rotatingF.upper()+self.liRota[i-1]
            x+=1
            if(i!=-1):
                i+=1
        return -1

    #  Permet d'effectuer un certain nombre de rotation à la suite 
    def applyCmd(self,cmd):
        cpt=0
        while(cpt!=len(cmd)):
            tmp=cmd[cpt]
            if(cpt==len(cmd)-1):
                self.rotation(tmp)
                return 0
            if(cmd[cpt+1]=="'" or cmd[cpt+1]=="2"):
                tmp+=cmd[cpt+1]
                self.rotation(tmp)
                cpt+=1
            else :
                self.rotation(tmp)
            tmp=''
            cpt+=1
        return 0
            


        
            
            
            
    

    def theCross(self,nameFace):
        tab=self.checkCross(nameFace)
        colorcross=self.cube.getCentralColor(nameFace)
        if(tab[0]==True):
            return 0
        # pour toute les faces qui n'ont pas encore été traitée
        while(len(tab[1])!=0):
            for x in tab[1]:
                #print(tab)
                
                # On cherche le cube de couleur "Face à traiter" + " Face où se trouve la croix"
                # on récupere donc la couleur de "Face à traiter" 
                curColor=self.cube.getCentralColor(x)
                result=self.cube.findCube([colorcross,curColor])
                #print(result)
                #cube.displayCube()

                # on traite les différents cas en fonction de la position du cube

                # cas ou la face de la couleur dont on veut faire la croix (ex blanc) se trouve sur la face de la croix
                if(result[0][1]==nameFace):

                    # si la croix n'a pas été commencé on peut économiser un mouvement
                    if(len(tab[1])==4):
                        self.applyCmd(self.getApproRot(result[1][1],x,result[0][1]))
                    else:
                        self.applyCmd(result[1][1].upper()+'2'+self.getApproRot(result[1][1],x,self.cube.getFaceInversed(nameFace))+x.upper()+'2')

                #cas ou la face de la couleur dont on veut faire la croix se trouve sur la face inverse de la croix
                if(result[0][1]==self.cube.getFaceInversed(nameFace)):
                    self.applyCmd(self.getApproRot(result[1][1],x,result[0][1])+x.upper()+'2')

                # si on se trouve dans aucun des deux
                if(result[0][1]!=self.cube.getFaceInversed(nameFace) and result[0][1]!=nameFace):

                    # on essaye d'approcher le morceau de croix par une seule rotation
                    # le nom de la rotation est donnée par getApproRot si une seule rotation suffit
                    # -1 est renvoyé si ce n'est pas possible ( le pire des cas )
                    # -2 est renvoyé si le la face blanche ( exemple ) se trouve sur la face de destination
                    rot=self.getApproRot(result[1][1],x,result[0][1])
                    if(rot==-1):
                        
                        # si ce n'est pas possible un minimum de trois rotations sera nécessaire
                        
                        # j'ai découpé cette partie en 2 cas à cause de certaines différences de procédure
                        # mais je pense qu'il est pssible de factoriser cette partie du code 
                        if(result[1][1]==nameFace or result[1][1]==self.cube.getFaceInversed(nameFace)):

                            # si la croix n'a pas été commencée
                            if(len(tab[1])==4):
                                tmpcmd=result[1][1].upper()
                                self.rotation(tmpcmd)
                                
                                tmppos=self.cube.findCube([colorcross,curColor])
                                tmpcmd=self.getApproRot(tmppos[1][1],x,tmppos[0][1])
                                self.rotation(tmpcmd)
                                
                                tmppos=self.cube.findCube([colorcross,curColor])
                                tmpcmd=self.getApproRot(tmppos[0][1],nameFace,x)
                                self.rotation(tmpcmd)
                                
                            # si la croix a été commencé on garde en mémoire le mouvement qui perturbe le travail déjà réalisé
                            # on fait ce mouvement à l'inverse une fois la face terminée
                            else:
                                tmpcmd=self.getApproRot(result[1][1],self.cube.getFaceInversed(nameFace),result[0][1])
                                self.rotation(tmpcmd)
                                self.rotation(self.cube.getFaceInversed(nameFace).upper())
                                tmppos=self.cube.findCube([colorcross,curColor])
                                tmpcmd=self.getApproRot(tmppos[1][1],x,tmppos[0][1])
                                
                                faceinter=tmppos[0][1]
                                mouvinter=self.getInvRot(tmpcmd)
                                
                                self.rotation(tmpcmd)
                                
                                tmppos==self.cube.findCube([colorcross,curColor])
                                tmpcmd=self.getApproRot(tmppos[0][1],nameFace,x)
                                self.rotation(tmpcmd)
                                if(faceinter not in tab[1]):
                                    self.rotation(mouvinter)
                        
                        else:
                            tmpcmd=self.getApproRot(result[0][1],self.cube.getFaceInversed(nameFace),result[1][1])
                            self.rotation(tmpcmd)
                            
                            faceinter=result[1][1]
                            mouvinter=self.getInvRot(tmpcmd)
                                
                            tmppos=self.cube.findCube([colorcross,curColor])
                            tmpcmd=self.getApproRot(tmppos[1][1],x,tmppos[0][1])
                            self.rotation(tmpcmd)
                                
                            tmppos=self.cube.findCube([colorcross,curColor])
                            tmpcmd=self.getApproRot(tmppos[0][1],nameFace,x)
                            self.rotation(tmpcmd)

                            if(faceinter not in tab[1]):
                                self.rotation(mouvinter)
                                

                    
                    # si la face blanche est sur la face cherchée il faut retourner le cube
                    elif(rot==-2):
                        #print('ok')
                        comeB=False
                        rr=result[1][1].upper()
                        if(result[1][1]!=self.cube.getFaceInversed(nameFace) and result[1][1]!=nameFace):
                            rr=self.getApproRot(result[0][1],self.cube.getFaceInversed(nameFace),result[1][1])
                            
                        self.rotation(rr)
                        tmppos=self.cube.findCube([colorcross,curColor])
                        self.rotation(self.getApproRot(tmppos[1][1],x,tmppos[0][1]))
                        if(result[1][1]==self.cube.getFaceInversed(nameFace)):
                            comeB=True
                        elif((rr[0].lower() not in tab[1] or (rr[0].lower()==nameFace and len(tab[1]!=4)))):
                            self.rotation(self.getInvRot(rr))
                        self.rotation(self.getApproRot(tmppos[0][1],nameFace,x))
                        if(comeB):
                            self.rotation(self.getInvRot(self.getApproRot(tmppos[1][1],x,tmppos[0][1])))
                            
                    # cas le plus simple ou il sufft de placer la partie de la croix sur la face ou on fait la croix
                    elif(rot==''):
                        self.rotation(self.getApproRot(result[0][1],nameFace,x))
                            
                        
    
                            
                            
                    # si rot est égal à une rotation 
                    else :
                        if(result[0][1] not in tab[1]):
                            self.applyCmd(rot+self.getApproRot(result[0][1],nameFace,x)+self.getInvRot(rot))
                        else :
                            self.applyCmd(rot+self.getApproRot(result[0][1],nameFace,x))
                #print("")
                tab[1].remove(x)            
            
                
    
    # Cette fonction permet de verifier si la croix a été réalisée sur une face
    # Le nom de la face à vérifier est donné dans nameFace
    # On utilisera la fonction findCube() en limitant les recherches à
    # la face nameFace
    
    # Si un ou des cube n'est/ne sont pas placé(s) au bon endroit
    # La structure rénvoyée sera de la forme
    # [ False , [ nom de la face1 avec un cube mal placé, .....]]
    # si tout est bien placé on aura
    # [ True ,[] ]
    
    def checkCross(self,nameFace):
        tmp=[True,[]]
        colorcross=self.cube.getCentralColor(nameFace)
        m=self.cube.getMouv(nameFace.upper())
        
        for x in m[1]:
            coloredge=self.cube.getCentralColor(x[0])
            result=self.cube.findCube([colorcross,coloredge],nameFace)
            
            if(result==-1 or result[1][1]!=x[0]):
                tmp[1]+=[x[0]]
                tmp[0]=False
                
                
        return tmp

    #verifie si les coin sont fait
    #entré : nom de la face à vérifier
    #sortie : tableau à deux case :
    #premiere case boolean true si les coins sont bien fait false sinon
    #deuxieme case : tableau à trois dimension chaque case represente un coin mal placé avec
    #[[face ou doit etre la couleur de gauche,couleur gauche],[face ou doit etre la couleur de droite,couleur droite]]
    # si tout est bien placé on aura
    # [ True ,[] ]
    def checkCorner(self,nameFace):
        tmp=[True,[]]
        colorcorner=self.cube.getCentralColor(nameFace)
        m=self.cube.getMouv(nameFace.upper())
        for x in range (4):
            colorPrev=self.cube.getCentralColor(m[1][(x+3)%4][0])
            colorNext=self.cube.getCentralColor(m[1][x][0])
            

            result=self.cube.findCube([colorcorner,colorPrev,colorNext],nameFace)
            
            if(result==-1 or result[1][1]!=m[1][(x+3)%4][0] or result[2][1]!=m[1][x][0] ):
                tmp[1]+=[[[m[1][(x+3)%4][0],colorPrev],[m[1][x][0],colorNext]]]
                #[[face ou doit etre la couleur de gauche,couleur gauche],[face ou doit etre la couleur de droite,couleur droite]] 


                tmp[0]=False
                
        return tmp

    #the corner permet de faire les coin d'une face sans prendre en compte se qu'elle fait sur les autre face
    def theCorner(self,nameFace):
        tab=self.checkCorner(nameFace)
        colorCorner=self.cube.getCentralColor(nameFace)
        inv=self.cube.getFaceInversed(nameFace)

        
        if(tab[0]==True):
        #si les coins sont bien placé on ne fait rien
            
            return 0
        else :
            
            for idx, x in enumerate (tab[1]) :
            #pour chaque coins mal placés
                   
                    
                tmp=self.cube.findCube([colorCorner,x[0][1],x[1][1]])
                #on trouve le cube à replacer corectement
                
                
                if (tmp[0][1] != inv):
                #si la couleur de la face à aranger n'est pas à l'opposer de où elle devrait etre (cas les plus simple)
                
                    for i in range (0,2) :
                    #on regarde quelle couleur est donc à l'opposé les rotation change selon celle ci c'est pour ça qu'il y à cette boucle
                        
                        if (tmp[1+i][1] == inv):
                            #la couleur choisi est bien à l'opposé de la face à aranger
                            
                            m=self.cube.getMouv(tmp[2-i][1].upper())
                            if (tmp[0][1] == m[1][1][0]):
                                #si la couleur de la face à aranger est à la droite de la dernière couleur faire c'est rotation
                                self.rotation(self.getApproRot(tmp[0][1],self.cube.getFaceInversed(x[1-i][0]),inv))
                                self.rotation(x[1-i][0].upper())
                                self.rotation(self.getInvRot(inv.upper()))
                                self.rotation(self.getInvRot(x[1-i][0].upper()))
                                
                            else :
                                #si la couleur de la face à aranger est à la gauche de la dernière couleur faire c'est rotation
                                self.rotation(self.getApproRot(tmp[0][1],self.cube.getFaceInversed(x[1-i][0]),inv))

                                self.rotation(self.getInvRot(x[1-i][0].upper()))
                                self.rotation(inv.upper())
                                self.rotation(x[1-i][0].upper())
                else :
                    #si la couleur de la face à aranger est à l'opposer de où elle devrait etre
                    
                    self.rotation(self.getApproRot(tmp[1][1],x[1][0],inv))
                    m=self.cube.getMouv(tmp[1][1].upper())

                    if tmp[2][1] == m[1][1][0] :
                        self.rotation(self.getInvRot(x[0][0].upper()))
                        self.rotation(inv.upper()+"2")
                        self.rotation(x[0][0].upper())
                        self.rotation(inv.upper())             
                        self.rotation(self.getInvRot(x[0][0].upper()))
                        self.rotation(self.getInvRot(inv.upper()))
                        self.rotation(x[0][0].upper())
                    else :
                        self.rotation(self.getInvRot(x[1][0].upper()))
                        self.rotation(inv.upper()+"2")
                        self.rotation(x[1][0].upper())
                        self.rotation(inv.upper())             
                        self.rotation(self.getInvRot(x[1][0].upper()))
                        self.rotation(self.getInvRot(inv.upper()))

                        self.rotation(m[1][1][0].upper())


   
                
                    
        
   

                        self.rotation(x[1][0].upper())
            tab=self.checkCorner(nameFace)
            if(tab[0]==True):
                #on vérifie si les rotation que l'on à fait on suffit
                #c.a.d qu'aucun des cube mal placé est été sur la couronne de la face à modifier
                
                return 0
            else :
                for idx, x in enumerate (tab[1]) :
                    
                    tmp=self.cube.findCube([colorCorner,x[0][1],x[1][1]])
                    #on trouve les cubes manquant 
                    
                    for i in range (3) :
                        if tmp[i][1] == nameFace :
                            #ontrouve la face étant sur la face à modifier
                            
                            mtp=self.cube.getMouv(tmp[(i+1)%3][1].upper())


                            #on va placer le cube pour qu'il soit sur la couronne opposer de là ou il est et qu'il puisse ainsi etre traiter par theCorner

                            if tmp[(i+2)%3][1] == mtp[1][1][0] :
                                self.rotation(tmp[(i+1)%3][1].upper())
                                self.rotation(inv.upper())
                                self.rotation(self.getInvRot(tmp[(i+1)%3][1].upper()))
                            else:
                                self.rotation(tmp[(i+2)%3][1].upper())
                                self.rotation(inv.upper())
                                self.rotation(self.getInvRot(tmp[(i+2)%3][1].upper()))
                    i=(len(tab[1]))        
                self.theCorner(nameFace)
                #on envoie la récursivité et normalement ça doit bien placé le cube deplacer sur la couronne opposer
                        
                                
            
                                
                
                

    def rfjaune(self):
        cube=self.cube
       
        j=cube.down
        r=cube.front
        b=cube.right
        g=cube.left
        o=cube.back
        if not cube.faceFinished('d') :
          
            if b[2][2]==j[1][1] and r[2][0]==b[2][2] and j[0][2]==b[2][2] and j[2][0]==b[2][2] and j[2][2]!=b[2][2] and j[0][0]!=b[2][2]:
                self.applyCmd("F'RFL'F'R'FL")
                
            elif b[2][0]==j[1][1] and b[2][2]==b[2][0] and j[0][0]==b[2][0] and j[2][0]==b[2][0]   and j[2][2]!=b[2][0]  and j[0][2]!=b[2][0] :
                self.applyCmd("F2UF'D2FU'F'D2F'")
                
            elif b[2][0]==j[1][1] and r[2][0]==b[2][0] and j[2][2]==b[2][0]  and j[0][0]!=b[2][0] and j[0][2]!=b[2][0]  and j[2][0]!=b[2][0]:
                self.applyCmd("FDF'DFD2F'")
                
            elif r[2][0]==j[1][1] and j[0][2]== r[2][0]  and j[2][2]== r[2][0]   and j[2][0]!= r[2][0]  and j[0][0]!= r[2][0] :
                self.applyCmd("F'R'FL'F'RFL")
                

            elif r[2][2]==j[1][1] and b[2][2]==r[2][2] and j[0][0]==r[2][2] and j[2][2]!=r[2][2] and j[2][0]!=r[2][2] and j[0][2]!=r[2][2]:
                self.applyCmd("FD2F'D'FD'F'")
                
            elif r[2][2]==r[2][0] and r[2][2]==j[1][1] and  j[0][0]!=r[2][0] and j[0][2]!=r[2][0] and j[2][0]!=r[2][0] and j[2][2]!=r[2][0] :
                self.applyCmd("BD2B2D'B2D'B2D2B")
                
                
            elif j[1][1]==b[2][0] and j[0][0]!=b[2][0] and j[0][2]!=b[2][0] and j[2][0]!=b[2][0] and j[2][2]!=b[2][0] and r[2][0]!=r[2][2] and b[2][0]!=b[2][2] and g[2][0]!=g[2][2] and o[2][0]!=o[2][2] :
                self.applyCmd("FD2F2D'F2D'F2D2F")
                
            else :
                self.rotation('D')       
            self.rfjaune()
            
        else :
            return 1        
    
############## PARTIE 2ND COURONNE #################################

    def checkscdcouronne(self):
        
        f = self.cube.getCentralColor('f')
        r = self.cube.getCentralColor('r')
        b = self.cube.getCentralColor('b')
        l = self.cube.getCentralColor('l')

        if self.cube.front[1] == [f,f,f] and self.cube.right[1] == [r,r,r] and self.cube.back[1] == [b,b,b] and self.cube.left[1] == [l,l,l]:
            return True
        else:
            return False

    def deuxcubeinv(self):
        #si 2 cubes sont inversé sur une 2 face opposées
        a = 0
        self.majcube()

        #si le cube bleu/rouge inversé avec le vert/rouge
        if (self.br[0][1] == 'l' and self.vr[0][1] == 'r') or (self.br[0][1] == 'f' and self.vr[0][1] == 'f') or (self.br[0][1] == 'l' and self.vr[0][1] == 'f') or (self.br[0][1] == 'f' and self.vr[0][1] == 'r'):
            a = "F"
        #si le cube bleu/rouge inversé avec le bleu/orange
        elif (self.br[1][1] == 'b' and self.bo[1][1] == 'f') or (self.br[1][1] == 'r' and self.bo[1][1] == 'r') or (self.br[1][1] == 'b' and self.bo[1][1] == 'r') or (self.br[1][1] == 'r' and self.bo[1][1] == 'f'):
            a = "R"
        #si le cube vert/orange inversé avec le bleu/orange
        elif (self.vo[0][1] == 'r' and self.bo[0][1] == 'l') or (self.vo[0][1] == 'b' and self.bo[0][1] == 'b') or (self.vo[0][1] == 'r' and self.bo[0][1] == 'b') or (self.vo[0][1] == 'b' and self.bo[0][1] == 'l'):
            a = "B"
        #si le cube vert/orange inversé avec le vert/rouge
        elif (self.vo[1][1] == 'f' and self.vr[1][1] == 'b') or (self.vo[1][1] == 'l' and self.vr[1][1] == 'l') or (self.vo[1][1] == 'f' and self.vr[1][1] == 'l') or (self.vo[1][1] == 'l' and self.vr[1][1] == 'b'):
            a = "L"
        if a!= 0:
            self.rotation(str(a)+str(2))
            self.rotation("D2")
            self.rotation(str(a)+str(2))
            self.rotation("D2")
            self.rotation(str(a)+str(2))

#si le cube est au bon endroit mais les couleurs sont inversés
    def cubeinv(self):
        #si cube au bon endroit mais couleurs inversées
        self.majcube()
        a = 0
        b = 0
        
        if self.br[0][1] == 'f' and self.br[1][1] == 'r':
            a = "F"
            b = "R"
        if self.vr[0][1] == 'f' and self.vr[1][1] == 'l':
            a = "L"
            b = "F"
        if self.vo[0][1] == 'b' and self.vo[1][1] == 'l':
            a = "B"
            b = "L"
        if self.bo[0][1] == 'b' and self.bo[1][1] == 'r':
            a = "R"
            b = "B"
        if a != 0:
            self.rotation(str(a))
            self.rotation("D")
            self.rotation(str(a)+"'")
            self.rotation("D2")
            self.rotation(str(a))
            self.rotation("D2")
            self.rotation(str(a)+"'")
            self.rotation("D")
            self.rotation(str(b)+"'")
            self.rotation("D'")
            self.rotation(str(b))
            
#fonction finale pour la deuxième couronne regroupant toutes les méthodes    
    def deuxcouronne(self):
        self.majcube()
        while self.checkscdcouronne()== False:
            while self.br[0][1] == 'd' or self.br[1][1] == 'd' or self.vr[0][1] == 'd' or self.vr[1][1] == 'd' or self.vo[0][1] == 'd' or self.vo[1][1] == 'd' or self.bo[0][1] == 'd' or self.bo[1][1] == 'd':
                self.deuxiemecouronne()
            if self.checkscdcouronne():
                break
            self.cubeinv()
            if self.checkscdcouronne():
                break
            self.deuxcubeinv()
            if self.checkscdcouronne():
                break
            if self.a == 4:
                self.a=0
            self.cubeinvenface()
    
#cette fonction permet de récupérer l'emplacement des cubes en coins de la deuxième couronne
#elle est utilisée en mise à jour lorsqu'il y a eu des changements sur le cube
    def majcube(self):
        #recupère la couleur des faces left, right, front, back
        f = self.cube.getCentralColor('f')
        r = self.cube.getCentralColor('r')
        b = self.cube.getCentralColor('b')
        l = self.cube.getCentralColor('l')
        #recupère les 4 coins de la deuxieme couronne, la couleur n'a pas d'importance. Les couleurs en commentaire sont la pour une meilleure visualisation
        self.br = self.cube.findCube([r, f]) #cube bleu/rouge
        self.vr = self.cube.findCube([l, f]) #vert/rouge
        self.vo = self.cube.findCube([l, b]) #cube vert/orange
        self.bo = self.cube.findCube([r, b]) #cube bleu/orange
        
#cette fonction permet de débloquer des situations rares dans la dispositions des 4 coins de la 2eme couronne
    def cubeinvenface(self):
        #si le cube vert/rouge est inversé avec le cube bleu/orange
        #if (self.bo[0][1] == 'l' or self.bo[0][1] == 'f') and (self.vr[0][1] == 'r' or self.vr[0][1] == 'b'):
        if self.a == 0:
            self.rotation("D")
            self.rotation("L")
            self.rotation("D'")
            self.rotation("L'")
            self.rotation("D'")
            self.rotation("F'")
            self.rotation("D")
            self.rotation("F")

        #si le cube vert/orange est inversé avec le cube bleu/rouge
        #elif (self.vo[0][1] == 'f' or self.vo[0][1] == 'r') and (self.br[0][1] == 'l' or self.br[0][1] == 'b'):
        if self.a == 1:
            #on doit faire basculer le cube a gauche/ au dessus du rouge
            self.rotation("D'")
            self.rotation("R'")
            self.rotation("D")
            self.rotation("R")
            self.rotation("D")
            self.rotation("F")
            self.rotation("D'")
            self.rotation("F'")
            
        if self.a == 2:
            self.rotation("D")
            self.rotation("R")
            self.rotation("D'")
            self.rotation("R'")
            self.rotation("D'")
            self.rotation("B'")
            self.rotation("D")
            self.rotation("B")

        self.a += 1

    def deuxiemecouronne(self):
    #regarder les 4 coins au dessus et si il n'y a pas de jaune la bouger au bon endroit
            #cube bleu/rouge
            self.majcube()
            #on remet le cube bleu/rouge sur sa face correspondante 
            if self.br[0][1] == 'd':  #ici le cube bleu est sur la face down
                if self.br[1][1] == 'l':
                    self.rotation("D")
                    
                elif self.br[1][1] == 'b':
                    self.rotation("D2")
                    
                elif self.br[1][1] == 'r':
                    self.rotation("D'")
                    
                #on doit faire basculer le cube a gauche/ au dessus du rouge
                self.rotation("D'")
                self.rotation("R'")
                self.rotation("D")
                self.rotation("R")
                self.rotation("D")
                self.rotation("F")
                self.rotation("D'")
                self.rotation("F'")
                    
            elif self.br[1][1] == 'd': #ici le cube rouge est sur la face down
                if self.br[0][1] == 'f':
                    self.rotation("D")
                    
                elif self.br[0][1] == 'l':
                    self.rotation("D2")
                    
                elif self.br[0][1] == 'b':
                    self.rotation("D'")
                    
                #on doit faire basculer le cube a droite
                self.rotation("D")
                self.rotation("F")
                self.rotation("D'")
                self.rotation("F'")
                self.rotation("D'")
                self.rotation("R'")
                self.rotation("D")
                self.rotation("R")

            
            #cube vert/rouge
            #on remet le cube vert/rouge sur sa face correspondante
            if self.vr[0][1] == 'd':  #ici le cube vert est sur la face down
                
                if self.vr[1][1] == 'l':
                    self.rotation("D")
                    
                elif self.vr[1][1] == 'b':
                    self.rotation("D2")
                    
                elif self.vr[1][1] == 'r':
                    self.rotation("D'")
                    
                #on doit faire basculer le cube a droite
                self.rotation("D")
                self.rotation("L")
                self.rotation("D'")
                self.rotation("L'")
                self.rotation("D'")
                self.rotation("F'")
                self.rotation("D")
                self.rotation("F")
                
            elif self.vr[1][1] == 'd': #ici le cube rouge est sur la face down
                
                if self.vr[0][1] == 'f':
                    self.rotation("D'")
                    
                elif self.vr[0][1] == 'r':
                    self.rotation("D2")
                    
                elif self.vr[0][1] == 'b':
                    self.rotation("D")
                    
                #on doit faire basculer le cube a gauche
                self.rotation("D'")
                self.rotation("F'")
                self.rotation("D")
                self.rotation("F")
                self.rotation("D")
                self.rotation("L")
                self.rotation("D'")
                self.rotation("L'")

            #cube vert/orange
            #on remet le cube vert/orange sur sa face correspondante 
            if self.vo[0][1] == 'd':  #ici le cube vert est sur la face down
                if self.vo[1][1] == 'f':
                    self.rotation("D2")
                    
                elif self.vo[1][1] == 'l':
                    self.rotation("D'")

                elif self.vo[1][1] == 'r':
                    self.rotation("D")
                    
                #on doit faire basculer le cube a gauche
                self.rotation("D'")
                self.rotation("L'")
                self.rotation("D")
                self.rotation("L")
                self.rotation("D")
                self.rotation("B")
                self.rotation("D'")
                self.rotation("B'")
                
            elif self.vo[1][1] == 'd': #ici le cube orange est sur la face down
                if self.vo[0][1] == 'f':
                    self.rotation("D'")
                    
                elif self.vo[0][1] == 'r':
                    self.rotation("D2")
                    
                elif self.vo[0][1] == 'b':
                    self.rotation("D")

                #on doit faire basculer le cube a droite
                self.rotation("D")
                self.rotation("B")
                self.rotation("D'")
                self.rotation("B'")
                self.rotation("D'")
                self.rotation("L'")
                self.rotation("D")
                self.rotation("L")

            #cube bleu/orange
            #on remet le cube bleu/orange sur sa face correspondante 
            if self.bo[0][1] == 'd':  #ici le cube bleu est sur la face down
                if self.bo[1][1] == 'f':
                    self.rotation("D2")
                    
                elif self.bo[1][1] == 'l':
                    self.rotation("D'")

                elif self.bo[1][1] == 'r':
                    self.rotation("D")
                    #on doit faire basculer le cube a droite
                self.rotation("D")
                self.rotation("R")
                self.rotation("D'")
                self.rotation("R'")
                self.rotation("D'")
                self.rotation("B'")
                self.rotation("D")
                self.rotation("B")
            
            elif self.bo[1][1] == 'd': #ici le cube orange est sur la face down
                if self.bo[0][1] == 'f':
                    self.rotation("D")

                elif self.bo[0][1] == 'b':
                    self.rotation("D'")
                    
                elif self.bo[0][1] == 'l':
                    self.rotation("D2")
                    
                #on doit faire basculer le cube a gauche
                self.rotation("D'")
                self.rotation("B'")
                self.rotation("D")
                self.rotation("B")
                self.rotation("D")
                self.rotation("R")
                self.rotation("D'")
                self.rotation("R'") 

############## PARTIE 2ND COURONNE #################################
        

############## PARTIE CROIX JAUNE #################################

#Dans la suite de l'algorithme, lorsque les fonctions font référence à la face jaune, il s'agit de la face sur laquelle nous utilisons notre algorithme, soit celle opposée à la face Up, donc Down.

#Fonction qui renvoie quelle face est de la couleur recherchée
#On compare avec la couleur de chaque face en [1][1] et donc au milieu
#Fonction plus utilisée à la fin car on se base directement sur la face Down
    def whichIsColor(self,color):

        colorF = self.cube.up[1][1]  
        if colorF == color :
            return "u"

        colorF = self.cube.down[1][1]
        if colorF == color :
            return "d"

        colorF = self.cube.right[1][1]
        if colorF == color :
            return "r"

        colorF = self.cube.left[1][1]
        if colorF == color :
            return "l"

        colorF = self.cube.back[1][1]
        if colorF == color :
            return "b"

        colorF = self.cube.front[1][1]
        if colorF == color:
            return "f"


            
#Fonction qui vérifie si la croix non orienté est vérifiée
    def checkCrossNonOriente(self):
        posColor = 'd'   #on trouve la position de la face jaune // au final on va se baser sur la base Down dans tous les cas
        listeColors=[self.cube.getCentralColor('f'),self.cube.getCentralColor('b'),self.cube.getCentralColor('r'),self.cube.getCentralColor('l')]       #c'est la liste des couleurs composants les aretes avec une face jaune
        for i in range(len(listeColors)):   #on parcout la liste des couleurs
            pos = self.cube.findCube([self.cube.getCentralColor('d'),listeColors[i][0][0]]) #on récupère la position des aretes
            if pos[0][1] != posColor:   #si la position de la face jaune des aretes n'est pas sur la face jaune, alors la croix n'est pas vérifiée
                return False
        return True


#on récupère l'emplacement des aretes entre la face Down et les faces adjacentes
    def checkEmplacement(self):
        posColor = 'd'
        listeColors=[self.cube.getCentralColor('f'),self.cube.getCentralColor('b'),self.cube.getCentralColor('r'),self.cube.getCentralColor('l')]
        listos=[]
        liste=[]
        for i in range(len(listeColors)):
            #plutot que leur couleur ; on va mettre la position de la couleur
            listos=[]
            pos = self.cube.findCube([self.cube.getCentralColor('d'),listeColors[i][0][0]])
            listos.append(pos[0][1])
            listos.append(pos[1][1])
            liste.append(listos)    
            #liste contenant les listes des arêtes avec (1) : sur quelle face se trouve la partie Y de l'arete et (2) : de quelle couleur est l'autre partie
        return liste

#fonction qui renvoie la face opposée, mais en majuscule pour éviter de devoir utiliser la fonction .upper() par la suite
    def opposite(self,face):
        if face == 'u':
            return 'D'
        elif face == 'd':
            return 'U'
        elif face == 'r':
            return 'L'
        elif face == 'l':
            return 'R'
        elif face == 'f':
            return 'B'
        elif face == 'b':
            return 'F'

#fonction qui renvoie les faces a utiliser pour le cas 1 de la résolution croix jaune
    def case1(self):
        posY='d'
        index=['u','d','f','b','r','l']         #l'index servait ici dans le cas de posY différent de Down, mais nous ne l'avons pas utilisé au final
        liste=[['F','U','R'],['F','D','L'],['D','F','R'],['U','B','R'],['F','R','D'],['F','L','U']]
        return liste[index.index(posY)]

#fonction qui renvoie les deux aretes dans le bon ordre pour le cas 2 de la croix jaune
    def case2(self,pos1,pos2):
    
        posY = 'd'
        index=['u','d','f','b','r','l']         #l'index servait ici dans le cas de posY différent de Down, mais nous ne l'avons pas utilisé au final
        liste=[['L','B','R','F'],['R','B','L','F'],['L','U','R','D'],['R','U','L','D'],['F','U','B','D'],['B','U','F','D']] #chaque liste correspond a un index respectif

        ind=index.index(posY)
        a=liste[ind].index(pos1.upper())
        b=liste[ind].index(pos2.upper())
        if a > b:
            if liste[ind][(a+1)%4] != pos2.upper() or a < 3:
                return [pos1,pos2]
            else:
                return [pos2,pos1]                  #L'ordre de renvoie est utile pour la résolution qui suit l'utilisation de cette fonction
        else:
            if liste[ind][(b+1)%4] != pos1.upper() or b <3:
                return [pos2,pos1]
            else:
                return [pos1,pos2]


#fonction qui renvoie les deux aretes dans le bon ordre pour le cas 3 de la croix jaune
    def case3(self,pos1):

        posY='d'
        index=['u','d','f','b','r','l']         #Comme pour les autres, on avait un index pour les différents cas up, down, etc... mais non utilisé
        liste=[['L','B','R','F'],['R','B','L','F'],['L','U','R','D'],['R','U','L','D'],['F','U','B','D'],['B','U','F','D']]
        listeDroite=[['F','R','B','L'],['F','L','B','R'],['R','U','L','D'],['R','D','L','U'],['D','B','U','F'],['D','F','U','B']]
        ind = index.index(posY)
        ind1 = liste[ind].index(pos1.upper())
        ind2 = listeDroite[ind].index(liste[ind][(ind1+1)%4])
        return [liste[ind][(ind1+1)%4] , listeDroite[ind][(ind2+1)%4] , posY.upper()]


    def resolutionCroixJaune(self):
        

        posY='d'

        #adj : lorsque on passe d'une des deux faces a l'autre par une simple rotation

        dicAdj = [['u','r'],['l','u'],['r','d'],['d','l'],['l','f'],['b','l'],['r','b'],['f','r']]

        #tant que la croix jaune n'est pas vérifiée
        while self.checkCrossNonOriente() != True:

            
            adj=False

            #on récupère la position des aretes jaunes qui sont sur la face jaune
            liste=self.checkEmplacement()   
            #liste contenant le placement des aretes dont la partie jaune est déjà sur la face jaune
            listeAretes=[]

            #on récupère la position des aretes dont la partie jaune est sur la face jaune
            for i in range(len(liste)):
                #si la partie jaune de l'arete est sur la face jaune
                if liste[i][0] == 'd':
                    #alors on récupère l'emplacement de la partie de l'autre couleur
                    listeAretes.append(liste[i][1])
            #si il n'y a que la case jaune du milieu

            if len(listeAretes) == 0 or len(listeAretes) == 3 or len(listeAretes)==1:

                # CAS 1

                tmp = self.case1()

                self.rotation(tmp[0])
                self.rotation(tmp[1])
                self.rotation(tmp[2])      
                self.rotation(tmp[1]+"'")
                self.rotation(tmp[2]+"'")
                self.rotation(tmp[0]+"'")
                
                    

                    # D F R Fi Ri Di
                    #on prend n'import lequel balek

                # F U R Ui Ri Fi
            if len(listeAretes) == 2:

                #Cas si les aretes sont 'adjacentes'
                for i in range(len(dicAdj)):

                    if listeAretes[0] in dicAdj[i] and listeAretes[1] in dicAdj[i]: #On vérifie qu'on est dans le cas de l'adjacence
                        adj = True

                if adj == True :    #CAS 2

                    tmp = self.case2(listeAretes[0],listeAretes[1])   #on récupère les aretes dans le bon ordre pour notre algorithme
                    #on applique les rotations par rapport aux bonnes faces du coup
                    self.rotation(self.opposite(tmp[0]))
                    self.rotation(posY.upper())
                    self.rotation(self.opposite(tmp[1]))
                    self.rotation(posY.upper() + "'")
                    self.rotation(self.opposite(tmp[1])+"'")
                    self.rotation(self.opposite(tmp[0])+"'")

                        # F U R Ui Ri Fi
                else :      #CAS 3
                    tmp = self.case3(listeAretes[0])
                    
                    self.rotation(tmp[0])
                    self.rotation(tmp[1])
                    self.rotation(tmp[2])
                    self.rotation(tmp[1]+"'")    
                    self.rotation(tmp[2]+"'")
                    self.rotation(tmp[0]+"'")

                        # F R U Ri Ui Fi




############## PARTIE CROIX JAUNE #################################            

## ETAPE 6 & 7 : FIN ##
    
    
    def lastStep(self) :
        if self.cube.cubeFinished() == False :
            # Récupération des différentes variables nécéssaire à la résolution
            faceJaune = self.getFaceJaune()
            tabLiFaceChange = self.getTabLiFaceChange(faceJaune)

            #Test si tout est bien placé (si c'est le cas on effectue une seule rotation et le cube est fini)
            faceTest = tabLiFaceChange[0]
            if faceJaune == 'u' :
                index = 0
            elif faceJaune == 'd' :
                index = 2

            counter = 0
            for i in tabLiFaceChange :
                if self.cube.getFace(i)[index][0] == self.cube.getFace(i)[index][1] == self.cube.getFace(i)[index][2] :
                    counter += 1
            if counter == 4 :
                for i in range(3) :
                    if self.cube.getCentralColor(tabLiFaceChange[i+1]) == self.cube.getFace(faceTest)[index][0] :
                        faceDest = tabLiFaceChange[i+1]

                self.rotation(self.getApproRot(faceTest,faceDest,faceJaune))
                return
            #Test si ...
            
            tabParc = self.getTabParc(faceJaune)

            # Résolution des coins et des arrêtes
            self.putCornerLastFace(faceJaune, tabParc, tabLiFaceChange)
            
        if self.cube.cubeFinished() == False :
            self.putAreteLastFace(faceJaune, tabParc, tabLiFaceChange)

    def getFaceJaune(self) :
        faceBlanche = ''
        faceJaune = ''

        # On trouve les deux face "finies" pour savoir quelles faces modifier par la suite
        for face in self.cube.liFace :
            faceBlanche = face
            faceJaune = self.cube.getFaceInversed(face)
            if self.cube.faceFinished(faceBlanche) and self.cube.faceFinished(faceJaune):
                break

        # Si les deux faces sont inversé
        counter = 0
        tabTemp = []
        for i in self.cube.liFace :
            if i != 'u' and i != 'd' :
                faceTest = self.cube.getFace(self.cube.liFace[(self.cube.liFace.index(i)+2)%6])
                if (faceJaune == 'u' and faceTest[0][0] == faceTest[0][1] == faceTest[0][2] == faceTest[1][1]) or ((faceJaune == 'd') and faceTest[2][0] == faceTest[2][1] == faceTest[2][2] == faceTest[1][1]) :
                    counter += 1

        if counter == 4 :
            temp = faceJaune
            faceJaune = faceBlanche
            faceBlanche = temp

        return faceJaune
        
    def getTabParc(self, faceJaune) :
        # TabParc va nous servir à parcourir le cube pour trouver les cubes inversés en fonction des 4 faces à finir
        if faceJaune == 'u' :
            tabParc = [0,'x']
            
        elif faceJaune == 'd' :
            tabParc = [2,'x']
            
        elif faceJaune == 'l' or 'f' :
            tabParc = ['x',0]
            
        elif faceJaune == 'r' or 'b' :
            tabParc = ['x',2]

        return tabParc

    def getTabLiFaceChange(self, faceJaune) :
        # Ce tableau contient les face non finies, il va nous permettre de nous afranchir des couleurs
        # car les mouvements à faire pour résoudre le cube sont symétrique
        if faceJaune == 'd' or faceJaune == 'u' :
            return ['l','f','r','b']
        elif faceJaune == 'l' or faceJaune == 'r' :
            return ['f','u','b','d']
        else :
            return ['d','r','u','l']
        
    def putCornerLastFace(self, faceJaune, tabParc, tabLiFaceChange) :
       
        tabMiniReplace = []
        
        #A ce niveau de résolution il est possible de bien placer deux coins,
        #donc tant que je n'obtient pas seulement deux coins mal placés :
        while len(tabMiniReplace) != 4 :
            tabMiniReplace = []
            for i in range(4) :
                faceEnCours = self.cube.getFace(tabLiFaceChange[i])
                if tabParc[0] != 'x' :
                    if faceEnCours[tabParc[0]][0] != faceEnCours[(tabParc[0]+1)%2][0] :
                        tabMiniReplace.append([i,tabParc[0],0])
                    if faceEnCours[tabParc[0]][2] != faceEnCours[(tabParc[0]+1)%2][2] :
                        tabMiniReplace.append([i,tabParc[0],2])
                else :
                    if faceEnCours[0][tabParc[1]] != faceEnCours[0][(tabParc[1]+1)%2] :
                        tabMiniReplace.append([i,0,tabParc[1]])
                    if faceEnCours[2][tabParc[1]] != faceEnCours[2][(tabParc[1]+1)%2] :
                        tabMiniReplace.append([i,2,tabParc[1]])
            # Si les coins sont déjà tous bien placés
            if len(tabMiniReplace) == 0 :
                return
            #(suite) je tourne la face "Jaune" (non résolue)
            if len(tabMiniReplace) != 4 :
                self.rotation(faceJaune.upper())

        # cas 1 : les deux cubes à intervertir sont sur la même face
        # cas 2 : les deux cubes à intervertir sont des coins opposés
        cas1 = False
        for i in range(4):
            if tabMiniReplace[i][0] == tabMiniReplace[(i+1)%4][0] or tabMiniReplace[i][0] == tabMiniReplace[(i+2)%4][0] or tabMiniReplace[i][0] == tabMiniReplace[(i+3)%4][0] :
                cas1 = True
                faceChange = tabMiniReplace[i][0]
                break

        if faceJaune == 'd' or faceJaune == 'r' or faceJaune == 'b' :
            sensRotation = 1
        else :
            sensRotation = -1

#CAS 1 : 
        if cas1 :
            self.rotation(tabLiFaceChange[faceChange].upper())
            self.rotation(faceJaune.upper())
            self.rotation(tabLiFaceChange[faceChange].upper()+'\'')
            self.rotation(faceJaune.upper()+'\'')
            self.rotation(tabLiFaceChange[faceChange].upper()+'\'')
            self.rotation(tabLiFaceChange[(faceChange+(1*sensRotation))%4].upper())
            self.rotation(tabLiFaceChange[faceChange].upper()+'2')
            self.rotation(faceJaune.upper()+'\'')
            self.rotation(tabLiFaceChange[faceChange].upper()+'\'')
            self.rotation(faceJaune.upper()+'\'')
            self.rotation(tabLiFaceChange[faceChange].upper())
            self.rotation(faceJaune.upper())
            self.rotation(tabLiFaceChange[faceChange].upper()+'\'')
            self.rotation(tabLiFaceChange[(faceChange+(1*sensRotation))%4].upper()+'\'')
        else :
            for i in range(4):
                if tabParc[0] != 'x' :
                    if tabMiniReplace[i][2] == 2 - tabParc[0] :
                        faceChange = tabMiniReplace[i][0]
                        break
                else : 
                    if tabMiniReplace[i][1] == tabParc[1] :
                        faceChange = tabMiniReplace[i][0]
                        break
#CAS 2 :
            self.rotation(tabLiFaceChange[faceChange].upper())
            self.rotation(tabLiFaceChange[(faceChange+(3*sensRotation))%4].upper())
            self.rotation(faceJaune.upper()+'\'') 
            self.rotation(tabLiFaceChange[(faceChange+(3*sensRotation))%4].upper()+'\'')
            self.rotation(faceJaune.upper()+'\'')
            self.rotation(tabLiFaceChange[(faceChange+(3*sensRotation))%4].upper())
            self.rotation(faceJaune.upper())
            self.rotation(tabLiFaceChange[(faceChange+(3*sensRotation))%4].upper()+'\'')
            self.rotation(tabLiFaceChange[faceChange].upper()+'\'')
            self.rotation(tabLiFaceChange[(faceChange+(3*sensRotation))%4].upper())
            self.rotation(faceJaune.upper())
            self.rotation(tabLiFaceChange[(faceChange+(3*sensRotation))%4].upper()+'\'')
            self.rotation(faceJaune.upper()+'\'')
            self.rotation(tabLiFaceChange[(faceChange+(3*sensRotation))%4].upper()+'\'')
            self.rotation(tabLiFaceChange[faceChange].upper())
            self.rotation(tabLiFaceChange[(faceChange+(3*sensRotation))%4].upper())
            self.rotation(tabLiFaceChange[faceChange].upper()+'\'')

    def putAreteLastFace(self, faceJaune, tabParc, tabLiFaceChange) :
        if faceJaune == 'd' or faceJaune == 'r' or faceJaune == 'b' :
            sensRotation = 1
        else :
            sensRotation = -1

        faceOpposeFinie = None
        for i in range(4) :
            if self.cube.faceFinished(tabLiFaceChange[i]) :
                faceOpposeFinie = self.cube.getFaceInversed(tabLiFaceChange[i])
                break

        if faceOpposeFinie != None :
            if tabParc[0] == 'x' :
                couleurMiniCube = self.cube.getFace(faceOpposeFinie)[1][tabParc[1]]
            else :
                couleurMiniCube = self.cube.getFace(faceOpposeFinie)[tabParc[0]][1]
                

            faceSuivanteOF = tabLiFaceChange[(tabLiFaceChange.index(faceOpposeFinie)+(1*sensRotation))%4]

            # CAS 2
            #R' U R' U' R' U' R' U R U R2
            if couleurMiniCube == self.cube.getCentralColor(self.cube.liFace[self.cube.liFace.index(faceSuivanteOF)]) :
                self.rotation(faceSuivanteOF.upper()+'\'')
                self.rotation(faceJaune.upper())
                self.rotation(faceSuivanteOF.upper()+'\'')
                self.rotation(faceJaune.upper()+'\'')
                self.rotation(faceSuivanteOF.upper()+'\'')
                self.rotation(faceJaune.upper()+'\'')
                self.rotation(faceSuivanteOF.upper()+'\'')
                self.rotation(faceJaune.upper())
                self.rotation(faceSuivanteOF.upper())
                self.rotation(faceJaune.upper())
                self.rotation(faceSuivanteOF.upper()+'2')

            # CAS 1
            # R2 U' R' U' R U R U R U' R
            else :
                self.rotation(faceSuivanteOF.upper()+'2')
                self.rotation(faceJaune.upper()+'\'')
                self.rotation(faceSuivanteOF.upper()+'\'')
                self.rotation(faceJaune.upper()+'\'')
                self.rotation(faceSuivanteOF.upper())
                self.rotation(faceJaune.upper())
                self.rotation(faceSuivanteOF.upper())
                self.rotation(faceJaune.upper())
                self.rotation(faceSuivanteOF.upper())
                self.rotation(faceJaune.upper()+'\'')
                self.rotation(faceSuivanteOF.upper())

        else :
            if tabParc[0] == 'x' :
                couleurMiniCube = self.cube.getFace(tabLiFaceChange[2])[1][tabParc[1]]
                index = 2
            else :
                couleurMiniCube = self.cube.getFace(tabLiFaceChange[0])[tabParc[0]][1]
                index = 0

            # CAS 1
            # M2 U M2 U2 M2 U M2           
            if couleurMiniCube == self.cube.getFace(self.cube.getFaceInversed(tabLiFaceChange[index]))[1][1] :
                # L2 + R2 = M2 ou B2 + F2 = M2 mais cela inverse la face haute et basse
                self.rotation(tabLiFaceChange[0].upper()+'2')
                self.rotation(tabLiFaceChange[2].upper()+'2')
                self.rotation(self.cube.getFaceInversed(faceJaune).upper())
                self.rotation(tabLiFaceChange[0].upper()+'2')
                self.rotation(tabLiFaceChange[2].upper()+'2')
                self.rotation(faceJaune.upper()+'2')
                self.rotation(tabLiFaceChange[0].upper()+'2')
                self.rotation(tabLiFaceChange[2].upper()+'2')
                self.rotation(self.cube.getFaceInversed(faceJaune).upper())
                self.rotation(tabLiFaceChange[0].upper()+'2')
                self.rotation(tabLiFaceChange[2].upper()+'2')

                self.nbCmd -= 4 

            # CAS 2
            # U R' U' R U' R U R U' R' U R U R2 U' R' U
            else :
                if self.cube.getFace(tabLiFaceChange[0])[2][1] == self.cube.getFace(tabLiFaceChange[1])[1][1] :
                    face = 0
                else :
                    face = 1
                
                self.rotation(faceJaune.upper())
                self.rotation(tabLiFaceChange[face].upper()+'\'')
                self.rotation(faceJaune.upper()+'\'')
                self.rotation(tabLiFaceChange[face].upper())
                self.rotation(faceJaune.upper()+'\'')
                self.rotation(tabLiFaceChange[face].upper())
                self.rotation(faceJaune.upper())
                self.rotation(tabLiFaceChange[face].upper())
                self.rotation(faceJaune.upper()+'\'')
                self.rotation(tabLiFaceChange[face].upper()+'\'')
                self.rotation(faceJaune.upper())
                self.rotation(tabLiFaceChange[face].upper())
                self.rotation(faceJaune.upper())
                self.rotation(tabLiFaceChange[face].upper()+'2')
                self.rotation(faceJaune.upper()+'\'')
                self.rotation(tabLiFaceChange[face].upper()+'\'')
                self.rotation(faceJaune.upper())
                
## ETAPE 6 & 7  : FIN  ##
                
def resolutionFinale(strcu="WWWWWWWWWGGGRRRBBBOOOGGGRRRBBBOOOGGGRRRBBBOOOYYYYYYYYY",entry=''):
    cube = Cube(strcu)
    resolution = Resolution(cube)
    resolution.applyCmd(entry)
    resolution.theCross('u')
    resolution.theCorner('u')
    resolution.deuxcouronne()
    resolution.resolutionCroixJaune()
    resolution.rfjaune()
    resolution.lastStep()
    return (resolution.liCmd)
