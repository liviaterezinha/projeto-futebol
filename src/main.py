import streamlit as st
import pandas as pd

st.title("Meu primeiro projeto com Streamlit")

st.write("Exemplo de tabela:")

df = pd.DataFrame ({
    "Nome": ["Philipe", "Vinícius", "Willian"],
    "Idade": [25, 26, 28]
})

st.table(df)

st.write("Exemplo de gráfico")
st.bar_chart(df["Idade"])