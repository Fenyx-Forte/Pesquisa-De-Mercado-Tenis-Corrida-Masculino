from dash import Dash, Input, Output, callback, page_container
from dash.dcc import Location
from dash_bootstrap_components import Col, Container, Row, Stack, icons, themes
from dashboard import cabecalho, minha_sidebar, processamento_dados
from modulos.uteis import carregar_env

# Inicializacao dados
## Carregando env
carregar_env.carregar_env()
"""
## Query banco de dados
df = processamento_dados.dados_mais_recentes()

## Processamento
### Cabecalho
data_coleta = processamento_dados.data_coleta(df)


### Pagina 2
pagina_2_dag_dados = processamento_dados.inicializacao_pagina_2(df)

pagina_2_dag_colunas = [
    {
        "headerName": "Marca",
        "field": "marca",
        "headerTooltip": "Marca do tênis",
    },
    {
        "headerName": "Preço",
        "field": "preco_atual",
        "headerTooltip": "Preço do tênis",
    },
]


# Callbacks
## Inicializacao
### Pagina 2
@callback(
    Output("meu-dag", "rowData"),
    Output("meu-dag", "columnDefs"),
    Input("input-estatico", "children"),
)
def inicializacao_pagina_2(_):
    return [
        pagina_2_dag_dados,
        pagina_2_dag_colunas,
    ]


## Pagina 2
@callback(
    Output("meu-dag", "exportDataAsCsv"),
    Input("csv-button", "n_clicks"),
    prevent_initial_call=True,
)
def exportar_csv(n_clicks):
    if n_clicks:
        return True
    return False
"""

# Dashboard
app = Dash(
    __name__,
    external_stylesheets=[themes.LUMEN, icons.FONT_AWESOME],
    update_title=None,
    assets_folder="../assets/",
    use_pages=True,
    pages_folder="./dashboard/paginas",
    # suppress_callback_exceptions=True,
    # prevent_initial_callbacks = True
)
data_coleta = ".."
app.layout = Container(
    [
        Location(id="url"),
        Row(
            [
                Col(minha_sidebar.sidebar(), width="auto"),
                Col(
                    Stack(
                        [
                            cabecalho.cabecalho(data_coleta),
                            page_container,
                        ],
                    ),
                ),
            ],
        ),
    ],
    fluid=True,
)

app.run(debug=True, dev_tools_hot_reload=False)
