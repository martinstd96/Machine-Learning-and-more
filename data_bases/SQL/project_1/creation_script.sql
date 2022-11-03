DROP TABLE IF EXISTS taller_2.paradas CASCADE;

CREATE TABLE taller_2.paradas (
    cod_parada integer PRIMARY KEY,
    longitud numeric(15,12) NOT NULL,
    latitud numeric(15,12) NOT NULL,
    tipo_parada varchar,
    calle varchar,
    altura integer,
    entre1 varchar,
    entre2 varchar
)
WITH (OIDS=FALSE);
ALTER TABLE taller_2.paradas OWNER TO postgres;

DROP TABLE IF EXISTS taller_2.colectivos_por_parada;

CREATE TABLE taller_2.colectivos_por_parada (
    cod_parada integer,
    num_colectivo integer,
    CONSTRAINT pk_parada_colectivo PRIMARY KEY (cod_parada, num_colectivo),
    -- en la fila anterior le estoy dando un nombre definido por mi a la pk
    CONSTRAINT fk_cod_parada FOREIGN KEY (cod_parada) REFERENCES taller_2.paradas (cod_parada)
    ON UPDATE CASCADE 
)
WITH (OIDS=FALSE);
ALTER TABLE taller_2.colectivos_por_parada OWNER TO postgres;

-- Esto es para cargar datos de un archivo
COPY taller_2.paradas 
FROM '/paradas.csv'
DELIMITER ';'
CSV HEADER
ENCODING 'LATIN1';

-- Esto es para cargar datos de un archivo
COPY taller_2.colectivos_por_parada
FROM '/colectivosPorParada.csv'
DELIMITER ';'
CSV HEADER
ENCODING 'LATIN1';
