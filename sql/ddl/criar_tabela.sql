create table if not exists tenis_corrida (
  marca varchar(255) not null
  , produto varchar(255) not null
  , preco_velho decimal(7, 2) not null
  , preco_atual decimal(7, 2) not null
  , promocao boolean not null
  , percentual_promocao decimal(5, 2) not null
  , nota_avaliacao decimal(3, 2) not null
  , num_avaliacoes integer not null
  , _data_coleta date not null
  , _horario_coleta time not null
  , _pagina smallint not null
  , _ordem smallint not null
);
