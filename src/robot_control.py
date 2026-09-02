from pymycobot import MyCobot280
import numpy as np
import time

class Cobot():
    def __init__(self, port='/dev/tty.usbserial-588D0017891', baudrate=115200):
        self.cobot = MyCobot280(port, baudrate)
        self.home_pos = [0,0,0,0,0,0] # in joint angles
        self.out_of_the_way_pos = [0,0,0,60,0,0] # in joint angles

    def power_on(self):
        self.cobot.power_on()
        self._change_color(0, 255, 0)
    
    def get_angles(self):
        return self.cobot.get_angles()    

    def send_angles(self, angles, speed):
        return self.cobot.send_angles(angles, speed)
    
    def get_coords(self):
        return self.cobot.get_coords()

    def send_coords(self, coord, speed):
        return self.cobot.send_coords(coord, speed)

    def home_position(self):
        self.cobot.send_angles(self.home_pos,30)
        #self._change_color(255, 255, 255)
        self.cobot.set_gripper_state(0, 50)
    
    def release_all_servos(self):
        return self.cobot.release_all_servos()
    
    def power_off(self):
        return self.cobot.power_off()
    
    def _change_color(self, r, g, b):
        self.cobot.set_color(r, g, b)

    def robot_state(self):
        if self.cobot.is_in_position(self.home_pos, 0):
            self._change_color(255, 255, 255)
            return 0
        else:    
            if self.cobot.is_moving():
                self._change_color(0, 0, 255)
                return 1
            elif not self.cobot.is_moving():
                self._change_color(0, 255, 0)
                return 0
            else:
                self._change_color(255, 0, 0)
                return -1

    def ready_pos(self):
        self.cobot.send_coords([200, 6, 180, -180, 0, -45],30)
        self.cobot.set_gripper_state(0, 50)

    def send_coord(self, id, coord, speed):
        self.cobot.send_coord(id, coord, speed)

    def grip_object(self):
        self.cobot.send_coord(3, 120, 30)
        time.sleep(5)
        self.cobot.set_gripper_state(1, 50)
        time.sleep(5)
        self.cobot.send_coord(3, 215, 30)
        time.sleep(5)

    def move_object_away(self, drop_off_pos):
        #self.cobot.send_coord(2, -50, 50)
        #self.cobot.send_coords([146.0, 135.0, 215.0, -180, 0, -45], 50)
        #self.cobot.send_angles([40, -35, -75, 23, 0, 0], 50) # Ablageposition von mir bestimmt
        self.cobot.send_angles(drop_off_pos, 50)
        time.sleep(5)
        self.cobot.set_gripper_state(0, 50)
        time.sleep(5)

    def out_of_the_way(self):
        self.cobot.send_angles(self.out_of_the_way_pos, 50)

    def control_gripper(self, state):
        '''0 = open, 1 = close'''
        self.cobot.set_gripper_state(state, 70) 