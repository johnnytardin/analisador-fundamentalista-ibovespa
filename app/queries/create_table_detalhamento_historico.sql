CREATE TABLE detalhamento_historico (
id INTEGER PRIMARY KEY AUTOINCREMENT,
stock TEXT,
tipo TEXT,
periodo TEXT,
valor INTEGER,
UNIQUE(stock, tipo, periodo)
);
