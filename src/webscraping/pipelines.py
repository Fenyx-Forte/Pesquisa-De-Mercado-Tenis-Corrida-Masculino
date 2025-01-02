"""Pipelines para o scrapy. Utilizei a configuração default."""

from scrapy import Item, Spider


class AppWebscrapingPipeline:
    """Pipeline default para o scrapy."""

    def process_item(self, item: Item, spider: Spider) -> Item:
        """Processa o item.

        Args:
            item (Item): Dicionário contendo os dados do item.
            spider (Spider): Objeto que realiza a extração dos itens.

        Returns:
            Item: O dicionário processado.
        """
        return item
