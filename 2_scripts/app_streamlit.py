
# import streamlit as st
# import pandas as pd
# import requests
# import plotly.express as px
# import sqlite3
# from sqlalchemy import create_engine 

# # Configuração da aplicação
# st.set_page_config(page_title="Análise Interativa", layout="wide")

# # Função para carregar dados da API Flask
# @st.cache_data
# def carregar_dados(api_url):
#     response = requests.get(api_url)
#     if response.status_code == 200:
#         return pd.DataFrame(response.json())
#     else:
#         st.error("Erro ao carregar os dados da API.")
#         return pd.DataFrame()

# # URL da API Flask
# api_url = "http://127.0.0.1:5000/dados"

# # Carregar os dados
# dados = carregar_dados(api_url)

# if dados.empty:
#     st.stop()

# # Interface do Streamlit
# st.title("Análise Interativa de Dados")
# st.sidebar.header("Configurações")

# variavel = st.sidebar.selectbox("Selecione a variável para análise:", dados.columns)
# tipo_analise = st.sidebar.radio("Tipo de Análise:", ["Univariada", "Multivariada"])

# # Exibição de estatísticas
# if variavel:
#     media = dados[variavel].mean().round(2)
#     mediana = dados[variavel].median().round(2)
#     desvio = dados[variavel].std().round(2)

#     st.write(f"**Média:** {media}")
#     st.write(f"**Mediana:** {mediana}")
#     st.write(f"**Desvio Padrão:** {desvio}")

# # Análise Univariada
# if tipo_analise == "Univariada":
#     st.subheader(f"Análise Univariada - {variavel}")
#     col1, col2 = st.columns(2)

#     with col1:
#         st.write("**Histograma**")
#         fig = px.histogram(dados, x=variavel)
#         st.plotly_chart(fig, use_container_width=True)

#         st.write("**Boxplot**")
#         fig = px.box(dados, y=variavel)
#         st.plotly_chart(fig, use_container_width=True)

#     with col2:
#         st.write("**Gráfico de Barras**")
#         fig = px.bar(dados, x=variavel)
#         st.plotly_chart(fig, use_container_width=True)

# # Análise Multivariada
# elif tipo_analise == "Multivariada":
#     variavel_color = st.sidebar.selectbox("Selecione a variável de cor:", dados.columns)
#     st.subheader(f"Análise Multivariada: {variavel} vs {variavel_color}")

#     fig = px.scatter(dados, x=variavel, y=variavel_color, color=variavel_color)
#     st.plotly_chart(fig, use_container_width=True)



import pandas as pd
import streamlit as st
import requests
import matplotlib.pyplot as plt
import seaborn as sns

# Função para carregar os dados diretamente da API Flask
@st.cache
def carregar_dados():
    url = 'http://127.0.0.1:5000/dados'  # URL da API Flask
    response = requests.get(url)
    dados = response.json()
    df = pd.DataFrame(dados)
    
    # Converte a coluna 'preco2' para valores numéricos, forçando valores não numéricos a se tornarem NaN
    df['preco2'] = pd.to_numeric(df['preco2'], errors='coerce')
    
    return df

# Carregar os dados
dados = carregar_dados()

# Certifique-se de que 'preco2' é uma coluna numérica antes de calcular as estatísticas
if dados['preco2'].isnull().any():
    st.write("Existem valores ausentes na coluna 'preco2' que foram convertidos para NaN.")

# Cálculos das estatísticas
media = dados['preco2'].mean()
mediana = dados['preco2'].median()
desvio_padrao = dados['preco2'].std()

# Exibir as estatísticas
st.write(f"### Estatísticas da Coluna 'preco2'")
st.write(f"- **Média**: {media:.2f}")
st.write(f"- **Mediana**: {mediana:.2f}")
st.write(f"- **Desvio Padrão**: {desvio_padrao:.2f}")

# Gráfico de Histogram
st.write("### Histograma de 'preco2'")
fig, ax = plt.subplots()
sns.histplot(dados['preco2'].dropna(), kde=True, ax=ax)  # Remove NaN antes de plotar
st.pyplot(fig)

# Gráfico de Boxplot
st.write("### Boxplot de 'preco2'")
fig, ax = plt.subplots()
sns.boxplot(x=dados['preco2'], ax=ax)
st.pyplot(fig)

# Gráfico de Barra (utilizando a contagem de preços por intervalos)
st.write("### Gráfico de Barras de Contagem de Intervalos de 'preco2'")
bins = [0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]  # Exemplo de intervalos de preços
dados['intervalo_preco'] = pd.cut(dados['preco2'], bins=bins)
fig, ax = plt.subplots()
dados['intervalo_preco'].value_counts().sort_index().plot(kind='bar', ax=ax)
st.pyplot(fig)

# Gráfico de Pizza (distribuição percentual dos preços)
st.write("### Gráfico de Pizza de 'preco2'")
fig, ax = plt.subplots()
dados['intervalo_preco'].value_counts().sort_index().plot(kind='pie', ax=ax, autopct='%1.1f%%')
st.pyplot(fig)
