"""Configurações para o dashboard."""

from dash import page_container
from dash_bootstrap_components import Col, Container, Row, icons, themes

from dashboard.componentes import cabecalho, minha_sidebar


def template_html_padrao() -> str:
    """Gera um template HTML comum para todas as páginas da aplicação.

    Returns:
        str: String contendo o HTML padrão de todas as páginas.
    """
    return """
    <!DOCTYPE html>
        <html lang="pt-BR">
            <head>
                {%metas%}
                <link rel="icon" type="image/x-icon" href="/assets/favicon.ico">
                <title>{%title%}</title>
                {%css%}
            </head>
            <body>
                {%app_entry%}
                <footer>
                    {%config%}
                    {%scripts%}
                    <script id="_dash-renderer" src="/assets/dash_js/dash_renderer.1.0.0.js"></script>
                </footer>
                <script src="/assets/dash_js/plotly-basic-2.35.2.min.js" async=""></script>
            </body>
        </html>
    """


def template_html_teste() -> str:
    """Gera um template HTML comum para todas as páginas da aplicação.

    ### NOTA ###
    Só deve ser usado em ambiente de dev.

    Returns:
        str: String contendo o HTML padrão de todas as páginas.
    """
    return """
    <!DOCTYPE html>
        <html lang="pt-BR">
            <head>
                {%metas%}
                <link rel="icon" type="image/x-icon" href="../assets/favicon.ico">
                <title>{%title%}</title>
                {%css%}
            </head>
            <body>
                {%app_entry%}
                <footer>
                    {%config%}
                    {%scripts%}
                    {%renderer%}
                </footer>
            </body>
        </html>
    """


def meta_tags_basicas() -> list[dict[str, str]]:
    """Gera uma lista de dicionários contendo as metatags básicas para a página.

    Returns:
        list[dict[str, str]]: Lista com dicionários que representam as metatags básicas.
    """
    return [
        {
            "charset": "UTF-8",
        },
        {
            "name": "viewport",
            "content": "width=device-width, initial-scale=1.0",
        },
        {
            "rel": "canonical",
            "href": "https://analise-de-dados-tenis-corrida.onrender.com/",
        },
        {
            "name": "google",
            "content": "notranslate",
        },
    ]


def meta_tags_og() -> list[dict[str, str]]:
    """Gera uma lista de dicionários contendo as meta tags Open Graph para a página.

    Returns:
        list[dict[str, str]]: Lista com dicionários que representam as meta tags Open Graph.
    """
    return [
        {
            "property": "og:title",
            "content": "Pesquisa de Mercado: Tênis de Corrida Masculino",
        },
        {
            "property": "og:description",
            "content": "Descricao Site",
        },
        {
            "property": "og:image",
            "content": "https://analise-de-dados-tenis-corrida.onrender.com/assets/images/imagem_link.jpg",
        },
        {
            "property": "og:url",
            "content": "https://analise-de-dados-tenis-corrida.onrender.com/",
        },
        {
            "property": "og:type",
            "content": "website",
        },
    ]


def meta_tags_twitter() -> list[dict[str, str]]:
    """Gera uma lista de dicionários contendo as meta tags Twitter para a página.

    Returns:
        list[dict[str, str]]: Lista com dicionários que representam as meta tags Twitter.
    """
    return [
        {
            "name": "twitter:card",
            "content": "summary_large_image",
        },
        {
            "name": "twitter:title",
            "content": "Pesquisa de Mercado: Tênis de Corrida Masculino",
        },
        {
            "name": "twitter:description",
            "content": "Descricao Site",
        },
        {
            "name": "twitter:image",
            "content": "https://analise-de-dados-tenis-corrida.onrender.com/assets/images/imagem_link.jpg",
        },
    ]


def meta_tags_aplicacao() -> list[dict[str, str]]:
    """Gera uma lista de dicionários contendo as meta tags do aplicativo.

    Returns:
        list[dict[str, str]]: Lista com dicionários que representam as meta tags do aplicativo.
    """
    return [
        {
            "name": "author",
            "content": "Fenyx Forte",
        },
        {
            "name": "application-name",
            "content": "Pesquisa de Mercado: Tênis de Corrida Masculino",
        },
        {
            "name": "keywords",
            "content": "webscraping, dashboard, dados",
        },
    ]


def minhas_meta_tags() -> list[dict[str, str]]:
    """Gera uma lista de dicionários contendo todas as meta tags do dashboard.

    Returns:
        list[dict[str, str]]: Lista com dicionários que representam as meta tags do dashboard.
    """
    return [
        {
            "property": "og:locale",
            "content": "pt_BR",
        },
        {
            "property": "og:site_name",
            "content": "Pesquisa de Mercado: Tênis de Corrida Masculino",
        },
        *meta_tags_basicas(),
        *meta_tags_aplicacao(),
    ]


def configuracoes_app() -> (
    dict[str, str | list[str] | bool | list[dict[str, str]]]
):
    """Gera um dicionário contendo as configurações do aplicativo.

    Returns:
        dict[str, str | list[str] | bool | list[dict[str, str]]]: Dicionário com configurações do aplicativo.
    """
    return {
        "external_stylesheets": [
            themes.LUMEN,
            icons.FONT_AWESOME,
            "/assets/css/styles.1.0.5.css",
        ],
        "external_scripts": [
            "/assets/js/clientside_callbacks.1.0.1.js",
        ],
        "assets_folder": "../assets",
        "assets_url_path": "/assets",
        "use_pages": True,
        "pages_folder": "./dashboard/paginas",
        "include_pages_meta": True,
        "serve_locally": True,
        "compress": False,
        "suppress_callback_exceptions": True,
        "show_undo_redo": False,
        "update_title": "",
        "index_string": template_html_padrao(),
        "meta_tags": minhas_meta_tags(),
    }


def configuracoes_app_teste() -> (
    dict[str, str | list[str] | bool | list[dict[str, str]]]
):
    """Gera um dicionário contendo as configurações do aplicativo.

    ### NOTA ###
    Configurações a serem usadas em ambiente DEV.

    Returns:
        dict[str, str | list[str] | bool | list[dict[str, str]]]: Dicionário com configurações do aplicativo.
    """
    return {
        "external_stylesheets": [
            themes.LUMEN,
            icons.FONT_AWESOME,
        ],
        "assets_folder": "../assets",
        "assets_url_path": "/assets",
        "use_pages": True,
        "pages_folder": "./dashboard/paginas",
        "include_pages_meta": True,
        "serve_locally": True,
        "compress": False,
        "suppress_callback_exceptions": True,
        "show_undo_redo": False,
        "update_title": "",
        "meta_tags": minhas_meta_tags(),
    }


def layout_app() -> Container:
    """Gera uma estrutura de layout para o aplicativo.

    Returns:
        Container: Elemento Container que define a estrutura do aplicativo.
    """
    return Container(
        [
            Row(
                Col(
                    cabecalho.cabecalho(),
                    width=True,
                    class_name="conteiner-cabecalho",
                ),
                class_name="g-0",
            ),
            Row(
                [
                    Col(
                        minha_sidebar.sidebar(),
                        xs="auto",
                        sm="auto",
                        id="coluna-sidebar",
                        class_name="coluna-sidebar-desativada",
                    ),
                    Col(
                        page_container,
                        xs=12,
                        sm=True,
                        class_name="conteiner-pagina",
                    ),
                ],
                class_name="g-0 linha-conteiner-pagina",
            ),
        ],
        fluid=True,
        id="conteiner-geral",
    )
