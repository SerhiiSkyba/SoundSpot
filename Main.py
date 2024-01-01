# This is the code for SoundSpot player.
# Thanks to our programmer Igor Kowalski for realization of this project

# Importing main extensions
from tkinter import *
import customtkinter as ctk
import glob,os,pygame,datetime
from mutagen.mp3 import MP3
import random
# For controlling volume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

window = ctk.CTk(fg_color="#211E1E",)
window.geometry("1080x720")
window.title("SoundSpot (Version Alpha 0.0.1)")
window.resizable("False","False")
pygame.mixer.init()
i = 0
dlugosc1 = 0  # variable for getting the legth of playing file 

# Importing all mp3 files from folder to a list
files = list(glob.glob('sounds/*.mp3',  
                   recursive = True))
print(files)

nr_ofFiles = len(files) - 1 
isplaying = ""

# Commands
def Volchange(val): # Changing volume
	devices = AudioUtilities.GetSpeakers()
	interface = devices.Activate(
	   IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
	volume = cast(interface, POINTER(IAudioEndpointVolume))
	 
	# Control volume
	print(Volvar.get())
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

def sound():
    global i,PlayButtonImage, filenr, NowPlaying,isplaying, TimelineLength, dlugosc1
    Volchange
    if (i==0): # In this case, music is played
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
        dlugosc2 = str(datetime.timedelta(seconds=dlugosc1))
        print(dlugosc2[0:7])
                
    elif (i%2==1): # In this case, music is paused
        pygame.mixer.music.pause()
        print ("paused sound")
        print("now playing: ", files[filenr])
        isplaying = "paused"
        PlayButtonImage.config(file="textures\\Play.png")
        audio = MP3(files[filenr])
        dlugosc1 = audio.info.length
        TimelineLength = dlugosc1/10
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
        dlugosc2 = str(datetime.timedelta(seconds=dlugosc1))
        print(dlugosc2[0:7])
    i = i+1

def przelacz(x): # Playlist functionality
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
    dlugosc2 = str(datetime.timedelta(seconds=dlugosc1))
    print(dlugosc2[0:7])
    i=i+1

def skip(): # Function for skipping to another file
    global filenr, nr_ofFiles, songstate
    if (filenr <= nr_ofFiles):
        filenr = filenr + 1
        songstate = 1
    else:
        filenr = 0

def goback(): # Function for going back to the previous file
    global filenr, songstate
    if (filenr != 0):
        filenr = filenr - 1
        songstate = -1

def ThemeChange():
    global BgMode
    if (BgMode == "dark"):
        BgMode = "light"
        BG.config(file = "textures\\bg_L.png")
        ArrowSkip.config(file = "textures\\Next_L.png")
        ArrowBack.config(file = "textures\\Previous_L.png")
        PlayButtonImage.config(file = "textures\\Play_L.png")
        HomeImage.config(file = "textures\\HOME_L.png")
        VolumeImage.config(file = "textures\\Volume_L.png")
        LogoImage.config(file = "textures\\SoundSpot_L.png")
        LabelImage.config(file = "textures\\Label_L.png")
        LineImage.config(file = "textures\\Line_L.png")
        window.configure(fg_color="#DEE1E1")
        NowPlayingLabel.configure(fg_color="#FFFFFF",text_color="#000000")
        GUIFrame.configure(fg_color="#DEE1E1")
        PlaylistFrame.configure(fg_color="#CFD2D2")
        LineLabel.configure(fg_color="#DEE1E1")
        LabelLabel.configure(fg_color="#DEE1E1")
        HomeLabel.configure(fg_color="#DEE1E1")
        LogoLabel.configure(fg_color="#DEE1E1")
        VolumeIcon.configure(fg_color="#DEE1E1")
        Volume.configure(button_color="#000000")
    elif (BgMode == "light"):
        BgMode = "dark"
        BG.config(file = "textures\\bg.png")
        ArrowSkip.config(file = "textures\\Next.png")
        ArrowBack.config(file = "textures\\Previous.png")
        PlayButtonImage.config(file = "textures\\Play.png")
        HomeImage.config(file = "textures\\HOME.png")
        VolumeImage.config(file = "textures\\Volume.png")
        LogoImage.config(file = "textures\\SoundSpot.png")
        LabelImage.config(file = "textures\\Label.png")
        LineImage.config(file = "textures\\Line.png")
        window.configure(fg_color="#211E1E")
        NowPlayingLabel.configure(fg_color="#302D2D",text_color="#FFFFFF")
        GUIFrame.configure(fg_color="#211E1E")
        PlaylistFrame.configure(fg_color="#302D2D")
        LineLabel.configure(fg_color="#211E1E")
        LabelLabel.configure(fg_color="#211E1E")
        HomeLabel.configure(fg_color="#211E1E")
        LogoLabel.configure(fg_color="#211E1E")
        VolumeIcon.configure(fg_color="#211E1E")
        Volume.configure(button_color = "#D9D9D9")
        

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
BgMode = "dark"

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

NowPlaying = "a"  # Name of the playing file used for functions
NowPlaying2 = StringVar()  # Name of the playing file shown in the app

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

for p in range(0,nr_ofFiles+1): # Generating music buttons
    btn = ctk.CTkButton(PlaylistFrame,
    	image = ListImage[random.randint(0,len(ListImage)-1)],
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

BtnBgMode = ctk.CTkButton(window,
    text= "Change Theme",
    height = 60,
    width = 30,
    command = ThemeChange
    )

# Creating starting values
filenr = 0 # Number of the playing file in folder
songstate = 0  #State of the song, 0 = playing, 1 = skip, -1 = go back
NowPlaying = files[filenr] # What music is currently playing
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
BtnBgMode.place(x = 10,y = 650)

window.mainloop()