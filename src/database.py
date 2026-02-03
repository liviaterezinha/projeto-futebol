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
            gols_jogador1 INTEGER DEFAULT 0,
            gols_jogador2 INTEGER DEFAULT 0,
            cartoes_amarelos_j1 INTEGER DEFAULT 0,
            cartoes_amarelos_j2 INTEGER DEFAULT 0,
            cartoes_vermelhos_j1 INTEGER DEFAULT 0,
            cartoes_vermelhos_j2 INTEGER DEFAULT 0
        );
        """
        self.conn.execute(query)
        self.conn.commit()


    def inserir_partida(self, dados):
        query = """
        INSERT INTO partidas (jogador1, jogador2, time1, time2, local, rodada, gols_jogador1, gols_jogador2, cartoes_amarelos_j1, cartoes_amarelos_j2, cartoes_vermelhos_j1, cartoes_vermelhos_j2)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
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

    def buscar_partidas(self):
        cursor = self.conn.execute("""
                       SELECT jogador1, jogador2, gols_jogador1, gols_jogador2,
                       cartoes_amarelos_j1, cartoes_amarelos_j2, cartoes_vermelhos_j1, cartoes_vermelhos_j2 FROM partidas
        """)
        rows = cursor.fetchall()
    
        partidas = []
        for r in rows:
            partidas.append({
                "jogador1": r[0],
                "jogador2": r[1],
                "gols_jogador1": r[2],
                "gols_jogador2": r[3],
                "cartoes_amarelos_j1": r[4],
                "cartoes_amarelos_j2": r[5],
                "cartoes_vermelhos_j1": r[6],
                "cartoes_vermelhos_j2": r[7]
            })

        return partidas

    def atualizar_partida(self, partida_id, dados):
        query = """
        UPDATE partidas SET
        jogador1 = ?,
        jogador2 = ?,
        time1 = ?,
        time2 = ?,
        local = ?,
        rodada = ?,
        gols_jogador1 = ?,
        gols_jogador2 = ?,
        cartoes_amarelos_j1 = ?,
        cartoes_amarelos_j2 = ?,
        cartoes_vermelhos_j1 = ?,
        cartoes_vermelhos_j2 = ?
        WHERE id = ?;
        """
        self.conn.execute(query, (*dados, partida_id))
        self.conn.commit()
