import sqlite3


class DataBase:
    def __init__(self, db_file):
        """Инициализация"""
        self.conn = sqlite3.connect(db_file)

        self.add_table('choose_right')
        self.add_table('collect_order')
        self.add_table('fast_reaction')

        self.cursor = self.conn.cursor()

    def add_table(self, name):
        data = self.conn.execute(f"select count(*) from sqlite_master where type='table' and name='{name}'")
        for row in data:
            if row[0] == 0:
                self.conn.execute(f'''CREATE TABLE {name} (
                    id       INTEGER  PRIMARY KEY AUTOINCREMENT
                                      NOT NULL,
                    score    INTEGER  NOT NULL,
                    datetime DATETIME NOT NULL
                                      DEFAULT ( (DATETIME('now') ) ) )''')
        return self.conn.commit()

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
