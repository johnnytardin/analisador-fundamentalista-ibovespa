UPDATE detalhamento_historico
SET valor = :valor
WHERE stock = :stock and tipo = :tipo and periodo = :periodo
