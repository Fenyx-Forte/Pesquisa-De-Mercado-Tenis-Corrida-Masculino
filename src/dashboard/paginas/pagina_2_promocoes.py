from dash import html, register_page

register_page(
    __name__,
    path="/promocoes",
    name="Promoções",
    title="Promoções",
    description="Página Promoções",
    image="images/imagem_link.jpg",
)


layout = html.Div(
    [
        html.H1("Página Promoções"),
        html.Div("Conteúdo Página Promoções"),
    ],
    className="pagina",
)
