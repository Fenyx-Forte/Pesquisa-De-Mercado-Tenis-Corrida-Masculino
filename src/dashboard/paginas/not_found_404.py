from dash import html, register_page

register_page(
    __name__,
    name="Not Found 404",
    title="Not Found 404",
    description="Not Found 404",
)


def titulo() -> html.H1:
    conteudo = html.H1("Page not found! Error 404", className="pagina")

    return conteudo


layout = titulo()
