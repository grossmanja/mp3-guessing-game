# from PyQt5.QtWidgets import QApplication, QLabel, QProgressBar, QPushButton, QWidget, QGridLayout, QMainWindow, QStatusBar
import typing
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QWidget
import qdarkstyle
import sys
import time
import math

global isDebugModeOn
isDebugModeOn = True

# @class Class that runs thread to move the progress bar.
class ThreadIncreaseProgress(QThread):
    finished = pyqtSignal()
    progress = pyqtSignal(int)
    currentLimit = 0
    debugMode = False

    def __init__(self, currentLimit, debugMode):
        super().__init__()
        self.currentLimit = currentLimit
        self.debugMode = debugMode
        self.running = False

    def run(self):
        if not self.running:
            self.startProgress()
        else:
            self.stopProgress()

    def startProgress(self):
        if self.debugMode:
            print("Current limit:", self.currentLimit)
            start = time.time()
        i = 0
        self.running = True

        while self.running and i < self.currentLimit + 1:
            # slowing down the loop
            time.sleep(0.0485)

            # setting value to progress bar
            self.progress.emit(i)

            i += 1

        if self.debugMode:
            end = time.time()
            print("Total Time:", end - start)

        self.finished.emit()

    def stopProgress(self):
        if self.debugMode:
            print("Thread Stop Progress")
        self.running = False
        self.wait()

    def updateCurrentLimit(self, currentLimit):
        if self.debugMode: print("Thread currentLimit updated, old value is", self.currentLimit, "New value is", currentLimit)
        self.currentLimit = currentLimit

# @class The main widget that contains the buttons and progress bar
class MainWidget(QWidget):
  
    def __init__(self):
        super().__init__()

        # calling initUI method
        self.initVariables()
        self.initUI()

    # @method: initializes the class variables
    def initVariables(self):
        #set time limits, each limit is multiplied by 0.05, so a limit of 20 = 1 second
        self.limits = [20,40,80,140,220,320]

        #set starting index in self.limits
        self.currentGuessIndex = 0

        #set the current limit
        self.currentLimit = self.limits[self.currentGuessIndex]

        self.ProgressBarRunning = 0

        self.currentSong = "Debug"

        self.currentGuess = 0

        # > Sets the program to debug mode to print things out to the console
        self.debugMode = isDebugModeOn


    # @method: Runs all of the initialization functions
    def initUI(self):

        self.createProgressBar()
        self.createPlayButton()
        self.createSkipButton()
        self.createInputTextbox()
        self.createQCompleter(self.inputTextbox)
        self.createSearchEnterButton()
        self.createGuessTable()
        self.createGuessCounter()
        self.createCurrentSongTime()

        self.createLayout()




    #*************************************
    #*  Start of initialization functions
    #*************************************

    # @method: Creates the Progress bar (shows how much of the song has been played)
    def createProgressBar(self):
         # creating progress bar
        self.ProgressBar = QProgressBar(self)

        #set progress bar's max steps
        self.ProgressBar.setMaximum(self.limits[-1])

        #Update the Progress Bar visual each time the Progress Bar step is increased 
        self.ProgressBar.valueChanged.connect(self.ProgressBar.repaint)

        #Hide the percent number on the progress bar
        self.ProgressBar.setTextVisible(False)

        if self.debugMode: print(self.ProgressBar.maximum())

        self.ProgressBar.setStyleSheet( "QProgressBar"
                          "{"
                          "background-color: steelblue;"
                          "}"
                                       "QProgressBar::chunk "
                          "{"
                          "background-color: green;"
                          "}")


    # @method: Creates the skip button, which skips guess and increases the song limit
    def createSkipButton(self):
        self.skipButton = QPushButton("Skip", self)
        self.skipButton.clicked.connect(self.skipButtonPressed)

        self.skipButton.setMaximumSize(QSize(150,50))
        self.skipButton.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.skipButton.setFont(QFont("Roboto", 16))
        self.skipButton.setStyleSheet("border-radius:10px")


    # @method: Creates the play button, which starts and stops the song depending if the song is playing or not
    def createPlayButton(self):
        self.PlayButton = QPushButton(self)
        self.PlayButton.clicked.connect(self.playButtonPressed)

        self.PlayButton.setIcon(QIcon("PlayButton.png"))
        self.PlayButton.setIconSize(QSize(100,100))
        self.PlayButton.setMaximumSize(QSize(120,120))

        self.PlayButton.setStyleSheet("background-color:transparent")
        self.PlayButton.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)


    # @method: Creates the input textbox, where the player guesses what the current song is
    def createInputTextbox(self):
        self.inputTextbox = QLineEdit(self)
        self.inputTextbox.setPlaceholderText("Enter Guess Here")
        self.inputTextbox.setStyleSheet("background-color:LightBlue; color:black; border-radius:10px")

        self.inputTextbox.setMaximumHeight(100)
        self.inputTextbox.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

        self.inputTextbox.setFont(QFont("Roboto", 16))


    # @method: Creates the button to enter their guess
    def createSearchEnterButton(self):
        self.searchEnterButton = QPushButton("Guess", self)
        self.searchEnterButton.clicked.connect(self.checkGuess)

        self.searchEnterButton.setMaximumSize(QSize(150,50))
        self.searchEnterButton.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)

        self.searchEnterButton.setFont(QFont("Roboto", 16))
        self.searchEnterButton.setStyleSheet("border-radius:10px")

   # @method: Creates a debug list for qCompleter
    def createDebugList(self):
        self.debugList = ["ABC", "Test", "The Boxer", "Debug"]


    # @method: Creates a the QCompleter that auto-completes the text in the search box
    def createQCompleter(self, lineEdit):
        self.createDebugList()
        self.completer = QCompleter(self.debugList, lineEdit)
        self.completer.setCaseSensitivity(0)
        lineEdit.setCompleter(self.completer)
   

    #@method: This version of createGuessTable will use QTableWidget instead of QTableView
    def createGuessTable(self):
        self.guessTable = QTableWidget(6, 1)

        for i in range(6):
            self.guessTable.showRow(i)
        
        self.guessTable.verticalHeader().hide()
        self.guessTable.horizontalHeader().hide()

        self.guessTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.guessTable.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.guessTable.setShowGrid(False)

        self.guessTable.setStyleSheet("""
            QTableView::item
                border: 2px;
                border-radius: 7px;
                font-size:18;                       
        """)

        self.guessTable.setFont(QFont("Roboto", 18))


        for i in range(6):
            tempString = str(i+1)
            tempString += ")"
            self.guessTable.setItem(i, 0, QTableWidgetItem(tempString))
    
    def createGuessCounter(self):
        self.guessCounter = QLabel("1/6")
        self.guessCounter.setFont(QFont("Roboto", 14))
        self.guessCounter.setAlignment(Qt.AlignBottom)
    
    def createCurrentSongTime(self):
        self.currentSongTime = QLabel("00:00/00:01")
        self.currentSongTime.setFont(QFont("Roboto", 14))
        self.currentSongTime.setAlignment(Qt.AlignBottom)


    # @method: Creates the Grid Layout that the buttons go in
    def createLayout(self):
        self.layout = QGridLayout()
        self.layout.addWidget(self.ProgressBar, 5, 0, 1, 5)
        self.layout.addWidget(self.PlayButton, 4, 2)
        self.layout.addWidget(self.skipButton, 6, 0)
        self.layout.addWidget(self.inputTextbox, 6, 1, 1, 3)
        self.layout.addWidget(self.searchEnterButton, 6, 4)
        self.layout.addWidget(self.currentSongTime, 4, 4)
        self.layout.addWidget(self.guessCounter, 4, 0)
        self.layout.addWidget(self.guessTable, 1, 1, 3, 3)

        for i in range(self.layout.rowCount()):
            self.layout.setRowStretch(i, 1)
        
        # for i in range(self.layout.columnCount()):
        self.layout.setColumnStretch(0, 0)
        self.layout.setColumnMinimumWidth(0, 100)

        self.layout.setColumnStretch(4, 0)
        self.layout.setColumnMinimumWidth(4, 100)

        self.layout.setRowStretch(0, 0)
        self.layout.setRowMinimumHeight(0, 10)
        
        if self.debugMode: print("row:", self.layout.rowCount(),"column", self.layout.columnCount())

        self.setLayout(self.layout)


             




        



#*************************************
#*  Start of functionality functions
#*************************************




    # @method: Either runs the startProgress or stopProgress when the play button is pressed
    def playButtonPressed(self):
        # > Check if the progress bar is running
        # > If it is running, then stop the progress bar (and eventually stop the song)
        # > If it isn't running, then start the progress bar (and eventually start the song)
        if self.debugMode:
            print("ProgressBarRunning", self.ProgressBarRunning)
        if self.ProgressBarRunning == 0: 
            self.startProgress()
        else:
            self.stopProgress()


    # @method: Plays the song from the beginning and starts the progress bar
    def startProgress(self):
        self.ProgressBarRunning = 1

        # > Change text on Play button to Stop
        # self.PlayButton.setText("Stop")
        self.PlayButton.setIcon(QIcon("StopButton.png"))

        # > initializes the ThreadIncreaseProgress function with the currentLimit and the debugMode
        self.thread = ThreadIncreaseProgress(currentLimit=self.currentLimit, debugMode=self.debugMode)
        self.thread.progress.connect(self.setProgressValue)
        self.thread.finished.connect(self.stopProgress)
        self.thread.start()


    # @method: Stops the song, stops the progress bar, and sets the progress bar back to 0 
    def stopProgress(self):
        self.ProgressBarRunning = 0
        self.thread.stopProgress()
        # self.PlayButton.setText("Play")
        self.PlayButton.setIcon(QIcon("PlayButton.png"))
        self.setProgressValue(0)


    # @method: Sets the progress bar value to the parameter value
    def setProgressValue(self, value):
        self.ProgressBar.setValue(value)
        if value % 20 == 0:
            self.updateCurrentSongTime(value)
        

    # @method: Increases the time limit of the song, based on the values in self.currentGuessIndex
    def increaseLimit(self):
        # > if we're at the end of the list, then just return to prevent out of index
        # TODO: Make it a failure to skip when at max limit
        if self.currentGuessIndex == len(self.limits) - 1: 
            return False

        self.currentGuessIndex += 1
        self.currentLimit = self.limits[self.currentGuessIndex]
        self.updateGuessCounter()


        if self.thread in locals():
            self.thread.updateCurrentLimit(self.currentLimit)

        return True
    
    def skipButtonPressed(self):
        # TODO: Make it a fail when you skip at the last guess
        if self.currentGuessIndex >= len(self.limits) - 1:
            return
        else:
            self.updateGuessTable()
            self.increaseLimit()
            self.updateCurrentSongTime()


    # @method: Adds guess to the guess table, index based on self.currentGuessIndex
    def updateGuessTable(self, guess="Skipped"):
        tempString = str(self.currentGuessIndex + 1) + ") " + guess
        # tempString = "X) " + guess
        # tempString = str(self.currentGuessIndex + 1) + ") X - " + guess
        tempTableItem = QTableWidgetItem(tempString)

        if guess == "Skipped":
            tempTableItem.setForeground(QColor(125, 125, 125))
        else:
            tempTableItem.setForeground(QColor(255, 0, 0))

        self.guessTable.setItem(self.currentGuessIndex, 0, tempTableItem)

        self.guessTable.repaint()


    # @method: Takes the text from the textbox, check if it is a valid song, and then checks if it matches the mystery song
    def checkGuess(self):
        guess = self.inputTextbox.text()
        if self.debugMode: print("Guess is:", guess)
        if not guess:
            if self.debugMode: print("Empty guess")
            return
        #TODO: check if guess is a valid song, if it isn't, don't take away a guess
        if guess == self.currentSong:
            if self.debugMode: print("WINNER")
        else:
            if self.debugMode: print("FAILURE")
            self.updateGuessTable(guess)
            self.increaseLimit()
    
    def updateGuessCounter(self):
        tempString = str(self.currentGuessIndex + 1) + "/6"
        self.guessCounter.setText(tempString)
        self.guessCounter.repaint()
    
    def updateCurrentSongTime(self, currentTime=0):
        if self.debugMode: print(currentTime, currentTime/20)
        
        currentMinute = str(int(math.floor((currentTime/20)/60)))
        currentSecond = str(int((currentTime/20) % 60))
        limitMinute = str(int(math.floor((self.currentLimit/20)/60)))
        limitSecond = str(int((self.currentLimit/20) % 60))
        formattedCurrentTime = ""
        
        # > If the current minute is less than 10 minutes, add a leading 0
        if float(currentMinute) < 10:
            formattedCurrentTime =  "0" + currentMinute
        else:
            formattedCurrentTime = currentMinute
        
        formattedCurrentTime += ":"

        # > If the current minute is less than 10 seconds, add a leading 0
        if float(currentSecond) < 10:
            formattedCurrentTime += "0" + currentSecond
        else:
            formattedCurrentTime += currentSecond


        formattedCurrentTime += "/"

        # > If the limit minute is less than 10 minutes, add a leading 0
        if float(limitMinute) < 10:
            formattedCurrentTime += "0" + limitMinute
        else:
            formattedCurrentTime = limitMinute
        
        formattedCurrentTime += ":"

        # > If the limit second is less than 10 seconds, add a leading 0 
        if float(limitSecond) < 10:
            formattedCurrentTime += "0" + limitSecond
        else:
            formattedCurrentTime += limitSecond
        
        self.currentSongTime.setText(formattedCurrentTime)




    



# @class: The Victory/Defeat Screen Widget that appears after you either guess correctly, or after 6 incorrect guesses
class EndScreenWidget(QWidget):
    def __init__(self, isWinner, currentSong):
        super().__init__()

        self.initVariables(isWinner, currentSong)


    def initVariables(self, isWin, currentSong):
        self.isWin = isWin
        self.resultMessage = QLabel()
        self.currentSong = QLabel()


    def initUI(self):
        self.createSongBox()
        self.createAlbumPicture()
        self.createPlayBUtton()
        
    
    def createSongBox(self):
        self.songBox = QLabel()
    
    def createAlbumPicture(self):
        self.albumPicture = QPixmap()

    def createVictoryMessage(self):
        self.resultMessage.setText("You Win!")

    def createFailMessage(self):
        self.resultMessage.setText("You Lose!")
    
    def createPlayBUtton(self):
        self.PlayButton = QPushButton(self)
        self.PlayButton.clicked.connect(self.playButtonPressed)

        self.PlayButton.setIcon(QIcon("PlayButton.png"))
        self.PlayButton.setIconSize(QSize(100,100))
        self.PlayButton.setMaximumSize(QSize(120,120))

        self.PlayButton.setStyleSheet("background-color:transparent")
        self.PlayButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

    def createLayout(self):
        self.layout = QGridLayout()
        self.layout.addWidget()


#*************************************
#*  Start of functionality functions
#*************************************


def playButtonPressed(self):
        # > Check if the progress bar is running
        # > If it is running, then stop the progress bar (and eventually stop the song)
        # > If it isn't running, then start the progress bar (and eventually start the song)
        if self.debugMode:
            print("ProgressBarRunning", self.ProgressBarRunning)
        if self.ProgressBarRunning == 0: 
            self.startProgress()
        else:
            self.stopProgress()

# @class: Class that makes the actual window that the user will see
class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setCentralWidget(MainWidget())


        # self.menu = self.menuBar()
        # self.fileMenu = self.menu.addMenu('&File')

        self.status = QStatusBar()
        self.status.showMessage("GUI Test V0.8")
        self.setStatusBar(self.status)

        # setting window geometry
        # self.setGeometry(300, 300, 800, 600)
        self.setFixedSize(1200, 900)

        # setting window action
        self.setWindowTitle("PyQT GUI Test")



        # showing all the widgets
        self.show()


    def changeEndScreen(self, widget):
        self.setCentralWidget(widget)


#******************
#*   main method
#******************
if __name__ == '__main__':
      
    # create pyqt5 app
    app = QApplication(sys.argv)

    darkStyle = qdarkstyle.load_stylesheet_pyqt5()

    app.setStyleSheet(darkStyle)

    print("Debug mode is", isDebugModeOn)
  
    # create the instance of our Window
    window = Window()
  
    # start the app
    sys.exit(app.exec())