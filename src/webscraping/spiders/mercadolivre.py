import scrapy
from modulos.uteis import teste_scrapy


class MercadoLivreSpider(scrapy.Spider):
    name = "mercadolivre"
    start_urls = ["https://lista.mercadolivre.com.br/tenis-corrida-masculino"]
    page_count = 1
    max_pages = 10

    def parse(self, response):
        produtos_seletor = "div.ui-search-result__content"

        produtos = response.css(produtos_seletor)

        marca_seletor = "span.ui-search-item__brand-discoverability.ui-search-item__group__element::text"
        nome_produto_seletor = "h2.ui-search-item__title::text"
        nota_avaliacao_seletor = "span.ui-search-reviews__rating-number::text"
        num_avaliacoes_seletor = "span.ui-search-reviews__amount::text"

        preco_real_seletor = "span.andes-money-amount__fraction::text"
        preco_centavo_seletor = "span.andes-money-amount__cents::text"

        for produto in produtos:
            precos_reais = produto.css(preco_real_seletor).getall()
            precos_centavos = produto.css(preco_centavo_seletor).getall()

            preco_velho_reais = (
                precos_reais[0] if len(precos_reais) > 0 else None
            )
            preco_novo_reais = (
                precos_reais[1] if len(precos_reais) > 1 else None
            )

            preco_velho_centavos = (
                precos_centavos[0] if len(precos_centavos) > 0 else None
            )
            preco_novo_centavos = (
                precos_centavos[1] if len(precos_centavos) > 1 else None
            )

            yield {
                "marca": produto.css(marca_seletor).get(),
                "nome": produto.css(nome_produto_seletor).get(),
                "preco_velho_reais": preco_velho_reais,
                "preco_velho_centavos": preco_velho_centavos,
                "preco_novo_reais": preco_novo_reais,
                "preco_novo_centavos": preco_novo_centavos,
                "nota_avaliacao": produto.css(nota_avaliacao_seletor).get(),
                "num_avaliacoes": produto.css(num_avaliacoes_seletor).get(),
            }

        if self.page_count < self.max_pages:
            next_page = response.css(
                "li.andes-pagination__button.andes-pagination__button--next a::attr(href)"
            ).get()

            if next_page:
                self.page_count += 1
                yield scrapy.Request(url=next_page, callback=self.parse)
