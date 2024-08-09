select
  count(distinct marca) as "Num Marcas Unicas"
from
  "../dados/processados/mercado_livre.parquet"
where
  marca <> 'GENERICA';
