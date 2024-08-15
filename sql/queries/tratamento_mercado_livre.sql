create function tratar_string(coluna)
as trim(
    regexp_replace(
      regexp_replace(
        replace(
          regexp_replace(
            regexp_replace(
              regexp_replace(
                regexp_replace(
                  regexp_replace(
                    upper(coluna), '[ÁÀÂÃÄÅ]', 'A', 'g'
                  ), '[ÉÈÊË]', 'E', 'g'
                ), '[ÍÌÎÏ]', 'I', 'g'
              ), '[ÓÒÔÕÖ]', 'O', 'g'
            ), '[ÚÙÛÜ]', 'U', 'g'
          ), 'Ç', 'C'
        ), '[^A-Z0-9 ]', ' ', 'g'
      ), '\s+', ' ', 'g'
    )
  );

create function adicionar_preco_completo(
  col_preco_reais,
  col_preco_centavos)
as cast(
    (
      case
        when col_preco_reais is not null and col_preco_centavos is not null
          then concat(replace(col_preco_reais, '.', ''), '.', col_preco_centavos)
        else
          col_preco_reais
      end
    ) as decimal(9, 2)
  );

with fase_1 as (
  select
      coalesce(
        tratar_string(marca), 'GENERICA'
      ) as marca
    , coalesce(
        tratar_string(produto), 'PRODUTO SEM NOME'
      ) as produto
    , adicionar_preco_completo(preco_velho_reais, preco_velho_centavos) as preco_velho
    , adicionar_preco_completo(preco_atual_reais, preco_atual_centavos) as preco_atual
    , (preco_velho_reais is not null) as promocao
    , cast(
        coalesce(nota_avaliacao, '0') as decimal(4, 2)
      ) as nota_avaliacao
    , cast(
        coalesce(trim(both '()' from num_avaliacoes), '0')
        as uinteger
      ) as num_avaliacoes
    , _fonte
    , _site
    , _data_coleta
    , cast(_pagina as utinyint) as _pagina
    , cast(_ordem as utinyint) as _ordem
  from
    df
  where
    preco_atual_reais is not null
)

select
    marca
  , produto
  , coalesce(preco_velho, preco_atual, preco_velho) as preco_velho
  , preco_atual
  , promocao
  , cast(
      case
        when promocao = true then ( (preco_velho - preco_atual) / preco_velho) * 100
        else 0
      end as decimal(4, 2)
    ) as percentual_promocao
  , nota_avaliacao
  , num_avaliacoes
  , _fonte
  , _site
  , _data_coleta
  , _pagina
  , _ordem
from
  fase_1;
