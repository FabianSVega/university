#!/usr/bin/env pybricks-micropython
#Autores: Fabian Segura, Fernando Gomez
# Fecha Actualizacion: 01/10/2022 

#_____________________  EV3 libraries   _______________________________
from pybricks.ev3devices    import (Motor, TouchSensor, ColorSensor,InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters    import Port, Stop, Direction, Button, Color
from pybricks.tools         import wait, StopWatch, DataLog
from pybricks.media.ev3dev  import SoundFile, ImageFile
from pybricks.nxtdevices    import (SoundSensor)
from pybricks.robotics      import DriveBase
from pybricks.hubs          import EV3Brick

#______________ Python Libraries ______________ 
import threading
import socket
import time


class EV3():
    
    ev3             = None
    data            = None
    robot           = None
    ubication       = []
    left_motor      = None
    drive_speed     = None
    right_motor     = None
    sound_sensor    = None
    sound_sensor_r  = None
    sound_sensor_l  = None
    obstacle_sensor = None    
    
    def __init__(self):
        self.build()
        
    def build(self):
        
        self.ev3                = EV3Brick()
        self.obstacle_sensor    = UltrasonicSensor(Port.S2)
        self.sound_sensor       = SoundSensor(Port.S3)
        self.sound_sensor_r     = SoundSensor(Port.S4)
        self.sound_sensor_l     = SoundSensor (Port.S1) 
        self.left_motor         = Motor(Port.A)
        self.right_motor        = Motor(Port.B)
        self.robot              = DriveBase(self.left_motor, self.right_motor, wheel_diameter=55.5, axle_track=104)
        self.drive_speed        = 200
        self.outsound()
        
        
    def server(self):
        
        self.mysv = socket.socket()
        self.mysv.bind(('169.254.231.179', 10000)) 
        self.mysv.listen(5)
        print("Servidor de voz creado correctamente")
        
        while True:
             
            print("esperando a que el cliente se conecte".encode('utf-8'))     
            self.conexion, self.addr = self.mysv.accept()
            print (self.addr)
            self.peticion = self.conexion.recv(1024)
            print(self.peticion.decode('utf-8'))
            
            if(self.peticion.decode('utf-8') == "ayuda" or self.peticion.decode('utf-8') == "auxilio" or self.peticion.decode('utf-8') =="socorro"):
                self.movimiento()
                self.conexion.close()
                break;
            
            elif(self.peticion.decode('utf-8') == "incapaz_de_reconocer"):
                self.avanzar_buscando_victima()
                
        self.conexion.close()
        print("Se cerro la conexion")
        
    def avanzar_buscando_victima(self):
        """
            Cuando la palabra especifica no es reconocida con exactitud o es una distinta a las 3 esperadas, se 
            procede a hacer un avance de 50 centimetros, estando al pendiente de los obstaculos.
        """
        self.d = self.obstacle_sensor.distance() / 10
        
        if self.d <30:
            print('giro -90')
            self.robot.turn(-90)
            self.ubication.append(-90)
            time.sleep(0.5)
            self.n = self.obstacle_sensor.distance()/10
            
            if  self.n <30:
                print('giro -90')
                self.robot.turn(-90)
                self.ubication.append(-90)
                time.sleep(0.5)
                print('avanzo -50')
                self.robot.straight(50)
                self.ubication.append(50)
                time.sleep(0.5)
                
            else:
                print('avanzo 50')
                self.robot.straight(50)
                self.ubication.append(50)
                time.sleep(0.5)
        else:
            self.robot.straight(50)
            self.ubication.append(50)
            time.sleep(0.5)
            print('avanzo 50')
    
    def outsound(self):
        
        forward =True
        i=1
        while forward:
            x = self.sound_sensor.intensity(audible_only=True)
            y = self.sound_sensor_r.intensity(audible_only=True)
            z = self.sound_sensor_l.intensity(audible_only=True)
            print("x: ",x," y: ",y," z: ",z)
            
            if((x > 10) or (y > 10) or (z > 10)):
                forward = False
                self.server()
            else:
                self.d = self.obstacle_sensor.distance() / 10
                print("Entro")
                print('avanzo 50')
                self.robot.straight(500)
                self.ubication.append(500)
                c=500
                time.sleep(0.5)
                
                if self.d <30:
                    print('giro -90')
                    self.robot.turn(-90)
                    self.ubication.append(-90)
                    time.sleep(0.5)
                    self.n = self.obstacle_sensor.distance()/10
                    
                    if  self.n <30:
                        print('giro -90')
                        self.robot.turn(-90)
                        self.ubication.append(-90)
                        time.sleep(0.5) 
                        print('avanzo -50')
                        self.robot.straight(50)
                        self.ubication.append(50)
                        time.sleep(0.5)
                                                
                    else:
                        print('avanzo 50')
                        self.ubication.append(50)
                        self.robot.straight(50)
                        time.sleep(0.5) 
                else:
                    self.robot.straight(500)
                    self.ubication.append(500)
                    print('avanzo 50+50')
                    time.sleep(0.5)
                    c = c+500
                    print(c)
                    
                if c==1000:
                    i=i*-1
                    print(i)
                    self.ubication.append(i*90)
                    self.robot.turn(i*90)
                    self.robot.straight(200)
                    self.ubication.append(200)
                    self.ubication.append(i*90)
                    self.robot.turn(i*90)
                    time.sleep(0.5)                    

    def obs(self):
        
        self.d = self.obstacle_sensor.distance() / 10
        #robot gira a la derecha por obstaculo
        if (self.d<25):
            time.sleep(0.5)
            self.robot.turn(90)
            self.ubication.append(90)
            pass
            self.n = self.obstacle_sensor.distance() / 10
            # robot avanza  y gira a la izquierda para esquivar el obstaculo
            if(self.n>=25):
                self.robot.straight(270)
                self.ubication.append(270)
                self.robot.turn(-90)
                self.ubication.append(-90)
                self.o = self.obstacle_sensor.distance() / 10
                
                #robot avanza  para esquivar el obstaculo
                if(self.o>=25):
                    self.robot.straight(250)
                    self.ubication.append(250)
                    self.p = self.obstacle_sensor.distance() / 10
                    
                    #sigue avanzando y gira alrededor del obstaculo
                    if(self.p>=25):
                        self.robot.straight(270)
                        self.ubication.append(270)
                        self.robot.turn(-90)
                        self.ubication.append(-90)
                        self.q = self.obstacle_sensor.distance() / 10
                        
                        #robot avanza al lado del obstaculo y gira a la derecha para retomar la poscicion
                        
                        if(self.q>=25):
                            self.robot.straight(270)
                            self.ubication.append(270)
                            self.robot.turn(90)
                            self.ubication.append(90)
                            self.r = self.obstacle_sensor.distance() / 10
                            
                            if(self.r>=25):
                                self.robot.straight(250)
                                self.ubication.append(250)
                        #self.p = self.obstacle_sensor.distance() / 10  
                              
            #se encuentra otro obstaculo y se gira 
            elif(self.n<=25):
                self.robot.turn(-180)
                self.ubication.append(-180)
                self.robot.straight(250)
                self.ubication.append(250)
                self.robot.turn(90)
                self.ubication.append(90)
                self. h= self.obstacle_sensor.distance() / 10

                if(self.h>=25):
                    self.robot.straight(270)
                    self.ubication.append(270)
                    self.robot.turn(90)
                    self.ubication.append(90)
                    self.o = self.obstacle_sensor.distance() / 10
                    
                #robot avanza  para esquivar el obstaculo
                if(self.o>=25):
                    self.robot.straight(250)
                    self.ubication.append(250)
                    self.p = self.obstacle_sensor.distance() / 10
                    
                    #sigue avanzando y gira alrededor del obstaculo
                    if(self.p>=25):
                        self.robot.straight(270)
                        self.ubication.append(270)
                        self.robot.turn(-90)
                        self.ubication.append(-90)
                        self.q = self.obstacle_sensor.distance() / 10
                        
                        #robot avanza al lado del obstaculo y gira a la derecha para retomar la poscicion
                        
                        if(self.q>=25):
                            self.robot.straight(270)
                            self.ubication.append(270)
                            self.robot.turn(-90)
                            self.ubication.append(-90)
                            self.r = self.obstacle_sensor.distance() / 10
                            
                            if(self.r>=25):
                                self.robot.straight(250)
                                self.ubication.append(250)
                
                
                
            

    def movimiento(self):
        
        self.conexion.close()
        
        def server2(data):
            mysv = socket.socket()
            mysv.bind(("169.254.231.179", 3200)) 
            mysv.listen(5)
            print("Servidor de turtle creado correctamente")
            
            while True:   
                print("Esperando a que el cliente se conecte")
                conexion, addr = mysv.accept()
                print (addr)
                
                if (data != None or data != "" or data != []):
                    conexion.send(str(data).encode('utf-8'))
                    peticion = conexion.recv(1024)
                    print(data)
                    conexion.close()
                    break;
                else: 
                    print("Ha ocurrido un error")

        while True:
            self.x = self.sound_sensor.intensity(audible_only=True)-10 #AVANZA
            self.y = self.sound_sensor_r.intensity(audible_only=True)-10 #DERECHA
            self.z = self.sound_sensor_l.intensity(audible_only=True)-10 #IZQUIERDA
               
            if((self.z > self.y) and (self.z > self.x) and (self.z > 5)):
                self.robot.turn(-90)
                self.ubication.append(-90)
                print("Gira a la izquierda")
                self.obs()
                time.sleep(0.5)
                
            elif((self.y > self.z) and (self.y > self.x) and (self.y > 5)):
                self.robot.turn(90)
                self.ubication.append(90)
                self.obs()
                print("Gira a la derecha")
                time.sleep(0.5)
                
            elif((self.x > self.y) and (self.x > self.z) and (self.x > 10)):
                self.robot.straight(150)
                self.ubication.append(150)
                print("avanza")           
                self.obs()    
                time.sleep(0.5)   
                
                if(self.x >= 85):
                    self.ubication.append(12)
                    print("Se ha encontrado la victima, enviando ubicacion")
                    print(self.ubication)
                    server2(self.ubication)
                    self.build()
                    break;
        self.build()
        
  
        

if __name__ == "__main__":
    EV3()