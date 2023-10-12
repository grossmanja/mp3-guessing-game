# from PyQt5.QtWidgets import QApplication, QLabel, QProgressBar, QPushButton, QWidget, QGridLayout, QMainWindow, QStatusBar
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import qdarkstyle
import sys
import time

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
    #TODO: add Stop

    def startProgress(self):
        if self.debugMode:
            print("Current limit:", self.currentLimit)
            start = time.time()
        i = 0
        self.running = True
        #TODO: add threadActive
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
        #set time limits
        self.limits = [20,40,80,140,220,320]

        #set starting index in self.limits
        self.limitsIndex = 0

        #set the current limit
        self.currentLimit = self.limits[self.limitsIndex]

        self.ProgressBarRunning = 0

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

        self.createLayout()


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
                          "background-color: white;"
                          "}")


    def createSkipButton(self):
        self.SkipButton = QPushButton("Skip", self)
        self.SkipButton.clicked.connect(self.increaseLimit)

        self.SkipButton.setMaximumSize(QSize(100,50))
        self.SkipButton.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)

    def createPlayButton(self):
        self.PlayButton = QPushButton(self)
        self.PlayButton.clicked.connect(self.playButtonPressed)

        self.PlayButton.setIcon(QIcon("PlayButton.png"))
        self.PlayButton.setIconSize(QSize(100,100))
        self.PlayButton.setMaximumSize(QSize(120,120))

        self.PlayButton.setStyleSheet("background-color:transparent")
        self.PlayButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

    def createInputTextbox(self):
        self.inputTextbox = QLineEdit(self)
        self.inputTextbox.setPlaceholderText("Enter Guess Here")
        self.inputTextbox.setStyleSheet("background-color:LightBlue; color:black")

    def createSearchEnterButton(self):
        self.searchEnterButton = QPushButton("Guess", self)


    def createLayout(self):
        self.layout  = QGridLayout()
        self.layout.addWidget(self.ProgressBar, 5, 0, 1, 5)
        self.layout.addWidget(self.PlayButton, 4, 2)
        self.layout.addWidget(self.SkipButton, 4, 4)
        self.layout.addWidget(self.inputTextbox, 7, 0, 1, 4)
        self.layout.addWidget(self.searchEnterButton, 7, 4)

        for i in range(self.layout.rowCount()):
            self.layout.setRowStretch(i, 1)
        
        if self.debugMode: print("row:", self.layout.rowCount(),"column", self.layout.columnCount())

        self.setLayout(self.layout)


    # @method: this method is to make a debug list for qCompleter
    def createDebugList(self):
        self.debugList = ["ABC", "Test", "The Boxer"]

    def createQCompleter(self, lineEdit):
        self.createDebugList()
        self.completer = QCompleter(self.debugList, lineEdit)
        self.completer.setCaseSensitivity(0)
        lineEdit.setCompleter(self.completer)





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


    def stopProgress(self):
        self.ProgressBarRunning = 0
        self.thread.stopProgress()
        # self.PlayButton.setText("Play")
        self.PlayButton.setIcon(QIcon("PlayButton.png"))
        self.setProgressValue(0)


    def setProgressValue(self, value):
        self.ProgressBar.setValue(value)
        

    def increaseLimit(self):
        # > if we're at the end of the list, then just return to prevent out of index
        # TODO: Make it a failure to skip when at max limit
        if self.limitsIndex == len(self.limits) - 1: return

        self.limitsIndex += 1
        self.currentLimit = self.limits[self.limitsIndex]

        self.thread.updateCurrentLimit(self.currentLimit)



class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setCentralWidget(MainWidget())


        self.menu = self.menuBar()
        self.fileMenu = self.menu.addMenu('&File')

        self.status = QStatusBar()
        self.status.showMessage("GUI Test V0.1")
        self.setStatusBar(self.status)

        # setting window geometry
        # self.setGeometry(300, 300, 800, 600)
        self.setFixedSize(800, 600)

        # setting window action
        self.setWindowTitle("PyQT GUI Test")



        # showing all the widgets
        self.show()

# main method
if __name__ == '__main__':
      
    # create pyqt5 app
    app = QApplication(sys.argv)

    darkStyle = qdarkstyle.load_stylesheet_pyqt5()

    app.setStyleSheet(darkStyle)

    # app.setStyleSheet("QPushButton {border-style: outset; border-width: 0px;}")
  
    # create the instance of our Window
    window = Window()
  
    # start the app
    sys.exit(app.exec())