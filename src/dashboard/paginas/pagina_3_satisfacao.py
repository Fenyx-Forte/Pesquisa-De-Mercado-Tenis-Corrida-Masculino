from dash import html, register_page

register_page(
    __name__,
    path="/satisfacao",
    name="Satisfação",
    title="Satisfação",
    description="Página Satisfação",
    image_url="/assets/images/imagem_link.jpg",
)


layout = html.Div(
    [
        html.H1("Página Satisfação"),
        html.Div("Conteúdo Página Satisfação"),
    ],
    className="pagina",
)
