-- Parte A
-- 1 
SELECT *
FROM taller_2.paradas
LIMIT 5;

SELECT *
FROM taller_2.colectivos_por_parada
LIMIT 5;

-- 2
SELECT calle
FROM taller_2.paradas;

-- 3
SELECT DISTINCT calle
FROM taller_2.paradas;

-- 4
SELECT cod_parada, calle, altura
FROM taller_2.paradas;

-- 5
SELECT cod_parada, calle || '' || altura as dirección
FROM taller_2.paradas;

-- 6
SELECT calle
FROM taller_2.paradas
ORDER BY calle ASC;

-- 7 
SELECT DISTINCT calle
FROM taller_2.paradas
ORDER BY calle ASC;

-- 9
CREATE TABLE taller_2.calles AS (SELECT DISTINCT calle
								 FROM taller_2.paradas);
								 
-- Parte B
-- 10
SELECT *
FROM taller_2.paradas
WHERE calle ILIKE '%Riva%'
ORDER BY altura ASC;

-- 11
SELECT *
FROM taller_2.paradas
WHERE calle ILIKE '%Riva%' AND altura < 1600;

-- 12
SELECT *
FROM taller_2.paradas
WHERE calle ILIKE '%paseo co%' AND altura BETWEEN 800 AND 899;

-- 13
SELECT *
FROM taller_2.paradas
WHERE calle ILIKE '%paseo co%' 
AND (entre1 ILIKE '%chile%' AND entre2 ILIKE '%mexico%')
OR (entre1 ILIKE '%mexico%' AND entre2 ILIKE '%chile%');

-- 14
SELECT *
FROM taller_2.paradas
WHERE latitud = (SELECT MAX(latitud)
				FROM taller_2.paradas);
				
-- 15
SELECT *
FROM taller_2.paradas
WHERE latitud = (SELECT MIN(latitud)
				FROM taller_2.paradas);
				
-- 16
SELECT COUNT(*)
FROM taller_2.paradas;

-- 17
SELECT COUNT(DISTINCT calle)
FROM taller_2.paradas;

-- 18
SELECT COUNT(*) AS cant_paradas
FROM taller_2.paradas
WHERE calle ILIKE '%riva%';

-- 19
SELECT DISTINCT cod_parada
FROM taller_2.colectivos_por_parada
WHERE num_colectivo = 28
INTERSECT
SELECT DISTINCT cod_parada
FROM taller_2.colectivos_por_parada
WHERE num_colectivo = 21;

-- 20
SELECT DISTINCT cod_parada
FROM taller_2.colectivos_por_parada
WHERE num_colectivo = 28 
OR num_colectivo = 21;

-- Parte C
--21
SELECT num_colectivo, COUNT(cod_parada) AS cantidad
FROM taller_2.colectivos_por_parada
GROUP BY num_colectivo
ORDER BY 2 DESC;

-- 22
SELECT num_colectivo, COUNT(cod_parada) AS cantidad
FROM taller_2.colectivos_por_parada
GROUP BY num_colectivo
HAVING COUNT(cod_parada) >= 100
ORDER BY 2 DESC;

-- 23
SELECT calle, COUNT(cod_parada) AS cantidad
FROM taller_2.paradas
WHERE calle ILIKE '%av%'
GROUP BY 1
ORDER BY COUNT(cod_parada) DESC;

-- 24
SELECT tipo_parada, COUNT(cod_parada)
FROM taller_2.paradas
GROUP BY 1;

-- 25
SELECT calle, (MAX(altura) - MIN(altura))/100 AS largo
FROM taller_2.paradas
WHERE altura IS NOT NULL
GROUP BY 1
ORDER BY 2 DESC
LIMIT 5;

-- 26
SELECT cod_parada, COUNT(num_colectivo) AS cant_colectivos
FROM taller_2.colectivos_por_parada
GROUP BY 1
HAVING COUNT(num_colectivo) >= ALL(SELECT COUNT(num_colectivo)
									 FROM taller_2.colectivos_por_parada
									 GROUP BY cod_parada);
									 
-- 28
SELECT cod_parada
FROM taller_2.colectivos_por_parada
GROUP BY 1
HAVING COUNT(num_colectivo) = 1;

-- 29
SELECT p.cod_parada, p.calle, p.altura
FROM (SELECT cod_parada
FROM taller_2.colectivos_por_parada
GROUP BY 1
HAVING COUNT(num_colectivo) = 1) c, taller_2.paradas p
WHERE c.cod_parada = p.cod_parada;

-- 30
SELECT DISTINCT tipo_parada
FROM taller_2.paradas;
SELECT *
FROM taller_2.paradas
WHERE 