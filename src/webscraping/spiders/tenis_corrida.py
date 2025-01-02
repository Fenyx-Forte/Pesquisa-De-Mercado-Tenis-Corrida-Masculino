"""Spider para coletar os dados de Tênis de corrida."""

from os import getenv
from typing import ClassVar

import scrapy
from scrapy.http.response import Response

from modulos.uteis import carregar_env, meu_tempo

carregar_env.carregar_env()


def seletor_caixa_produtos() -> str:
    """Retorna o seletor CSS para a div onde estão localizados todos os resultados de pesquisa.

    Returns:
        str: Seletor CSS.
    """
    return "div.ui-search-result__content"


def seletor_marca() -> str:
    """Retorna o seletor CSS para obter o nome da marca de um produto.

    Returns:
        str: Seletor CSS.
    """
    return "span.ui-search-item__brand-discoverability.ui-search-item__group__element::text"


def seletor_nome_produto() -> str:
    """Retorna o seletor CSS para obter o nome do produto.

    Returns:
        str: Seletor CSS.
    """
    return "a.ui-search-link__title-card::text"


def seletor_nota_avaliacao() -> str:
    """Retorna o seletor CSS para obter a nota de avaliação do produto.

    Returns:
        str: Seletor CSS.
    """
    return "span.ui-search-reviews__rating-number::text"


def seletor_num_avaliacoes() -> str:
    """Retorna o seletor CSS para obter o número total de avaliações do produto.

    Returns:
        str: Seletor CSS.
    """
    return "span.ui-search-reviews__amount::text"


def seletor_caixa_precos() -> str:
    """Retorna o seletor CSS para a div onde estão localizados todos os preços dos produtos.

    Returns:
        str: Seletor CSS.
    """
    return "div.ui-search-price.ui-search-price--size-medium"


def seletor_caixa_preco_velho() -> str:
    """Retorna o seletor CSS para a div onde está localizado o preço velho do produto.

    Returns:
        str: Seletor CSS.
    """
    return "s.ui-search-price__original-value"


def seletor_caixa_preco_atual() -> str:
    """Retorna o seletor CSS para a div onde está localizado o preço atual do produto.

    Returns:
        str: Seletor CSS.
    """
    return "div.ui-search-price__second-line"


def seletor_preco_reais() -> str:
    """Retorna o seletor CSS para a parte inteira (em reais) do preço de um produto.

    Returns:
        str: Seletor CSS.
    """
    return "span.andes-money-amount__fraction::text"


def seletor_preco_centavos() -> str:
    """Retorna o seletor CSS para a parte decimal (centavos) do preço de um produto.

    Returns:
        str: Seletor CSS.
    """
    return "span.andes-money-amount__cents::text"


def seletor_proxima_pagina() -> str:
    """Retorna o seletor CSS para obter o link da próxima página do site.

    Returns:
        str: Seletor CSS.
    """
    return "li.andes-pagination__button.andes-pagination__button--next a::attr(href)"


def retorna_marca(produto: scrapy.Selector) -> str | None:
    """Retorna o nome da marca se encontrado.

    Args:
        produto (scrapy.Selector): Objeto do Scrapy com as informações do produto.

    Returns:
        str | None: Nome da marca, ou None se não for encontrado.
    """
    return produto.css(seletor_marca()).get()


def retorna_nome_produto(produto: scrapy.Selector) -> str | None:
    """Retorna o nome do produto se encontrado.

    Args:
        produto (scrapy.Selector): Objeto do Scrapy com as informações do produto.

    Returns:
        str | None: Nome do produto, ou None se não for encontrado.
    """
    return produto.css(seletor_nome_produto()).get()


def retorna_nota_avaliacao(produto: scrapy.Selector) -> str | None:
    """Retorna a avaliação do produto se encontrada.

    Args:
        produto (scrapy.Selector): Objeto do Scrapy com as informações do produto.

    Returns:
        str | None: Nota do produto, ou None se não for encontrada.
    """
    return produto.css(seletor_nota_avaliacao()).get()


def retorna_num_avaliacoes(produto: scrapy.Selector) -> str | None:
    """Retorna o número de avaliações do produto se encontrado.

    Args:
        produto (scrapy.Selector): Objeto do Scrapy com as informações do produto.

    Returns:
        str | None: Número de avaliações, ou None se não for encontrado.
    """
    return produto.css(seletor_num_avaliacoes()).get()


def retorna_preco_velho_reais(produto: scrapy.Selector) -> str | None:
    """Retorna a parte inteira do preço velho do produto.

    Args:
        produto (scrapy.Selector): Objeto do Scrapy com as informações do produto.

    Returns:
        str | None: Parte inteira do preço velho, ou None se não for encontrado.
    """
    caixa_precos = produto.css(seletor_caixa_precos())

    caixa_preco_velho = caixa_precos.css(seletor_caixa_preco_velho())

    return caixa_preco_velho.css(seletor_preco_reais()).get()


def retorna_preco_velho_centavos(produto: scrapy.Selector) -> str | None:
    """Retorna a parte decimal do preço velho do produto.

    Args:
        produto (scrapy.Selector): Objeto do Scrapy com as informações do produto.

    Returns:
        str | None: Parte decimal do preço velho, ou None se não for encontrado.
    """
    caixa_precos = produto.css(seletor_caixa_precos())

    caixa_preco_velho = caixa_precos.css(seletor_caixa_preco_velho())

    return caixa_preco_velho.css(seletor_preco_centavos()).get()


def retorna_preco_atual_reais(produto: scrapy.Selector) -> str | None:
    """Retorna a parte inteiro do preço atual do produto.

    Args:
        produto (scrapy.Selector): Objeto do Scrapy com as informações do produto.

    Returns:
        str | None: Parte inteira do preço atual, ou None se não for encontrado.
    """
    caixa_precos = produto.css(seletor_caixa_precos())

    caixa_preco_atual = caixa_precos.css(seletor_caixa_preco_atual())

    return caixa_preco_atual.css(seletor_preco_reais()).get()


def retorna_preco_atual_centavos(produto: scrapy.Selector) -> str | None:
    """Retorna a parte decimal do preço atual do produto.

    Args:
        produto (scrapy.Selector): Objeto do Scrapy com as informações do produto.

    Returns:
        str | None: Parte decimal do preço atual, ou None se não for encontrado.
    """
    caixa_precos = produto.css(seletor_caixa_precos())

    caixa_preco_atual = caixa_precos.css(seletor_caixa_preco_atual())

    return caixa_preco_atual.css(seletor_preco_centavos()).get()


def retorna_proxima_pagina(response: Response) -> str | None:
    """Retorna o link para a próxima página da busca.

    Args:
        response (scrapy.Selector): Objeto de resposta do Scrapy com as informações da página atual.

    Returns:
        str | None: URL da próxima página, ou None se não for encontrada.
    """
    return response.css(seletor_proxima_pagina()).get()


class TenisCorridaSpider(scrapy.Spider):
    """Spider para a extração de dados de tênis de corrida masculinos."""

    name = "teniscorrida"
    sops_job_name = "JOB_TENIS_CORRIDA"
    allowed_domains: ClassVar[list[str]] = [
        str(getenv("DOMAIN")),
        "proxy.scrapeops.io",
    ]
    start_urls: ClassVar[list[str]] = [str(getenv("START_URL"))]
    cont_pagina = 1
    max_pagina = 10
    ordem_produto = 0

    def parse(self, response: Response) -> dict:
        """Parse uma página da web e extraia informações do produto.

        Args:
            response (Response): Conteúdo HTML da página atual.

        Yields:
            dict: Dicionário contendo as informações extraídas.
        """
        data_coleta = meu_tempo.data_agora_string()

        produtos = response.css(seletor_caixa_produtos())

        for produto in produtos:
            self.ordem_produto += 1

            yield {
                "marca": retorna_marca(produto),
                "produto": retorna_nome_produto(produto),
                "preco_velho_reais": retorna_preco_velho_reais(produto),
                "preco_velho_centavos": retorna_preco_velho_centavos(produto),
                "preco_atual_reais": retorna_preco_atual_reais(produto),
                "preco_atual_centavos": retorna_preco_atual_centavos(produto),
                "nota_avaliacao": retorna_nota_avaliacao(produto),
                "num_avaliacoes": retorna_num_avaliacoes(produto),
                "_data_coleta": data_coleta,
                "_pagina": self.cont_pagina,
                "_ordem": self.ordem_produto,
            }

        if self.cont_pagina < self.max_pagina:
            proxima_pagina = retorna_proxima_pagina(response)

            if proxima_pagina:
                self.cont_pagina += 1
                self.ordem_produto = 0
                yield scrapy.Request(url=proxima_pagina, callback=self.parse)
