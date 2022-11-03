-- Parte A:  Consultas basicas
/*
1 ) Para familiarizarse, muestre por pantalla las cinco primeras filas de cada tabla
 y observe sus estructuras
*/
SELECT *
FROM taller_2.paradas
LIMIT 5;

SELECT *
FROM taller_2.colectivos_por_parada
LIMIT 5;

/*
2) Listar todas las calles que tengan paradas de colectivos
*/
SELECT calle
FROM taller_2.paradas;

/*
3) 
Idem al anterior, pero asegurese de que el resultado no contenga calles repetidas
*/
SELECT DISTINCT calle
FROM taller_2.paradas;

/*
4) Listar el codigo de parada, calle y altura de cada parada
*/
SELECT cod_parada, calle, altura
FROM taller_2.paradas;

/*
5) Idem al anterior pero mostrando calle y altura separados por un espacio en blanco y que el
encabezado de la columna sea 'direccion'.
*/
SELECT cod_parada, calle || '' || altura as dirección
FROM taller_2.paradas;

/*
6) Mostrar nuevamente todas las calles ordenadas en forma ascendente. ¿como ordena el SGBD
los valores nulos?
*/
SELECT calle
FROM taller_2.paradas
ORDER BY calle ASC;

/*
7) Idem al anterior pero sin repeticiones. ¿Que sucedio ahora con los valores nulos?
*/
SELECT DISTINCT calle
FROM taller_2.paradas
ORDER BY calle ASC;

/*
8) Crear una nueva tabla a partir de la consulta 4.
*/
CREATE TABLE taller_2.calles AS (SELECT DISTINCT calle
				 FROM taller_2.paradas);
								 
-- Parte B: Parte b: Consultas intermedias
/*
9) Listar las paradas que estan sobre la Avenida Rivadavia ordenadas por altura
*/
SELECT *
FROM taller_2.paradas
WHERE calle ILIKE '%Riva%'
ORDER BY altura ASC;

/*
10) Listar las paradas que esten en la Avenida Rivadavia hasta la altura del 1600
*/
SELECT *
FROM taller_2.paradas
WHERE calle ILIKE '%Riva%' AND altura < 1600;

/*
11) Listar las paradas que esten en Avenida Paseo Colon sobre la Facultad de Ingenieria.
*/
SELECT *
FROM taller_2.paradas
WHERE calle ILIKE '%paseo co%' AND altura BETWEEN 800 AND 899;

/*
12) Listar las paradas que esten en Avenida Paseo Colon entre las calles Mexico y Chile
*/
SELECT *
FROM taller_2.paradas
WHERE calle ILIKE '%paseo co%' 
AND (entre1 ILIKE '%chile%' AND entre2 ILIKE '%mexico%')
OR (entre1 ILIKE '%mexico%' AND entre2 ILIKE '%chile%');

/*
13) Listar la parada ubicada mas al norte de la Ciudad
*/
SELECT *
FROM taller_2.paradas
WHERE latitud = (SELECT MAX(latitud)
		 FROM taller_2.paradas);
				
/*
14) Listar la parada ubicada mas al sur de la Ciudad
*/
SELECT *
FROM taller_2.paradas
WHERE latitud = (SELECT MIN(latitud)
		 FROM taller_2.paradas);
				
/*
15) Mostrar cuantas paradas de colectivos hay
*/
SELECT COUNT(*)
FROM taller_2.paradas;

/*
16) Mostrar cuantas calles tienen alguna parada de colectivos en la ciudad.
*/
SELECT COUNT(DISTINCT calle)
FROM taller_2.paradas;

/*
17) Mostrar cuantas paradas de colectivos hay en la avenida Rivadavia.
*/
SELECT COUNT(*) AS cant_paradas
FROM taller_2.paradas
WHERE calle ILIKE '%riva%';

/*
18) Obtener la paradas que comparten las lıneas 28 y 21.
*/
SELECT DISTINCT cod_parada
FROM taller_2.colectivos_por_parada
WHERE num_colectivo = 28
INTERSECT
SELECT DISTINCT cod_parada
FROM taller_2.colectivos_por_parada
WHERE num_colectivo = 21;

/*
19) Obtener la paradas de las lıneas 28 y/o 21.
*/
SELECT DISTINCT cod_parada
FROM taller_2.colectivos_por_parada
WHERE num_colectivo = 28 
OR num_colectivo = 21;

-- Parte C: Consultas avanzadas
/*
20) Obtener el ranking de la cantidad de paradas que hay por lınea de colectivo, ordenando de
mayor a menor por dicha cantidad
*/
SELECT num_colectivo, COUNT(cod_parada) AS cantidad
FROM taller_2.colectivos_por_parada
GROUP BY num_colectivo
ORDER BY 2 DESC;

/*
21) Idem al anterior, pero limitando el ranking a las lıneas cuya cantidad de paradas sea de al
menos 100.
*/
SELECT num_colectivo, COUNT(cod_parada) AS cantidad
FROM taller_2.colectivos_por_parada
GROUP BY num_colectivo
HAVING COUNT(cod_parada) >= 100
ORDER BY 2 DESC;

/*
22) Mostrar el ranking de la cantidad de paradas que hay por avenida
*/
SELECT calle, COUNT(cod_parada) AS cantidad
FROM taller_2.paradas
WHERE calle ILIKE '%av%'
GROUP BY 1
ORDER BY COUNT(cod_parada) DESC;

/*
23) Obtener la cantidad de paradas que hay por cada tipo de parada
*/
SELECT tipo_parada, COUNT(cod_parada)
FROM taller_2.paradas
GROUP BY 1;

/*
24) Obtener las 5 calles con mayor cantidad de cuadras entre los dos extremos de sus paradas
*/
SELECT calle, (MAX(altura) - MIN(altura))/100 AS largo
FROM taller_2.paradas
WHERE altura IS NOT NULL
GROUP BY 1
ORDER BY 2 DESC
LIMIT 5;

/*
25) Mostrar la/las parada/s en que pare el mayor numero de colectivos.
*/
SELECT cod_parada, COUNT(num_colectivo) AS cant_colectivos
FROM taller_2.colectivos_por_parada
GROUP BY 1
HAVING COUNT(num_colectivo) >= ALL(SELECT COUNT(num_colectivo)
				   FROM taller_2.colectivos_por_parada
				   GROUP BY cod_parada);
									 
/*
26) Obtener todas las paradas que sean exclusivas, es decir, que sean para una sola lınea de
colectivos.
*/
SELECT cod_parada
FROM taller_2.colectivos_por_parada
GROUP BY 1
HAVING COUNT(num_colectivo) = 1;

/*
27) Idem al anterior pero mostrando la direccion de dicha parada de colectivos.
*/
SELECT p.cod_parada, p.calle, p.altura
FROM (SELECT cod_parada
FROM taller_2.colectivos_por_parada
GROUP BY 1
HAVING COUNT(num_colectivo) = 1) c, taller_2.paradas p
WHERE c.cod_parada = p.cod_parada;
