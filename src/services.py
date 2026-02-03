import pandas as pd

def gerar_classificacao(partidas):
    dados = {}

    for p in partidas:
        j1, j2 = p["jogador1"], p["jogador2"]
        g1, g2 = p["gols_jogador1"], p["gols_jogador2"]

        ca1, ca2 = p["cartoes_amarelos_j1"], p["cartoes_amarelos_j2"] 
        cv1, cv2 = p["cartoes_vermelhos_j1"], p["cartoes_vermelhos_j2"]

        for j in [j1, j2]:
            if j not in dados:
                dados[j] = {
                    "Jogador": j,
                    "Pontos": 0,
                    "Gols Marcados": 0,
                    "Gols Sofridos": 0, 
                    "Cartões Amarelos": 0,
                    "Cartões Vermelhos": 0
                }

        dados[j1]["Gols Marcados"] += g1
        dados[j1]["Gols Sofridos"] += g2
        dados[j1]["Cartões Amarelos"] += ca1
        dados[j1]["Cartões Vermelhos"] += cv1    
           
        dados[j2]["Gols Marcados"] += g2
        dados[j2]["Gols Sofridos"] += g1
        dados[j2]["Cartões Amarelos"] += ca2
        dados[j2]["Cartões Vermelhos"] += cv2

        if g1 > g2:
            dados[j1]["Pontos"] += 3
        elif g2 > g1:
            dados[j2]["Pontos"] += 3
        else:
            dados[j1]["Pontos"] += 1
            dados[j2]["Pontos"] += 1

        if not dados:
            return pd.DataFrame(columns=[
        "Jogador",
        "Pontos",
        "Gols Marcados",
        "Gols Sofridos",
        "Saldo de Gols",
        "Cartões Amarelos",
        "Cartões Vermelhos"
    ])

        df = pd.DataFrame(dados.values())

        df["Saldo de Gols"] = df["Gols Marcados"] - df["Gols Sofridos"]

        df = df.sort_values(
            by=[
            "Pontos", 
            "Saldo de Gols", 
            "Gols Marcados", 
            "Gols Sofridos", 
            "Cartões Amarelos",
            "Cartões Vermelhos"
            ], ascending=[False, False, False, True, True, True]
    )
        
        df = df.reset_index(drop=True)

        df["Colocação"] = df.index + 1
        df.insert(0, "Posição", df.index + 1)
        
    return df
