insert into
db.tenis_corrida (
  marca
  , produto
  , preco_velho
  , preco_atual
  , promocao
  , percentual_promocao
  , nota_avaliacao
  , num_avaliacoes
  , _data_coleta
  , _horario_coleta
  , _pagina
  , _ordem
)
select
  marca
  , produto
  , preco_velho
  , preco_atual
  , promocao
  , percentual_promocao
  , nota_avaliacao
  , num_avaliacoes
  , _data_coleta
  , _horario_coleta
  , _pagina
  , _ordem
from
  df;
