#!/usr/bin/env pybricks-micropython
#Autores: Fabian Segura, Fernando Gomez
# Fecha Actualizacion: 01/10/2022 

#_____________________  EV3 libraries   _______________________________
from pybricks.ev3devices    import (Motor,UltrasonicSensor)
from pybricks.parameters    import Port
from pybricks.nxtdevices    import (SoundSensor)
from pybricks.robotics      import DriveBase
from pybricks.hubs          import EV3Brick

#______________ Python Libraries ______________ 
from umqtt.simple import MQTTClient
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
    state           = None
    
    def __init__(self):
        self.build()
        
    def build(self):
        
        self.ev3                = EV3Brick()
        self.obstacle_sensor    = UltrasonicSensor(Port.S2)
        self.sound_sensor       = SoundSensor(Port.S3)
        self.sound_sensor_r     = SoundSensor(Port.S4)
        self.sound_sensor_l     = SoundSensor (Port.S1) 
        self.left_motor         = Motor(Port.C)
        self.right_motor        = Motor(Port.B)
        self.robot              = DriveBase(self.left_motor, self.right_motor, wheel_diameter=55.5, axle_track=104)
        self.drive_speed        = 200
        self.host             = "192.168.39.167"
        expect=self.mainmqtt(self.host)
        print(expect, " i am in build")
        
    def sub_cb(self,topic, msg):
        print((topic, msg))
        self.state = msg
        return self.state

    def mainmqtt(self,server):
        
        c = MQTTClient("umqtt_clinet", server)
        c.set_callback(self.sub_cb)
        print(c.set_callback(self.sub_cb),"callback")
        c.connect()
        c.subscribe(b"test/message")
        print("Connected to ")
        
        try:
            while 1:
                c.wait_msg()
                print(self.state,"i am in while")
                break;
                
        finally:
                
            c.disconnect()
            print("hello there")
            if self.state == b"let search":      self.movimiento()
                
            elif self.state == b"unable to recognize":  self.avanzar_buscando_victima()
                
            elif self.state == b"continue":             print("continue")
                
            return self.state
        
    def hellothere(self,msgp):
        c = MQTTClient("umqtt_client",self.host)
        c.connect()
        c.publish(b"test/droid",msgp)
        c.disconnect()
        expect = self.mainmqtt(self.host)
        
        if expect == b"continue":
            print("continue exit to function")
        elif expect == b"unable to recognize":
            self.avanzar_buscando_victima()
        
    def avanzar_buscando_victima(self):
        """
            Cuando la palabra especifica no es reconocida con exactitud o es una distinta a las 3 esperadas, se 
            procede a hacer un avance de 50 centimetros, estando al pendiente de los obstaculos.
        """
        self.d = self.obstacle_sensor.distance() / 10 #Ultrasonic sensor
        
        if self.d <50:
            print('giro -90')
            self.robot.turn(-90)
            self.ubication.append(-90)
            time.sleep(0.5)
            self.n = self.obstacle_sensor.distance()/10
            
            if  self.n < 50:
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
                    
                    if((x > 10) or (y > 10) or (z > 10)):
                        forward = False
                        self.server()
                    
                    elif  self.n <30:
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
                    
                    if((x > 10) or (y > 10) or (z > 10)):
                        forward = False
                        self.server()                  

    def obs(self):
        
        self.d = self.obstacle_sensor.distance() / 10
        #robot gira a la derecha por un primer obstaculo
        if (self.d<25):
            time.sleep(0.5)
            self.robot.turn(90)
            self.ubication.append(90)
            pass
            self.e = self.obstacle_sensor.distance() / 10
            # robot avanza  y gira a la izquierda para esquivar el obstaculo -------------------------------------------------------------------
            if(self.e>=27):
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
                        self.robot.straight(250)
                        self.ubication.append(250)
                        self.robot.turn(-90)
                        self.ubication.append(-90)
                        self.q = self.obstacle_sensor.distance() / 10
                        
                        #robot avanza al lado del obstaculo y gira a la derecha para retomar la posicion
                        
                        if(self.q>=27):
                            self.robot.straight(270)
                            self.ubication.append(270)
                            self.robot.turn(90)
                            self.ubication.append(90)
                            self.r = self.obstacle_sensor.distance() / 10
                            
                            if(self.r>=25):
                                self.robot.straight(250)
                                self.ubication.append(250)
                                self.hellothere(b"fabian")
                        #self.p = self.obstacle_sensor.distance() / 10  
            #se encuentra un segundo obstaculo y se gira -------------------------------------------------------------------------------------------------
            elif(self.e<=25):
                self.robot.turn(-180)
                self.ubication.append(-180)
                self. ultimateobs= self.obstacle_sensor.distance() / 10
                pass
                
                #No se reconoce ningun obstaculo ---------------------------------------------------------------------------------------------------
                if(self.ultimateobs>=27):
                    self.robot.straight(250)
                    self.ubication.append(250)
                    self.f = self.obstacle_sensor.distance() / 10
                    
                    #robot avanza  para esquivar el obstaculo
                    if(self.f>=25):
                        self.robot.straight(250)
                        self.ubication.append(250)
                        self.robot.turn(90)
                        self.ubication.append(90)
                        self.p = self.obstacle_sensor.distance() / 10
                        
                        #sigue avanzando y gira alrededor del obstaculo
                        if(self.p>=27):
                            self.robot.straight(270)
                            self.ubication.append(270)
                            self.q = self.obstacle_sensor.distance() / 10
                            
                            #robot avanza al lado del obstaculo y gira a la derecha para retomar la poscicion
                            
                            if(self.q>=27):
                                self.robot.straight(270)
                                self.ubication.append(270)
                                self.robot.turn(90)
                                self.ubication.append(90)
                                self.r = self.obstacle_sensor.distance() / 10
                                
                                
                                if(self.r>=27):
                                    self.robot.straight(270)
                                    self.ubication.append(270)
                                    self.s = self.obstacle_sensor.distance() / 10
                            
                                    #robot avanza al lado del obstaculo y gira a la derecha para retomar la poscicion
                                    
                                    if(self.s>=27):
                                        self.robot.straight(270)
                                        self.ubication.append(270)
                                        self.robot.turn(-90)
                                        self.ubication.append(-90)
                                        self.hellothere(b"fabian")
                                        
                                
                                
                # se reconoce un tercer obstaculo -----------------------------------------------------------------------------------------------------                           
                elif(self.ultimateobs<=27):
                    self.robot.turn(-90)
                    self.ubication.append(-90)
                    self.robot.straight(270)
                    self.ubication.append(270)
                    self.robot.turn(90)
                    self.ubication.append(90)
                    self. j= self.obstacle_sensor.distance() / 10

                    if(self.j>=27):
                        self.robot.straight(270)
                        self.ubication.append(270)
                        self.robot.turn(90)
                        self.ubication.append(90)
                        self.f = self.obstacle_sensor.distance() / 10
                        
                    
                    if(self.f>=27):
                        self.robot.straight(270)
                        self.ubication.append(270)
                        self.p = self.obstacle_sensor.distance() / 10
                        
                        
                        if(self.p>=27):
                            self.robot.straight(270)
                            self.ubication.append(270)
                            self.q = self.obstacle_sensor.distance() / 10
                            
                            
                            if(self.q>=27):
                                self.robot.straight(270)
                                self.ubication.append(270)
                                self.r = self.obstacle_sensor.distance() / 10
                                
                                if(self.r>=27):
                                    self.robot.straight(270)
                                    self.ubication.append(270)
                                    self.robot.turn(90)
                                    self.ubication(90)
                                    self.s = self.obstacle_sensor.distance() / 10
                                    
                                    if(self.s>=27):
                                        self.robot.straight(270)
                                        self.ubication.append(270)
                                        self.t = self.obstacle_sensor.distance() / 10
                                        
                                        if(self.r>=27):
                                            self.robot.straight(270)
                                            self.ubication.append(270)
                                            self.robot.turn(90)
                                            self.ubication(90)
                                            self.hellothere(b"fabian")

    def movimiento(self):
        
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
                
                self.far = self.obstacle_sensor.distance() / 10
                
                if (self.far>25):
                    time.sleep(0.5)
                    self.robot.straight(150)
                    self.ubication.append(150)
                    print("avanza")           
                    self.obs()   
                    
                    time.sleep(0.5)   
                    
                    if(self.x >= 55):
                        self.ubication.append(12)
                        
                        print("Se ha encontrado la victima, enviando ubicacion")
                        print(self.ubication)
                        self.hellothere(str(self.ubication).encode())
                        break;
                else:
                    self.obs()    
                    time.sleep(0.5)   
                    
                    if(self.x >= 55):
                        self.ubication.append(12)
                    
                        print("Se ha encontrado la victima, enviando ubicacion")
                        print(self.ubication)
                        self.hellothere(str(self.ubication).encode())

if __name__ == "__main__":  EV3()