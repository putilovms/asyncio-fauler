# Chapter 5

DB = {
    'host': '127.0.0.1',
    'port': 5432,
    'user': 'mickle',
    'password': '1234',
    'database': 'fauler',
}

CREATE_BRAND_TABLE = \
    """
    CREATE TABLE IF NOT EXISTS brand(
        brand_id SERIAL PRIMARY KEY,
        brand_name TEXT NOT NULL
    );"""

CREATE_PRODUCT_TABLE = \
    """
    CREATE TABLE IF NOT EXISTS product(
        product_id SERIAL PRIMARY KEY,
        product_name TEXT NOT NULL,
        brand_id INT NOT NULL,
        FOREIGN KEY (brand_id) REFERENCES brand(brand_id)
    );"""

CREATE_PRODUCT_COLOR_TABLE = \
    """
    CREATE TABLE IF NOT EXISTS product_color(
        product_color_id SERIAL PRIMARY KEY,
        product_color_name TEXT NOT NULL
    );"""

CREATE_PRODUCT_SIZE_TABLE = \
    """
    CREATE TABLE IF NOT EXISTS product_size(
        product_size_id SERIAL PRIMARY KEY,
        product_size_name TEXT NOT NULL
    );"""

CREATE_SKU_TABLE = \
    """
    CREATE TABLE IF NOT EXISTS sku(
        sku_id SERIAL PRIMARY KEY,
        product_id INT NOT NULL,
        product_size_id INT NOT NULL,
        product_color_id INT NOT NULL,
        FOREIGN KEY (product_id)
        REFERENCES product(product_id),
        FOREIGN KEY (product_size_id)
        REFERENCES product_size(product_size_id),
        FOREIGN KEY (product_color_id)
        REFERENCES product_color(product_color_id)
    );"""

COLOR_INSERT = \
    """
    INSERT INTO product_color VALUES(1, 'Blue');
    INSERT INTO product_color VALUES(2, 'Black');
    """

SIZE_INSERT = \
    """
    INSERT INTO product_size VALUES(1, 'Small');
    INSERT INTO product_size VALUES(2, 'Medium');
    INSERT INTO product_size VALUES(3, 'Large');
    """

DROP_TABLES = \
    """
    DROP TABLE IF EXISTS sku CASCADE;
    DROP TABLE IF EXISTS product_size CASCADE;
    DROP TABLE IF EXISTS product_color CASCADE;
    DROP TABLE IF EXISTS product CASCADE;
    DROP TABLE IF EXISTS brand CASCADE;
    """

# Chapter 10

DB_CART = {
    'host': '127.0.0.1',
    'port': 5432,
    'user': 'mickle',
    'password': '1234',
    'database': 'cart',
}

DB_FAVORITES = {
    'host': '127.0.0.1',
    'port': 5432,
    'user': 'mickle',
    'password': '1234',
    'database': 'favorites',
}

DROP_CART = '''
    DROP TABLE IF EXISTS user_cart CASCADE;
    '''

DROP_FAVORITE = '''
    DROP TABLE IF EXISTS user_favorite CASCADE;
    '''

USER_CART_CREATE = '''
    CREATE TABLE user_cart (
        user_id INT NOT NULL,
        product_id INT NOT NULL
    );
    '''

USER_CART_INSERT = '''
    INSERT INTO user_cart VALUES (1, 1);
    INSERT INTO user_cart VALUES (1, 2);
    INSERT INTO user_cart VALUES (1, 3);
    INSERT INTO user_cart VALUES (2, 1);
    INSERT INTO user_cart VALUES (2, 2);
    INSERT INTO user_cart VALUES (2, 5);
    '''

USER_FAVORITE_CREATE = '''
    CREATE TABLE user_favorite (
        user_id INT NOT NULL,
        product_id INT NOT NULL
    );
    '''

USER_FAVORITE_INSERT = '''
    INSERT INTO user_favorite VALUES (1, 1);
    INSERT INTO user_favorite VALUES (1, 2);
    INSERT INTO user_favorite VALUES (1, 3);
    INSERT INTO user_favorite VALUES (3, 1);
    INSERT INTO user_favorite VALUES (3, 2);
    INSERT INTO user_favorite VALUES (3, 3);
    '''
