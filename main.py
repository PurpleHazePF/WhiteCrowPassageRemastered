import sys

from ParcheesiDialecto import ParcheesiDialecto
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QLineEdit, QComboBox
from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia
from random import randint
import sqlite3

SCREEN_SIZE = [800, 600]

con = sqlite3.connect("mapCoords")
cur = con.cursor()
result = cur.execute("""SELECT * FROM coords """).fetchall()


class CrowGame(QMainWindow):
    readyButton: QPushButton | QPushButton

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 200, *SCREEN_SIZE)
        self.setWindowTitle('White Crow Passage')
        self.setFixedSize(800, 650)
        self.mapC = []
        self.mapNames = ["-", "assets/classic1.png", "assets/eternityRun1.png", "assets/cicles1.png",
                         "assets/portalGame.png"]
        self.members = ["игрок", "игрок", "игрок", "игрок"]

        self.rules_text = self.customization(QLabel(self), rect=(200, 400, 500, 400),
                                        text='Расслабьтесь, обязательно позовите друзей\nПо очереди кидайте кости\nпобедит тот, кто первый доведёт все 3 фишки до финиша',
                                        font_size=12)
        self.rules_text.hide()
        self.welcome_text = self.customization(QLabel(self), rect=(450, 230, 350, 91),
                                               text='Белая ворона большая редкость в природе\nкто знает, куда вас может привести эта птица',
                                               font_size=12)

        self.start_btn = self.customization(QtWidgets.QPushButton(self), rect=(120, 160, 221, 61), text="Старт",
                                            font_size=24)
        self.rules_btn = self.customization(QtWidgets.QPushButton(self), rect=(120, 230, 221, 51),
                                            text="Как играть?", font_size=18)
        self.exit_btn = self.customization(QtWidgets.QPushButton(self), rect=(120, 290, 221, 61), text="Выход",
                                           font_size=24)

        self.continue_btn = self.customization(QPushButton(self), rect=(200, 200, 400, 120), text="Продолжить игру",
                                               font_size=18)

        self.new_game_btn = self.customization(QtWidgets.QPushButton(self), rect=(200, 230, 400, 120), text="Новая игра",
                                               font_size=18)
        self.new_game_btn.hide()
        self.continue_btn.hide()
        self.map_pick_text = self.customization(QLabel(self), rect=(200, 5, 670, 100), text="      Куда отправимся?",
                                                font_size=24)
        self.map_pick_text.hide()

        self.crow_menu_pic = self.customization(QLabel(self), rect=(505, 0, 295, 249))
        self.crow_menu_pic.setPixmap(QPixmap("assets/whiteCrow.png"))
        self.miniClassic = QLabel(self)
        self.miniClassic.hide()

        self.menuButton = self.customization(QtWidgets.QPushButton(self), rect=(10, 10, 40, 40), text="←", font_size=18)
        self.menuButton.hide()

        self.minimap = QLabel(self)
        self.minimap.setPixmap(QPixmap("assets/miniMaps.png"))
        self.minimap.setGeometry(QtCore.QRect(0, 50, 800, 200))
        self.minimap.hide()
        x = 0
        self.test = []
        self.desctxt = ["Классический", "Бесконечные бега", "Циклы", "Портальная игра"]
        self.cBtns = []
        for i in range(4):
            self.desc = self.customization(QLabel(self), rect=(10 + x, 290, 200, 40), text=self.desctxt[i],
                                           font_size=14)
            self.desc.hide()
            self.test.append(self.desc)
            self.minimap2 = QLabel(self)
            self.miniBtn = self.customization(QPushButton(self), rect=(10 + x, 250, 180, 40), text="▶", font_size=18)
            self.miniBtn.hide()
            self.cBtns.append(self.miniBtn)
            x += 200
        self.nMap = 0
        self.name_input = self.customization(QLineEdit(self), rect=(10, 250, 180, 35), font_size=14)
        self.name_input2 = self.customization(QLineEdit(self), rect=(210, 250, 180, 35), font_size=14)
        self.name_input3 = self.customization(QLineEdit(self), rect=(410, 250, 180, 35), font_size=14)
        self.name_input4 = self.customization(QLineEdit(self), rect=(610, 250, 180, 35), font_size=14)
        self.combo_box1 = self.customization(QComboBox(self), rect=(10, 100, 180, 40), font_size=10)
        self.combo_box1.addItems(["игрок", "бот", "АнальныйПенетратор3000", "отключено"])
        self.combo_box1.currentTextChanged.connect(self.update_member_status1)
        self.combo_box2 = self.customization(QComboBox(self), rect=(210, 100, 180, 40), font_size=10)
        self.combo_box2.addItems(["игрок", "бот", "АнальныйПенетратор3000", "отключено"])
        self.combo_box2.currentTextChanged.connect(self.update_member_status2)
        self.combo_box3 = self.customization(QComboBox(self), rect=(410, 100, 180, 40), font_size=10)
        self.combo_box3.addItems(["игрок", "бот", "АнальныйПенетратор3000", "отключено"])
        self.combo_box3.currentTextChanged.connect(self.update_member_status3)
        self.combo_box4 = self.customization(QComboBox(self), rect=(610, 100, 180, 40), font_size=10)
        self.combo_box4.addItems(["игрок", "бот", "АнальныйПенетратор3000", "отключено"])
        self.combo_box4.currentTextChanged.connect(self.update_member_status4)
        self.combo_boxes = [self.combo_box1, self.combo_box2, self.combo_box3, self.combo_box4]
        self.miniChips = self.customization(QLabel(self), rect=(0, 200, 800, 40))
        self.miniChips.setPixmap(QPixmap("assets/nChips.png"))

        self.readyButton = self.customization(QPushButton(self), rect=(580, 530, 200, 100), text="Готово", font_size=14)
        self.ready = [self.name_input, self.name_input2, self.name_input3, self.name_input4, self.readyButton,
                      self.miniChips]
        self.nicknames = [self.name_input, self.name_input2, self.name_input3, self.name_input4]
        for i in self.ready:
            i.hide()
        for i in self.combo_boxes:
            i.hide()
        self.cNumber = 0
        self.turn = 0
        self.cubics = [0, 0]
        self.dice1 = self.customization(QLabel(self), rect=(0, 560, 80, 80))
        self.dice1.setPixmap(QPixmap("diceR1.png"))
        self.dice2 = self.customization(QLabel(self), rect=(0, 560, 80, 80))
        self.dice2.setPixmap(QPixmap("diceR2.png"))
        self.dice3 = self.customization(QLabel(self), rect=(0, 560, 80, 80))
        self.dice3.setPixmap(QPixmap("diceR3.png"))
        self.dice4 = self.customization(QLabel(self), rect=(0, 560, 80, 80))
        self.dice4.setPixmap(QPixmap("diceR4.png"))
        self.dice5 = self.customization(QLabel(self), rect=(0, 560, 80, 80))
        self.dice5.setPixmap(QPixmap("diceR5.png"))
        self.dice6 = self.customization(QLabel(self), rect=(0, 560, 80, 80))
        self.dice6.setPixmap(QPixmap("diceR6.png"))
        self.dices = [self.dice1, self.dice2, self.dice3, self.dice4, self.dice5, self.dice6]
        self.diceSounds = ["diceRoll1.mp3", "diceRoll2.mp3", "diceRoll4.mp3", ]
        for i in self.dices:
            i.hide()
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.PlayerTurn = self.customization(QLabel(self), rect=(0, 470, 500, 120), font_size=24)
        self.PlayerMsg = self.customization(QLabel(self), rect=(10, 550, 400, 60), font_size=24)
        self.skipTurn = self.customization(QPushButton("Пропустить ход", self), rect=(530, 530, 110, 30))
        self.skipTurn.setEnabled(False)
        self.GoChip1 = self.customization(QPushButton("Сходить фишкой №1", self), rect=(350, 530, 170, 30))
        self.GoChip1.setEnabled(False)
        self.GoChip2 = self.customization(QPushButton("Сходить фишкой №2", self), rect=(350, 565, 170, 30))
        self.GoChip2.setEnabled(False)
        self.GoChip3 = self.customization(QPushButton("Сходить фишкой №3", self), rect=(350, 600, 170, 30))
        self.GoChip3.setEnabled(False)
        self.chipCommands = [self.GoChip1, self.GoChip2, self.GoChip3]
        self.rollTheDice = self.customization(QPushButton("Бросить кубик", self), rect=(530, 570, 110, 30))
        self.gameButtons = [self.GoChip1, self.GoChip2, self.GoChip3, self.skipTurn, self.rollTheDice, self.PlayerTurn]
        for i in self.gameButtons:
            i.hide()
        self.way_pick_script = [[self.start_btn,
                                 self.exit_btn,
                                 self.rules_btn,
                                 self.crow_menu_pic,
                                 self.welcome_text,
                                 self.rules_text],
                                [self.new_game_btn,
                              self.menuButton]]
        self.back_to_menu_script = [[
            self.new_game_btn,
            self.menuButton,
            self.map_pick_text,
            self.desc,
            self.minimap, *self.test, *self.cBtns, *self.ready, *self.combo_boxes], [self.start_btn,
                                                                                     self.exit_btn,
                                                                                     self.rules_btn,
                                                                                     self.crow_menu_pic,
                                                                                     self.welcome_text]]
        self.map_pick_script = [[self.new_game_btn,
                                 self.continue_btn,
                                 ], [self.map_pick_text,
                                     self.desc,
                                     self.minimap,
                                     self.miniBtn,
                                     *self.test,
                                     *self.cBtns]]
        self.members_pick_script = [[*self.test, *self.cBtns, self.minimap], [*self.ready, *self.combo_boxes]]
        self.load_mp3(self.diceSounds[randint(0, 2)])
        self.exit_btn.clicked.connect(self.app_exit)
        self.menuButton.clicked.connect(self.back_to_menu)
        self.start_btn.clicked.connect(self.way_pick)
        self.new_game_btn.clicked.connect(self.map_pick)
        self.rollTheDice.clicked.connect(self.player.play)
        self.rollTheDice.clicked.connect(self.roll)
        self.GoChip1.clicked.connect(self.chipN1)
        self.GoChip1.clicked.connect(self.goChip)
        self.GoChip2.clicked.connect(self.chipN2)
        self.GoChip2.clicked.connect(self.goChip)
        self.GoChip3.clicked.connect(self.chipN3)
        self.GoChip3.clicked.connect(self.goChip)
        self.skipTurn.clicked.connect(self.tskip)
        self.cBtns[0].clicked.connect(self.map1)
        self.cBtns[1].clicked.connect(self.map2)
        self.cBtns[2].clicked.connect(self.map3)
        self.cBtns[3].clicked.connect(self.map4)
        self.readyButton.clicked.connect(self.mapCheck)
        self.rules_btn.clicked.connect(self.rules_show)

    def customization(self, label, rect=(0, 0, 0, 0), text='nonactive', font_size=-1):
        if font_size != -1:
            font = QtGui.QFont()
            font.setPointSize(font_size)
            label.setFont(font)
        if text != 'nonactive':
            label.setText(text)
        if rect != (0, 0, 0, 0):
            label.setGeometry(QtCore.QRect(*rect))
        return label

    def update_member_status1(self, text):
        self.members[0] = text
        if self.members[0] != 'игрок':
            self.name_input.setReadOnly(True)
            self.name_input.setText('')
        else:
            self.name_input.setReadOnly(False)
        print(self.members)

    def update_member_status2(self, text):
        self.members[1] = text
        if self.members[1] != 'игрок':
            self.name_input2.setReadOnly(True)
            self.name_input2.setText('')
        else:
            self.name_input2.setReadOnly(False)

    def update_member_status3(self, text):
        self.members[2] = text
        if self.members[2] != 'игрок':
            self.name_input3.setReadOnly(True)
            self.name_input3.setText('')
        else:
            self.name_input3.setReadOnly(False)

    def update_member_status4(self, text):
        self.members[3] = text
        if self.members[3] != 'игрок':
            self.name_input4.setReadOnly(True)
            self.name_input4.setText('')
        else:
            self.name_input4.setReadOnly(False)

    def rules_show(self):
        self.rules_text.show()

    def app_exit(self):
        sys.exit(app.exec())

    def way_pick(self):
        for i in self.way_pick_script[0]:
            i.hide()
        for i in self.way_pick_script[1]:
            i.show()

    def back_to_menu(self):
        for i in self.back_to_menu_script[0]:
            i.hide()
        for i in self.back_to_menu_script[1]:
            i.show()
        self.map_pick_text.setText("      Куда отправимся?")

    def map_pick(self):
        for i in self.map_pick_script[0]:
            i.hide()
        for i in self.map_pick_script[1]:
            i.show()

    def create_game(self):
        for i in self.combo_boxes:
            i.hide()
        for i in self.ready:
            i.hide()
        self.map_pick_text.hide()
        self.menuButton.hide()
        self.background2 = QLabel(self)
        self.background2.setPixmap(QPixmap("classicBackground.png"))
        self.background2.resize(800, 500)
        self.background2.move(0, 0)
        self.background2.show()
        self.background = QLabel(self)
        self.background.setPixmap(QPixmap(self.mapNames[self.nMap]))
        self.background.resize(800, 500)
        self.background.move(0, 0)
        self.background.show()
        for i in self.gameButtons:
            i.show()
        for elem in result:
            if elem[self.nMap] == "end":
                break
            a = elem[self.nMap].find(":")
            self.mapC.append((int(elem[self.nMap][:a]), int(elem[self.nMap][a + 1:])))
        """self.nameInput(self.nicknames[0].text(), "red")
        self.nameInput(self.nicknames[1].text(), "blue")
        self.nameInput(self.nicknames[2].text(), "green")
        self.nameInput(self.nicknames[3].text(), "yellow")
        self.queueOfPlayers.append(self.playerRed)
        self.queueOfPlayers.append(self.playerBlue)
        self.queueOfPlayers.append(self.playerGreen)
        self.queueOfPlayers.append(self.playerYellow)
        self.playersCount = 4
        pointLen = len(self.mapC) // self.playersCount
        startPoint = - pointLen
        for i in range(self.playersCount):
            startPoint += pointLen
            self.queueOfPlayers[i]["endpoint"] = startPoint
        self.turnColor = self.queueOfPlayers[self.turn]["color"]
        self.PlayerTurn.setText("Ход игрока из команды: " + self.turnColor)"""
        self.cRed1 = self.customization(QLabel(self), rect=(0, 0, 50, 40))
        self.cRed1.setPixmap(QPixmap("assets/chipR1.png"))
        self.cRed2 = self.customization(QLabel(self), rect=(10, 0, 50, 40))
        self.cRed2.setPixmap(QPixmap("assets/chipR2.png"))
        self.cRed3 = self.customization(QLabel(self), rect=(20, 0, 50, 40))
        self.cRed3.setPixmap(QPixmap("assets/chipR3.png"))
        self.cBlue1 = self.customization(QLabel(self), rect=(30, 0, 50, 40))
        self.cBlue1.setPixmap(QPixmap("assets/chipB1.png"))
        self.cBlue2 = self.customization(QLabel(self), rect=(40, 0, 50, 40))
        self.cBlue2.setPixmap(QPixmap("assets/chipB2.png"))
        self.cBlue3 = self.customization(QLabel(self), rect=(50, 0, 50, 40))
        self.cBlue3.setPixmap(QPixmap("assets/chipB3.png"))
        self.cGreen1 = self.customization(QLabel(self), rect=(60, 0, 50, 40))
        self.cGreen1.setPixmap(QPixmap("assets/chipG1.png"))
        self.cGreen2 = self.customization(QLabel(self), rect=(70, 0, 70, 40))
        self.cGreen2.setPixmap(QPixmap("assets/chipG2.png"))
        self.cGreen3 = self.customization(QLabel(self), rect=(80, 0, 50, 40))
        self.cGreen3.setPixmap(QPixmap("assets/chipG3.png"))
        self.cYellow1 = self.customization(QLabel(self), rect=(90, 0, 50, 40))
        self.cYellow1.setPixmap(QPixmap("assets/chipY1.png"))
        self.cYellow2 = self.customization(QLabel(self), rect=(100, 0, 50, 40))
        self.cYellow2.setPixmap(QPixmap("assets/chipY2.png"))
        self.cYellow3 = self.customization(QLabel(self), rect=(110, 0, 50, 40))
        self.cYellow3.setPixmap(QPixmap("assets/chipY3.png"))
        chip_list = [self.cRed1, self.cRed2, self.cRed3, self.cBlue1, self.cBlue2, self.cBlue3, self.cGreen1,
                     self.cGreen2, self.cGreen3, self.cYellow1, self.cYellow2, self.cYellow3]
        for i in chip_list:
            i.hide()
        self.win = QLabel(self)
        self.win.setPixmap(QPixmap("winner.png"))
        self.win.resize(800, 500)
        self.win.move(0, 0)
        self.win.hide()
        font1 = QtGui.QFont()
        font1.setPointSize(26)
        self.tWin = QLabel(self)
        self.tWin.setText("")
        self.tWin.setFont(font1)
        self.tWin.resize(600, 100)
        self.tWin.move(200, 200)
        self.tWin.hide()
        font = QtGui.QFont()
        font.setPointSize(14)
        self.rp = 0
        self.bp = 0
        self.gp = 0
        self.yp = 0
        self.cBlue1.show()

        """self.winner = {"red": self.rp, "blue": self.bp, "green": self.gp, "yellow": self.yp}
        self.chipsVis = {"red": (self.cRed1, self.cRed2, self.cRed3),
                         "blue": (self.cBlue1, self.cBlue2, self.cBlue3),
                         "green": (self.cGreen1, self.cGreen2, self.cGreen3),
                         "yellow": (self.cYellow1, self.cYellow2, self.cYellow3)}
        self.mapLen = len(self.mapC)
        self.mapEntity = [self.ChipR1, self.ChipR2, self.ChipR3,
                          self.ChipB1, self.ChipB2, self.ChipB3,
                          self.ChipG1, self.ChipG2, self.ChipG3,
                          self.ChipY1, self.ChipY2, self.ChipY3]
        self.PlayerTurn.setText(
            "Ход игрока " + self.playersDict[self.turnColor]["name"] + "\nиз команды: " + self.turnColor)"""

    def map1(self):
        self.nMap = 1
        self.members_pick()

    def map2(self):
        self.nMap = 2
        self.members_pick()

    def map3(self):
        self.nMap = 3
        self.members_pick()

    def map4(self):
        self.nMap = 4
        self.members_pick()

    def members_pick(self):
        for i in self.members_pick_script[0]:
            i.hide()
        for i in self.members_pick_script[1]:
            i.show()
        self.map_pick_text.setText("Введите имена\n(не более 12 симв.)")

    def mapCheck(self):
        names = ""
        colors = ["Красного, ", "Синего, ", "Зелёного, ", "Жёлтого, "]
        for i in range(4):
            if len(self.nicknames[i].text()) > 12 or len(self.nicknames[i].text()) == 0:
                names += colors[i]
        if names:
            msg = "Некорректные ники у\n" + names[:-2]
            self.map_pick_text.setText(msg)
        else:
            self.create_game()

    def load_mp3(self, filename):
        self.media = QtCore.QUrl.fromLocalFile(filename)
        content = QtMultimedia.QMediaContent(self.media)
        self.player = QtMultimedia.QMediaPlayer()
        self.player.setMedia(content)

    def roll(self):
        print(f'random: {1}')
        self.GoChip1.setEnabled(True)
        self.GoChip2.setEnabled(True)
        self.GoChip3.setEnabled(True)
        self.rollTheDice.setEnabled(False)
        self.skipTurn.setEnabled(True)

    def goChip(self):
        print('removed')

    def tskip(self):
        for i in self.chipCommands:
            i.setEnabled(False)
        self.rollTheDice.setEnabled(True)
        self.skipTurn.setEnabled(False)
        print('removed')

    def chipN1(self):
        self.cNumber = 1

    def chipN2(self):
        self.cNumber = 2

    def chipN3(self):
        self.cNumber = 3


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CrowGame()
    ex.show()
    sys.exit(app.exec())
