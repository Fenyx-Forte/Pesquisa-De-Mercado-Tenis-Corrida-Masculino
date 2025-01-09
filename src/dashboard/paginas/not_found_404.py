"""Página Erro 404."""

from dash import html, register_page

register_page(
    __name__,
    name="Not Found 404",
    title="Not Found 404",
    description="Not Found 404",
)


def titulo() -> html.H1:
    """Conteúdo da página.

    Returns:
        H1: Conteúdo.
    """
    return html.H1("Essa página não existe!", className="pagina")


layout = titulo()
