#!/usr/bin/env pybricks-micropython
#Autores: Fabian Segura, Fernando Gomez
# Fecha Actualizacion: 29/04/2023

#_____________________  EV3 libraries   _______________________________
from pybricks.ev3devices    import (Motor,UltrasonicSensor)
from pybricks.parameters    import Port
from pybricks.nxtdevices    import (SoundSensor)
from pybricks.robotics      import DriveBase
from pybricks.hubs          import EV3Brick

#______________ Python Libraries ______________ 
from umqtt.simple import MQTTClient
import time
import utime
import threading



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
    state           = None
    
    def __init__(self):
        self.build()
        
    def build(self):
        self.ev3                = EV3Brick()                        #Instanciamos EV3
        self.obstacle_sensor    = UltrasonicSensor(Port.S2)         #Intanciamos sensor de ultasonido EV3
        self.sound_sensor       = SoundSensor(Port.S3)              #Instanciamos sensor de sonido
        self.sound_sensor_r     = SoundSensor(Port.S4)              #Instanciamos sensor de sonido
        self.sound_sensor_l     = SoundSensor (Port.S1)             #Instanciamos sensor de sonido
        self.left_motor         = Motor(Port.C)                     #Instanciamos motor izquierda
        self.right_motor        = Motor(Port.B)                     #Instanciamos motor derecha
        self.robot              = DriveBase(self.left_motor, self.right_motor, wheel_diameter=55.5, axle_track=104) #Creamos una instancia(objeto) de nuestro robot, especificandole motores, diametro de las ruedas y la longitud del eje  
        self.drive_speed        = 200                               #Definimos una velocidad constante para el robot
        self.host               = "192.168.0.13"                    #Creamos una variable que manejara la direccion IP de nuestro cliente.
        expect=self.mainmqtt(self.host)
        print(expect, " i am in build")
        

        
    def turns(self):        #Funcion para establecer giros en el entorno  
        while True:      
            giro=input("giro")
            if giro == "1":
                self.robot.turn(-122)
            elif giro == "2":
                self.robot.turn(122) 
            elif giro == "3":
                self.robot.turn(-240)
            elif giro == "4":
                self.robot.turn(240) 
            elif giro == "5":
                self.forward()
            elif giro == "6":
                return False
                        
    def sub_cb(self,topic, msg): 
        print((topic, msg))
        self.state = msg
        return self.state

    def mainmqtt(self,server):
        c = MQTTClient("umqtt_clinet", server) #Establecemos conexion con el cliente
        c.set_callback(self.sub_cb)
        c.connect()
        c.subscribe(b"test/message")
        print("Connected to ",c.server)
        c.wait_msg()                        
        c.disconnect()
        if self.state == b"let search":    
            print("El mensaje recibido fue: ",self.state)  
            return self.movimiento()
            
        elif self.state == b"unable to recognize":  
            print("Incapaz de reconocer ó la palabra no es la adecuada")
            return self.mainmqtt(self.host)
            
        return self.state

    def mqtt_rpi4(self,msgp):
        c = MQTTClient("umqtt_client",self.host)
        c.connect()
        c.publish(b"test/droid",msgp)
        c.disconnect()
        self.mainmqtt(self.host)

    def distance(self):
        return self.obstacle_sensor.distance() / 10

    def forward(self): #Avanza
        self.robot.straight(270)
        self.robot.turn(-2)
        self.ubication.append(270)

    def left(self): #Izquierda
        self.robot.turn(-130)
        self.ubication.append(-90)

    def right(self): #Derecha
        self.robot.turn(130)
        self.ubication.append(90)
    def halfturn(self): #Giro de 180°
        self.robot.turn(-230)
        self.ubication.append(-180)
        
        
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
                    
                    if((x > 10) or (y > 10) or (z > 10)):
                        forward = False
                        self.server()
                    
                    elif  self.n <30:
                        
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
                    
                    if((x > 10) or (y > 10) or (z > 10)):
                        forward = False
                        self.server()          
        
    def obs(self):
        #robot gira a la derecha por un primer obstaculo
        self.x = self.sound_sensor.intensity(audible_only=True)-10 #AVANZA
        if (self.distance()<25):
            if(self.x >= 40):
                self.ubication.append(12)
                print("Se ha encontrado la victima, enviando ubicacion")
                print(self.ubication)
                self.mqtt_rpi4(str(self.ubication).encode())
                
            self.right()
            time.sleep(0.5)
            pass
            # robot avanza  y gira a la izquierda para esquivar el obstaculo -------------------------------------------------------------------
            if(self.distance()>=27):
                self.forward()
                time.sleep(0.5)
                self.left()
                #robot avanza  para esquivar el obstaculo
                if(self.distance()>=25):
                    self.forward()
                    time.sleep(0.5)
                    #Sigue avanzando y gira alrededor del obstaculo
                    if(self.distance()>=25):
                        self.forward()
                        time.sleep(0.5)
                        self.left()
                        #robot avanza al lado del obstaculo y gira a la derecha para retomar la posicion
                        if(self.distance()>=27):
                            self.forward()
                            time.sleep(0.5)
                            self.right()
                            
                            if(self.distance()>=25):
                                self.forward()
                                self.mqtt_rpi4(b"recognize")
            #se encuentra un segundo obstaculo y se gira -------------------------------------------------------------------------------------------------
            elif(self.distance()<=25):
                self.halfturn()
                time.sleep(0.5)
                pass
                #No se reconoce ningun obstaculo ---------------------------------------------------------------------------------------------------
                if(self.distance()>=27):
                    self.forward()
                    time.sleep(0.5)
                    #robot avanza  para esquivar el obstaculo
                    if(self.distance()>=25):
                        self.forward()
                        time.sleep(0.5)
                        self.right()
                        #sigue avanzando y gira alrededor del obstaculo
                        if(self.distance()>=27):
                            self.forward()
                            time.sleep(0.5)
                            self.right()
                            self.mqtt_rpi4(b"recognize")
                            #robot avanza al lado del obstaculo y gira a la derecha para retomar la poscicion
                            if(self.distance()<=27):
                                self.forward()
                                time.sleep(0.5)
                                self.right()                       
                                if(self.distance()>=27):
                                    self.forward()
                                    #robot avanza al lado del obstaculo y gira a la derecha para retomar la poscicion
                                    if(self.distance()>=27):
                                        self.forward()
                                        time.sleep(0.5)
                                        self.left()
                                        self.mqtt_rpi4(b"recognize")
                # se reconoce un tercer obstaculo -----------------------------------------------------------------------------------------------------                           
                elif(self.distance()<=27):
                    self.left()
                    time.sleep(0.5)
                    self.forward()
                    time.sleep(0.5)
                    self.right()
                    if(self.distance()>=27):
                        self.forward()
                        time.sleep(0.5)
                        self.right()
                    if(self.distance()>=27):
                        self.forward()
                        if(self.distance()>=27):
                            self.forward()
                            if(self.distance()>=27):
                                self.forward()
                                if(self.distance()>=27):
                                    self.forward()
                                    time.sleep(0.5)
                                    self.right()
                                    if(self.distance()>=27):
                                        self.forward()
                                        time.sleep(0.5)
                                        if(self.distance()>=27):
                                            self.forward()
                                            time.sleep(0.5)
                                            self.right()
                                            self.mqtt_rpi4(b"recognize")

    def movimiento(self):
        while True:
            self.x = self.sound_sensor.intensity(audible_only=True)-10 #AVANZA
            self.y = self.sound_sensor_r.intensity(audible_only=True)-10 #DERECHA
            self.z = self.sound_sensor_l.intensity(audible_only=True)-10 #IZQUIERDA
            if((self.z > self.y) and (self.z > self.x) and (self.z > 5)):
                self.left()
                print("Gira a la izquierda")
                self.obs()
                time.sleep(0.5)
                if(self.z>= 55):
                    print(self.x )
                    self.ubication.append(12)
                    print("Se ha encontrado la victima, enviando ubicacion")
                    print(self.ubication)
                    self.mqtt_rpi4(str(self.ubication).encode())
                    break;
            elif((self.y > self.z) and (self.y > self.x) and (self.y > 5)):
                self.right()
                self.obs()
                print("Gira a la derecha")
                time.sleep(0.5)
                if(self.y >= 55):
                    print(self.x )
                    self.ubication.append(12)
                    print("Se ha encontrado la victima, enviando ubicacion")
                    print(self.ubication)
                    self.mqtt_rpi4(str(self.ubication).encode())
                    break;
            elif((self.x > self.y) and (self.x > self.z) and (self.x > 10)):
                self.robot.straight(150)
                self.ubication.append(150)
                print("Avanza", self.x)
                self.obs()
                time.sleep(0.5)   
                if(self.x >= 55):
                    print(self.x )
                    self.ubication.append(12)
                    print("Se ha encontrado la victima, enviando ubicacion")
                    print(self.ubication)
                    self.mqtt_rpi4(str(self.ubication).encode())
                    break;           
          
                
            
if __name__ == "__main__":  EV3()