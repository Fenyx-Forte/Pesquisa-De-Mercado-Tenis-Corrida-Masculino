from dash import page_container
from dash_bootstrap_components import Col, Container, Row, Stack, icons, themes

from dashboard.componentes import cabecalho, minha_sidebar


def template_html_padrao() -> str:
    template = """
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

    return template


def template_html_teste() -> str:
    template = """
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

    return template


def meta_tags_basicas() -> list[dict[str, str]]:
    meta_tags = [
        {
            "charset": "UTF-8",
        },
        {
            "name": "viewport",
            "content": "width=device-width, initial-scale=1.0",
        },
        {
            "rel": "canonical",
            "href": "https://analise-de-dados-mercadolivre.onrender.com/",
        },
        {
            "name": "google",
            "content": "notranslate",
        },
    ]

    return meta_tags


def meta_tags_og() -> list[dict[str, str]]:
    meta_tags = [
        {
            "property": "og:title",
            "content": "Pesquisa de Mercado: Tênis de Corrida no Mercado Livre",
        },
        {
            "property": "og:description",
            "content": "Descricao Site",
        },
        {
            "property": "og:image",
            "content": "https://analise-de-dados-mercadolivre.onrender.com/assets/images/imagem_link.jpg",
        },
        {
            "property": "og:url",
            "content": "https://analise-de-dados-mercadolivre.onrender.com/",
        },
        {
            "property": "og:type",
            "content": "website",
        },
    ]

    return meta_tags


def meta_tags_twitter() -> list[dict[str, str]]:
    meta_tags = [
        {
            "name": "twitter:card",
            "content": "summary_large_image",
        },
        {
            "name": "twitter:title",
            "content": "Pesquisa de Mercado: Tênis de Corrida no Mercado Livre",
        },
        {
            "name": "twitter:description",
            "content": "Descricao Site",
        },
        {
            "name": "twitter:image",
            "content": "https://analise-de-dados-mercadolivre.onrender.com/assets/images/imagem_link.jpg",
        },
    ]

    return meta_tags


def meta_tags_aplicacao() -> list[dict[str, str]]:
    meta_tags = [
        {
            "name": "author",
            "content": "Fenyx Forte",
        },
        {
            "name": "application-name",
            "content": "Pesquisa de Mercado: Tênis de Corrida no Mercado Livre",
        },
        {
            "name": "keywords",
            "content": "webscraping, dashboard, dados",
        },
    ]

    return meta_tags


def minhas_meta_tags() -> list[dict[str, str]]:
    meta_tags = [
        {
            "property": "og:locale",
            "content": "pt_BR",
        },
        {
            "property": "og:site_name",
            "content": "Pesquisa de Mercado: Tênis de Corrida no Mercado Livre",
        },
        *meta_tags_basicas(),
        *meta_tags_aplicacao(),
        # *meta_tags_og(),
        # *meta_tags_twitter(),
    ]

    return meta_tags


def configuracoes_app() -> dict:
    configuracoes = {
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

    return configuracoes


def configuracoes_app_teste() -> dict:
    configuracoes = {
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

    return configuracoes


def layout_app() -> Container:
    layout = Container(
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

    return layout
