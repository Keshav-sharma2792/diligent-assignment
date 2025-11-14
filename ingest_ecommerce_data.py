"""
Ingest synthetic e-commerce CSVs stored in ./data into a SQLite database.
"""

from __future__ import annotations

import csv
import sqlite3
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parent / "data"
DB_PATH = Path(__file__).resolve().parent / "ecommerce.db"


def create_tables(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        PRAGMA foreign_keys = ON;

        CREATE TABLE IF NOT EXISTS customers (
            customer_id TEXT PRIMARY KEY,
            full_name   TEXT NOT NULL,
            email       TEXT NOT NULL,
            city        TEXT,
            created_at  TEXT
        );

        CREATE TABLE IF NOT EXISTS products (
            product_id   TEXT PRIMARY KEY,
            product_name TEXT NOT NULL,
            category     TEXT,
            price        REAL NOT NULL
        );

        CREATE TABLE IF NOT EXISTS orders (
            order_id    TEXT PRIMARY KEY,
            customer_id TEXT NOT NULL,
            order_date  TEXT NOT NULL,
            order_status TEXT,
            FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
        );

        CREATE TABLE IF NOT EXISTS order_items (
            item_id    TEXT PRIMARY KEY,
            order_id   TEXT NOT NULL,
            product_id TEXT NOT NULL,
            quantity   INTEGER NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders (order_id),
            FOREIGN KEY (product_id) REFERENCES products (product_id)
        );

        CREATE TABLE IF NOT EXISTS payments (
            payment_id     TEXT PRIMARY KEY,
            order_id       TEXT NOT NULL,
            payment_amount REAL NOT NULL,
            payment_mode   TEXT,
            payment_date   TEXT NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders (order_id)
        );
        """
    )


def truncate_tables(conn: sqlite3.Connection) -> None:
    # Delete children before parents to satisfy foreign key constraints.
    conn.execute("DELETE FROM payments")
    conn.execute("DELETE FROM order_items")
    conn.execute("DELETE FROM orders")
    conn.execute("DELETE FROM products")
    conn.execute("DELETE FROM customers")


def load_csv_rows(filename: str) -> list[dict[str, str]]:
    path = DATA_DIR / filename
    with path.open(newline="", encoding="utf-8") as csvfile:
        return list(csv.DictReader(csvfile))


def insert_customers(conn: sqlite3.Connection) -> None:
    rows = load_csv_rows("customers.csv")
    conn.executemany(
        """
        INSERT INTO customers (customer_id, full_name, email, city, created_at)
        VALUES (:customer_id, :full_name, :email, :city, :created_at)
        """,
        rows,
    )


def insert_products(conn: sqlite3.Connection) -> None:
    rows = load_csv_rows("products.csv")
    formatted = [
        {
            **row,
            "price": float(row["price"]) if row["price"] else None,
        }
        for row in rows
    ]
    conn.executemany(
        """
        INSERT INTO products (product_id, product_name, category, price)
        VALUES (:product_id, :product_name, :category, :price)
        """,
        formatted,
    )


def insert_orders(conn: sqlite3.Connection) -> None:
    rows = load_csv_rows("orders.csv")
    conn.executemany(
        """
        INSERT INTO orders (order_id, customer_id, order_date, order_status)
        VALUES (:order_id, :customer_id, :order_date, :order_status)
        """,
        rows,
    )


def insert_order_items(conn: sqlite3.Connection) -> None:
    rows = load_csv_rows("order_items.csv")
    formatted = [
        {
            **row,
            "quantity": int(row["quantity"]),
        }
        for row in rows
    ]
    conn.executemany(
        """
        INSERT INTO order_items (item_id, order_id, product_id, quantity)
        VALUES (:item_id, :order_id, :product_id, :quantity)
        """,
        formatted,
    )


def insert_payments(conn: sqlite3.Connection) -> None:
    rows = load_csv_rows("payments.csv")
    formatted = [
        {
            **row,
            "payment_amount": float(row["payment_amount"]),
        }
        for row in rows
    ]
    conn.executemany(
        """
        INSERT INTO payments (
            payment_id,
            order_id,
            payment_amount,
            payment_mode,
            payment_date
        )
        VALUES (
            :payment_id,
            :order_id,
            :payment_amount,
            :payment_mode,
            :payment_date
        )
        """,
        formatted,
    )


def main() -> None:
    if not DATA_DIR.exists():
        raise FileNotFoundError(f"Data directory not found: {DATA_DIR}")

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("PRAGMA foreign_keys = ON;")

        create_tables(conn)
        truncate_tables(conn)

        insert_customers(conn)
        insert_products(conn)
        insert_orders(conn)
        insert_order_items(conn)
        insert_payments(conn)

        conn.commit()

    print("Successfully imported CSV data into ecommerce.db")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # pylint: disable=broad-except
        print(f"Data import failed: {exc}")

