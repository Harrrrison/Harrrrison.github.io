"""
CC attributions:
u/Thunder246 - for the space-ship sprite here:
https://www.reddit.com/r/PixelArt/comments/jy89x7/new_spaceship_that_i_made_i_am_still_quite_new_to/
u/v78 - for the space background here:
https://www.reddit.com/r/space/comments/ccz82i/i_find_drawing_stars_in_the_16_colors_ega_palette/?utm_source=ifttt
u/tiskolin - for the planet sprite here:
https://www.reddit.com/r/pics/comments/a84yo5/oc_pixel_art_planet/

To enter a cheat:
You must go into the chnage keybinds menu and enter the word "Speed" into the entry box and then press save
this will give you a speed boost

This game is a newer version of galaxian, the objective is the prevent the asteroids from hitting the planet
You play as a spaceship, and you must shoot the asteroids to destroy them
The game is over when the planet is destroyed
or when you are destroyed -- you have a shield bar at the top of the screen

"""

import random
import tkinter
from tkinter import *
from tkinter import simpledialog, messagebox, ttk
from tkinter.ttk import Progressbar
import math

from PIL import ImageTk, Image, ImageSequence

class objective():
    """This class is used to create the objective for the game
    its coords should be checked agaisnt the enemy coords --using the get methods inside
     to see if a collision has occured
    Logic can be based off this"""

    def __init__(self, gameWindow, canvas):
        self.tkinter = tkinter

        self.gameWindow = gameWindow
        self.canvas = canvas

        self.x = self.canvas.winfo_screenwidth()
        self.y = 1.9 * self.canvas.winfo_screenheight()

        self.body = self.canvas.create_rectangle((self.x - 100) / 2, (self.y - 80) / 2,
                                                 (self.x + 100) / 2, (self.y + 80) / 2, fill="black", outline="white",
                                                 width=2, dash=(4, 4), stipple="gray50")

    def updateImage(self):
        """When called Places the planet sprite over the coordinates of the objective"""
        self.img = Image.open("planetSprite.png")
        canvasCoords = self.canvas.coords(self.body)

        self.resizedImage = self.img.resize((150, 150))
        self.image = ImageTk.PhotoImage(self.resizedImage)

        self.chords = ((canvasCoords[0] + canvasCoords[2]) / 2, (canvasCoords[1] + canvasCoords[3]) / 2)

        self.planetImage = self.canvas.create_image(self.chords[0], self.chords[1], image=self.image)
        self.canvas.tag_raise(self.planetImage)
        self.canvas.focus_set()

    def getBbox(self):
        """Returns the bounding box of the objective"""
        return self.canvas.bbox(self.body)

    def getMothershipX(self):
        """Returns the x coordinate of the objective"""
        return self.getBbox()[2] - self.getBbox()[0]

    def getMothershipY(self):
        """Returns the y coordinate of the objective"""
        return self.getBbox()[3] - self.getBbox()[1]

class leaderboard():
    """This class is used to create the leaderboard for the game"""

    def __init__(self):

        self.file = self.readLeaderboardData()  # r+ means read and write
        self.scoreList = [{"name": "test", "score": 0}]
        self.leaderboardFlag = True
        self.written = False

    def outputLeaderboard(self, frame):
        """This method is used to output the leaderboard to the screen in a text box, this makes it scorllable,
        the board comes from the readLeaderboardData method and file is Leaderboard.txt"""
        self.output = Text(frame, width=50, height=50)
        self.output.pack()
        self.file = self.readLeaderboardData()
        if self.leaderboardFlag:
            for entry in self.file:
                self.output.insert(END, f"{entry['name']}: {entry['score']}\n")

        else:
            self.output.insert(END, self.file)

    def readLeaderboardData(self):
        """This method is used to read the leaderboard data from the file Leaderboard.txt"""
        self.leaderBoard = []
        try:
            with open("Leaderboard.txt", 'r') as file:
                self.leaderboardFlag = True
                for line in file:
                    name, score = line.strip().split()
                    self.leaderBoard.append({'name': name, 'score': int(score)})
        except FileNotFoundError:
            self.leaderboardFlag = False
            return "No leaderboard data found."
        return self.leaderBoard

    def writeLeaderboardData(self, name, score):
        """This method is used to write the leaderboard data to the file Leaderboard.txt"""
        with open("Leaderboard.txt", 'w') as file:
            self.insertScoreToDict({'name': name, 'score': score})
            for player in self.leaderBoard:
                file.write(f"{player['name']} {player['score']}\n")
            self.written = True

    def insertScoreToDict(self, newEntry):
        """This method is used to insert the score into the dictionary using the .sort method to sort the scores in"""
        self.leaderBoard.append(newEntry)
        self.leaderBoard.sort(key=lambda x: x['score'], reverse=True)

class bullet():
    """This class is used to create the bullets for the charicter to shoot"""
    def __init__(self, gameWindow, canvas, charicterX, charicterY, angle):

        self.gameWindow = gameWindow
        self.canvas = canvas

        self.x = charicterX
        self.y = charicterY
        self.angle = math.radians(angle - 180)

        self.bulletObject = self.canvas.create_rectangle(self.x - 2, self.y - 2, self.x + 2, self.y + 2, fill="red")

        #self.canvas.lift(self.bulletObject)

        self.canvas.focus_set()

        self.hit = False

    def moveBullet(self):
        """This method is used to move the bullet across the screen, it uses the angle of the
        charicter to determine the trajectory"""
        if self.bulletObject:
            self.canvas.delete(self.bulletObject)

        if self.y < 0 or self.y > self.canvas.winfo_height() or self.x < 0 or self.x > self.canvas.winfo_width():
            self.canvas.delete(self.bulletObject)
            self.bulletObject = None
        else:
            dx = math.sin(self.angle)
            dy = math.cos(self.angle)

            self.x += dx * 10  # the int val is the speed of the bullet
            self.y += dy * 10

            self.bulletObject = self.canvas.create_rectangle(self.x - 2, self.y - 2, self.x + 2, self.y + 2, fill="red")

        #self.gameWindow.after(30, self.moveBullet)

    def getBbox(self):
        """This method is used to get the bounding box of the bullet"""
        return self.canvas.bbox(self.bulletObject)

    def destroy(self):
        """This method is used to destroy the bullet should be called when it hits the objective"""
        self.canvas.delete(self.bulletObject)


class playerChar(bullet):
    """This class is used to create the charicter for the game"""
    def __init__(self, canvas, gameWindow):

        self.tkinter = tkinter

        self.canvas = canvas
        self.gameWindow = gameWindow

        self.x = self.canvas.winfo_screenwidth()
        self.y = 1.5*self.canvas.winfo_screenheight()

        self.character = self.canvas.create_rectangle((self.x - 20)/2, (self.y - 20)/2,
                                                      (self.x + 20)/2, (self.y + 20)/2, fill="red")
        self.playerChords = (200, 200)
        canvasCoords = self.canvas.coords(self.character)
        self.playerChords = ((canvasCoords[0] + canvasCoords[2]) / 2, (canvasCoords[1] + canvasCoords[3]) / 2)

        #self.image = self.tkinter.PhotoImage(file="player.png")
        self.img = Image.open("player.png")

        self.resizedImage = self.img.resize((100, 100))
        self.image = ImageTk.PhotoImage(self.resizedImage)

        self.movementSpeed = 20

        self.characterImage = self.canvas.create_image(self.playerChords[0], self.playerChords[1], image=self.image)

        self.angle = 0

        self.updatePlayerCoords()

        self.bullets = [] # This is a list of all the bullets that the player has fired

        self.canvas.tag_raise(self.characterImage)

        self.canvas.focus_set()

    def getCharicter(self):
        """This method is used to get the charicter object"""
        return self.character

    def getBbox(self):
        """This method is used to get the bounding box of the charicter"""
        return self.canvas.bbox(self.character)

    def movePlayerLeft(self):
        """This method is used to move the charicter and image left by the movement speed"""
        self.canvas.move(self.character, -self.movementSpeed, 0)
        self.canvas.move(self.characterImage, -self.movementSpeed, 0)

    def movePlayerRight(self):
        """This method is used to move the charicter and image right by the movement speed"""
        self.canvas.move(self.character, self.movementSpeed, 0)
        self.canvas.move(self.characterImage, self.movementSpeed, 0)

    def movePlayerUp(self):
        """This method is used to move the charicter and image up by the movement speed"""
        self.canvas.move(self.character, 0, -self.movementSpeed)
        self.canvas.move(self.characterImage, 0, -self.movementSpeed)

    def movePlayerDown(self):
        """This method is used to move the charicter and image down by the movement speed"""
        self.canvas.move(self.character, 0, self.movementSpeed)
        self.canvas.move(self.characterImage, 0, self.movementSpeed)

    def rotateRight(self):
        """PIL is used rotate the image and thus the ship at the same time storing the angle"""
        self.angle -= 30
        rotatedImage = self.resizedImage.rotate(self.angle)
        self.image = ImageTk.PhotoImage(rotatedImage)
        self.canvas.itemconfig(self.characterImage, image=self.image)

    def rotateLeft(self):
        """PIL is used rotate the image and thus the ship at the same time storing the angle"""
        self.angle += 30
        rotatedImage = self.resizedImage.rotate(self.angle)
        self.image = ImageTk.PhotoImage(rotatedImage)
        self.canvas.itemconfig(self.characterImage, image=self.image)

    def updatePlayerCoords(self):
        """This method is used to update the players coords every 100ms"""
        canvasCoords = self.canvas.coords(self.character)
        self.playerChords = ((canvasCoords[0] + canvasCoords[2])/2, (canvasCoords[1] + canvasCoords[3])/2)
        self.gameWindow.after(100, self.updatePlayerCoords)

    def getPlayerCoords(self):
        """This method is used to get the players coords"""
        return self.playerChords

    def fireBullet(self):
        """A new instance of the bullet class is created and the moveBullet method is called"""
        self.bullet = bullet(self.gameWindow, self.canvas, self.playerChords[0], self.playerChords[1],
                                        self.angle)
        self.bullet.moveBullet()
        self.bullets.append(self.bullet) # This adds the bullet to the list of bullets that the player has fired

    def speedCheat(self):
        """This method is used to increase the players movement speed -- should be when the speed cheat is called"""
        self.movementSpeed = 100

class baseEnemy():
    """This class is used to create the base enemy for the game"""
    def __init__(self, canvas, gameWindow):
        self.canvas = canvas
        self.gameWindow = gameWindow

        self.x = 0
        self.y = 0

        self.enemyObject = None


class bossScreen():
    """When called this class will create the boss screen freezing the game state"""
    def __init__(self, gameWindow):
        self.gameWindow = gameWindow
        self.frame = Frame(self.gameWindow)
        #self.frame.__setattr__(-topmost, True)
        self.image = Image.open("fakeWorkImage2.jpeg")
        self.image = self.image.resize((self.gameWindow.winfo_width(), self.gameWindow.winfo_height()))
        self.workImage = ImageTk.PhotoImage(self.image)
        self.imageLable = Label(self.frame, image=self.workImage, bg="black", cursor="arrow", width=5000, height=5000)

    def placeFrame(self):
        """This method is used to place the frame which contains the image on the screen
        allowing it to be lifted above the canvas and block everything"""
        self.frame.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.frame.lift()
        self.frame.configure(bg="black")
        self.frame.configure(width=5000, height=5000)
        self.frame.configure(cursor="arrow")
        self.imageLable.pack()

    def forgetFrame(self):
        """Called when the frame is to be removed from the screen"""
        self.frame.place_forget()
        self.imageLable.pack_forget()


class enemyImp(baseEnemy):
    """This class is used to create the enemy"""
    def __init__(self, canvas, gameWindow):
        self.enemyBody = None
        self.tkinter = tkinter

        self.canvas = canvas
        self.gameWindow = gameWindow

        self.enemyBody = self.canvas.create_rectangle(190, 190, 210, 210, fill="grey")

        self.health = 100
        self.speed = random.randint(3, 7)

        self.canvas.focus_set()

    def destroy(self):
        """This method just .deletes the enemy body from the canvas"""
        self.canvas.delete(self.enemyBody)

    def getBbox(self):
        """This method is used to get the bounding box of the enemy"""
        return self.canvas.bbox(self.enemyBody)

    def moveEnemy(self, targetX, targetY):
        """When called the enemy will move towards the target coords at the speed defined above, a random number"""
        currentX, currentY, _, _ = self.canvas.coords(self.enemyBody)

        angle = math.atan2(targetY - currentY, targetX - currentX)
        new_x = currentX + (self.speed * math.cos(angle))
        new_y = currentY + (self.speed * math.sin(angle))
        self.canvas.coords(self.enemyBody, new_x, new_y, new_x + 20, new_y + 20)

class menuWindow(leaderboard):
    """When called this class will instanciate the menu window -- but will not show it"""
    def __init__(self, gameWindow, canvas, resumeCb, quitCb, changeScreenSizeCb, loadSaveCb, saveCb):
        self.perfomanceMode = False
        self.speedCheat = False
        self.refreshKeyBroadcast = False
        self.gameWindow = gameWindow
        self.leaderboard = leaderboard()
        self.frame = tkinter.Frame(gameWindow, width=300, height=300)
        self.canvas = canvas
        self.style = tkinter.ttk.Style()
        self.style.configure("TButton",
                             font=("Arial", 12, "bold"),
                             padding=5,
                             width=20,
                             foreground="white",
                             background="#3498db",  # Blue color
                             borderwidth=2,
                             relief="flat")
        self.label = tkinter.Label(self.frame, text="Paused", font=("Arial", 100))
        self.resumeButton = ttk.Button(self.frame, text="Resume", command=resumeCb, style="TButton")
        self.startGame = ttk.Button(self.frame, text="StartGame", command=resumeCb, style="TButton")
        self.quitButton = ttk.Button(self.frame, text="Quit", command=quitCb, style="TButton")
        self.leaderboardButton = ttk.Button(self.frame, text="Leaderboard", command=self.leaderboardDisplayLogic,
                                            style="TButton")
        self.saveButton = ttk.Button(self.frame, text="Save", command=saveCb, style="TButton")
        self.loadSaveButton = ttk.Button(self.frame, text="Load Save", command=loadSaveCb, style="TButton")
        self.changeSizeButton = ttk.Button(self.frame, text="   Toggle\nFullscreen", command=changeScreenSizeCb, style="TButton")
        self.controlsButton = ttk.Button(self.frame, text="Controls", command=self.showControls, style="TButton")
        self.controlsLabel = tkinter.Label(self.frame, text="WASD to move\nSpace to shoot\nEsc to pause\n", font=("Arial", 20))
        self.backButton = ttk.Button(self.frame, text="Back", command=self.hideControls, style="TButton")
        self.performanceButton = ttk.Button(self.frame, text="Performance\n      Mode", command=self.performanceMode,
                                            style="TButton")
        self.takeKeyInput = ttk.Button(self.frame, text="Change binds", command=self.showKeyWindow,
                                       style="TButton")  # this
        # is where the key input will be taken
        self.keyNames = ["up", "down", "left", "right", "Boss Key", "rotateRight", "rotateLeft"]
        self.keyEntries = {"up": "<w>", "down": "<s>", "left": "<a>", "right": "<d>", "shoot": "<space>",
                           "pause": "<Escape>", "Boss Key": "b", "rotateRight": "e", "rotateLeft": "q"}
        self.keyEntriesToSave = {"up": "<w>", "down": "<s>", "left": "<a>", "right": "<d>", "shoot": "<space>",
                                 "pause": "<Escape>", "Boss Key": "b", "rotateRight": "e", "rotateLeft": "q"}

        self.currentKey = "r"

    def show(self):
        """Called when the frame is to be shown, places the frame in the center of the screen
        and packs the selection of buttons"""
        self.frame.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.resumeButton.pack()
        self.leaderboardButton.pack()
        self.changeSizeButton.pack()
        self.controlsButton.pack()
        self.takeKeyInput.pack()
        self.saveButton.pack()
        self.quitButton.pack()
        self.previousWindow = "mainWindow"

    def hide(self):
        """Called when the frame is to be hidden, unpacks all the buttons currently in the frame
        and hides the frame"""
        for iWidget in self.frame.winfo_children():
            iWidget.pack_forget()
        self.frame.place_forget()
        print("hidden")

    def startGameWindow(self):
        """should be called when the game is started, shows information about the game and the leaderboard"""
        self.frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        self.startGame.pack()
        self.leaderboardButton.pack()
        self.loadSaveButton.pack()
        self.takeKeyInput.pack()
        self.controlsButton.pack()
        self.changeSizeButton.pack()
        self.performanceButton.pack()
        self.quitButton.pack()
        self.previousWindow = "startGameWindow"

    def showControls(self):
        """packs the controls label and the back button"""
        self.hide()
        self.frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        self.controlsLabel.pack()
        self.backButton.pack()

    def hideControls(self):
        """unpacks the controls label and the back button and returns to the previous window"""
        self.hide()
        if self.previousWindow == "startGameWindow":
            self.startGameWindow()
        else:
            self.show()

    def showKeyWindow(self):
        """shows the key window, where the user can change the key binds"""
        self.hide()
        self.frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        for keyName in self.keyNames:
            keyLabel = tkinter.Label(self.frame, text=f"{keyName}:", font=("Arial", 20))
            entryVar = tkinter.StringVar()
            entry = tkinter.Entry(self.frame, width=10, textvariable=entryVar)
            keyLabel.pack()
            entry.pack()
            self.keyEntriesToSave[keyName] = entryVar

        saveKeysButton = ttk.Button(self.frame, text="Save", command=self.saveKeys, style="TButton")
        saveKeysButton.pack()
        self.backButton.pack()

    def saveKeys(self):
        """saves the keys to the keyEntries dictionary and sets the refreshKeyBroadcast to True
        should be called when the user presses the save button in the key window changing the key binds"""
        for keyName in self.keyNames:
            if self.keyEntriesToSave[keyName].get() == "Speed":
                print("speed")
                self.speedCheat = True
            elif self.keyEntriesToSave[keyName].get() != '':
                self.keyEntries[keyName] = self.keyEntriesToSave[keyName].get()

        self.refreshKeyBroadcast = True
        print(self.keyEntries)

    def performanceMode(self):
        """toggles the performance mode on and off -- this removes images from the game to increase performance"""
        if self.perfomanceMode:
            self.perfomanceMode = False
            print("perfrom off")
            self.performanceButton.configure(text="Performance\n   mode: OFF")
        elif not self.perfomanceMode:
            self.perfomanceMode = True
            self.performanceButton.configure(text="Performance\n   mode: ON")

    def leaderboardDisplayLogic(self):
        """called when the leaderboard button is pressed, hides the current frame and shows the leaderboard"""
        self.hide()
        self.frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        # self.leaderboard.testCase()
        self.leaderboard.outputLeaderboard(self.frame)
        self.backButton.pack()

    def passThroughScore(self, score):
        """passes through the score to the class, so it can be saved"""
        self.score = score



class MainWindow(playerChar, enemyImp, menuWindow,
                 leaderboard, objective):
    """This class is the main window of the game, the other classes are passed though and isntantiated here"""

    def __init__(self):
        """Instantiates the main window"""
        self.name = None
        self.doneClicked = None
        self.gameWindow = Tk()
        self.style = tkinter.ttk.Style()
        self.gameWindow.title("Galaxian 2.0")

        self.gameState = "playing"
        self.gameWindow.bind("<0>", lambda e: self.exitGame())

        # canvas creation
        self.canvas = tkinter.Canvas(self.gameWindow, background="gray1", width=1080, height=720)
        self.canvas.pack(fill=BOTH, expand=True)
        self.canvas.configure(cursor="none")

        self.gameWindow.attributes("-fullscreen", True)
        # window resizing
        self.gameWindow.geometry("{0}x{1}+0+0".format(
           self.gameWindow.winfo_screenwidth(), self.gameWindow.winfo_screenheight()))
        self.gameWindow.resizable(False, False)
        self.fullScreenState = True
        self.pauseMenu = menuWindow(self.gameWindow, self.canvas, self.resumeGame, self.quitGame,
                                               self.changeWindowSize, self.loadGame, self.saveGame)
        self.startGame()

        # player controls
        self.player = playerChar(self.canvas, self.gameWindow)
        self.canvas.bind(self.pauseMenu.keyEntries["left"], lambda e: self.player.movePlayerLeft())
        self.canvas.bind(self.pauseMenu.keyEntries["right"], lambda e: self.player.movePlayerRight())
        self.canvas.bind(self.pauseMenu.keyEntries["up"], lambda e: self.player.movePlayerUp())
        self.canvas.bind(self.pauseMenu.keyEntries["down"], lambda e: self.player.movePlayerDown())
        self.canvas.bind(self.pauseMenu.keyEntries["shoot"], lambda e: self.player.fireBullet())
        self.canvas.bind(self.pauseMenu.keyEntries["rotateRight"], lambda e: self.player.rotateRight())
        self.canvas.bind(self.pauseMenu.keyEntries["rotateLeft"], lambda e: self.player.rotateLeft())

        # Background creation


        # pause menu
        self.canvas.bind("<Escape>", lambda e: self.pauseMenuLogic())
        self.leaderboard = leaderboard()

        # Boss Key
        self.bossKey = bossScreen(self.gameWindow)
        self.canvas.bind("<b>", lambda e: self.bossKeyLogic())

        # Difficulty
        self.difficulty = 0
        self.spawnEnemyDelay = 2500
        self.increaseDifficulty()

        # init objective
        self.motherShip = objective(self.gameWindow, self.canvas)

        # init enemy
        self.enemiesList = []
        self.spawnEnemy()
        print(self.player.getPlayerCoords())
        self.removeEnemies()

        # additonal Varibles
        self.score = 0
        self.scoreLabel = Label(self.gameWindow, text="Score: " + self.getScore(), font="Times 20 italic bold",
                                background="red").place(x=5, y=5)
        self.style.theme_use('clam')
        self.style.configure('style.Horizontal.TProgressbar', background="cadetblue1", troughcolor='blue', darkcolor='red',
                             lightcolor='red', bordercolor='red')
        self.healthBar = Progressbar(self.gameWindow, orient=HORIZONTAL,
                                     length=200, mode="determinate", style='style.Horizontal.TProgressbar')
        self.healthBar["value"] = 100
        self.healthBar.pack()
        self.healthBar.place(relx=0.5, rely=0.03, anchor=CENTER, width=500, height=20)
        self.motherShipHealth = 100

        self.gameStateDict = {
            "score": self.score,
            "health": self.healthBar["value"],
            "MotherShipHealth": self.motherShipHealth,
            "difficulty": self.difficulty,
            "spawnEnemyDelay": self.spawnEnemyDelay,
        }



        self.gameLoop()
        self.gameWindow.mainloop()

    # this will be made varible def resize(self, width, height):

    def startGame(self):
        """this will start the game and set the game state to playing"""
        self.canvas.configure(cursor="arrow")
        self.gameState = "notStarted"
        self.pauseMenu.startGameWindow()

    def updateHealthBar(self):
        """checks the value of the healthbar and if its above 0 it will remove 20 from the value if its below 0 it will
        close the window / end the game"""
        if self.healthBar["value"] > 0:
            self.healthBar["value"] -= 20
        else:
            self.gameWindow.destroy()

    def refreshKeyInput(self):
        """When the keybinds are chenged in the menu this can be called to update them in the game"""
        self.canvas.bind(self.pauseMenu.keyEntries["left"], lambda e: self.player.movePlayerLeft())
        self.canvas.bind(self.pauseMenu.keyEntries["right"], lambda e: self.player.movePlayerRight())
        self.canvas.bind(self.pauseMenu.keyEntries["up"], lambda e: self.player.movePlayerUp())
        self.canvas.bind(self.pauseMenu.keyEntries["down"], lambda e: self.player.movePlayerDown())
        self.canvas.bind("<space>", lambda e: self.player.fireBullet())
        self.canvas.bind(self.pauseMenu.keyEntries["rotateRight"], lambda e: self.player.rotateRight())
        self.canvas.bind(self.pauseMenu.keyEntries["rotateLeft"], lambda e: self.player.rotateLeft())

    def saveGame(self):
        """saves the game state to a file (saveData.txt)"""
        self.gameStateDict = {
            "score": self.score,
            "health": self.healthBar["value"],
            "MotherShipHealth": self.motherShipHealth,
            "difficulty": self.difficulty,
            "spawnEnemyDelay": self.spawnEnemyDelay,
        }

        with open('saveData.txt', 'w') as outfile:
            for item in self.gameStateDict:
                outfile.write(f"{item}: {self.gameStateDict[item]}\n")

    def loadGame(self):
        """loads the game state from a file(saveData.txt)"""
        try:
            with open('saveData.txt', 'r') as infile:
                for line in infile:
                    key, value = line.split(": ")
                    self.gameStateDict[key] = int(value)
        except FileNotFoundError:
            messagebox.showinfo(title="Error", message="No save data found")

        self.score = self.gameStateDict["score"]
        self.healthBar["value"] = self.gameStateDict["health"]
        self.motherShipHealth = self.gameStateDict["MotherShipHealth"]
        self.difficulty = self.gameStateDict["difficulty"]
        self.spawnEnemyDelay = self.gameStateDict["spawnEnemyDelay"]

    def pauseGame(self):
        """changes the game state to paused and shows the pause menu"""
        self.canvas.configure(cursor="arrow")
        self.gameState = "paused"
        self.pauseMenu.show()

    def resumeGame(self):
        """hides the pause menu and changes the game state to playing"""
        self.canvas.configure(cursor="none")
        if not self.pauseMenu.perfomanceMode:
            self.gif = Image.open("backgroundGIf.gif")
            self.gif = self.gif.resize((self.gameWindow.winfo_width(), self.gameWindow.winfo_height()))
            self.gifFrames = [frame.copy() for frame in ImageSequence.Iterator(self.gif)]
            self.gif = ImageTk.PhotoImage(self.gifFrames[0])
            self.backgroundImage = self.canvas.create_image(0, 0, image=self.gif, anchor=NW)
            self.canvas.lower(self.backgroundImage)
            self.motherShip.updateImage()
        self.pauseMenu.hide()
        self.gameState = "playing"

    def quitGame(self):
        """Destroys the application"""
        self.gameWindow.destroy()

    def escapeFullScreen(self):
        """when the assinged key is pressed the window will go from full screen to a set size -- currently 1080x720"""
        self.gameWindow.attributes("-fullscreen", False)
        self.gameWindow.geometry("1080x720")
        self.gameWindow.resizable(True, True)
        self.fullScreenState = False
        self.canvas.configure(cursor="arrow")
        # self.gameWindow.configure(background="black")
        self.gameWindow.mainloop()
        return True

    def fullScreen(self):
        """when the assinged key is pressed the window will go from a set size to full screen"""
        self.gameWindow.attributes("-fullscreen", True)
        self.gameWindow.resizable(False, False)
        self.canvas.configure(cursor="none")
        self.fullScreenState = True
        # self.gameWindow.configure(background="black")
        self.gameWindow.mainloop()

    def pauseMenuLogic(self):
        """"checks the current game state and will ajust the pause menu and change the state"""
        if self.gameState == "playing":
            self.canvas.configure(cursor="arrow")
            self.pauseMenu.show()
            self.gameState = "paused"
            print(self.gameState)
        elif self.gameState == "paused":
            self.canvas.configure(cursor="none")
            self.pauseMenu.hide()
            self.gameState = "playing"

    def bossKeyLogic(self):
        """checks the current game state and will ajust the boss key screen and change the state"""
        if self.gameState == "playing":
            self.canvas.configure(cursor="arrow")
            self.bossKey.placeFrame()
            self.gameState = "bossKey"
        elif self.gameState == "bossKey":
            self.canvas.configure(cursor="none")
            self.bossKey.forgetFrame()
            self.gameState = "playing"

    def changeWindowSize(self):
        """calls the full screen and escape full screen functions - used to clean up code"""

        if self.gameWindow.attributes("-fullscreen", True):
            self.escapeFullScreen()

        elif self.gameWindow.attributes("-fullscreen", False):
            self.fullScreen()


    def getScore(self):
        """Returns the score as a string"""
        return str(self.score)

    def spawnEnemy(self):
        """if the game state is playing spawns an enemy at a random location on the screen and adds it to the enemies
        list """
        if self.gameState == "playing":
            self.enemy = enemyImp(self.canvas, self.gameWindow)
            if random.random() < self.difficulty:
                spawn_x = random.randint(0,
                                         self.gameWindow.winfo_width())
                spawn_y = random.randint(-int(self.gameWindow.winfo_height() / 2), 0)
            else:
                spawn_x = random.randint(0, self.gameWindow.winfo_width())
                spawn_y = random.randint(-int(self.gameWindow.winfo_height() / 2), self.gameWindow.winfo_height())
            self.canvas.move(self.enemy.enemyBody, spawn_x, spawn_y)
            self.enemiesList.append(self.enemy)
        self.gameWindow.after(self.spawnEnemyDelay, self.spawnEnemy)

    def changeSpawnEnemyDelay(self):
        """changes the spawn enemy delay to increase the difficulty of the game"""
        self.spawnEnemyDelay -= 10

    def exitGame(self):
        """When called will destroy the window and quit the application"""

        self.gameWindow.destroy()
        self.gameWindow.quit()

    def spawnDifficulty(self):
        """Depending on the difficulty and time of the game the closer the enemies spawn to the mothership"""
        return int(0 + (self.difficulty * 80))

    def increaseDifficulty(self):
        """Increases the difficulty of the game, after a set amount of time"""
        if self.difficulty > 1:
            self.difficulty = 1
        else:
            self.difficulty += 0.05
            self.changeSpawnEnemyDelay()
            self.gameWindow.after(1000, self.increaseDifficulty)

    def removeBullets(self):
        """Removes the bullets from the screen when they go off the screen."""
        # Collect IDs of bullets to be deleted
        bullets_to_delete = [bullet.bulletObject for bullet in self.player.bullets if bullet.y <= 0]

        # Delete all bullets at once
        self.canvas.delete(*bullets_to_delete)

        # Remove bullets from player's list
        self.player.bullets = [bullet for bullet in self.player.bullets if bullet.y >= 0]

        # Schedule the next call to removeBullets
        self.gameWindow.after(50, self.removeBullets)

    def removeEnemies(self):
        """Removes enemies from the enemies list if they have been shot"""
        self.enemiesList = [self.enemy for self.enemy in self.enemiesList if self.enemy.health > 0]
        for self.enemy in self.enemiesList:
            if self.enemy.health < 0:
                self.canvas.delete(self.enemy.enemyBody)
                del self.enemy

    def checkBulletCollision(self, bullet, enemy):
        """checks if the bullet has hit the enemy"""
        if bullet.bulletObject is not None:
            bulletBbox = bullet.getBbox()
            enemyBbox = enemy.getBbox()

            if bulletBbox and enemyBbox:
                if (bulletBbox[0] < enemyBbox[2] and  # Check left edge of bullet vs right edge of enemy
                        bulletBbox[2] > enemyBbox[0] and  # Check right edge of bullet vs left edge of enemy
                        bulletBbox[1] < enemyBbox[3] and  # Check top edge of bullet vs bottom edge of enemy
                        bulletBbox[3] > enemyBbox[1]):  # Check bottom edge of bullet vs top edge of enemy
                    return True
            else:
                return False

    def checkPlayerCollision(self, enemy):
        """checks if the player has been hit by an enemy"""
        playerBbox = self.player.getBbox()
        enemyBbox = enemy.getBbox()

        if playerBbox and enemyBbox:
            if (playerBbox[0] < enemyBbox[2] and  # Check left edge of player vs right edge of enemy
                    playerBbox[2] > enemyBbox[0] and  # Check right edge of player vs left edge of enemy
                    playerBbox[1] < enemyBbox[3] and  # Check top edge of player vs bottom edge of enemy
                    playerBbox[3] > enemyBbox[1]):  # Check bottom edge of player vs top edge of enemy
                return True
            else:
                return False

    def checkMotherShipCollision(self, enemy):
        """checks if the mothership has been hit by an enemy by compairing the bounding boxes of the two objects"""
        motherBbox = self.motherShip.getBbox()
        enemyBbox = enemy.getBbox()

        if motherBbox and enemyBbox:
            if motherBbox[0] < enemyBbox[2] and motherBbox[2] > enemyBbox[0] and motherBbox[1] < enemyBbox[3] and \
                    motherBbox[3] > enemyBbox[1]:
                return True
            else:
                return False

    def handleEndGame(self):
        """When this is called a sialog box is created"""
        userName = simpledialog.askstring("Name", "Enter your name:")

        if userName is not None:
            self.leaderboard.writeLeaderboardData(userName, self.score)
            return True
        elif userName is None:
            self.exitGame()

    def gameLoop(self):
        """the main game loop, in here the movements are upded and the methods are called,
        the game updates every 20ms -- from the after method"""
        if self.pauseMenu.speedCheat:
            self.player.movementSpeed = 100
            self.healthBar["value"] = 100
            self.pauseMenu.speedCheat = False

        if self.gameState == "playing":

            # Below checks if the player has been hit by an enemy -- then deducts the health and removes the enemy
            for self.enemy.enemy in self.enemiesList:
                self.enemy.enemy.moveEnemy(0.5 * self.canvas.winfo_width(), self.canvas.winfo_height())
                if self.checkMotherShipCollision(self.enemy.enemy):
                    self.gameState = "end"
                    if self.handleEndGame():
                        self.exitGame()
                if self.checkPlayerCollision(self.enemy.enemy):
                    if self.healthBar["value"] <= 0:
                        self.gameState = "end"
                        if self.handleEndGame():
                            self.exitGame()
                    else:
                        self.healthBar["value"] -= 20
                        self.enemy.enemy.destroy()
                        self.enemy.enemy.health = 0
                        self.removeEnemies()

            # Below checks if a bullet has hit an enemy -- then removes the enemy
            for self.player.bullet in self.player.bullets:
                for self.enemy.enemy in self.enemiesList:
                    if self.checkBulletCollision(self.player.bullet, self.enemy.enemy):
                        self.score += 1
                        # self.scoreLabel.configure(text=self.getScore())
                        self.enemy.enemy.destroy()
                        self.enemy.enemy.health = 0
                        self.removeEnemies()
                self.player.bullet.moveBullet()

            # Below checks if the player has chnaged the key input then updated the controls
            if self.pauseMenu.refreshKeyBroadcast:
                self.pauseMenu.refreshKeyBroadcast = False
                self.refreshKeyInput()

            self.removeBullets()
            Label(self.gameWindow, text="Score: " + self.getScore(), font="Times 20 italic bold",
                  background="red").place(x=5, y=5)

        self.gameWindow.after(20, self.gameLoop)

if __name__ == '__main__':
    window = MainWindow()
    # window.initGame()
