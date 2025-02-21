# MASTERMIND GAME

Two players play the game against each other; let’s assume Player 1 and Player 2.

Player 1 plays first by setting a multi-digit number.
Player 2 now tries his first attempt at guessing the number.
If Player 2 succeeds in his first attempt (despite odds which are highly unlikely) he wins the game and is crowned Mastermind! If not, then Player 1 hints by revealing which digits or numbers Player 2 got correct.
The game continues till Player 2 eventually is able to guess the number entirely.
Now, Player 2 gets to set the number and Player 1 plays the part of guessing the number.
If Player 1 is able to guess the number within a lesser number of tries than Player 2 took, then Player 1 wins the game and is crowned Mastermind.
If not, then Player 2 wins the game.

# How to Play
1. Player 1 sets a secret number.

2. Player 2 attempts to guess the secret number.

3. Feedback is provided for each guess:

- 'X' indicates a correct digit in the correct position.
- 'O' indicates a correct digit in the wrong position.
- '-' indicates an incorrect digit.
  Examples:
  * Secret number: 1234
  * Guess: 1256
  * Feedback: XX-- (1 and 2 are correct and in the correct position)

  * Secret number: 5687
  * Guess: 5789
  * Feedback: O-XO (5 and 7 are correct but in the wrong position, 8 is correct and in the correct position)
4. The game continues until Player 2 guesses the secret number.

5. Roles switch for round 2: Player 2 sets a secret number, and Player 1 guesses.

6. The winner is determined by the fewest attempts taken to guess the opponent's secret number.

## Features

- Two-player mode
- Customizable number of digits (1 to 8)
- Intuitive GUI with PyQt5
- Feedback provided for each guess in the form of 'X', 'O', and '-'

## Requirements

- Python 3.x
- PyQt5
- MySQL Connector
- python-dotenv


You can install the required packages using pip:

```sh
pip install PyQt5 mysql-connector-python
```

## MySQL Database

This project uses a MySQL database to store game results.

### Database Schema

**Database Name:** mastermind_game

**Table Name:** game_results

**Schema:**
- id (INT, Primary Key, Auto Increment)
- game_number (INT)
- player1 (VARCHAR(50))
- player2 (VARCHAR(50))
- time_taken (TIME)
- number_of_guesses (INT)
- winner (VARCHAR(50))
- date (TIMESTAMP, Default: CURRENT_TIMESTAMP)

### Example SQL to Create the Database and Table

```sql
CREATE DATABASE mastermind_game;

USE mastermind_game;

CREATE TABLE game_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    game_number INT,
    player1 VARCHAR(50),
    player2 VARCHAR(50),
    time_taken TIME,
    number_of_guesses INT,
    winner VARCHAR(50),
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Screenshots 
<p align="center">
  <img src="Screenshot 1.png" width="250" />
  <img src="Screenshot 2.png" width="250" />
  <img src="Screenshot 3.png" width="250" />  
  <img src="Screenshot 4.png" width="250" />
  <img src="Screenshot 5.png" width="250" />
</p>
