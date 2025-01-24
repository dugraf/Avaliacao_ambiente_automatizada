-- VERSAO DO BANCO
SELECT 
    SUBSTRING(@@VERSION, 1, CHARINDEX('(', @@VERSION) - 2) AS Version,
    CASE
        WHEN CHARINDEX('Express', @@VERSION) > 0 THEN 'Express'
        WHEN CHARINDEX('Standard', @@VERSION) > 0 THEN 'Standard'
        WHEN CHARINDEX('Enterprise', @@VERSION) > 0 THEN 'Enterprise'
        WHEN CHARINDEX('RTM', @@VERSION) > 0 THEN 'RTM'
        ELSE 'Unknown'
    END AS Edition;

-- MEMORIA MAXIMA E MINIMA
SELECT 
    name, 
    CAST(value AS INT) AS value 
FROM 
    sys.configurations 
WHERE 
    name IN ('min server memory (MB)', 'max server memory (MB)');

--ARMAZENAMENTO
EXEC sp_helpfile;

-- TABELAS MAIS PESADAS
SELECT TOP 5
    t.NAME AS TableName,
    p.rows AS RowCounts,
    SUM(a.total_pages) * 8 / 1024 AS TotalSpaceMB,
    SUM(a.used_pages) * 8 / 1024 AS UsedSpaceMB,
    SUM(a.data_pages) * 8 / 1024 AS DataSpaceMB
FROM  
    sys.tables t
INNER JOIN
    sys.indexes i ON t.OBJECT_ID = i.object_id
INNER JOIN
    sys.partitions p ON i.object_id = p.OBJECT_ID AND i.index_id = p.index_id
INNER JOIN
    sys.allocation_units a ON p.partition_id = a.container_id
WHERE
    t.is_ms_shipped = 0 
GROUP BY
    t.Name, p.Rows
ORDER BY
    TotalSpaceMB DESC;
