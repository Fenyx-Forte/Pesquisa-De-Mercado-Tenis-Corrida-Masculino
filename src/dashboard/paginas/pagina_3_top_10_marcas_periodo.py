from dash import html, register_page

register_page(
    __name__,
    path="/top-10-marcas-periodo",
    name="Top 10 Marcas Período",
    title="Top 10 Marcas Período",
    description="Top 10 Marcas Período",
    image_url="/assets/images/imagem_link.jpg",
)


def titulo() -> html.H1:
    conteudo = html.H1("Top 10 Marcas Período")

    return conteudo


layout = html.Div(
    [
        titulo(),
        html.Div("Conteúdo Página Top 10 Marcas Período"),
    ],
    className="pagina",
)
