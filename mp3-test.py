import time
import os
import random

import vlc
import eyed3
import tkinter as tk
from tkinter import filedialog

print()

root = tk.Tk()
root.withdraw()
path = filedialog.askdirectory()                                                                    ### Getting the folder path of the MP3 files
# path = r"D:/Github/Repositories/mp3-guessing-game/music-test"
path += "/"                                                                                         ### Adding a slash at the end of the path to indicate that this is a folder path
# print(path)
songList = os.listdir(path)                                                                         ### Accessing the list of songs in the directed folder
#print(songList)

# for i in range(len(songList)):
#     print(i, songList[i])

playedSongs = []
rand = random.randint(0, len(songList) - 1)
# p = vlc.MediaPlayer()

for i in range(5):
    while rand in playedSongs:
        rand = random.randint(0, len(songList) - 1)
    playedSongs.append(rand)
    songPath = path + songList[rand]
    
    songTag = eyed3.load(songPath)
    print(songTag.tag.title)

    # print()

    p = vlc.MediaPlayer(songPath)
    p.play()
    time.sleep(6)
    p.stop()

# print(playedSongs)

# for i in playedSongs:
#     print(songList[i])
# p.play()
# time.sleep(10)
# p.stop()