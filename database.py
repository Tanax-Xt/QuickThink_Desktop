import sqlite3


class DataBase:
    def __init__(self, db_file):
        """Инициализация"""
        self.conn = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def get_result(self, game):
        '''Достаем результаты'''
        result = self.cursor.execute(f"SELECT * FROM {game}")
        return result.fetchall()[-3:]

    def add_result(self, game, score):
        '''Добавляем результат пользователя'''
        self.cursor.execute(f"INSERT INTO {game} (score) VALUES (?)", (score,))
        return self.conn.commit()

    def close(self):
        """Закрываем соединение с БД"""
        self.conn.close()
