from dash import Dash, _dash_renderer

from dashboard import configuracoes_dash
from dashboard.processamento import gerenciador

_dash_renderer._set_react_version("18.2.0")


def aplicacao():
    gerenciador.inicializar_escopo_global()

    app = Dash(__name__, **configuracoes_dash.configuracoes_app())

    app.layout = configuracoes_dash.layout_app()

    server = app.server

    return server


def desenvolvimento():
    gerenciador.inicializar_escopo_global()

    app = Dash(__name__, **configuracoes_dash.configuracoes_app())

    app.layout = configuracoes_dash.layout_app()

    app.run(debug=True, dev_tools_hot_reload=False)


if __name__ == "__main__":
    desenvolvimento()
