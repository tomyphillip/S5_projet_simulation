import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import time

class blenderObject:
    x = 0
    y = 0
    z = 0
    scale = 100
    radius = 2
    def __init__(self, x, y, z):
        self.x = x*scale
        self.y = y*100
        self.z = z*100

    def show(self, fig, ax):
        ax.plot(self.x, self.y, "xr")



class sonar(blenderObject): 
    max_range = 450 #centimètres
    angle = 30 # angle en degrées
    precision = 10

    def __init__(self, x, y, z):
        super().__init__(x,y,z)

        #vision du sonar
        largeur = np.int16(round(np.sin(np.radians(self.angle))*self.max_range, 2))
        milieu = np.int16((largeur)/2)+4 #le +4 parce que
        longueur = np.int16(self.max_range)

        self.onde = np.zeros((largeur, longueur))

        for angle_actuel in range(int(-self.angle/2), int(self.angle/2)):
            angleRad = np.radians(angle_actuel)
            nombre_de_step = np.int16(self.max_range/self.precision)
            for step in np.linspace(0, longueur-1, nombre_de_step, dtype=np.int16):
                step_x = np.int16(np.sin(angleRad)*step) + milieu
                step_y = np.int16(np.cos(angleRad)*step)
                self.onde[step_x][step_y] = 1


    def collisionBound(self, position1, position2):
        return np.abs(position1-position2) < self.radius

    def Check(self, blenderObjectList):
        for obj in blenderObjectList:
            for index, value in np.ndenumerate(self.onde):
                position_obj = obj.y
                position_sonar = index[0]+self.y
                if(self.collisionBound(position_obj, position_sonar) == True):
                    #vérification du y
                    position_obj = obj.x
                    position_sonar = index[1]+self.x
                    if(self.collisionBound(position_obj, position_sonar) == True):
                        #sleep pour simuler le temps réel
                        length = (index[0]**2 + index[1]**2)**0.5 #pythagore
                        C = 333.34 #m/s
                        time.sleep(2*(length/100)/C)
                        return length
        return -1 #dans la librairie, -1 est retourné s'il y a rien

    def show(self, fig, ax):
        
        ax.set_title('sonar')
        ax.imshow(self.onde)




objlist = []
objlist.append(blenderObject(4, 0, 0))
objlist.append(blenderObject(4, -1, 0))
objlist.append(blenderObject(6, 0, 0))

fig, ax = plt.subplots()
capteur_sonar = sonar(0,0,0)
L = capteur_sonar.Check(objlist)

print(f"obstacle détecté à ${L/100}m")

capteur_sonar.show(fig, ax)

for obj in objlist:
    obj.show(fig, ax)

plt.show()