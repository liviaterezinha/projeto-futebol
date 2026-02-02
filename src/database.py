import sqlite3 

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("campeonato.db", check_same_thread=False)
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS partidas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            jogador1 TEXT NOT NULL,
            jogador2 TEXT NOT NULL,
            time1 TEXT NOT NULL,
            time2 TEXT NOT NULL,
            local TEXT NOT NULL,
            rodada INTEGER NOT NULL,
        );
        """
        self.conn.execute(query)
        self.conn.commit()


    def inserir_partida(self, dados):
        query = """
        INSERT INTO partidas (jogador1, jogador2, time1, time2, local, rodada)
        VALUES (?, ?, ?, ?, ?, ?);
        """
        self.conn.execute(query, dados)
        self.conn.commit()

    def listar_partidas(self):
        query = "SELECT * FROM partidas;"
        cursor = self.conn.execute(query)
        return cursor.fetchall()
    
    def deletar_partida(self, partida_id):
        query = "DELETE FROM partidas WHERE id = ?;"
        self.conn.execute(query, (partida_id,))
        self.conn.commit()