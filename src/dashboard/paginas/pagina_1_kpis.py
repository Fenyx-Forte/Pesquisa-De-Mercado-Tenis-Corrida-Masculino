from dash import html, register_page

register_page(
    __name__,
    path="/kpis",
    name="KPI's",
    title="KPI's",
    description="Página KPI's",
    image_url="/assets/images/imagem_link.jpg",
)


def titulo() -> html.H1:
    conteudo = html.H1("Página KPI's")

    return conteudo


layout = html.Div(
    [
        titulo(),
        html.Div("Conteúdo Página KPI's"),
    ],
    className="pagina",
    id="pagina_1",
)
