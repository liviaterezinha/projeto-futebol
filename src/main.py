import streamlit as st
import pandas as pd
from database import Database
from partida import Partida
from services import gerar_classificacao

dB = Database()

st.title("Campeonato de Fifa 2026")

partidas = dB.buscar_partidas()
classificacao = gerar_classificacao(partidas)
    
st.subheader("Classificação")   
st.dataframe(classificacao, use_container_width=True)

menu = st.selectbox("Menu", 
                    ["Visualizar partidas", "Inserir partida", "Alterar Partida", "Deletar Partida"])

if menu == "Visualizar partidas":
    dados = dB.listar_partidas()
    df = pd.DataFrame(dados, columns=[
        "ID da Partida", 
        "Jogador 1", 
        "Jogador 2", 
        "Time 1", 
        "Time 2", 
        "Local", 
        "Rodada", 
        "Gols Jogador 1", 
        "Gols Jogador 2",
        "Cartões Amarelos Jogador 1",
        "Cartões Amarelos Jogador 2",
        "Cartões Vermelhos Jogador 1",
        "Cartões Vermelhos Jogador 2"
        ])
    st.dataframe(df, use_container_width=True)

elif menu == "Inserir partida":
    j1 = st.text_input("Jogador 1")
    j2 = st.text_input("Jogador 2")
    t1 = st.text_input("Time do Jogador 1")
    t2 = st.text_input("Time do Jogador 2")
    local = st.text_input("Console")
    rodada = st.number_input("Rodada", min_value=1, step=1)
    golsj1 = st.number_input("Gols do Jogador 1", min_value=0, step=1)
    golsj2 = st.number_input("Gols do Jogador 2", min_value=0, step=1)
    ca1 = st.number_input("Cartões Amarelos - Jogador 1", min_value=0, step=1)
    ca2 = st.number_input("Cartões Amarelos - Jogador 2", min_value=0, step=1)
    cv1 = st.number_input("Cartões Vermelhos - Jogador 1", min_value=0, step=1)
    cv2 = st.number_input("Cartões Vermelhos - Jogador 2", min_value=0, step=1)

    if st.button("Salvar"):
        partida = Partida(j1, j2, t1, t2, local, rodada, golsj1, golsj2)
        dB.inserir_partida((
            partida.jogador1, 
            partida.jogador2, 
            partida.time1, 
            partida.time2, 
            partida.local, 
            partida.rodada,
            partida.gols_jogador1,
            partida.gols_jogador2,
            ca1,
            ca2,
            cv1,
            cv2
        ))
        st.success("Partida inserida com sucesso!")
        st.rerun()

elif menu == "Deletar Partida":
    partida_id = st.number_input("ID da Partida a ser deletada", min_value=1, step=1)

    if st.button("Deletar"):
        dB.deletar_partida(partida_id)
        st.success("Partida deletada com sucesso!")
        st.rerun()

elif menu == "Alterar Partida":
    partida_id = st.number_input("ID da partida", min_value=1, step=1)

    if st.button("Carregar dados"):
        dados = dB.listar_partidas()
        partida = next((p for p in dados if p[0] == partida_id), None)

        if partida:
            st.session_state['editar_partida'] = {
            "id": partida_id,
            "j1": partida[1],
            "j2": partida[2],
            "t1": partida[3],
            "t2": partida[4],
            "local": partida[5],
            "rodada": partida[6],
            "g1": partida[7],
            "g2": partida[8],
            "ca1": partida[9],
            "ca2": partida[10],
            "cv1": partida[11],
            "cv2": partida[12]
            }   
            st.rerun()
        else:
            st.warning("Partida não encontrada.")

    if 'editar_partida' in st.session_state:
        ep = st.session_state['editar_partida']

        j1 = st.text_input("Jogador 1", ep["j1"])
        j2 = st.text_input("Jogador 2", ep["j2"])
        t1 = st.text_input("Time 1", ep["t1"])
        t2 = st.text_input("Time 2", ep["t2"])
        local = st.text_input("Local", ep["local"])
        rodada = st.number_input("Rodada", min_value=1, value=ep["rodada"])
        g1 = st.number_input("Gols Jogador 1", min_value=0, value=ep["g1"])
        g2 = st.number_input("Gols Jogador 2", min_value=0, value=ep["g2"])
        ca1 = st.number_input("Cartões Amarelos Jogador 1", min_value=0, value=ep["ca1"])
        ca2 = st.number_input("Cartões Amarelos Jogador 2", min_value=0, value=ep["ca2"])
        cv1 = st.number_input("Cartões Vermelhos Jogador 1", min_value=0, value=ep["cv1"])
        cv2 = st.number_input("Cartões Vermelhos Jogador 2", min_value=0, value=ep["cv2"])

        if st.button("Salvar alterações"):
            dB.atualizar_partida(
                ep["id"],
                (j1, j2, t1, t2, local, rodada, g1, g2, ca1, ca2, cv1, cv2)
                )
            st.success("Partida atualizada!")
            del st.session_state['editar_partida']
            st.rerun()

st.subheader("Gráficos")

opcao = st.radio(
    "Escolha o gráfico que deseja visualizar:",
    [
    "Pontos", 
    "Saldo de Gols", 
    "Gols Marcados", 
    "Gols Sofridos",    
    "Cartões Amarelos",
    "Cartões Vermelhos"
    ]
    )

df_grafico = classificacao.set_index("Jogador")

if opcao == "Pontos":
    st.bar_chart(df_grafico["Pontos"])

elif opcao == "Saldo de Gols":
    st.bar_chart(df_grafico["Saldo de Gols"])

elif opcao == "Gols Marcados":
    st.bar_chart(df_grafico["Gols Marcados"])

elif opcao == "Gols Sofridos":
    st.bar_chart(df_grafico["Gols Sofridos"])

elif opcao == "Cartões Amarelos":
    st.bar_chart(df_grafico["Cartões Amarelos"])

elif opcao == "Cartões Vermelhos":
    st.bar_chart(df_grafico["Cartões Vermelhos"])
