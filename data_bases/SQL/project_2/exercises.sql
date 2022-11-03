/*
a) Obtener el padron y apellido de el/los estudiante/s que tenga/n la
mayor cantidad de materias aprobadas.
*/
SELECT n.padron, e.apellido
FROM parcialito.estudiantes e, parcialito.notas n
WHERE e.padron = n.padron AND n.nota >= 4
GROUP BY 1, 2
HAVING COUNT(n.nota) >= ALL(SELECT COUNT(nota)
						   FROM parcialito.notas
						   WHERE nota >= 4
						   GROUP BY padron);

/*
b) Obtener el padron y apellido de aquellos estudiantes que tienen nota 
en las materias 71.14 y 71.15 y no tienen nota ni en la materia 75.01
ni en 75.15.
TODO: corregir
*/
SELECT DISTINCT m.padron, e.apellido
FROM parcialito.estudiantes e, (SELECT padron, codigo, numero
							    FROM parcialito.NOTAS
							    WHERE codigo = 71 AND numero IN (14, 15)
							    INTERSECT
							    SELECT padron, codigo, numero
							    FROM parcialito.NOTAS
							    WHERE codigo <> 75 AND numero NOT IN (1, 15)) m
WHERE m.padron = e.padron;

/*
c) Para cada carrera y cada departamento, devuelva el codigo de carrera,
codigo de departamento y promedio de notas que los estudiantes anotados
en esa carrera tienen en materias de ese departamento.
*/
SELECT i.padron, i.codigo, n.codigo, n.nota
FROM parcialito.inscripto_en i, parcialito.notas n
WHERE i.padron = n.padron;
SELECT i.codigo, n.codigo, AVG(n.nota)::numeric(3,2) promedio
FROM parcialito.inscripto_en i, parcialito.notas n
WHERE i.padron = n.padron
GROUP BY 1, 2;

/*
d) Mostrar el padron, apellido y promedio para aquellos estudiantes 
que tienen nota en mas de 3 materias y un promedio de al menos 5.
*/
SELECT n.padron, e.apellido, n.promedio
FROM parcialito.estudiantes e, (SELECT padron, AVG(nota)::numeric(3,2) AS promedio
							    FROM parcialito.NOTAS
								GROUP BY 1
								HAVING COUNT(DISTINCT codigo::varchar ||'.'|| numero::varchar) > 3 AND AVG(nota) >= 5) n
WHERE n.padron = e.padron;

/*
e) Para cada nota del estudiante mas antiguo, mostrar su padron, codigo
de departamento, numero de materia y el valor de la nota.
*/
SELECT e.padron, n.codigo, n.numero, n.nota
FROM parcialito.NOTAS n, (SELECT padron
						  FROM parcialito.estudiantes
						  WHERE fecha_ingreso = (SELECT MIN(fecha_ingreso)
					  							 FROM parcialito.estudiantes)) e
WHERE n.padron = e.padron;

/*
f) Listar el padron de aquellos estudiantes que, por lo menos, tienen 
nota en todas las materias que aprobo el estudiante de padron 71000.
TODO: corregir
*/
SELECT DISTINCT padron
FROM parcialito.NOTAS 
WHERE codigo::varchar ||'.'|| numero::varchar IN (SELECT DISTINCT codigo::varchar ||'.'|| numero::varchar AS materia
												  FROM parcialito.NOTAS 
												  WHERE padron = 71000
												  GROUP BY 1
												  HAVING MAX(nota) >= 4);
