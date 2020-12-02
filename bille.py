import numpy as np
import time
from threading import Thread


#plot le contenant

class bille2D():
    deltaH = -0.0015

    #constantes
    angle = np.radians(-4.3)
    g = -9.81
    m = 0.1 #estimé
    rayon = 0.02
    friction = 0.06

    #pour le thread
    vitesseBille = 0
    deltaHFinal = deltaH
    end = False

    def __init__(self, x, y, z, framerate):
        self.framerate = framerate
        if(x and y and z):
            raise Exception("Juste 2 dimensions à True")

        self.xRegister = x
        self.yRegister = y
        self.zRegister = z

    def nouveauDeltah(self, vitesse):
        deltah = ((vitesse**2)/(2*self.g))
        print(f"{deltah=}")
        return deltah

    def calculeVitesse(self, deltah):
        vitesse = ((self.g*2*deltah*(1-self.friction))**0.5)
        
        if(vitesse < 0.08):
            vitesse = 0
        print(f"{vitesse=}")
        return vitesse

    #retourne la vitesse maximal du véhicule pour préserver la bille.
    def calculVitesseMax(self):
        vMax = np.sqrt((2*self.g*self.m*-0.0015)/(0.97*self.m)) 
        return vMax

    #met à jour les paramètres d'accélération de la bille
    def appliqueAcceleration(self, vitesseVehicule, z):
        #retourne la vitesse de la bille selon le support du véhicule (C'est à dire un point fixe)
        self.vitesseBille = -vitesseVehicule
        #calcul du nouveau deltaH
        #step1: Calculer l'énergie cinétique de la bille
        #step2: Calculer l'élévation maximale que la bille aura
        self.deltaHFinal = self.nouveauDeltah(self.vitesseBille)
        self.directionX = 1

        if((self.deltaHFinal + z) > 0):
            print("Bille pu dans le moule")

    def corrigeErreur(self, x, z, hauteurMax, directionX, position):
        if(z > hauteurMax):
            position[2] = hauteurMax
            z = hauteurMax
        else:
            position[2] = self.deltaH
            z = self.deltaH
            if(self.xRegister):
                position[0] = 0.0
                x = 0.0
            else:
                position[1] = 0.0
                x = 0.0
        return x, z

    #Met à jour la position de la bille en fonction de la vitesse du véhicule
    def updatePosition(self,x, z, position):
        #position en Z de la bille
        #à l'extrémité, la bille doit se retourner dans l'autre sense.
        #self.vitesseBille = self.calculeVitesse()  #calcul la vitesse actuel
        deltaX = 0
        deltaZ = 0
        hauteurMax = self.deltaH-self.deltaHFinal
        if(z >= hauteurMax or z <= self.deltaH):
            x, z = self.corrigeErreur(x, z, hauteurMax, self.directionX, position)
            if(z <= self.deltaH):
                self.deltaHFinal =self.nouveauDeltah(self.vitesseBille)
                hauteurMax = self.deltaH-self.deltaHFinal

            #si self.z > deltaH, changer la direction en X
            if(z>=hauteurMax):
                self.directionX = -self.directionX

            #recalcule la vitesse en fonction de la hauteur maximale
            vitesse = self.calculeVitesse(self.deltaHFinal)
            #si vitesse était positive, devient négative
            if(self.vitesseBille > 0):
                self.vitesseBille = vitesse
                self.angle = self.angle
            else:
                self.vitesseBille = -vitesse
                self.angle = -self.angle
        
        viteseParFrame = self.vitesseBille/self.framerate
        deltaX = self.directionX * viteseParFrame * np.cos(self.angle)
        deltaZ = viteseParFrame * np.sin(self.angle)
        #step3: Valider que la bille est toujours dans le moule
        
        #step4: Calculer les keyframes de la bille
        return np.array([deltaX if self.xRegister else 0, deltaX if self.yRegister else 0, deltaZ if self.zRegister else 0])
    

class BilleMath():
    position = np.array([0, 0, -0.0015])
    billeXZ = bille2D(True, False, True, 100)
    billeYZ = bille2D(False, True, True, 100)
    vitesseAngulaire = 0

    def appliqueAcceleration(self, X_vitesse, Y_vitesse):
        self.billeXZ.appliqueAcceleration(X_vitesse, self.position[2])
        self.billeYZ.appliqueAcceleration(Y_vitesse, self.position[2])
    
    def appliqueRotation(self, vitesseAngulaire):
        raise Exception("à voir si pertinant")

    def updatePosition(self):
        offset1 = self.billeXZ.updatePosition(self.position[0], self.position[2], self.position)
        offset2 = self.billeYZ.updatePosition(self.position[1], self.position[2], self.position)
        self.position = self.position+offset1+offset2
        return self.position

def test():
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D


    vmax = np.sqrt(2*-9.81*-0.0015)

    #test
    print(f"vitesse vertical = {vmax*np.sin(np.radians(4.7))}")
    print(f"temps de montée = {0.0015/(vmax*np.sin(np.radians(4.7)))}")
    print(f"vitesse horizontal = {(vmax*np.cos(np.radians(4.7)))}")
    print(f"tempps de hor = {0.02/(vmax*np.cos(np.radians(4.7)))}")

    bille = BilleMath()
    bille.appliqueAcceleration(vmax*0.7, vmax*0.7)
    position = []
    for i in range(100*10):
        position.append(bille.updatePosition())
        print(position[-1])

    position = np.array(position)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    #plt.plot(position[:,0])
    ax.plot(position[:,0], position[:,1], position[:,2])
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    plt.show()
    #print(f"Vitesse en x = {vitesse[0]}")
    #print(f"Vitesse en y = {vitesse[1]}")
    #print(f"norme = {np.sqrt(vitesse[0]**2 + vitesse[1]**2)}")

#test() #pour afficher les graphiques, parcontre ça marche pas avec blender donc commenter