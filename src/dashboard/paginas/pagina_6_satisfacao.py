from dash import html, register_page

register_page(
    __name__,
    path="/satisfacao",
    name="Satisfação",
    title="Satisfação",
    description="Página Satisfação",
    image_url="/assets/images/imagem_link.jpg",
)


def titulo() -> html.H1:
    conteudo = html.H1("Página Satisfação")

    return conteudo


layout = html.Div(
    [
        titulo(),
        html.Div("Conteúdo Página Satisfação"),
    ],
    className="pagina",
    id="pagina_6",
)
