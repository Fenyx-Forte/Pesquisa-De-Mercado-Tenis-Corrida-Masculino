from dash import html, register_page

register_page(
    __name__,
    path="/",
    name="Home",
    title="Home",
    description="Página Home",
    image_url="https://analise-de-dados-mercadolivre.onrender.com/assets/images/imagem_link.jpg",
)


def titulo() -> html.H1:
    conteudo = html.H1("Página Home")

    return conteudo


layout = html.Div(
    [
        titulo(),
        html.Div("Conteúdo Página Home"),
        html.Script(type="speculationrules", src="/assets/js/pre_render.js"),
    ],
    className="pagina",
    id="home",
)
