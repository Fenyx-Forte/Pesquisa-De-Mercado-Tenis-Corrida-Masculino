import dash
from dash import Input, Output, callback, html
from dash.dash_table import DataTable, FormatTemplate

dash.register_page(
    __name__, path="/pagina-1", name="Pagina 1", title="Pagina 1"
)


def layout(**kwargs) -> html.Div:
    conteudo = html.Div(
        [
            html.H1("This is our Analytics page"),
            # DataTable(id="tabela", page_size=10),
            html.Div("This is our Analytics page content."),
        ],
        className="pagina",
    )
    return conteudo


"""
@callback(
    Output("tabela", "data"),
    Input("store", "data"),
)
def tabela_valores(store):
    return store["df"]


@callback(
    Output("tabela", "columns"),
    Input("store", "data"),
)
def tabela_colunas(store):
    money = FormatTemplate.money(2)
    percentage = FormatTemplate.percentage(2)

    return [
        {"name": "Marca", "id": "marca"},
        {
            "name": "Preço",
            "id": "preco_atual",
            "type": "numeric",
            "format": money,
        },
        {
            "name": "Preço Velho",
            "id": "preco_velho",
            "type": "numeric",
            "format": money,
        },
        {
            "name": "Desconto",
            "id": "percentual_promocao",
            "type": "numeric",
            "format": percentage,
        },
    ]
"""
