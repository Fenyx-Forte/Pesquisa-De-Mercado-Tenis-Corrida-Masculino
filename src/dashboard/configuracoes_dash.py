from dash import page_container
from dash_bootstrap_components import Col, Container, Row, Stack, icons, themes

from dashboard.componentes import cabecalho, minha_sidebar


def template_html_padrao() -> str:
    template = """
    <!DOCTYPE html>
        <html>
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
                    <script id="_dash-renderer" src="/assets/dash_js/dash_renderer.js"></script>
                </footer>
                <script src="/assets/dash_js/plotly-basic-2.35.2.min.js" async=""></script>
            </body>
        </html>
    """

    return template


def meta_tags_og():
    pass


def meta_tags_twitter():
    pass


def meta_tags_robots():
    pass


def meta_tags_aplicacao():
    pass


def minhas_meta_tags() -> list[dict[str, str]]:
    meta_tags = [
        {
            "charset": "UTF-8",
        },
        {
            "name": "viewport",
            "content": "width=device-width, initial-scale=1.0",
        },
        {
            "http-equiv": "Content-Language",
            "content": "pt-BR",
        },
        {
            "name": "author",
            "content": "Fenyx Forte",
        },
        {
            "name": "application-name",
            "content": "Pesquisa de Mercado: Tênis de Corrida no Mercado Livre",
        },
        {
            "name": "description",
            "content": "Descricao Site",
        },
        {
            "name": "keywords",
            "content": "webscraping, dashboard, dados",
        },
        {
            "property": "og:title",
            "content": "Titulo",
        },
        {
            "property": "og:description",
            "content": "Descricao",
        },
        {
            "property": "og:image",
            "content": "Link imagem",
        },
        {
            "property": "og:url",
            "content": "Link canonical",
        },
        {
            "property": "og:type",
            "content": "website",
        },
        {
            "name": "twitter:card",
            "content": "summary_large_image",
        },
        {
            "name": "twitter:title",
            "content": "Site",
        },
        {
            "name": "twitter:description",
            "content": "descricao",
        },
        {
            "name": "twitter:image",
            "content": "Link imagem",
        },
        {
            "rel": "icon",
            "type": "image/x-icon",
            "href": "link",
        },
        {
            "rel": "canonical",
            "href": "link",
        },
        {
            "name": "google",
            "content": "notranslate",
        },
        {
            "name": "robots",
            "content": "index, follow",
        },
        {
            "name": "googlebot",
            "content": "index, follow",
        },
    ]

    return meta_tags


def configuracoes_app() -> dict:
    configuracoes = {
        "external_stylesheets": [
            themes.LUMEN,
            icons.FONT_AWESOME,
            "/assets/css/styles.css",
        ],
        "external_scripts": [
            "/assets/js/clientside_callbacks.js",
        ],
        "assets_folder": "../assets",
        "assets_url_path": "/assets",
        "use_pages": True,
        "pages_folder": "./dashboard/paginas",
        "include_pages_meta": False,
        "serve_locally": True,
        "compress": False,
        "suppress_callback_exceptions": True,
        "show_undo_redo": False,
        "update_title": "",
        "index_string": template_html_padrao(),
        "meta_tags": minhas_meta_tags(),
    }

    return configuracoes


def layout_app() -> Container:
    layout = Container(
        Row(
            [
                Col(
                    minha_sidebar.sidebar(),
                    width="auto",
                ),
                Col(
                    Stack(
                        [
                            cabecalho.cabecalho(),
                            page_container,
                        ],
                    ),
                    width=True,
                    class_name="conteiner-pagina",
                ),
            ],
        ),
        fluid=True,
        id="meu-conteiner",
    )

    return layout
