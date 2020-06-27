CREATE TABLE IF NOT EXISTS
financial
(
    id SERIAL PRIMARY KEY,
    stock_code varchar(50),
    coleta_id uuid, 
    timestamp timestamp,
    data json
);

CREATE TABLE IF NOT EXISTS
dre
(
    id SERIAL PRIMARY KEY,
    stock_code varchar(50),
    coleta_id uuid, 
    timestamp timestamp,
    data json
);
