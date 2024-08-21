from dashboard import dash_dash
from modulos.uteis import carregar_env


def ativar_configuracoes():
    carregar_env.carregar_env()


if __name__ == "__main__":
    ativar_configuracoes()
    dash_dash.meu_dashboard()
