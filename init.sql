-- Tabla para Product
CREATE TABLE product (
    id SERIAL PRIMARY KEY,
    name VARCHAR(500) NOT NULL,
    serial VARCHAR(250) UNIQUE NOT NULL,
    price DECIMAL(100, 20) DEFAULT 0.0 NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Tabla para Inventory
CREATE TABLE inventory (
    id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES product(id) ON DELETE CASCADE,
    count BIGINT DEFAULT 0 NOT NULL
);

-- Tabla para Payment
CREATE TABLE payment (
    id SERIAL PRIMARY KEY,
    total_amount DECIMAL(100, 20) DEFAULT 0.0 NOT NULL,
    status SMALLINT DEFAULT 1 NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    CHECK (status IN (1, 2, 3))
);

-- Tabla para PaymentDetail
CREATE TABLE payment_detail (
    id SERIAL PRIMARY KEY,
    payment_id INTEGER REFERENCES payment(id) ON DELETE CASCADE,
    product_id INTEGER REFERENCES product(id) ON DELETE SET NULL
);

-- Índice para los campos en las tablas
CREATE INDEX idx_payment_status ON payment(status);
CREATE INDEX idx_payment_detail_payment ON payment_detail(payment_id);
CREATE INDEX idx_payment_detail_product ON payment_detail(product_id);
CREATE INDEX idx_inventory_product ON inventory(product_id);



-- Creación del Pago en Estado "Edición" (DRAFT)
CREATE OR REPLACE PROCEDURE create_payment(INOUT new_payment_id INTEGER)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO payment (total_amount, status, created_at, updated_at)
    VALUES (0.0, 1, NOW(), NOW())
    RETURNING id INTO new_payment_id;

    IF new_payment_id IS NULL THEN
        RAISE EXCEPTION 'Failed to create a new payment';
    END IF;
END;
$$;


-- Agregar un Producto a un Payment en Estado "Edición"

CREATE OR REPLACE PROCEDURE add_payment_detail(IN payment_id INTEGER, IN product_id INTEGER, IN quantity INTEGER)
LANGUAGE plpgsql
AS $$
DECLARE
    product_price DECIMAL;
BEGIN
    -- Verifica que el payment esté en estado "Edición" (Draft)
    IF (SELECT status FROM payment WHERE id = payment_id) != 1 THEN
        RAISE EXCEPTION 'Cannot add products to a non-draft payment';
    END IF;

    -- Obtén el precio del producto
    SELECT price INTO product_price FROM product WHERE id = product_id;

    IF product_price IS NULL THEN
        RAISE EXCEPTION 'Product with ID % does not exist', product_id;
    END IF;

    -- Inserta el nuevo detalle del pago
    INSERT INTO payment_detail (payment_id, product_id)
    VALUES (payment_id, product_id);

    -- Actualiza el total_amount del payment
    UPDATE payment
    SET total_amount = (
        SELECT COALESCE(SUM(p.price), 0)
        FROM payment_detail pd
        JOIN product p ON pd.product_id = p.id
        WHERE pd.payment_id = payment.id
    ),
    updated_at = NOW()
    WHERE id = payment_id;
END;
$$;


-- Eliminar un Payment Detail si el Payment está en Estado "Edición"

CREATE OR REPLACE PROCEDURE remove_payment_detail(IN payment_detail_id INTEGER)
LANGUAGE plpgsql
AS $$
DECLARE
    payment_id INTEGER;
    product_price DECIMAL;
BEGIN
    SELECT pd.payment_id, p.price INTO payment_id, product_price
    FROM payment_detail pd
    JOIN product p ON pd.product_id = p.id
    WHERE pd.id = payment_detail_id;

    IF payment_id IS NULL THEN
        RAISE EXCEPTION 'Payment detail with ID % does not exist', payment_detail_id;
    END IF;

    IF (SELECT status FROM payment WHERE id = payment_id) != 1 THEN
        RAISE EXCEPTION 'Cannot remove products from a non-draft payment';
    END IF;

    DELETE FROM payment_detail WHERE id = payment_detail_id;

    UPDATE payment
    SET total_amount = total_amount - product_price,
        updated_at = NOW()
    WHERE id = payment_id;
END;
$$;


-- Pasar un Payment de Estado "Edición" a "Pagado" (Pagado)

CREATE OR REPLACE PROCEDURE mark_payment_as_paid(IN payment_id INTEGER)
LANGUAGE plpgsql
AS $$
DECLARE
    product_id INTEGER;
    inventory_count INTEGER;
BEGIN
    IF (SELECT status FROM payment WHERE id = payment_id) != 1 THEN
        RAISE EXCEPTION 'Cannot mark a non-draft payment as paid';
    END IF;

    FOR product_id IN (SELECT product_id FROM payment_detail WHERE payment_id = payment_id)
    LOOP
        SELECT count INTO inventory_count FROM inventory WHERE product_id = product_id;

        IF inventory_count IS NULL OR inventory_count < 1 THEN
            RAISE EXCEPTION 'Not enough inventory for product %', product_id;
        END IF;

        UPDATE inventory SET count = count - 1 WHERE product_id = product_id;
    END LOOP;

    UPDATE payment SET status = 3, updated_at = NOW() WHERE id = payment_id;
END;
$$;


-- Cancelar un Payment en Estado "Edición"

CREATE OR REPLACE PROCEDURE cancel_payment(IN payment_id INTEGER)
LANGUAGE plpgsql
AS $$
BEGIN
    IF (SELECT status FROM payment WHERE id = payment_id) != 1 THEN
        RAISE EXCEPTION 'Cannot cancel a non-draft payment';
    END IF;

    UPDATE payment SET status = 2, updated_at = NOW() WHERE id = payment_id;
END;
$$;


-- Eliminar Payments en Estado "Cancelado"

CREATE OR REPLACE PROCEDURE delete_cancelled_payments(IN payment_id INTEGER)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM payment WHERE status = 2 AND id = payment_id;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'No cancelled payment found with ID %', payment_id;
    END IF;
END;
$$;

