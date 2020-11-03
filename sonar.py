import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt


class blenderObject:
    x = 0
    y = 0
    z = 0
    radius = 0.5
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class sonar(blenderObject): 
    max_range = 4.5 #mètres
    angle = 30 # angle en radians
    precision = 0.1

    def Check(self):
        #remplir une matrice de point depuis l'origine

        largeur = np.int16(round(np.sin(np.radians(self.angle))*self.max_range, 2)*100)
        milieu = np.int16((largeur-1)/2)
        longueur = np.int16(self.max_range*100)

        self.onde = np.zeros((largeur, longueur))

        for angle_actuel in range(int(-self.angle/2), int(self.angle/2)):
            angleRad = np.radians(angle_actuel)
            nombre_de_step = np.int16(self.max_range/self.precision)
            for step in np.linspace(0, longueur-1, nombre_de_step, dtype=np.int16):
                step_x = np.int16(np.sin(angleRad)*step) + milieu
                step_y = np.int16(np.cos(angleRad)*step)
                self.onde[step_x][step_y] = 1

        #originbnp.array


    def show(self):
        fig, ax = plt.subplots()
        ax.set_title('sonar')
        ax.imshow(self.onde)
        plt.show()





obj = blenderObject(4, 1, 0)
obj = blenderObject(4, -1, 0)
obj = blenderObject(6, 0, 0)
capteur_sonar = sonar(0,0,0)
capteur_sonar.Check()
capteur_sonar.show()