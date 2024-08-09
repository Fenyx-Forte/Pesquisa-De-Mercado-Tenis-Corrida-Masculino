import pandas as pd
import streamlit as st
from modulos.uteis import ler_sql


@st.cache_data
def retorna_dataframe(caminho_query) -> pd.DataFrame:
    return ler_sql.ler_query(caminho_query)


def cabecalho() -> None:
    st.set_page_config(page_title="Análise de Dados - Mercado Livre")
    st.title("Pesquisa de Mercado: Tênis de Corrida no Mercado Livre")

    df = retorna_dataframe("../sql/queries/data_coleta_dados.sql")

    data_coleta = df.squeeze()

    st.write(f"Data Coleta: {data_coleta}")


def kpi_principais_sistema() -> None:
    st.subheader("KPIs principais do sistema")

    col1, col2, col3 = st.columns(3)

    df_1 = retorna_dataframe("../sql/queries/kpi_1_num_total_itens.sql")
    total_itens = df_1.squeeze()
    col1.metric(label="Número Total de Itens", value=total_itens)

    df_2 = retorna_dataframe("../sql/queries/kpi_2_num_marcas_unicas.sql")
    num_marcas_unicas = df_2.squeeze()
    col2.metric(label="Número de Marcas Únicas", value=num_marcas_unicas)

    df_3 = retorna_dataframe("../sql/queries/kpi_3_preco_atual_medio.sql")
    preco_atual_medio = df_3.squeeze()
    col3.metric(
        label="Preço Médio Atual (R$)", value=f"{preco_atual_medio:.2f}"
    )


def marcas_mais_encontradas_ate_a_10_pagina() -> None:
    st.subheader("Top 10 marcas mais encontradas até a 10ª página")
    col1, col2 = st.columns([3, 3])

    df = retorna_dataframe("../sql/queries/marcas_mais_encontradas.sql")

    col1.bar_chart(
        df,
        x="Marca",
        y="Qtd Produtos",
    )
    col2.dataframe(df, hide_index=True)


def preco_medio_por_marca() -> None:
    st.subheader("Preço médio por marca")
    col1, col2 = st.columns([3, 3])

    df = retorna_dataframe("../sql/queries/preco_medio_por_marca.sql")

    col1.bar_chart(
        df.style.format("{:.2f}", ["Preço Médio"]), x="Marca", y="Preço Médio"
    )
    col2.dataframe(df.style.format("{:.2f}", ["Preço Médio"]), hide_index=True)


def satisfacao_media_por_marca() -> None:
    st.subheader("Satisfação Média por marca")
    st.write("OBS: Apenas produtos com 20 ou mais avaliações")

    df = retorna_dataframe("../sql/queries/satisfacao_media_por_marca.sql")

    st.dataframe(
        df.style.format("{:.2f}", ["Satisfação Média"]), hide_index=True
    )


def dashboard() -> None:
    cabecalho()

    kpi_principais_sistema()

    marcas_mais_encontradas_ate_a_10_pagina()

    preco_medio_por_marca()

    satisfacao_media_por_marca()
