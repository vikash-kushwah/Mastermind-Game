from mysql.connector import connect, Error
from dotenv import load_dotenv
import os

class Database:
    def __init__(self):
        load_dotenv()
        host = os.getenv('DB_HOST')
        user = os.getenv('DB_USER')
        password = os.getenv('DB_PASSWORD')
        database = os.getenv('DB_NAME')

        self.connection = None
        try:
            self.connection = connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            print("Database connection successful")
        except Error as e:
            print(f"Error: '{e}'")

    def create_table(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS game_results (
            id INT AUTO_INCREMENT PRIMARY KEY,
            game_number INT,
            player1 VARCHAR(50),
            player2 VARCHAR(50),
            time_taken TIME,
            number_of_guesses INT,
            winner VARCHAR(50),
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        with self.connection.cursor() as cursor:
            cursor.execute(create_table_query)
            self.connection.commit()

    def insert_game_result(self, game_number, player1, player2, time_taken, number_of_guesses, winner):
        insert_query = """
        INSERT INTO game_results (game_number, player1, player2, time_taken, number_of_guesses, winner)
        VALUES (%s, %s, %s, %s, %s, %s);
        """
        data = (game_number, player1, player2, time_taken, number_of_guesses, winner)
        with self.connection.cursor() as cursor:
            cursor.execute(insert_query, data)
            self.connection.commit()

    def close_connection(self):
        if self.connection:
            self.connection.close()