# This is a code to SoundSpot player.
# Thanks to our programer Igor Kowalski for realization of this project

# Importing main extensions
from tkinter import *
import customtkinter as ctk
import glob,os,pygame,datetime
from mutagen.mp3 import MP3 # For playing MP3 files

# For controling volume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

window = ctk.CTk(fg_color="#302D2D",)
window.geometry("1080x720")
window.title("SoundSpot (Version Alpha 0.0.1)")
window.resizable("False","False")
pygame.mixer.init()
i = 0
dlugosc1 = 0

# Stands for recieving all Mp3 files from folder
files = list(glob.glob('sounds/*.mp3',  
                   recursive = True))
print(files)

nr_ofFiles = len(files) - 1 
isplaying = ""
window.wm_attributes("-transparent","#000000")

print(files)

# Commands
def Volchange(val): # Stands for changing volume up and down
	devices = AudioUtilities.GetSpeakers()
	interface = devices.Activate(
	   IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
	volume = cast(interface, POINTER(IAudioEndpointVolume))
	 
	# Control volume
	print(Volvar.get())
	#volume.SetMasterVolumeLevel(-0.0, None) #max
	#volume.SetMasterVolumeLevel(-5.0, None) #72%
	volume.SetMasterVolumeLevel(-50+(Volvar.get()/2), None) #51%

def playing1(): # Change to next song
    global songstate, files,i, NowPlaying, Volvar
    Volchange
    songstate = 1
    if (songstate == 0):
        sound()
        
    elif (songstate==1):
        pygame.mixer.music.stop()
        PlayButtonImage.config(file="textures\\Play.png")
        skip()
        try:
            if (i%2!=1):
                i=i+2
            else: 
                i=i+1
            pygame.mixer.music.load(files[filenr])
            pygame.mixer.music.play(loops=0)
            pygame.mixer.music.pause()
            songstate = 0
            NowPlaying = files[filenr]
            NowPlaying = NowPlaying.replace("sounds\\","")
            NowPlaying2.set("Now Playing: " + NowPlaying)
        except:
            i=0

def playing2(): # Change to previous song
    global songstate, files,i, NowPlaying
    Volchange
    try:
        songstate = -1
        if (songstate == 0):
            sound()
        elif (songstate == -1):
            pygame.mixer.music.stop()
            PlayButtonImage.config(file="textures\\Play.png")
            goback()
            if (i%2!=1):
                i = i + 2
            else: 
                i = i + 1
            pygame.mixer.music.load(files[filenr])
            pygame.mixer.music.play(loops=0)
            pygame.mixer.music.pause()
            songstate = 0
            NowPlaying = files[filenr]
            NowPlaying = NowPlaying.replace("sounds\\","")
            NowPlaying2.set("Now Playing: " + NowPlaying)
    except:
        i = len(files)-1

def sound(): # Stands for song state
    global i,PlayButtonImage, filenr, NowPlaying,isplaying, TimelineLength, dlugosc1
    Volchange
    if (i==0): # In that case, music would be in playing state
        pygame.mixer.music.load(files[filenr])
        pygame.mixer.music.play(loops=0)

        print ("played sound")
        print("now playing: ",files[filenr])
        isplaying ="playing"

        NowPlaying = files[filenr]
        NowPlaying = NowPlaying.replace("sounds\\","")
        NowPlaying2.set("Now Playing: " + NowPlaying)

        PlayButtonImage.config(file="textures\\Pause.png")
        audio = MP3(files[filenr])
        dlugosc1 = audio.info.length
        TimelineLength = dlugosc1/10
        #Draw()
        #Refresh()
        dlugosc2 = str(datetime.timedelta(seconds=dlugosc1))
        print(dlugosc2[0:7])
                
    elif (i%2==1): # In that case, music would be in pause state
        pygame.mixer.music.pause()
        print ("paused sound")
        print("now playing: ", files[filenr])
        isplaying = "paused"
        PlayButtonImage.config(file="textures\\Play.png")
        audio = MP3(files[filenr])
        dlugosc1 = audio.info.length
        TimelineLength = dlugosc1/10
        #Draw()
        #Refresh()
        dlugosc2 = str(datetime.timedelta(seconds=dlugosc1))
        print(dlugosc2[0:7])

    elif (i%2==0):
        if (pygame.mixer.get_busy() == False):
            pygame.mixer.music.unpause()

        print ("unpaused sound")
        print("now playing: ", files[filenr])
        isplaying="playing"

        PlayButtonImage.config(file="textures\\Pause.png")
        audio = MP3(files[filenr])
        dlugosc1 = audio.info.length
        TimelineLength = dlugosc1/10
        #Draw()
        #Refresh()
        dlugosc2 = str(datetime.timedelta(seconds=dlugosc1))
        print(dlugosc2[0:7])
    i = i+1

def przelacz(x): # Stands for music buttons
    global i,PlayButtonImage, filenr, NowPlaying,isplaying,songstate, TimelineLength, dlugosc1
    Volchange
    pygame.mixer.music.load(files[x])
    pygame.mixer.music.play(loops=0)
    print ("played sound")
    print("now playing: ", files[x])
    isplaying="playing"

    NowPlaying = files[x]
    NowPlaying = NowPlaying.replace("sounds\\","")
    NowPlaying2.set("Now Playing: " + NowPlaying)

    PlayButtonImage.config(file="textures\\Pause.png")
    audio = MP3(files[x])
    dlugosc1 = audio.info.length
    TimelineLength = dlugosc1/10
    #Draw()
    #Refresh()
    dlugosc2 = str(datetime.timedelta(seconds=dlugosc1))
    print(dlugosc2[0:7])
    i=i+1



def skip(): # Stands for changing music to next one
    global filenr, nr_ofFiles, songstate
    if (filenr <= nr_ofFiles):
        filenr = filenr + 1
        songstate = 1
    else:
        filenr = 0

def goback(): # Stands for changing music to previous one
    global filenr, songstate
    if (filenr != 0):
        filenr = filenr - 1
        songstate = -1

def Draw():
    global progressbar, Timelinestate, TimelineLength
    progressbar.step(Timelinestate)

def Refresh():
    global progressbar, Timelinestate, TimelineLength, dlugosc1
    if (Timelinestate < TimelineLength): 
        Timelinestate = Timelinestate + (dlugosc1 * 0.0001)
        progressbar.config(variable = TimelineLength)
        progressbar.step(Timelinestate)
        window.after(1000,Refresh)





# Creating GUI widgets
Image1 = PhotoImage(file = "textures\\image 1.png")
Image2 = PhotoImage(file = "textures\\image 2.png")
Image3 = PhotoImage(file = "textures\\image 3.png")
Image4 = PhotoImage(file = "textures\\image 4.png")
Image5 = PhotoImage(file = "textures\\image 5.png")
ArrowSkip = PhotoImage(file = "textures\\Next.png")
ArrowBack = PhotoImage(file = "textures\\Previous.png")
PlayButtonImage = PhotoImage(file = "textures\\Play.png")
HomeImage = PhotoImage(file = "textures\\HOME.png")
VolumeImage = PhotoImage(file = "textures\\Volume.png")
LogoImage = PhotoImage(file = "textures\\SoundSpot.png")
LabelImage = PhotoImage(file = "textures\\Label.png")
LineImage = PhotoImage(file = "textures\\Line.png")

ListImage = [Image1,Image2,Image3]

# Creating GUI frames
BG = PhotoImage(file = "textures\\bg.png") 
BGLabel = ctk.CTkLabel(window,
    image = BG,
    text = "")

GUIFrame = ctk.CTkFrame(window,
	fg_color = "#211E1E",
	bg_color = "transparent",
	)

PlaylistFrame = ctk.CTkFrame(window,
	fg_color = "#302D2D",
	bg_color = "transparent",
	)

NowPlaying = "a"
NowPlaying2 = StringVar()

NowPlayingLabel = ctk.CTkButton(window,
	image = Image4,
	textvariable = NowPlaying2,
	text_color = "#FFFFFF",
	font = ("Inter",15),
	fg_color = "#302D2D",
	bg_color = "#211E1E",
	state = "DISABLED",
	corner_radius = 16
	)

VolumeUp = ctk.CTkButton(GUIFrame,command=lambda:c)

for p in range(0,nr_ofFiles+1): # Generating music buttons
    btn = ctk.CTkButton(PlaylistFrame,
    	image = ListImage[p],
    	text = files[p],
    	width = 709,
    	anchor = "w",
    	text_color = "#FFFFFF",
    	font = ("Inter",15),
    	fg_color = "#686464",
    	bg_color = "transparent",
    	corner_radius = 6,
    	height = 36,
    	command = lambda p = p:przelacz(p))
    btn.pack(ipadx = 21,pady = 4)


pixel = PhotoImage(height = 1,width = 1)

PlaceHolder = ctk.CTkFrame(window,
	bg_color = "transparent",
	fg_color = "transparent",
	height = 0,
	width = 0
	)

LineLabel = ctk.CTkLabel(window,
	image = LineImage,
	fg_color = "#211E1E",
	text = "")

LabelLabel = ctk.CTkLabel(window,
	image = LabelImage,
	fg_color = "#211E1E",
	text = "")

HomeLabel = ctk.CTkLabel(window,
	image = HomeImage,
	fg_color = "#211E1E",
	text = "")

LogoLabel = ctk.CTkLabel(window,
	image = LogoImage,
	fg_color = "#211E1E",
	text = "")

BtnPlay = ctk.CTkButton(GUIFrame, 
	image = PlayButtonImage,
	text = "",
	fg_color = "transparent",
	bg_color = "transparent",
	width = 20,
	height = 80,
	command = lambda:sound())

VolumeIcon = ctk.CTkLabel(window, 
	image = VolumeImage,
	fg_color = "#211E1E",
	bg_color = "#211E1E",
	text = "",
	width = 16,
	height = 14,
	)


BtnSkip = ctk.CTkButton(GUIFrame,
	image = ArrowSkip,
	text = "",
	fg_color = "transparent",
	bg_color = "transparent",
	height = 80,
	width = 50,
	command = lambda:playing1())

BtnGoBack = ctk.CTkButton(GUIFrame,
	image = ArrowBack,
	text = "",
	fg_color = "transparent",
	bg_color = "transparent",
	height = 80,
	width = 50,
	command = lambda:playing2())


Volvar = DoubleVar() # Stands for volume

Volume = ctk.CTkSlider(window,
	variable = Volvar,
	from_ = 0,
	to = 100,
	bg_color = "#211E1E",
	button_color = "#D9D9D9",
	progress_color = "#10B93F",
	command = Volchange
	)

# Creating starting values
filenr = 1 
songstate = 0 # Stands for song state
NowPlaying = files[filenr] # What is music now playing
NowPlaying = NowPlaying.replace("sounds\\","")
NowPlaying2.set("Now Playing: " + NowPlaying)

Timelinestate = 0
TimelineLength = 0




# Creating wigets
HomeLabel.place(x = 77, y = 69)
LogoLabel.place(x = 983, y = 18)
BGLabel.place(x = 0, y = 0)
PlaceHolder.pack(side = BOTTOM, pady = 50)
GUIFrame.pack(side = BOTTOM, ipady = 6)
NowPlayingLabel.pack(side = BOTTOM, ipady = 8, ipadx = 24, pady = 18)
PlaylistFrame.pack(ipadx = 50, ipady = 24,side = BOTTOM)
LineLabel.pack(side = BOTTOM)
LabelLabel.pack(side = BOTTOM)
BtnGoBack.pack(side = LEFT)
BtnPlay.pack(side = LEFT)
BtnSkip.pack(side = LEFT)
VolumeIcon.place(x = 855, y = 626)
Volume.place(x = 884, y = 626)


#Draw()
#Refresh()


window.mainloop()