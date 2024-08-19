insert into db.mercado_livre (
    marca
  , produto
  , preco_velho
  , preco_atual
  , promocao
  , percentual_promocao
  , nota_avaliacao
  , num_avaliacoes
  , _fonte
  , _site
  , _data_coleta
  , _pagina
  , _ordem
)
select
  *
from
  df;
