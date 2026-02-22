
from guizero import App, PushButton, Picture,Drawing,Box,Text
from pygame import mixer
import wave
from piper.voice import PiperVoice
import threading
from queue import Queue
import time
import keyboard
import pyautogui
import asyncio
from bleak import BleakScanner,BleakClient


async def CitajControler():
    try:
        characteristicUid="beb5483e-36e1-4688-b7f5-ea07361b26a8"
        devices = await BleakScanner.discover()
        counter=0
        name="Slovarica"
        for d in devices:
          if(d.name==name):
                async with BleakClient(d) as client:
                    print("Conected to the desegnated device "+str(client.is_connected))
                    while client.is_connected:
                        code= (await client.read_gatt_char(characteristicUid)).decode("utf-8")
                        if code=="LEVO":
                            print(f"Model Number: {code}")
                            pyautogui.move(-50, 0,duration=0.5)
                        if code=="DOLE":
                            print(f"Model Number: {code}")
                            pyautogui.move(0, 50,duration=0.5)
                        if code=="DESNO":
                            print(f"Model Number: {code}")
                            pyautogui.move(50, 0,duration=0.5)
                        if code=="GORE":
                            print(f"Model Number: {code}") 
                            pyautogui.move(0, -50,duration=0.5)    
    except Exception as e:
        print("error citaj controler "+str(e))

def PhoneComunication(q):
    while True:
        print("hello from phone")
        key=keyboard.read_key()
        print(key)
        if key == "p":
                    break
        time.sleep(0.5)
       
def Ispisitext(num,textarea:Text,Mod,Slovo):
   # print("Button was pressed  "+str( UiBox.children[1]))
    textarea.append(Slovo)
    mixer.init()
    if Mod==0:
     mixer.music.load("AudioPojam/"+num+".mp3")
    else:
     mixer.music.load("AudioSlova/"+num+".mp3")
    mixer.music.set_volume(0.7)
    mixer.music.play()

def izbrisitext(textarea:Text):
    text=textarea.value
    textmaller=text[:-1]
    textarea.value=textmaller
    
def PustiPesmu():
    print("Button was pressed  playing the song ")
    mixer.init()
    mixer.music.load("Pesma.mp3")
    mixer.music.set_volume(0.7)
    mixer.music.play()
    
def PiperPlay(textarea:Text):
    model_path = "sr_RS-serbski_institut-medium.onnx" # Replace with your .onnx file path
    config_path = "sr_RS-serbski_institut-medium.onnx.json" # Replace with your .onnx.json file path

    # Load the voice model
    voice = PiperVoice.load(model_path, config_path=config_path)

    text = textarea.value
    output_wav_file = "output.wav"

    # Synthesize the audio and save it to a WAV file
    with wave.open(output_wav_file, "wb") as wav_file:
        voice.synthesize_wav(text, wav_file)
        
    mixer.init() # Initialize the mixer module
    sound = mixer.Sound('output.wav')
    sound.play()

    print(f"Audio saved to {output_wav_file}")


cirilica:bool=False
Mod=0
lastmod=-1 
def ScreenDisplay(q:Queue):
  
    def ModeSwitch(q:Queue,slova:list[PushButton]):
        try:
            global cirilica
            global Mod
            global lastmod
            data=None
            if(q.qsize() != 0):
             data=q.get()
             print("data resived ="+str(data))
             print("data is type of "+str(type(data)))
            if(data=="0" or data=="1" or data=="2"):  
                    print("modovi change")
                    Mod=int(data)
                    slovo=0
                    if(Mod!=lastmod):
                        for SlikeSlova in slova:
                            lastmod=Mod
                            if cirilica:
                                SlikeSlova.image=ListaCirilica[Mod]+listaSlovaLat[slovo]+".png"
                                SlikeSlova.update_command(Ispisitext,args=[listaSlovaLat[slovo],textarea,Mod,listaSlovaCir[slovo]])
                            else:
                                SlikeSlova.image=ListaLatinica[Mod]+listaSlovaLat[slovo]+".png"
                                SlikeSlova.update_command(Ispisitext,args=[listaSlovaLat[slovo],textarea,Mod,listaSlovaLat[slovo]])
                            SlikeSlova.width=appwitdh
                            SlikeSlova.height=appheight
                            slovo+=1
            elif(data=="Cirilica"):
                print("pismo change")
                cirilica=True
                slovo=0
                for SlikeSlova in slova:
                            lastmod=Mod
                            if cirilica:
                                SlikeSlova.image=ListaCirilica[Mod]+listaSlovaLat[slovo]+".png"
                                SlikeSlova.update_command(Ispisitext,args=[listaSlovaLat[slovo],textarea,Mod,listaSlovaCir[slovo]])
                            else:
                                SlikeSlova.image=ListaLatinica[Mod]+listaSlovaLat[slovo]+".png"
                                SlikeSlova.update_command(Ispisitext,args=[listaSlovaLat[slovo],textarea,Mod,listaSlovaLat[slovo]])
                            SlikeSlova.width=appwitdh
                            SlikeSlova.height=appheight
                            slovo+=1
            elif(data=="Latinica"):
                    print("pismo change")
                    cirilica=False
                    slovo=0
                    for SlikeSlova in slova:
                            lastmod=Mod
                            if cirilica:
                                SlikeSlova.image=ListaCirilica[Mod]+listaSlovaLat[slovo]+".png"
                                SlikeSlova.update_command(Ispisitext,args=[listaSlovaLat[slovo],textarea,Mod,listaSlovaCir[slovo]])
                            else:
                                SlikeSlova.image=ListaLatinica[Mod]+listaSlovaLat[slovo]+".png"
                                SlikeSlova.update_command(Ispisitext,args=[listaSlovaLat[slovo],textarea,Mod,listaSlovaLat[slovo]])
                            SlikeSlova.width=appwitdh
                            SlikeSlova.height=appheight
                            slovo+=1
                
        except Exception as e:
            print("error "+str(e))
           
          
        
   


    ListaLatinica=["slike/","SlovaiSlikeLatinica/","Slovalatinica/"]    
    ListaCirilica=["slike/","slikeislova/","Slova/"]
    slova:list[PushButton]=[]
    listaSlovaLat=["A","B","V","G","D","Đ","E","Ž","Z","I","J","K","L","Lj","M","N","Nj","O","P","R","S","T","Ć","U","F","H","C","Č","Ć","Š"]
    listaSlovaCir=["А","Б", "В", "Г", "Д", "Ђ", "Е", "Ж", "З", "И", "Ј", "К", "Л", "Љ", "М", "Н", "Њ", "О", "П", "Р", "С", "Т", "Ћ", "У", "Ф", "Х", "Ц", "Ч", "Џ", "Ш"]
    appwitdh=10
    appheight=10
    app = App(title="My app")
    app.set_full_screen()
    appwitdh=round(app.width*0.098)
    appheight=round(app.height*0.125)
    #app.tk.config(cursor="cursor/pointer.cur") 
    #MainBox = Box(app,layout="grid",align="bottom",width=app.width,height=app.height)

    UiBox= Box(app,align="top",width=app.width,height=appheight)

    PushButton(UiBox, image="Pesma.png",width=appwitdh,height=appheight,align="left",command=PustiPesmu)
    textarea=Text(UiBox,text="",align="left",width="fill",size=30,font="Helvetica",)
    PushButton(UiBox, image="Delete.png",width=appwitdh,height=appheight,command= izbrisitext ,align="left",args=[textarea])

    UiBox2= Box(app,align="top",width=app.width,height=appheight)

    PushButton(UiBox2, image="izgovor.png",width=appwitdh,height=appheight,command= PiperPlay ,args=[textarea])

    slovaBox = Box(app,layout="grid",align="bottom",width=app.width,height=appheight*3.3)
    slovo=0
    for y in range(3):
        for x in range(10):

            try:
                if(Mod==0 or Mod==1 or Mod==2):
                    if cirilica:
                     slova.append (PushButton(slovaBox , image=ListaLatinica[Mod]+listaSlovaLat[slovo]+".png",width=appwitdh,height=appheight,grid=[x,y],command= Ispisitext,args=[listaSlovaLat[slovo],textarea,Mod,listaSlovaCir[slovo]]))
                    else:
                     slova.append (PushButton(slovaBox , image=ListaLatinica[Mod]+listaSlovaLat[slovo]+".png",width=appwitdh,height=appheight,grid=[x,y],command= Ispisitext,args=[listaSlovaLat[slovo],textarea,Mod,listaSlovaLat[slovo]]))

                else:
                    print("out of range "+str(Mod))
                    
            except Exception as e:
                print("error "+str(e))
            slovo+=1

    slovaBox.repeat(100,ModeSwitch,args=[q,slova])
   
        

    app.display()


async def Conection():
    devices = await BleakScanner.discover()
    counter=0
    for d in devices:
        print(f"({counter})"+str(d))
        counter+=1
    number=int(input())
    if(number!=2007):
        async with BleakClient(devices[number]) as client:
                print("Conected to the desegnated device "+str(client.is_connected))
                return client

def between_callback():
    asyncio.run(CitajControler())

def PhoneComunication(q:Queue):
    try:
        while True:
            key=keyboard.read_key()
            print(key)
            match key:
             case "0":
                q.put("0")
             case "1":
                q.put("1")
             case "2":
                q.put("2")
    except:
        print("error")
        
async def CitajProfesorskiControler(q):
    try:
        lastcode=-1
        characteristicUid="beb5483e-36e1-4688-b7f5-ea07361b26a8"
        devices = await BleakScanner.discover()
        name="SlovaricaProfesorskiKontroler"
        counter=0
        
        for d in devices:
          if(d.name==name):
                async with BleakClient(d) as client:
                        print("Conected to the desegnated device SlovaricaProfesorskiKontroler "+str(client.is_connected))
                        while client.is_connected:
                            code= (await client.read_gatt_char(characteristicUid)).decode("utf-8")
                            if (code=="0" or  code=="1" or code=="2" or code=="Cirilica" or code=="Latinica"):
                                if(lastcode!=code):
                                    q.put(code)
                                    lastcode=code
                                    print(code)
                      
                               
    except Exception as e:
        print("error citaj controler "+str(e))
        
def between_callbackProfesorski(q:Queue):
    asyncio.run(CitajProfesorskiControler(q))       
async def main():
    
    q = Queue()
    q.put("1")
    CreateDisplay= threading.Thread(target=ScreenDisplay,args=[q]) 
    CreateDisplay.start()
  
   
    Citajcontroler= threading.Thread(target=between_callback) 
    Citajcontroler.start()
    
    CitajAplikaciju= threading.Thread(target=between_callbackProfesorski,args=[q]) 
    CitajAplikaciju.start()
   
                    
    print("after jojstick")       
    
    
    CreateDisplay.join()
   # Citajcontroler.join()
    CitajAplikaciju.join()
    q.join()
    
   
   
try:
    asyncio.run(main())   
except Exception as e:
    print("eror during boot "+str(e))
