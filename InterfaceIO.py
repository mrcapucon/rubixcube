from Resolution import *
import random
import os
class InterfaceIO:

#classe qui gère les entrées sorties avec l'utilisateur
    
    def __init__(self, entree=None, sortie=None):
        self.entry=entree
        self.output=sortie
        self.path="D:/Projet Python RUBIK'S CUBE/Rubikcube_of_death_that_kill/"
        self.file="cube.txt"

#l'utilisateur entre dans le programme la position du cube de départ
        
    def getEntry(self):
        self.entry = input("Entrez la configuration du Rubik's Cube a résoudre :")
        
        #54 correspond au nombre de cases d'un rubik's cube
        while self.checkEntry() == False:
            print("Erreur, configuration impossible.")
            self.entry = input("Réessayez : ")

#vérifie que l'entrée contient le nombre de caractères nécessaires et les bons caracteres
            
    def checkEntry(self):
        carac=["B","R","Y","W","G","O"]
        n = len(self.entry)
#On vérifie que l'entrée contient 54 caracteres
        if len(self.entry) != n :
            return False
#On verifie que les caracteres entrés sont les bons
        for i in range(n):
            if self.entry[i] not in carac:
                return False
        return True
            
#crée un Liste de cube aléatoire sous la forme de chaine de caractères 
    
    def batCube(self,nbcube=1000):
        tCube=[]
        j=0
        while (j <= nbcube) :
        
            tab = ['U','L','R','B','D','F','U2','L2','R2','B2','D2','F2',]
            cube = Cube("WWWWWWWWWGGGRRRBBBOOOGGGRRRBBBOOOGGGRRRBBBOOOYYYYYYYYY")
         
            for i in range(random.randint(0,100)):
                mouv = tab[random.randint(0,11)]
                cube.rotation(mouv)
            strtmp=cube.getStr()
            
            if strtmp not in tCube :
                tCube.append(strtmp)
                j+=1
            
        
        writeTab(tCube,self.path,self.file)
               
        return tCube

    #fait une resolution pour chaque cube present dans la liste en entré
    def batTest(self,TCube=None):
        nbfini=0
        nbmvt=0
        Tfail=[]
        if(TCube==None):
            TCube=getCubeFile(self.path+self.file)
            print("nbcube à tester : ",len(TCube))
        for idi,i in enumerate (TCube) :
            self.output = resolutionFinale(i)
            if self.output[1]==True:
                nbfini+=1
            else :
                Tfail.append(i)
            nbmvt+=self.output[2]
            print("cube num : ",nbfini)
            print("moyfini : ",nbfini/(idi+1))
            print("moymvt : ",nbmvt/(nbfini))
            
#renvoie les mouvements a faire a l'utilisateur      
    def setOutput(self):
        self.output = resolutionFinale("WROWWOGYYGGRWGRGWWBBOGGOYRYBBWBORORBRWRBOOGGBWRYYYBYOY")
        print(self.output)
        
        

def writeInFile(strcu,path,new=False,ficName="cube.txt"):
    if(new==True):
        mode='w'
    else :
        mode ='a'
    os.chdir(path)
    fic = open(ficName,mode) 
    fic.write(strcu)
    fic.close()

def writeTab(tab,path,ficName="cube.txt"):
    new=True
    for x in tab :
        writeInFile(x+"\n",path,new,ficName)
        new=False

     
def getCubeFile(path):
    liCube=[]
    tmp=''

    fic = open(path, 'r') # url = fichier .txt
    data = fic.read()
    fic.close()
    data.replace('\n',' ') # Remplace le 2eme parametre par le character que tu
    #veut ou laisse comme ca pour juste supprimer
    data.split()
    for x in data:
        if(x=='\n'):
            cube = Cube(tmp)
            liCube+=[tmp]
            tmp=''
        else :
            tmp+=x   
    return liCube

    

        
#bonjour = InterfaceIO()
#bonjour.getEntry()

resolutionCube = InterfaceIO()


#batTestOfBatCube=resolutionCube.batCube(10000)

#batTestOfBatCube=resolutionCube.batCube(10000)

resolutionCube.batTest()
#resolutionCube.setOutput()
#batTestOfBatCube=resolutionCube.batCube(10)
#resolutionCube.batTest()
#resolutionCube.getEntry()
#resolutionCube.setOutput()

