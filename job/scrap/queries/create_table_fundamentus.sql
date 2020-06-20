CREATE TABLE IF NOT EXISTS
fundamentus
(
    id SERIAL PRIMARY KEY,
    stock_code varchar(50),
    coleta_id uuid, 
    timestamp timestamp,
    details json
);
