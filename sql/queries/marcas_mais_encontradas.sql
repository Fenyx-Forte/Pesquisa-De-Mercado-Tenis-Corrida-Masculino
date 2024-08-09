select
  marca as "Marca"
  , count(marca) as "Qtd Produtos"
from
  "../dados/processados/mercado_livre.parquet"
group by
  marca
order by
    "Qtd Produtos" desc
  , "Marca" asc
limit
  10;
