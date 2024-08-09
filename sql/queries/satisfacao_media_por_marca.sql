select
  marca as "Marca"
  , avg(nota_avaliacao) as "Satisfação Média"
from
  "../dados/processados/mercado_livre.parquet"
where
  num_avaliacoes >= 20
group by
  marca
order by
    "Satisfação Média" desc
  , "Marca" asc;
