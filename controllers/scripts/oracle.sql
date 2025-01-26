-- VERSAO DO BANCO
--SELECT * FROM v$version
SELECT * FROM product_component_version;

-- MEMORIA MAXIMA E MINIMA
SELECT 
    name, 
    value 
FROM 
    V$PARAMETER
WHERE 
    name IN ('sga_target', 'pga_aggregate_target');

-- ARMAZENAMENTO
SELECT
    tablespace_name,
    SUM(bytes) / 1024 / 1024 / 1024 AS space_used_GB
FROM
    dba_segments
WHERE
    owner = USER
GROUP BY
    tablespace_name;

-- TABELAS MAIS PESADAS
SELECT
    s.segment_name AS table_name,
    SUM(s.bytes) / 1024 / 1024 / 1024 AS space_used_GB,
    t.num_rows AS row_count
FROM
    dba_segments s
JOIN
    dba_tables t ON s.segment_name = t.table_name
WHERE
    s.owner = USER
    AND s.segment_type = 'TABLE'
GROUP BY
    s.segment_name, t.num_rows
ORDER BY
    space_used_GB DESC
FETCH FIRST 5 ROWS ONLY;
