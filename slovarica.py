
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
adresaslike=""
app="a"
timer=0
slova:list[PushButton]
igra=False
ListaLatinica=["slike/","SlovaiSlikeLatinica/","Slovalatinica/"]   
ListaCirilica=["slike/","slikeislova/","Slova/"]
listaSlovaCirLatinica=["A","B", "V", "G", "D", "Đ", "E", "Ž", "Z",
 "I", "J", "K", "L", "Lj", "M", "N", "Nj", "O", "P", "R", "S", "T",
 "Ć", "U", "F", "H", "C", "Č", "Dž", "Š"]
listaSlovaLat=["A", "B", "C", "Č", "Ć", "D", "Dž", "Đ", "E", "F", "G", "H", "I", "J", "K", "L", "Lj", "M", "N", "Nj", "O", "P", "R", "S", "Š", "T", "U", "V", "Z", "Ž"]
listaSlovaCir=["А","Б", "В", "Г", "Д", "Ђ", "Е", "Ж", "З", "И", "Ј", "К", "Л", "Љ", "М", "Н", "Њ", "О", "П", "Р", "С", "Т", "Ћ", "У", "Ф", "Х", "Ц", "Ч", "Џ", "Ш"]

def PromeniMod(mod):
    global igra
    global Mod
    if(mod=="0" or mod=="1" or mod=="2"):
     Mod=mod
def PromeniPismo(pismo):
    global cirilica                           
    if(pismo=="1"):
        cirilica=True
    if(pismo=="0" ):
        cirilica=False
    
def zadajslovo(Slovo :str):
    global zadatoslovo
    global listaSlovaLat
    global listaSlovaCir
    global listaSlovaCirLatinica
    global adresaslike
    if cirilica:
        for slovo in listaSlovaCirLatinica:
            if(slovo.lower()==Slovo.lower()):
                if(zadatoslovo!=slovo):
                 zadatoslovo=slovo
                 adresaslike=ListaCirilica[int(Mod)]+slovo+".png"
                 GameStart()
                else:
                    print("vec je to slovo bilo zadato")
        for slovo in listaSlovaLat:
            if(slovo.lower()==Slovo.lower()):
                if(zadatoslovo!=slovo):
                 zadatoslovo=slovo
                 adresaslike=ListaCirilica[int(Mod)]+slovo+".png"
                 GameStart()
                else:
                    print("vec je to slovo bilo zadato")
        
    else:
        for slovo in listaSlovaLat:
            
            if(slovo.lower()==Slovo.lower()):
             if(zadatoslovo!=slovo):   
              zadatoslovo=slovo
              adresaslike=ListaLatinica[int(Mod)]+slovo+".png"
              GameStart()
             else:
              print("vec je to slovo bilo zadato")

    
def Anim(color:str):
    global app
    global picture
    global zadatoslovo
    global Mod
    global cirilica
    app.bg=color
    if("lightgreen"==color):
     if cirilica:
         picture.image=adresaslike
     else:
         print(adresaslike)
         picture.image=adresaslike
     mixer.init()
     mixer.music.set_volume(1)
     mixer.music.load("AudioSlova/"+zadatoslovo+".mp3")
     mixer.music.play()
     picture.visible=True
     time.sleep(1)
    if("green"==color):
     mixer.init()
     mixer.music.set_volume(1)
     mixer.music.load("game/win.mp3")
     mixer.music.play()
     picture.visible=True
     if cirilica:
         picture.image=adresaslike
     else:
         print(adresaslike)
         picture.image=adresaslike
    if("red"==color):
      picture.visible=False
      print("red")
    if("orange"==color):
         mixer.init()
         mixer.music.load("pronadji.mp3")
         mixer.music.set_volume(0.7)
         mixer.music.play()
         time.sleep(3) 
         mixer.music.load("AudioSlova/"+zadatoslovo+".mp3")
         mixer.music.set_volume(0.7)
         mixer.music.play()
         picture.visible=True
         if cirilica:
             picture.image=adresaslike
         else:
             print(adresaslike)
             picture.image=adresaslike
        
    time.sleep(2)
    app.bg="white"
    picture.image="temp.png"
    picture.visible=False
def Hint():
     anim = threading.Thread(target=Anim,args=["orange"]) 
     anim.start()
async def Citaj(client:BleakClient,uiid):# cita i salje podatke
    global igra
    global cirilica
    global Mod
    global zadatoslovo
    code= (await client.read_gatt_char(uiid)).decode("utf-8")
    tekst=code.split('_')
    if(isinstance(tekst, list) and len(tekst)==4):
      if(igra==False):
         PromeniPismo(tekst[0])
         PromeniMod(tekst[1])
         print("Zadato slovo: "+tekst[2])
         if(Mod=="1" or Mod=="2"):
          zadajslovo(tekst[2])
          
      return tekst
    else:
     return code
HintBoll=True
def Game():
    global igra
    global timer
    global HintBoll
    if(timer>=30):
        if(HintBoll==True):
         HintBoll=False
         Hint()
    if(timer>=60):
        GameEndFail()
    if(igra):
     timer+=1
     
def GameEnd():
     global igra
     global timer
     anim = threading.Thread(target=Anim,args=["green"]) 
     anim.start()
     igra=False
     timer=0
     
def GameEndFail():
     global igra
     global timer
     anim = threading.Thread(target=Anim,args=["lightgreen"]) 
     anim.start()
     igra=False
     timer=0
 
def ShowLetter():
    global cirilica
    global Mod
    global slova
    string
    for slovo in slova:
       string=str(slovo.image).split("/")
def GameStart():
    global timer
    global igra
    global cirilica
    global zadatoslovo
    igra=True
    textarea.value=""
    timer=0
    mixer.init()
    mixer.music.load("pronadji.mp3")
    mixer.music.set_volume(0.7)
    mixer.music.play()
    time.sleep(3) 
    mixer.music.load("AudioSlova/"+zadatoslovo+".mp3")
    mixer.music.set_volume(0.7)
    mixer.music.play()
    
    
async def Pisi(client :BleakClient,uiid,poruka:Queue):#procita i pise podatke (cita da nebi doslo do brisanja podataka)
     text=await Citaj(client,uiid)
     if(poruka.qsize() != 0):
      await client.write_gatt_char(uiid,SastaviPoruku(text,poruka),True)


def SastaviPoruku(original,q:Queue):
    original[3]=str(q.get())
    return (f"{original[0]}_{original[1]}_{original[2]}_{original[3]}").encode("utf-8")
    

async def CitajControler(q:Queue):
    while True:
        try:
            characteristicUidControler="beb5483e-36e1-4688-b7f5-ea07361b26a8"
            characteristicUid="beb5483e-36e1-4688-b7f5-ea07361b26b9"
            devices = await BleakScanner.discover()
            counter=0
            name="Slovarica"
            for d in devices:
             if(d.name==name):
                    async with BleakClient(d) as client:
                        print("Conected to the desegnated device "+str(client.is_connected))
                        while client.is_connected:
                            code= await Citaj(client,characteristicUidControler)
                            if code=="TASTER":
                                print("TASTER")
                                pyautogui.click()
                            if code=="LEVO":
                                print(f"Model Number: {code}")
                                pyautogui.move(-100, 0,duration=0.1)
                            if code=="DOLE": 
                                print(f"Model Number: {code}")
                                pyautogui.move(0, 100,duration=0.1)
                            if code=="DESNO":
                                print(f"Model Number: {code}")
                                pyautogui.move(100, 0,duration=0.1)
                            if code=="GORE":
                                print(f"Model Number: {code}") 
                                pyautogui.move(0, -100,duration=0.1)    
                            tekst=await Citaj(client,characteristicUid)
                            if(q.qsize!=0):
                             await Pisi(client,characteristicUid,q)
                            print("jojstic: "+str(code))
                            print("phone: "+str(tekst))
                            time.sleep(0.1)
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
       
def Ispisitext(num #Za audio
               ,textarea:Text,Mod,Slovo #slovo koje se unosi
               ):
   print("pritisnuto")
   global igra
   if(igra==False):
        if(len(textarea.value)<29):
         textarea.append(Slovo)
        mixer.init()
        if Mod==0:
           print("AudioPojam/"+num+".mp3")
           mixer.music.load("AudioPojam/"+num+".mp3")
        else:
            print("AudioSlova/"+num+".mp3")
            mixer.music.load("AudioSlova/"+num+".mp3")
        mixer.music.set_volume(0.7)
        mixer.music.play()
   else:
        if(Slovo==zadatoslovo):
            GameEnd()
        elif(num==zadatoslovo):
            GameEnd()
        else:
            mixer.init()
            if Mod==0:
             print("AudioPojam/"+num+".mp3")
             mixer.music.load("AudioPojam/"+num+".mp3")
            else:
                print("AudioSlova/"+num+".mp3")
                mixer.music.load("AudioSlova/"+num+".mp3")
                mixer.music.set_volume(0.7)
                mixer.music.play()
            anim = threading.Thread(target=Anim,args=["red"]) 
            anim.start()
           

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

textarea="A"
cirilica:bool=True
Mod=1
zadatoslovo="/"
lastmod=-1 
lastpismo=False
picture=Picture
def ScreenDisplay(q:Queue):
  
    def ModeSwitch(q:Queue,slova:list[PushButton]):
        try:
            global listaSlovaCirLatinica
            global cirilica
            global Mod
            global lastmod
            global lastpismo
            if(Mod=="0" or Mod=="1" or Mod=="2"): 
                    slovo=0
                    if(Mod!=lastmod):
                        print("modovi change" +str(Mod))
                        for SlikeSlova in slova:
                            lastmod=Mod
                            if cirilica:
                                SlikeSlova.image=ListaCirilica[int(Mod)]+listaSlovaCirLatinica[slovo]+".png"
                                SlikeSlova.update_command(Ispisitext,args=[listaSlovaCirLatinica[slovo],textarea,int(Mod),listaSlovaCir[slovo]])
                            else:
                                SlikeSlova.image=ListaLatinica[int(Mod)]+listaSlovaLat[slovo]+".png"
                                SlikeSlova.update_command(Ispisitext,args=[listaSlovaLat[slovo],textarea,int(Mod),listaSlovaLat[slovo]])
                            SlikeSlova.width=appwitdh
                            SlikeSlova.height=appheight
                            slovo+=1
            if(cirilica==True and lastpismo==False):
                slovo=0
                print("cirilica")
                lastpismo=cirilica
                for SlikeSlova in slova:
                            if cirilica:
                                SlikeSlova.image=ListaCirilica[int(Mod)]+listaSlovaCirLatinica[slovo]+".png"
                                SlikeSlova.update_command(Ispisitext,args=[listaSlovaCirLatinica[slovo],textarea,int(Mod),listaSlovaCir[slovo]])
                            else:
                                SlikeSlova.image=ListaLatinica[int(Mod)]+listaSlovaLat[slovo]+".png"
                                SlikeSlova.update_command(Ispisitext,args=[listaSlovaLat[slovo],textarea,int(Mod),listaSlovaLat[slovo]])
                            SlikeSlova.width=appwitdh
                            SlikeSlova.height=appheight
                            slovo+=1
            elif(cirilica==False and lastpismo==True):
                    slovo=0
                    print("latinica")
                    lastpismo=cirilica
                    for SlikeSlova in slova:
                            if cirilica:
                                SlikeSlova.image=ListaCirilica[int(Mod)]+listaSlovaCirLatinica[slovo]+".png"
                                SlikeSlova.update_command(Ispisitext,args=[listaSlovaCirLatinica[slovo],textarea,int(Mod),listaSlovaCir[slovo]])
                            else:
                                SlikeSlova.image=ListaLatinica[int(Mod)]+listaSlovaLat[slovo]+".png"
                                SlikeSlova.update_command(Ispisitext,args=[listaSlovaLat[slovo],textarea,int(Mod),listaSlovaLat[slovo]])
                            SlikeSlova.width=appwitdh
                            SlikeSlova.height=appheight
                            slovo+=1

        except Exception as e:
            print("error switch "+str(e))
           
    global listaSlovaCirLatinica
    global picture
    global textarea
    global slova
    global app
    global ListaLatinica
    global ListaCirilica
    global listaSlovaLat
    global listaSlovaCir
    slova=[]
    appwitdh=10
    appheight=10
    app = App(title="Slovarica ",width=1920,height=1080)
    app.set_full_screen()
    appwitdh=round(app.width*0.098)
    appheight=round(app.height*0.125)
    #app.tk.config(cursor="cursor/pointer.cur") 
    #MainBox = Box(app,layout="grid",align="bottom",width=app.width,height=app.height)
    app.bg="White"

    UiBox= Box(app,align="top",width=app.width,height=appheight)

    PushButton(UiBox, image="Pesma.png",width=appwitdh,height=appheight,align="left",command=PustiPesmu)
    textarea=Text(UiBox,text="",align="left",width="fill",size=50,font="Arial",)
    PushButton(UiBox, image="Delete.png",width=appwitdh,height=appheight,command= izbrisitext ,align="left",args=[textarea])

    UiBox2= Box(app,align="top",width=app.width,height=appheight)
    UiBox3= Box(app,align="top",width=appwitdh,height=appheight*1.5)
    picture = Picture(UiBox3,width=appwitdh,height=appheight ,image="temp.png",align="bottom") 
    PushButton(UiBox2, image="izgovor.png",width=appwitdh,height=appheight,command= PiperPlay ,args=[textarea])

    slovaBox = Box(app,layout="grid",align="bottom",width=app.width,height=appheight*3.3)
    slovo=0
    for y in range(3):
        for x in range(10):

            try:
                if(Mod==0 or Mod==1 or Mod==2):
                    if cirilica:
                     slova.append (PushButton(slovaBox , image=ListaCirilica[Mod]+listaSlovaCirLatinica[slovo]+".png",width=appwitdh,height=appheight,grid=[x,y],command= Ispisitext,args=[listaSlovaLat[slovo],textarea,Mod,listaSlovaCir[slovo]]))
                    else:
                     slova.append (PushButton(slovaBox , image=ListaLatinica[Mod]+listaSlovaLat[slovo]+".png",width=appwitdh,height=appheight,grid=[x,y],command= Ispisitext,args=[listaSlovaLat[slovo],textarea,Mod,listaSlovaLat[slovo]]))

                else:
                    print("out of range "+str(Mod))
                    
            except Exception as e:
                print("error "+str(e))
            slovo+=1

    slovaBox.repeat(100,ModeSwitch,args=[q,slova])
    app.repeat(1000,Game,args=[])

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

def between_callback(q:Queue):
    asyncio.run(CitajControler(q))

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
        

async def main():

    q = Queue()
    q.put("1")
    CreateDisplay= threading.Thread(target=ScreenDisplay,args=[q]) 
    CreateDisplay.start()
  
   
    Citajcontroler= threading.Thread(target=between_callback,args=[q]) 
    Citajcontroler.start()
    
   
                    
    print("after jojstick")       
    
    
    CreateDisplay.join()
    Citajcontroler.join()
    q.join()
    
   
   
try:
    asyncio.run(main())   
except Exception as e:
    print("eror during boot "+str(e))
