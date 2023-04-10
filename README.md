# Introduction
This is a homebrew offline version of my Spotify Guessing Game.  I've had this idea for a while and wanted to integrate with my own Spotify playlists, but idk how to do that.  So, I'm starting with local MP3 files to figure out how the game actually works before figuring out the Spotify API and stuff.

# How To Play
First, you select which

# Game Modes
There are 3 game modes available 
* Heardle
* Score
* Survival

## Heardle
The player is given a single song, and is initially able to only listen to the first second of the song.  The player can guess the song or skip.  If the player guesses incorrectly or skips, they are able to listen to an additional second of the song.  The player has 6 attempts to correctly identify the song, each guess giving more and more additional time, with the final guess giving the player the first 16 seconds of the song.  Scoring is based on how many guesses it take for the player to identify the song.  

## Score
The player is given 10 songs, and is given the first 30 seconds of a song.  The player will guess the song and be given a number of points depending on how many seconds into the song they correctly guess the song.  Players will be given bonus points if they correctly guess on their first try.

## Survival
The player is given __ lives, and are given the first 30 seconds of a song.  The player will guess the song, and if they incorrectly guess a song, they will lose a life and be moved onto the next song. If a player loses all their lives, the game ends and their score is the number of correctly identified songs.  If the player correctly identifies __ songs in a row, they will earn 1 life back.

# Difficulties
The game modes each have their own difficulty settings, which 

## Heardle difficulties
* Normal: This is how the Heardle is set up.
    * 6 guesses
    * Each guess adds an increasing amount of time, up to 16 seconds total on last guess
    * Search allows for both song title and artist

* Easy: An easier version of the Heardle
    * 10 guesses
    * Each guess adds an increasing amount of time, up to 60 seconds on last guess
    * Hint system allows for player to get the first letter of the artist or song title
    * Search allows for both song title and artist

* Hard:
    * 5 guesses
    * Each guess adds an additional 1 second, up to 5 seconds on last guess
    * Search only allows for song title

## Score & Survival difficulties
The Score & Survival game modes are split into two modes:
* Multiple Choice
    * The player is presented with 4 possible song choices, and the player will choose the correct answer from the 4
* Write-in
    * The player must write in the correct answer, with help from a search bar.  The search bar will let the player search by song title or artist.
### Multiple Choice
* Easy
    * The player is presented with 4 choices.  As the song plays, two options will fade out, one at 10 seconds and one at 20 seconds.
* Normal
    * The player is presented with 4 choices.  As the song plays, one option will fade out at 15 seconds.
* Hard
    * The player is presented with 5 choices.  No options will fade out.
### Write-in
* Easy
    * The player starts with 6 lives.  Every 3 consecutive correct guesses 
* Normal
* Hard

## Bonus Modifiers:
These modifiers can be added to any game mode:
* Double Time
