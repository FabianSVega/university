
from kivy.app import App 
from kivy.uix.widget import Widget
from kivy.lang.builder import Builder
from kivy.core.window import Window
import speech_recognition as sr
import threading
from turtle 					import * 

#_____________	Librerias funcionales	_______________________
import os
import sys
import ast
import time
import turtle
import threading
import logging
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
from   logging.handlers     import TimedRotatingFileHandler
from kivy.clock             import Clock


formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
datefmt		= '%Y-%m-%d %H:%M:%S',
handler = logging.handlers.TimedRotatingFileHandler(os.path.dirname(os.path.realpath(__file__))+"/logs/logs.log", when='d', interval=1, backupCount=3)
handler.setFormatter(formatter)
logger = logging.getLogger()
logger.addHandler(handler)
logger.setLevel(logging.INFO)

os.environ["KIVY_NO_CONSOLELOG"] = "1"

Window.size = (385, 520)

Builder.load_file('./assets/screens/principal.kv')  
pin	= 17
pin2 = 27
pin3 = 19
pin4 = 20
pin5 = 21

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin,GPIO.OUT)
GPIO.setup(pin2,GPIO.OUT)
GPIO.setup(pin3,GPIO.OUT)
GPIO.setup(pin5,GPIO.OUT)
GPIO.setup(pin4,GPIO.OUT)  

class work(Widget):
    
    fraseDicha 	= None
    ipev3		= "192.168.248.232"
    topic		= "test/message"
    
    def __init__(self, **kwargs):
        super(work, self).__init__(**kwargs)
        
    def thr(self):
        Clock.schedule_once(self.ledtells,0)
        # Clock.schedule_interval(self.ledtells)
        threading.Thread(target=self.reconocimiento).start()

    def ledtells(self,dt):
        count=0
        while count <= 10:
            GPIO.output(pin, GPIO.HIGH)
            time.sleep(.05)
            GPIO.output(pin,GPIO.LOW)
            GPIO.output(pin2, GPIO.HIGH)
            time.sleep(.05)
            GPIO.output(pin2,GPIO.LOW)
            GPIO.output(pin3, GPIO.HIGH)
            time.sleep(.05)
            GPIO.output(pin3,GPIO.LOW)
            GPIO.output(pin4, GPIO.HIGH)
            time.sleep(.05)
            GPIO.output(pin4,GPIO.LOW)
            GPIO.output(pin5, GPIO.HIGH)
            time.sleep(.05)
            GPIO.output(pin5,GPIO.LOW)
            count	= 1+count

    def principal(self,datamain): 
        self.ids.input_n.text = datamain

    def received(self):
        print("Recibi un mensaje desde el EV3")
        while True:
            msg = subscribe.simple("test/droid",hostname="localhost")
            answerto = (msg.payload).decode("utf-8")
            print(answerto)
            if(answerto == "fabian"):
                print("Recibi como mensaje FABIAN")
                return self.reconocimiento()
            
            self.draw_vector(answerto)
            Clock.schedule_once(self.ledtells,0)
            return False

    # Funcion reconocimiento de palabras
    def reconocimiento(self):
        try:
            micro 	= sr.Microphone()   
            r		= sr.Recognizer()
        except Exception as e:
            logging.error(f"Ha ocurrido un error: {e}")
            sys.exit(1)
        while True:
            with micro as source:
                try:
                    print("Porfavor hable fuerte y claro")
                    self.principal("Porfavor hable fuerte y claro")
                    r.adjust_for_ambient_noise(source)
                    audio = r.listen(source)
                    client = mqtt.Client()
                    client.connect("localhost",1883,60)
                    self.fraseDicha = r.recognize_google(audio,language='es-CO')

                    if self.fraseDicha == "Ayuda" or self.fraseDicha == "ayuda":
                        self.principal(self.fraseDicha.capitalize())
                        logging.info(f'La palabra reconocida fue: {self.fraseDicha}')
                        time.sleep(1)
                        client.publish("test/message","let search")
                        client.disconnect()
                        break;
                            
                    elif self.fraseDicha == "Auxilio" or self.fraseDicha == "auxilio":
                        self.principal(self.fraseDicha.capitalize())
                        logging.info(f'La palabra reconocida fue: {self.fraseDicha}')
                        time.sleep(1)
                        client.publish("test/message","let search")
                        client.disconnect()
                        break;

                    elif self.fraseDicha == "Socorro" or self.fraseDicha == "socorro":
                        self.principal(self.fraseDicha.capitalize())
                        logging.info(f'La palabra reconocida fue: {self.fraseDicha}')
                        time.sleep(1)
                        client.publish("test/message","let search")
                        client.disconnect()
                        break;
                    else:
                        self.principal("Incapaz de reconocer")
                        logging.info("Incapaz de reconocer")
                
                except Exception as e:
                    self.principal('Incapaz de reconocer')
                    logging.error(f'Ha ocurrido un error : {e}')
        self.received()

    
                        
    def draw_vector(self,x):
        if x == "" or ast.literal_eval(x)==[]:
            logging.error("Vector nulo")
            self.principal("Ha ocurrido un error")
            sys.exit(1)

        else:
            lista = ast.literal_eval(x)
                
            turtle.Screen().bgcolor("white")
            title("Movimiento ev3")
            self.square()
            self.cross()
            turtle.speed(speed=1)

            for x in lista:
                turtle.speed(speed=1)
                turtle.pencolor("red")
                logging.info(x)

                if x== 90:
                    turtle.right(90)
                elif x== -90:
                    turtle.left(90)
                elif x== 50:
                    turtle.forward(5)
                elif x == 200:
                    turtle.forward(20)
                elif x== 250:
                    turtle.forward(25)
                elif x== -180:
                    turtle.left(180)
                elif x== 150:

                    turtle.forward(15)
                elif x== 500:
                    turtle.forward(50)
                elif x==12: 
                    positiont=turtle.position()
                    logging.info(positiont)
                    turtle.write(str(positiont), True, align="center")
                    exitonclick()

    # Function to draw the cross

    def square(self):
        
        i=1
        turtle.pencolor("black")
        turtle.speed(speed=1000)

        for i in range (8):
            turtle.penup()
            turtle.setpos(0,40*i) 
            turtle.pendown()
            turtle.write(str(int(turtle.ycor())),True,align="left")
            turtle.penup()
            turtle.setpos(0,40*i) 
            turtle.pendown()
            turtle.forward (360)
            turtle.left(-180)
            turtle.forward (720)
        i=1  
        turtle.penup()
        turtle.home()
        turtle.pendown() 

        for i in range (8):
            turtle.penup()
            turtle.setpos(0,-40*i) 
            turtle.pendown()
            turtle.write(str(int(turtle.ycor())),True,align="left")
            turtle.penup()
            turtle.setpos(0,-40*i) 
            turtle.pendown() 
            turtle.forward (360)
            turtle.left(-180)
            turtle.forward (720)
        i=1 	
        turtle.penup()
        turtle.home()
        turtle.pendown() 
        turtle.left(90)

        for i in range (10):
            turtle.penup()
            turtle.setpos(40*i,0) 
            turtle.pendown()
            turtle.write(str(int(turtle.xcor())),align="center")
            turtle.penup()
            turtle.setpos(40*i,0) 
            turtle.pendown()
            turtle.forward (280)
            turtle.left(-180)
            turtle.forward (560)

        i=1	
        turtle.penup()
        turtle.home()
        turtle.pendown() 
        turtle.left(90)

        for i in range (10):
            turtle.penup()
            turtle.setpos(-40*i,0) 
            turtle.pendown()
            turtle.write(str(int(turtle.xcor())),True,align="left")
            turtle.penup()
            turtle.setpos(-40*i,0) 
            turtle.pendown()
            turtle.forward (280)
            turtle.left(-180)
            turtle.forward (560)

        turtle.penup()
        turtle.home()
        turtle.pendown()

    # Function to draw the grid
    def cross(self):
        
        turtle.shape("turtle")
        turtle.color("white", "red")
        turtle.pencolor("green")
        turtle.speed(speed=100)
        turtle.forward (500)
        turtle.write("x", True,font=("Verdana", 12, "bold"))
        turtle.home()
        turtle.forward (-500)
        turtle.home()
        turtle.left (90)
        turtle.forward (300)
        turtle.write("y", True, font=("Verdana", 12, "bold"))
        turtle.penup() 
        turtle.setpos(0,300) 
        turtle.pendown() 
        turtle.home()
        turtle.left(-90)
        turtle.forward (300)
        turtle.home()
                        
      
class workapp(App):
    def build(self):
        return work()
    
if __name__ == '__main__':
    workapp().run()