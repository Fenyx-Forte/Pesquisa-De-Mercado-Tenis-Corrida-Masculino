from dash import html, register_page

register_page(
    __name__,
    path="/kpis",
    name="KPI's",
    title="KPI's",
    description="Página KPI's",
    image="imagem_link.jpg",
)


layout = html.Div(
    [
        html.H1("Página KPI's"),
        html.Div("Conteúdo Página KPI's"),
    ],
    className="pagina",
)
