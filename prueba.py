import speech_recognition       as sr
micro = sr.Microphone()   
r = sr.Recognizer()
fraseDicha = "ERROR"
while True:
    with micro as source:
        print('Porfavor hable fuerte y claro')
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        try:
            fraseDicha = r.recognize_google(audio,language='es-CO')
            print(fraseDicha)
        except:
            print("Errror")
        if fraseDicha == "Ayuda":
            print("Ayuda")

        elif fraseDicha == "ayuda":
            print("aYUDA")
                
        elif fraseDicha == "Auxilio":
            print("Auxilio")

        elif fraseDicha == "auxilio":
            print("Auxilio")

        elif fraseDicha == "Socorro":
            print("socorro")

        elif fraseDicha == "socorro":
            print("Socorro")
