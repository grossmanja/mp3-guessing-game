import vlc
import time
import os
import random
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()
path = filedialog.askdirectory()
# path = r"C:\Users\jyg16102\Documents\CSE stff\Projects\MP3 Guessing Game\music-test\\"
path += "/"
print(path)
#raise Exception
songList = os.listdir(path)
#print(songList)

# for i in range(len(songList)):
#     print(i, songList[i])

playedSongs = []
rand = random.randint(0, len(songList) - 1)
# p = vlc.MediaPlayer()

for i in range(5):
    while rand in playedSongs:
        rand = random.randint(0, len(songList) - 1)
    p = vlc.MediaPlayer(path + songList[rand])
    playedSongs.append(rand)
    p.play()
    time.sleep(6)
    p.stop()

# print(playedSongs)

for i in playedSongs:
    print(songList[i])
# p.play()
# time.sleep(10)
# p.stop()