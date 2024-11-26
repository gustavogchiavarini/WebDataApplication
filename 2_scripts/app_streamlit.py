import pandas as pd
import streamlit as st
import requests
import matplotlib.pyplot as plt
import seaborn as sns

from sqlalchemy import create_engine 
engine = create_engine('sqlite:///banco.db', echo=True)

dados = pd.read_sql('SELECT * FROM dados', con=engine)
dados['preco2'] = pd.to_numeric(dados['preco2'], errors='coerce')

# df_lido = pd.read_sql('SELECT * FROM dados', con=engine)

# Função para carregar os dados diretamente da API Flask


# Carregar os dados
# dados = carregar_dados()


# Cálculos das estatísticas
media = dados['preco2'].mean()
mediana = dados['preco2'].median()
desvio_padrao = dados['preco2'].std()

# Exibir as estatísticas
st.write(f"### Estatísticas dos Preços:")
st.write(f"- **Média**: {media:.2f}")
st.write(f"- **Mediana**: {mediana:.2f}")
st.write(f"- **Desvio Padrão**: {desvio_padrao:.2f}")

# Gráfico de Histogram
st.write("### Histograma:")
fig, ax = plt.subplots()
sns.histplot(dados['preco2'].dropna(), kde=True, ax=ax)  # Remove NaN antes de plotar
st.pyplot(fig)

# Gráfico de Boxplot
st.write("### Boxplot:")
fig, ax = plt.subplots()
sns.boxplot(x=dados['preco2'], ax=ax)
st.pyplot(fig)

# Gráfico de Barra (utilizando a contagem de preços por intervalos)
st.write("### Gráfico de Barras de Contagem de Intervalos:")
bins = [0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]  # Exemplo de intervalos de preços
dados['intervalo_preco'] = pd.cut(dados['preco2'], bins=bins)
fig, ax = plt.subplots()
dados['intervalo_preco'].value_counts().sort_index().plot(kind='bar', ax=ax)
st.pyplot(fig)

# Gráfico de Pizza (distribuição percentual dos preços)
st.write("Distribuição percentual dos preços:")
fig, ax = plt.subplots()
dados['intervalo_preco'].value_counts().sort_index().plot(kind='pie', ax=ax, autopct='%1.1f%%')
st.pyplot(fig)
