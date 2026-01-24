
from guizero import App, PushButton, Picture,Drawing,Box,Text
from pygame import mixer

def Ispisitext(num,textarea:Text):
    print("Button was pressed  "+str( UiBox.children[1]))
    textarea.append(num)
    mixer.init()
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



    
Mod=2
ListaLatinica=["","",""]    
ListaCirilica=["slike/","slikeislova/","Slova/"]
slova=[]
listaSlova=["A","B","V","G","D","Đ","E","Ž","Z","I","J","K","L","Lj","M","N","Nj","O","P","R","S","T","Ć","U","F","H","C","Č","Ć","Š"]
appwitdh=10
appheight=10


app = App(title="My app")
app.set_full_screen()
appwitdh=round(app.width*0.099)
appheight=round(app.height*0.125)

#MainBox = Box(app,layout="grid",align="bottom",width=app.width,height=app.height)

UiBox= Box(app,align="top",width=app.width,height=appheight)

PushButton(UiBox, image="Pesma.png",width=appwitdh,height=appheight,align="left",command=PustiPesmu)
textarea=Text(UiBox,text="",align="left",width="fill",size=30,font="Helvetica")
PushButton(UiBox, image="Delete.png",width=appwitdh,height=appheight,command= izbrisitext ,align="left",args=[textarea])
slovaBox = Box(app,layout="grid",align="bottom",width=app.width,height=appheight*3.3)
slovo=0
for y in range(3):
 for x in range(10):

  try:
   if(Mod==0):
    slova.append (PushButton(slovaBox , image=ListaCirilica[Mod]+listaSlova[slovo]+".png",width=appwitdh,height=appheight,grid=[x,y],command= Ispisitext,args=[listaSlova[slovo],textarea]))
   elif(Mod==1):
    slova.append (PushButton(slovaBox , image=ListaCirilica[Mod]+listaSlova[slovo]+".png",width=appwitdh,height=appheight,grid=[x,y],command= Ispisitext,args=[listaSlova[slovo],textarea]))
   elif(Mod==2):
    slova.append (PushButton(slovaBox , image=ListaCirilica[Mod]+listaSlova[slovo]+".png",width=appwitdh,height=appheight,grid=[x,y],command= Ispisitext,args=[listaSlova[slovo],textarea]))
   else:
    print("out of range "+Mod)
       
  except Exception as e:
   print("error "+str(e))
  slovo+=1

app.display()

