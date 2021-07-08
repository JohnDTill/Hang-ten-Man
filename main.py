import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
import random
import requests


word_site = "https://www.mit.edu/~ecprice/wordlist.10000"
response = requests.get(word_site)
word_bank = response.content.splitlines()

ascii_art = [
    "       |>\n"
    "       |   \\O/\n"
    "~^~^~~ | ~~ | ~~^~~",

    "     ____--\n"
    "   _/  /   O\n"
    " _/   /  -/-\n"
    "/    /    |\\\n"
    "    | ^----- ~~~~~~~",

    "    /-        O\n"
    "   /\\       -/-\n"
    "  /  \\       |\\\n"
    "~/    \\~ ^----- ~~~~~~~",

    "             O\n"
    "           -/-\n"
    "  /\\        |\\\n"
    "~/  \\~~ ^----- ~~~~~~~",

    "        O\n"
    "      -/-\n"
    "       |\\\n"
    "~~ ^----- ~~~~~~~"
]

ascii_win = "          \\O_\n" \
            "          /\n" \
            "         |\\\n" \
            "     ^-----\n" \
            "   ------\n" \
            " _/  /\n" \
            "/   /\n" \
            "    | ~~~~~~~"


class DlgMain(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hang-ten man")
        self.resize(400, 350)
        self.mainLayout = QVBoxLayout()

        font = QFont("nonexistent")
        font.setStyleHint(QFont.Monospace)

        self.pictorialEdit = QPlainTextEdit(self)
        self.pictorialEdit.setReadOnly(True)
        self.pictorialEdit.setPlainText(ascii_art[-1])
        self.pictorialEdit.setFont(font)
        self.pictorialEdit.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.mainLayout.addWidget(self.pictorialEdit)

        self.wordLabel = QLabel()
        self.mainLayout.addWidget(self.wordLabel)

        self.guessLabel = QLabel()
        self.mainLayout.addWidget(self.guessLabel)

        self.hintLabel = QLabel()
        self.mainLayout.addWidget(self.hintLabel)

        self.inputLayout = QHBoxLayout()
        self.inputLayout.addWidget(QLabel("Guess: "))
        self.guessEdit = QLineEdit(self)
        self.guessEdit.setMaxLength(1)
        self.guessEdit.returnPressed.connect(self.on_submit)
        self.inputLayout.addWidget(self.guessEdit)
        self.btn = QPushButton("Submit")
        self.btn.pressed.connect(self.on_submit)
        self.inputLayout.addWidget(self.btn)
        self.mainLayout.addLayout(self.inputLayout)

        self.setCentralWidget(QWidget(self))
        self.centralWidget().setLayout(self.mainLayout)

        self.guessedLetters = None
        self.lives = None
        self.word = None
        self.new_game()

    def update_display_word(self):
        hidden_word = ""
        for ch in self.word:
            if ch.lower() in self.guessedLetters:
                hidden_word += ch
            else:
                hidden_word += '*'
        self.wordLabel.setText(hidden_word)

    def update_display_guesses(self):
        self.guessLabel.setText("{} guesses remaining".format(self.lives))
        if self.lives < len(ascii_art):
            self.pictorialEdit.setPlainText(ascii_art[self.lives])
        else:
            self.pictorialEdit.setPlainText(ascii_art[-1])

    def on_submit(self):
        if self.guessEdit.isEnabled():
            self.on_guess()
        else:
            self.new_game()

    def on_guess(self):
        guess = self.guessEdit.text().lower()
        if not guess:
            self.hintLabel.setText("Enter a letter in the box, bro!")
        elif not guess.isalpha():
            self.hintLabel.setText("Letters only, dude!")
        elif guess in self.guessedLetters:
            self.hintLabel.setText("You already guessed '{}', dude!".format(guess))
        elif guess in self.word.lower():
            self.hintLabel.setText("'{}' is part of the word!".format(guess))
            self.guessedLetters.append(guess)
            self.update_display_word()
            if self.wordLabel.text() == self.word:
                self.hintLabel.setText("Radical! You win!")
                self.pictorialEdit.setPlainText(ascii_win)
                self.btn.setText("New game")
                self.guessEdit.setEnabled(False)
        else:
            self.hintLabel.setText("'{}' is not present.".format(guess))
            self.guessedLetters.append(guess)
            self.lives -= 1
            self.update_display_guesses()
            if not self.lives:
                self.hintLabel.setText("Wipe out!")
                self.wordLabel.setText(self.word)
                self.btn.setText("New game")
                self.guessEdit.setEnabled(False)

    def new_game(self):
        self.guessedLetters = []
        self.lives = 4
        self.word = random.choice(word_bank).decode("utf-8").capitalize()
        self.update_display_word()
        self.update_display_guesses()
        self.btn.setText("Submit")
        self.hintLabel.setText("Go ahead- guess a letter!")
        self.guessEdit.clear()
        self.guessEdit.setEnabled(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dlgMain = DlgMain()
    dlgMain.show()
    sys.exit(app.exec_())
