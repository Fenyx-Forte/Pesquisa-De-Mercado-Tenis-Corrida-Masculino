import scrapy


class MercadoLivreSpider(scrapy.Spider):
    name = "mercadolivre"
    start_urls = ["https://lista.mercadolivre.com.br/tenis-corrida-masculino"]

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
            precos_real = produto.css(preco_real_seletor).getall()
            precos_centavo = produto.css(preco_centavo_seletor).getall()

            preco_velho_real = precos_real[0] if len(precos_real) > 0 else None
            preco_novo_real = precos_real[1] if len(precos_real) > 1 else None

            preco_velho_centavo = (
                precos_centavo[0] if len(precos_centavo) > 0 else None
            )
            preco_novo_centavo = (
                precos_centavo[1] if len(precos_centavo) > 1 else None
            )

            num_avaliacoes_nao_tratado = produto.css(
                num_avaliacoes_seletor
            ).get()

            if num_avaliacoes_nao_tratado is None:
                num_avaliacoes = None
            else:
                num_avaliacoes = num_avaliacoes_nao_tratado[1:-1]

            yield {
                "marca": produto.css(marca_seletor).get(),
                "nome_produto": produto.css(nome_produto_seletor).get(),
                "preco_velho": f"{preco_velho_real}.{preco_velho_centavo}",
                "preco_novo": f"{preco_novo_real}.{preco_novo_centavo}",
                "nota_avaliacao": produto.css(nota_avaliacao_seletor).get(),
                "num_avaliacoes": num_avaliacoes,
            }
