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

        preco_velho_seletor = "s.andes-money-amount.ui-search-price__part.ui-search-price__part--small.ui-search-price__original-value.andes-money-amount--previous.andes-money-amount--cents-superscript.andes-money-amount--compact"
        preco_velho_real_seletor = "span.andes-money-amount__fraction::text"
        preco_velho_centavo_seletor = "span.andes-money-amount__cents.andes-money-amount__cents--superscript-16::text"

        preco_novo_seletor = "div.ui-search-price__second-line"
        preco_novo_real_seletor = "span.andes-money-amount__fraction::text"
        preco_novo_centavo_seletor = "span.andes-money-amount__cents.andes-money-amount__cents--superscript-24::text"

        for produto in produtos:
            preco_velho = produto.css(preco_velho_seletor)

            preco_velho_real = preco_velho.css(preco_velho_real_seletor).get()
            preco_velho_centavo = preco_velho.css(
                preco_velho_centavo_seletor
            ).get()

            preco_novo = produto.css(preco_novo_seletor)
            preco_novo_real = preco_novo.css(preco_novo_real_seletor).get()
            preco_novo_centavo = preco_novo.css(
                preco_novo_centavo_seletor
            ).get()

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
