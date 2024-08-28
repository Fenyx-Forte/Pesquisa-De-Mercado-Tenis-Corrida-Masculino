from dash import Dash

from dashboard import configuracoes_dash
from dashboard.uteis import processamento_dados


def aplicacao():
    processamento_dados.inicializacao()

    app = Dash(__name__, **configuracoes_dash.configuracoes_app())

    app.layout = configuracoes_dash.layout_app()

    server = app.server

    return server


def desenvolvimento():
    processamento_dados.inicializacao()

    app = Dash(__name__, **configuracoes_dash.configuracoes_app())

    app.layout = configuracoes_dash.layout_app()

    app.run(debug=True, dev_tools_hot_reload=False)


if __name__ == "__main__":
    desenvolvimento()
