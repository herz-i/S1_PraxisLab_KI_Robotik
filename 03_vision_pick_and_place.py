#######################################################################################
### Trage hier den Port aus myBlockly ein.                                          ###
#######################################################################################

port = '/dev/tty.usbserial-588D0017891'

#######################################################################################
### Trage hier deine abgelesenen Punkte ein.                                        ###
#######################################################################################

# Wichtig! Das Format muss gleich bleiben, ersetze nur die 0 mit deinen Winkeln!

punkt_ablegen = [0, 0, 0, 0, 0, 0]                   # Ablageposition über der Box in Gelenkwinkeln

#######################################################################################
### Versuche hier die Geschwindigkeit und die Anzahl der Wiederholungen zu ändern.  ###
#######################################################################################

# Trage hier deinen Modellnamen ein. Die Datei muss im selben Verzeichnis wie dieses Skript liegen!

vision_modell = 'beispielmodell.pt'                  # 'modellname.pt'

#######################################################################################
### Ändere ab hier nichts mehr! Ansonsten funktioniert dein Programm danach nicht!  ###
#######################################################################################



import numpy as np
import time
from src.camera_input import LuxonisCamera
from src.object_detection import get_object_centers
from src.robot_control import Cobot
from src.coord_transform import get_transform_a_b

camera = LuxonisCamera()
robot = Cobot(port=port)
robot.power_on()
robot.home_position()
robot.out_of_the_way()
time.sleep(5)

# Get objects from picture frame and return objects with world coordinates
color_image = camera.get_image()
objects = get_object_centers(color_image, vision_modell)

print(objects)

for obj in objects:
    label, x1, x2, y1, y2 = obj
    world_coords = camera.get_world_coordinates(x1, x2, y1, y2)
    np_world_coords = np.array(world_coords)

    if world_coords:
        print(f"Object: {label}, World Coordinates: {world_coords}")
        base_coords = get_transform_a_b(np_world_coords)
        pos_des = base_coords[0]
        robot.ready_pos()
        try:
            robot.send_coord(1, pos_des[0], 50)
            robot.send_coord(2, pos_des[1], 50)
            time.sleep(5)
            robot.grip_object()
            robot.move_object_away(punkt_ablegen)
        except:
            print("Coordinate out of bounds!")

robot.home_position()
camera.end_pipeline()

        
