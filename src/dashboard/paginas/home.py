import dash
import dash_bootstrap_components as dbc
import duckdb
import plotly.express as px
import polars as pl
from dash import Input, Output, callback, dash_table, dcc, html
from modulos.uteis import ler_sql, minhas_queries

dash.register_page(__name__, path="/", name="Home", title="Home")


def layout(**kwargs) -> html.Div:
    conteudo = cabecalho()
    return conteudo


def cabecalho():
    content_style = {
        "marginLeft": "16rem",
        "marginRight": "2rem",
        "padding": "2rem 1rem",
    }

    titulo_1 = html.Div(
        children="Pesquisa de Mercado: Tênis de Corrida no Mercado Livre",
        className="text-primary text-center fs-3",
    )

    data_coleta_html = html.Div(
        children="", className="text-center", id="data_coleta"
    )

    linha = dbc.Row([titulo_1, data_coleta_html], style=content_style)

    return linha


# @callback(
#    Output(component_id="data_coleta", component_property="children"),
#    Input(component_id="store", component_property="data"),
# )
def data_coleta(json_dict):
    query = minhas_queries.data_coleta_mais_recente()

    df_data_coleta = ler_sql.query_pl_para_pl(query, json_dict)

    data_coleta = df_data_coleta.item(0, 0)

    horario_coleta = df_data_coleta.item(0, 1)

    data_e_hora = f"Data Coleta: {data_coleta} - {horario_coleta}"

    return data_e_hora


def testando_coisas(df: pl.DataFrame):
    df_filtrado = df.select(
        pl.col("marca"),
        pl.col("preco_atual"),
        pl.col("preco_velho"),
    ).filter(pl.col("marca").is_in(["OLYMPIKUS", "MIZUNO", "ADIDAS", "FILA"]))

    titulo = html.H3(
        children="Aprendendo",
        className="text-center fs-3",
    )

    opcoes = dbc.RadioItems(
        options=[
            {"label": x, "value": x} for x in ["preco_atual", "preco_velho"]
        ],
        value="preco_atual",
        inline=True,
        id="radio-buttons-final",
    )

    tabela = dash_table.DataTable(
        data=df_filtrado.to_dicts(),
        page_size=12,
        style_table={"overflowX": "auto"},
        id="minha_tabela",
    )

    grafico = dcc.Graph(figure={}, id="my-first-graph-final")

    coluna_1 = dbc.Col([tabela], width=6)

    coluna_2 = dbc.Col([grafico], width=6)

    linha_0 = dbc.Row([html.Hr()])

    linha_1 = dbc.Row([titulo])

    linha_2 = dbc.Row([opcoes])

    linha_3 = dbc.Row([coluna_1, coluna_2])

    container = dbc.Container([linha_0, linha_1, linha_2, linha_3])

    return container


# Add controls to build the interaction
"""
@callback(
    Output(component_id="my-first-graph-final", component_property="figure"),
    Input(component_id="radio-buttons-final", component_property="value"),
    Input(component_id="minha_tabela", component_property="data"),
)
"""


def update_graph(col_chosen, df_dicts):
    df = pl.DataFrame(df_dicts)

    fig = px.histogram(df, x="marca", y=col_chosen, histfunc="avg")
    return fig
