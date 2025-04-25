import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from sqlalchemy import create_engine

# ============ CONFIGURAÇÕES DO BANCO ============

DB_USER = st.secrets["DB_USER"]
DB_PASSWORD = st.secrets["DB_PASSWORD"]
DB_HOST = st.secrets["DB_HOST"]
DB_PORT = st.secrets["DB_PORT"]
DB_NAME = st.secrets["DB_NAME"]
TABLE_NAME = "virtual_gate"


# ============ CONEXÃO COM POSTGRESQL ============
@st.cache_data
def carregar_dados():
    engine = create_engine(
        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
        connect_args={'client_encoding': 'utf8'}
    )
    query = f"""
        SELECT 
            EXTRACT(MONTH FROM emissao) AS mes,
            EXTRACT(YEAR FROM emissao) AS ano,
            SUM(fluxo) AS total_fluxo
        FROM {TABLE_NAME}
        WHERE loja = '1'
        GROUP BY ano, mes
        ORDER BY ano DESC, mes DESC
    """
    df = pd.read_sql(query, engine)
    df["mes"] = df["mes"].astype(int)
    df["ano"] = df["ano"].astype(int)
    return df

# ============ DASHBOARD STREAMLIT ============
st.title("📊 Dashboard de Fluxo - Loja 11")

# Carregar dados
df = carregar_dados()

# Converter mês para nome
nomes_meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
               'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
df["mes_nome"] = df["mes"].apply(lambda x: nomes_meses[x-1])

# Separar anos disponíveis
anos = sorted(df["ano"].unique(), reverse=True)
if len(anos) < 2:
    st.error("São necessários pelo menos dois anos de dados para comparação.")
else:
    ano_atual, ano_anterior = anos[0], anos[1]
    df_atual = df[df["ano"] == ano_atual]
    df_anterior = df[df["ano"] == ano_anterior]

    # Garantir ordem dos meses
    df_atual = df_atual.sort_values("mes", ascending=False)
    df_anterior = df_anterior.sort_values("mes", ascending=False)

    # Gráfico
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_atual["mes_nome"],
        y=df_atual["total_fluxo"],
        name=f"{ano_atual}",
        marker_color='#F1B19D',
        text=[f'{int(v):,} pessoas' for v in df_atual["total_fluxo"]],
        textposition='inside',
        hoverinfo='x+y'
    ))
    fig.add_trace(go.Bar(
        x=df_anterior["mes_nome"],
        y=df_anterior["total_fluxo"],
        name=f"{ano_anterior}",
        marker_color='#E9633A',
        text=[f'{int(v):,} pessoas' for v in df_anterior["total_fluxo"]],
        textposition='inside',
        hoverinfo='x+y'
    ))
    fig.update_layout(
        title='Comparativo de Fluxo Mês a Mês - Loja 11',
        xaxis_title='Meses',
        yaxis_title='Quantidade de Pessoas',
        yaxis_tickformat=',d',
        barmode='group',
        template='plotly_white'
    )

    st.plotly_chart(fig, use_container_width=True)

    # Indicadores
    col1, col2 = st.columns(2)
    col1.metric(f"🟠 Total {ano_atual}", f"{int(df_atual['total_fluxo'].sum()):,} pessoas")
    col2.metric(f"🟠 Total {ano_anterior}", f"{int(df_anterior['total_fluxo'].sum()):,} pessoas")
