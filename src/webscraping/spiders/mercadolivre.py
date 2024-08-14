import scrapy
from modulos.uteis import meu_tempo


def seletor_caixa_produtos() -> str:
    return "div.ui-search-result__content"


def seletor_marca() -> str:
    return "span.ui-search-item__brand-discoverability.ui-search-item__group__element::text"


def seletor_nome_produto() -> str:
    return "h2.ui-search-item__title::text"


def seletor_nota_avaliacao() -> str:
    return "span.ui-search-reviews__rating-number::text"


def seletor_num_avaliacoes() -> str:
    return "span.ui-search-reviews__amount::text"


def seletor_caixa_precos() -> str:
    return "div.ui-search-price.ui-search-price--size-medium"


def seletor_caixa_preco_velho() -> str:
    return "s.ui-search-price__original-value"


def seletor_caixa_preco_atual() -> str:
    return "div.ui-search-price__second-line"


def seletor_preco_reais() -> str:
    return "span.andes-money-amount__fraction::text"


def seletor_preco_centavos() -> str:
    return "span.andes-money-amount__cents::text"


def seletor_proxima_pagina() -> str:
    return "li.andes-pagination__button.andes-pagination__button--next a::attr(href)"


def retorna_marca(produto) -> str:
    marca = produto.css(seletor_marca()).get()

    return marca


def retorna_nome_produto(produto) -> str:
    nome_produto = produto.css(seletor_nome_produto()).get()

    return nome_produto


def retorna_nota_avaliacao(produto) -> str:
    nota_avaliacao = produto.css(seletor_nota_avaliacao()).get()

    return nota_avaliacao


def retorna_num_avaliacoes(produto) -> str:
    num_avaliacoes = produto.css(seletor_num_avaliacoes()).get()

    return num_avaliacoes


def retorna_preco_velho_reais(produto) -> str:
    caixa_precos = produto.css(seletor_caixa_precos())

    caixa_preco_velho = caixa_precos.css(seletor_caixa_preco_velho())

    preco_velho_reais = caixa_preco_velho.css(seletor_preco_reais()).get()

    return preco_velho_reais


def retorna_preco_velho_centavos(produto) -> str:
    caixa_precos = produto.css(seletor_caixa_precos())

    caixa_preco_velho = caixa_precos.css(seletor_caixa_preco_velho())

    preco_velho_centavos = caixa_preco_velho.css(seletor_preco_centavos()).get()

    return preco_velho_centavos


def retorna_preco_atual_reais(produto) -> str:
    caixa_precos = produto.css(seletor_caixa_precos())

    caixa_preco_atual = caixa_precos.css(seletor_caixa_preco_atual())

    preco_atual_reais = caixa_preco_atual.css(seletor_preco_reais()).get()

    return preco_atual_reais


def retorna_preco_atual_centavos(produto) -> str:
    caixa_precos = produto.css(seletor_caixa_precos())

    caixa_preco_atual = caixa_precos.css(seletor_caixa_preco_atual())

    preco_atual_centavos = caixa_preco_atual.css(seletor_preco_centavos()).get()

    return preco_atual_centavos


def retorna_proxima_pagina(response) -> str:
    proxima_pagina = response.css(seletor_proxima_pagina()).get()

    return proxima_pagina


class MercadoLivreSpider(scrapy.Spider):
    name = "mercadolivre"
    sops_job_name = "JOB_MERCADO_LIVRE"
    allowed_domains = ["lista.mercadolivre.com.br", "proxy.scrapeops.io"]
    start_urls = ["https://lista.mercadolivre.com.br/tenis-corrida-masculino"]
    fonte = "https://lista.mercadolivre.com.br/tenis-corrida-masculino"
    site = "MERCADO LIVRE"
    cont_pagina = 1
    max_pagina = 10
    ordem_produto = 0

    def parse(self, response):
        data_coleta = meu_tempo.data_agora()

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
                "_fonte": self.fonte,
                "_site": self.site,
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
