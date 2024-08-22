import dash
import dash_bootstrap_components as dbc
from dash import Dash, dcc
from dashboard import cabecalho, minha_sidebar
from modulos.uteis import carregar_env, ler_sql, minhas_queries


def dashboard():
    carregar_env.carregar_env()

    query = minhas_queries.dados_mais_recentes_do_banco_de_dados()

    df = ler_sql.query_banco_de_dados_apenas_leitura(query)

    # Pre-computacao de dados a serem armazenados na store
    query_data_coleta = minhas_queries.data_coleta_mais_recente()
    df_data_coleta = ler_sql.query_pl_para_pl(query_data_coleta, df)

    data_coleta = df_data_coleta.item(0, 0)
    horario_coleta = df_data_coleta.item(0, 1)

    data_e_horario = f"{data_coleta} - {horario_coleta}"

    store = {
        "data_e_horario": data_e_horario,
        "df": df.to_dicts(),
        "colunas": [{"name": i, "id": i} for i in df.columns],
    }

    external_stylesheets = [dbc.themes.LUMEN]
    app = Dash(
        __name__,
        external_stylesheets=external_stylesheets,
        update_title=None,
        assets_folder="../assets/",
        use_pages=True,
        pages_folder="./dashboard/paginas",
        # suppress_callback_exceptions = True,
        # prevent_initial_callbacks = True
    )

    app.layout = dbc.Container(
        [
            dcc.Store(id="store", data=store),
            dcc.Location(id="url"),
            dbc.Row(
                [
                    dbc.Col(minha_sidebar.sidebar(), width="auto"),
                    dbc.Col(
                        dbc.Stack(
                            [
                                cabecalho.cabecalho(),
                                dash.page_container,
                            ],
                        ),
                    ),
                ],
            ),
        ],
        fluid=True,
    )

    app.run(debug=True, dev_tools_hot_reload=False)


if __name__ == "__main__":
    dashboard()
