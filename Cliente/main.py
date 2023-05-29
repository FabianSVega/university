#Autores: Fabian Segura, Fernando Gomez
# Fecha Actualizacion: 02/23/2023 

from kivy.lang					import Builder
from kivy.core.window 			import Window
from kivymd.app					import MDApp
from turtle 					import * 
import speech_recognition       as sr

#_____________	Librerias funcionales	_______________________
import os
import ast
import time
import turtle
import threading
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe

#____________	Variables Globales	___________________________
pin	 = 11
pin2 = 13
pin3 = 35
pin4 = 38
pin5 = 40
pin6 = 15

GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin,GPIO.OUT)
GPIO.setup(pin2,GPIO.OUT)
GPIO.setup(pin3,GPIO.OUT)
GPIO.setup(pin4,GPIO.OUT)
GPIO.setup(pin5,GPIO.OUT)
GPIO.setup(pin5,GPIO.OUT)

Window.fullscreen = 0
Window.size = (500,500)


class MainApp(MDApp):
	screens		= {}
	lista		= []
	fraseDicha 	= None
	ipev3		= "192.168.10.232"
	topic		= "test/message"	

	def build(self):
		self.theme_cls.primary_palette	= "DeepPurple"
		self.principal("welcome")

	def go_screen(self, screenname):	
		self.root.ids.sm.switch_to(self.load_screen(screenname), direction	= 'left', duration=.07)  

	def load_screen(self, screenname):
		self.view	= screenname
		if self.screens.get(screenname) is not None:	return self.screens.get(screenname)

		if os.path.exists(os.path.dirname(os.path.realpath(__file__))+'/build/screens/' + screenname.replace(" ", "") + '.kv'):	screen	= Builder.load_file(os.path.dirname(os.path.realpath(__file__))+'/build/screens/' + screenname.replace(" ", "") + '.kv')
		else:																			screen	= Builder.load_string('''
Screen:
	name: '{screenname} Not Defined'

	MDBoxLayout:
		orientation: 'vertical'
		MDLabel:
			text: "Screen {screenname} Not Defined"
			font_size: 40
			halign: 'center'
			size_hint_y: None
			''')
		self.screens[screenname]	= screen

		return screen

	def principal(self,datamain):	
		self.go_screen('principal')
		self.screens['principal'].ids.dato.text=datamain 

	def thread_voice(self):
		threading.Thread(target=self.reconocimiento).start()

	#Function to search of sound
	def ledtells(self):
     
		timew=0
		led=True
		while led:
			
			GPIO.output(pin2, GPIO.HIGH)
			GPIO.output(pin3, GPIO.HIGH)
			GPIO.output(pin5, GPIO.HIGH)
			GPIO.output(pin4, GPIO.HIGH)
			time.sleep(.05)
			GPIO.output(pin5,GPIO.LOW)
			GPIO.output(pin2,GPIO.LOW)
			GPIO.output(pin3,GPIO.LOW)
			GPIO.output(pin4,GPIO.LOW)
			time.sleep(.05)
			timew	= 1+timew

			if timew == 40:
				
				led=False			
    
	# Function to recognize words
	def reconocimiento(self):

		micro 	= sr.Microphone()   
		r		= sr.Recognizer()
		threading.Thread(target= self.ledtells()).start()

		while True:

			with micro as source:
				
				print('Porfavor hable fuerte y claro')
				self.screens['principal'].ids.dato.text='!!Porfavor hable fuerte y claro¡¡'
				r.adjust_for_ambient_noise(source)
				audio = r.listen(source)
				client = mqtt.Client()
				client.connect("localhost",1883,60)

				try:
					self.fraseDicha = r.recognize_google(audio,language='es-CO')
					print(self.fraseDicha)
				except:
					client.publish("test/message","unable to recognize" )
					client.disconnect()
						
					self.screens['principal'].ids.dato.text='Incapaz de reconocer'
					self.reconocimiento()

				if self.fraseDicha == "Ayuda" or "ayuda":
					client.publish("test/message","let search")
					client.disconnect()
					self.screens['principal'].ids.dato.text= self.fraseDicha
					threading.Thread(target= self.ledtells()).start()	
					break;
						
				elif self.fraseDicha == "Auxilio" or  "auxilio":
					client.publish("test/message","let search")
					client.disconnect()
					self.screens['principal'].ids.dato.text=self.fraseDicha
					threading.Thread(target= self.ledtells()).start()
					break;
				
				elif self.fraseDicha == "Socorro" or "socorro":
					client.publish("test/message","let search")
					client.disconnect()
					self.screens['principal'].ids.dato.text=self.fraseDicha
					threading.Thread(target= self.ledtells()).start()
					break;
				
				# Test
				elif self.fraseDicha == "Hola" or "hola":
					client.publish("test/message","let search")
					client.disconnect()
					self.screens['principal'].ids.dato.text=self.fraseDicha
					threading.Thread(target= self.ledtells()).start()
					break;

				else:
					client.publish("test/message","unable to recognize")
					client.disconnect()
					self.screens['principal'].ids.dato.text='Incapaz de reconocer'
		self.received()
    
	# Function to wait messages of EV3 
	def received(self):
		print("i am on received")
		state_msg = True
		while state_msg:
			print("on while")

			msg = subscribe.simple("test/droid",hostname="localhost")
			answerto = (msg.payload).decode("utf-8")  # --> payload: bytes | bytearray
			print(answerto)
			
			if(answerto == "fabian"):
				print("thanks")
				micro 	= sr.Microphone()   
				r		= sr.Recognizer()
				threading.Thread(target= self.ledtells()).start()
				reply = True  
				while reply:
			
					with micro as source:
						
						print('Porfavor hable fuerte y claro')
						self.screens['principal'].ids.dato.text='!!Porfavor hable fuerte y claro¡¡'
						r.adjust_for_ambient_noise(source)
						audio = r.listen(source)
						client = mqtt.Client()
						client.connect("localhost",1883,60)
			
			
						try:
							self.fraseDicha = r.recognize_google(audio,language='es-CO')
							print(self.fraseDicha)
			
						except:
							client.publish("test/message","unable to recognize" )
							self.received()
								
							self.screens['principal'].ids.dato.text='Incapaz de reconocer'
							self.reconocimiento()
			
						if self.fraseDicha == "Ayuda" or "ayuda":
							client.publish("test/message","let search" )
							client.disconnect()
							print('ayuda')
							self.screens['principal'].ids.dato.text=self.fraseDicha								
							threading.Thread(target= self.ledtells()).start()
							break;

						elif self.fraseDicha == "Auxilio" or "auxilio":
							client.publish("test/message","let search" )
							client.disconnect()
							print('auxilio')
							self.screens['principal'].ids.dato.text=self.fraseDicha						
							threading.Thread(target= self.ledtells()).start()
							break;

						elif self.fraseDicha == "Socorro" or "socorro":
							client.publish("test/message","let search" )
							client.disconnect()
							print('socorro')
							self.screens['principal'].ids.dato.text=self.fraseDicha							
							threading.Thread(target= self.ledtells()).start()
							break;

						elif self.fraseDicha == "Hola" or "hola":
							client.publish("test/message","let search")
							client.disconnect()
							print('ayuda')
							self.screens['principal'].ids.dato.text=self.fraseDicha
							threading.Thread(target= self.ledtells()).start()
							break;	
			elif(answerto == "there are sound"): # There are sound, but the words is unable to recognize
				print("click buttom")
			elif(answerto == "without sound"):
				self.principal("there aren't sound")
			else:
				self.draw_vector(answerto)
				state_msg = False

	# Function to draw the route of EV3
	def draw_vector(self,x):
		self.ledtells() # advertise that the ev3 found the victim
		state_list	= True
		while state_list:
			print(x)
   
			if x == None or x == "" or x == []:
				print("Ha ocurrido un error")
				state_list = False
    
			else:
				self.lista = ast.literal_eval(x)
				print(self.lista)
				state_list = False
				
				
		turtle.Screen().bgcolor("white")
		title("Movimiento ev3")
		self.square()
		self.cross()
		turtle.speed(speed=1)
   
		for x in self.lista:
			turtle.speed(speed=1)
			turtle.pencolor("red")
			print(x)
   
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
				print(positiont)
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
			
if __name__	== '__main__':	MainApp().run()