import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import time
import bpy
import os
from pathlib import Path

class blenderObject():
    scale = 1
    radius = 2
    name = "undefined" #name of the blender object
    frameNb = 0
    framerate = 100 #besoin de savoir ça?

    def __init__(self, x, y, z, name="undefined", scene=None):
        self.position = np.array([x*self.scale, y*self.scale, z*self.scale])
        self.name = name
        self.scene = scene
        if scene is not None:
            if not self.name in bpy.data.objects:
                path = Path(os.getcwd()) / "blender" / f"{self.name}.dae"
                bpy.ops.wm.collada_import(filepath=str(path), import_units=False, keep_bind_info=False)
            
            self.blenderObj = bpy.data.objects[self.name]
            self.blenderObj.animation_data_clear()
        
            #place l'objet à son point de départ
            self.scene.frame_set(self.frameNb)
            self.blenderObj.location = tuple(self.position/self.scale)
            self.blenderObj.keyframe_insert(data_path="location", index=-1)
            self.blenderObj.animation_data.action.fcurves[-1].keyframe_points[-1].interpolation = 'LINEAR'
    
    def mouvementLocal(self, positionArray):
        if self.scene is not None:
            for position in positionArray:
                self.frameNb += 1
                self.scene.frame_set(self.frameNb)
                self.blenderObj.location = tuple(position+(self.position/self.scale))
                self.blenderObj.keyframe_insert(data_path="location", index=-1)
                self.blenderObj.animation_data.action.fcurves[-1].keyframe_points[-1].interpolation = 'LINEAR'
            
    def showBlender(self):
        self.blenderObj.location = tuple(self.position/self.scale)

    def show(self, fig, ax):
        ax.plot(self.position[0], self.position[1], "xr")




class sonar(blenderObject): 

    def __init__(self, x, y, z, name, scene):
        self.scale = 100
        super().__init__(x,y,z, name, scene)
        self.max_range = 4.5*self.scale #mètre
        self.angle = 30 # angle en degrées
        self.precision = 1*self.scale

        #vision du sonar
        largeur = np.int16(round(np.sin(np.radians(self.angle))*self.max_range, 2))
        milieu = np.int16((largeur)/2)+np.int16(0.04*self.scale) #le +0.04 pour être au milieu
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
                position_obj = obj.position[1]
                position_sonar = index[0]+self.position[1]
                if(self.collisionBound(position_obj, position_sonar) == True):
                    #vérification du y
                    position_obj = obj.position[0]
                    position_sonar = index[1]+self.position[0]
                    if(self.collisionBound(position_obj, position_sonar) == True):
                        #sleep pour simuler le temps réel
                        length = (index[0]**2 + index[1]**2)**0.5 #pythagore
                        C = 333.34 #m/s
                        time.sleep(2*(length/self.scale)/C)
                        return length/self.scale
        return -1 #dans la librairie, -1 est retourné s'il y a rien        

    def show(self, fig, ax):
        ax.set_title('sonar')
        ax.imshow(self.onde)



#load blender scene
scene = bpy.context.scene
if scene is not None:
    scene.render.fps = 100

objlist = []
objlist.append(blenderObject(0, 4, 0, scene=scene))

capteur_sonar = sonar(0, 0, 0, "vehicule", scene)

#L = capteur_sonar.Check(objlist)
#print(f"obstacle detecte a {L}m")

#capteur_sonar.avance(1, (10,2,0))
position = np.array([np.array([0.0]*3)]*100)
for x in np.linspace(0.01, 1, 100):
    position[int(x*100)-1] = np.array([x, -x, x*2])

capteur_sonar.mouvementLocal(position)


if scene is None:
    fig, ax = plt.subplots()
    capteur_sonar.show(fig, ax)

    for obj in objlist:
        obj.show(fig, ax)

    plt.show()
