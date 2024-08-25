from dash import html, register_page

register_page(
    __name__,
    path="/",
    name="Home",
    title="Home",
    description="Página Home",
    image="imagem_link.jpg",
)


layout = html.Div(
    [
        html.H1("Página Home"),
        html.Div("Conteúdo Página Home"),
    ],
    className="pagina",
)
