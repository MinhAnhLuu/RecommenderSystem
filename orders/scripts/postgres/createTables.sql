-- Author: ChauTran

-- Prepare data
-- Drop and create public Database
-- DROP SCHEMA public CASCADE;
-- CREATE SCHEMA public;

CREATE EXTENSION postgis;
CREATE EXTENSION postgis_topology;

-- Create tables

CREATE TABLE IF NOT EXISTS orders (
    id              SERIAL PRIMARY KEY,
    status          VARCHAR(10) NOT NULL,
    customer_id     VARCHAR(10) NOT NULL
)

CREATE TABLE IF NOT EXISTS order_details (
    id              SERIAL PRIMARY KEY,
    order_id        INTEGER REFERENCES orders (id),
    product_id      VARCHAR(16) NOT NULL,
    product_name    VARCHAR(32) NOT NULL,
    price           NUMERIC(18,2) NOT NULL,
    quantity        INTEGER NOT NULL,
    currency        VARCHAR(3) NOT NULL

)
CREATE TABLE IF NOT EXISTS orders (id SERIAL PRIMARY KEY,)