# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 00:39:50 2024

@author: vikash kushwaha
"""

import sys
import csv
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QInputDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QTimer, QTime


class MastermindGame(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.time = QTime(0, 0, 0)
        self.game_number = 1  # Initialize game number
        self.init_game_data_storage()


    def initUI(self):
        self.setWindowTitle('Mastermind Guess Game')
        self.setGeometry(100, 100, 500, 350)
        self.setWindowIcon(QIcon('icon.png'))  # for  Setting the window icon

        # Setting styles
        self.setStyleSheet("""
            QWidget {
                background-color: #f8f8f8; /* Light grey background */
                font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif; /* Default font */
            }
            QLabel {
                font-size: 14pt;
                font-weight: bold;
                color: #333; /* Dark grey text color */
            }
            QLineEdit {
                font-size: 12pt;
                padding: 8px;
                border: 1px solid #ccc; /* Light grey border */
                border-radius: 5px;
            }
            QPushButton {
                font-size: 12pt;
                background-color: #2196F3; /* Blue button color */
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #1976D2; /* Darker blue on hover */
            }
            QPushButton:disabled {
                background-color: #c1c1c1;
            }
            QInputDialog {
                background-color: #f0f0f0;
                font-size: 12pt;
                font-family: Arial, Helvetica, sans-serif;
            }
            QInputDialog QLineEdit {
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            QInputDialog QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
            }
            QInputDialog QPushButton:hover {
                background-color: #45a049;
            }
        """)

        # Player names and digit input
        self.player1_label = QLabel('Player 1\'s Name:')
        self.player1_entry = QLineEdit()
        self.player2_label = QLabel('Player 2\'s Name:')
        self.player2_entry = QLineEdit()
        self.digits_label = QLabel('Number of Digits (max 8):')
        self.digits_entry = QLineEdit()

        # Start game button
        self.start_button = QPushButton('Start Game')
        self.start_button.clicked.connect(self.start_game)
        self.start_button.setDefault(True)  # Set as default to capture Enter key

        # Game state labels
        self.round_label = QLabel('')
        self.feedback_label = QLabel('')
        self.attempts_label = QLabel('Attempts:')

        # Timer label
        self.timer_label = QLabel('Time: 00:00:00')

        # Guess input and submit button
        self.guess_entry = QLineEdit()
        self.guess_entry.returnPressed.connect(self.check_guess)  # Connect Enter key
        self.submit_button = QPushButton('Submit Guess')
        self.submit_button.clicked.connect(self.check_guess)
        self.submit_button.setEnabled(False)        

        # Layout setup
        vbox = QVBoxLayout()
        vbox.addWidget(self.player1_label)
        vbox.addWidget(self.player1_entry)
        vbox.addWidget(self.player2_label)
        vbox.addWidget(self.player2_entry)
        vbox.addWidget(self.digits_label)
        vbox.addWidget(self.digits_entry)
        vbox.addWidget(self.start_button)
        vbox.addWidget(self.round_label)
        vbox.addWidget(self.timer_label)

        # Feedback and attempts layout
        hbox_feedback = QVBoxLayout()
        hbox_feedback.addWidget(self.feedback_label)
        hbox_feedback.addWidget(self.attempts_label)
        hbox_game = QVBoxLayout()
        hbox_game.addWidget(self.guess_entry)
        hbox_game.addWidget(self.submit_button)
        hbox = QVBoxLayout()
        hbox.addLayout(hbox_game)
        hbox.addLayout(hbox_feedback)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        # Game variables
        self.secret_number = None
        self.player1 = ""
        self.player2 = ""
        self.num_digits = 0
        self.attempts = 0
        self.player1_attempts = 0
        self.player2_attempts = 0
        self.current_player = 1  # 1 for Player 1 setting, 2 for Player 2 guessing
        self.game_in_progress = False
        self.round = 1  # Keep track of the current round

    def init_game_data_storage(self):
        with open('game_data.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Game Number", "Player 1", "Player 2", "Time Taken", "Number of Guesses"])

    def start_game(self):
        if self.game_in_progress:
            return
        self.num_digits = int(self.digits_entry.text())
        if self.num_digits <= 0 or self.num_digits > 8:
            QMessageBox.critical(self, 'Invalid Input', 'Number of digits must be between 1 and 8.')
            return
        self.player1 = self.player1_entry.text()
        self.player2 = self.player2_entry.text()

        # Player 1 sets the secret number
        self.current_player = 1
        self.set_secret_number()

        self.start_timer()
    
    def start_timer(self):
        self.time = QTime(0, 0, 0)
        self.timer.start(1000)  # Update every second
    
    def stop_timer(self):
        self.timer.stop()
    
    def update_timer(self):
        self.time = self.time.addSecs(1)
        self.timer_label.setText(f'Time: {self.time.toString("hh:mm:ss")}')

    def set_secret_number(self):
        if self.round == 1:  # Player 1 sets the secret number in round 1
            player_name = self.player1
        else:  # Player 2 sets the secret number in round 2
            player_name = self.player2
        self.secret_number, ok = QInputDialog.getText(self, f'{player_name}, enter a {self.num_digits}-digit number:', 'Number:', QLineEdit.Normal, '', Qt.WindowTitleHint | Qt.WindowSystemMenuHint)
        if not ok:
            self.reset_game()
            return

        # Validate the input:
        if len(self.secret_number) != self.num_digits or not self.secret_number.isdigit():
            QMessageBox.warning(self, 'Invalid Input', f'Please enter a valid {self.num_digits}-digit number.')
            self.set_secret_number()  # Ask for the number again
            return

        self.secret_number = str(self.secret_number)  # Ensure it's a string

        # Start the game loop with Player 2 guessing
        if self.round == 1:
            self.round_label.setText(f'**Round 1: {self.player2} guesses**')
        else:
            self.round_label.setText(f'**Round 2: {self.player1} guesses**')
        self.submit_button.setEnabled(True)
        self.start_button.setEnabled(False)
        self.game_in_progress = True
        self.attempts = 0  # Reset attempts for the new round

    def get_feedback(self, secret_number, guess):
        feedback = ""
        for i in range(len(secret_number)):
            if secret_number[i] == guess[i]:
                feedback += "X"
            elif guess[i] in secret_number:
                feedback += "O"
            else:
                feedback += "-"
        return feedback

    def check_guess(self):
        guess = self.guess_entry.text()
        if len(guess) != self.num_digits or not guess.isdigit():
            QMessageBox.warning(self, 'Invalid Guess', f'Please enter a {self.num_digits}-digit number.')
            return

        self.attempts += 1
        feedback = self.get_feedback(self.secret_number, guess)
        self.feedback_label.setText(f'Feedback: {feedback}')
        self.attempts_label.setText(f'Attempts: {self.attempts}')

        if guess == self.secret_number:
            self.stop_timer()
            if self.round == 1:  # Player 2 guessed correctly in round 1
                self.player2_attempts = self.attempts
                self.round = 2  # Move to round 2
                self.current_player = 1  # Switch to Player 1's turn
                self.set_secret_number()  # Player 1 now sets a new secret number
                self.start_timer()
            else:  # Player 1 guessed correctly in round 2
                self.player1_attempts = self.attempts
                self.end_game()
        else:
            self.guess_entry.clear()

    def end_game(self):
        self.stop_timer()
        elapsed_time = self.timer_label.text().split(' ')[1]

        # Determine the winner based on the fewest attempts across both rounds
        if self.player1_attempts < self.player2_attempts:
            winner_msg = f'{self.player1} is the Mastermind! They guessed the number in {self.player1_attempts} attempts. Time taken: {elapsed_time}'
        elif self.player2_attempts < self.player1_attempts:
            winner_msg = f'{self.player2} is the Mastermind! They guessed the number in {self.player2_attempts} attempts. Time taken: {elapsed_time}'
        else:
            winner_msg = f'It\'s a tie! Both players are Masterminds. Time taken: {elapsed_time}'
        
        QMessageBox.information(self, 'Game Over', winner_msg)
        play_again = QMessageBox.question(self, 'Play Again?', 'Do you want to play again?', QMessageBox.Yes | QMessageBox.No)
        if play_again == QMessageBox.Yes:
            self.reset_game()
        else:
            self.close()
    
    def save_game_data(self, elapsed_time):
        with open('game_data.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([self.game_number, self.player1, self.player2, elapsed_time, self.attempts])
        self.game_number += 1


    def reset_game(self):
        self.start_button.setEnabled(True)
        self.submit_button.setEnabled(False)
        self.round_label.setText('')
        self.feedback_label.setText('')
        self.attempts_label.setText('Attempts:')
        self.timer_label.setText('Time: 00:00:00')
        self.guess_entry.clear()
        self.attempts = 0
        self.player1_attempts = 0
        self.player2_attempts = 0
        self.secret_number = None
        self.game_in_progress = False
        self.current_player = 1  # Player 1 sets the number for the next round
        self.round = 1  # Reset round to 1

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = MastermindGame()
    game.show()
    sys.exit(app.exec_())
