select
  marca as "Marca"
  , avg(preco_atual) as "Preço Médio"
from
  "../dados/processados/mercado_livre.parquet"
group by
  marca
order by
    "Preço Médio" desc
  , "Marca" asc;
