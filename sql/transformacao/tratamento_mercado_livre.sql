create table
  marcas as
select
  marcas_unicas.marca
from
  '../dados/marcas_unicas/marcas_unicas.csv' as marcas_unicas;

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
        -- Se col_preco_reais for NULL, entao eu quero que o resultado seja NULL
        else
          replace(col_preco_reais, '.', '')
      end
    ) as decimal(9, 2)
  );

with fase_1 as (
  select
      coalesce(tratar_string(df.marca), 'GENERICA') as marca
    , coalesce(tratar_string(df.produto), 'PRODUTO SEM NOME') as produto
    , adicionar_preco_completo(df.preco_velho_reais, df.preco_velho_centavos) as preco_velho
    , adicionar_preco_completo(df.preco_atual_reais, df.preco_atual_centavos) as preco_atual
    , (df.preco_velho_reais is not null) as promocao
    , cast(
        coalesce(df.nota_avaliacao, '0') as decimal(4, 2)
      ) as nota_avaliacao
    , cast(
        coalesce(trim(both '()' from df.num_avaliacoes), '0')
        as uinteger
      ) as num_avaliacoes
    , df._fonte
    , df._site
    , df._data_coleta::date as data_coleta
    , df._data_coleta::time as horario_coleta
    , cast(df._pagina as utinyint) as _pagina
    , cast(df._ordem as utinyint) as _ordem
  from
    df
  where
    df.preco_atual_reais is not null
)

select distinct
    case
      when f.marca = 'GENERICA'
        then coalesce(
          (
            select
              m.marca
            from
              marcas as m
            where
				      starts_with(f.produto, m.marca || ' ')
              or contains(f.produto, ' ' || m.marca || ' ')
				      or ends_with(f.produto, ' ' || m.marca)
			      order by
				      length(m.marca) desc
			      limit
				      1
          )
          , 'GENERICA'
        )
      else
        f.marca
    end as marca
  , f.produto
  , coalesce(f.preco_velho, f.preco_atual) as preco_velho
  , f.preco_atual
  , f.promocao
  , cast(
      case
        when f.promocao = true
          then ( (f.preco_velho - f.preco_atual) / f.preco_velho) * 100
        else
          0
      end as decimal(4, 2)
    ) as percentual_promocao
  , f.nota_avaliacao
  , f.num_avaliacoes
  , f._fonte
  , f._site
  , f.data_coleta as _data_coleta
  , f.horario_coleta as _horario_coleta
  , f._pagina
  , f._ordem
from
  fase_1 as f;
