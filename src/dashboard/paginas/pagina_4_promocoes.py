from dash import html, register_page

register_page(
    __name__,
    path="/promocoes",
    name="Promoções",
    title="Promoções",
    description="Página Promoções",
    image_url="/assets/images/imagem_link.jpg",
)


def titulo() -> html.H1:
    conteudo = html.H1("Página Promoções")

    return conteudo


layout = html.Div(
    [
        titulo(),
        html.Div("Conteúdo Página Promoções"),
    ],
    className="pagina",
    id="pagina_4",
)
