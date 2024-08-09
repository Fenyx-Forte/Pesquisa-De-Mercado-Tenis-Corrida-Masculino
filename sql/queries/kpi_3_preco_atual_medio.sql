select
  avg(preco_atual) as "Média Preço"
from
  "../dados/processados/mercado_livre.parquet";
