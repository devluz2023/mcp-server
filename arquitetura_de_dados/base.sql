-- 1. Criar Catalog (namespace principal)
CREATE CATALOG IF NOT EXISTS pedido;

-- 2. Criar Schema (database)
CREATE SCHEMA IF NOT EXISTS pedido.default;

-- 3. Garantir uso
USE CATALOG pedido;
USE SCHEMA default;