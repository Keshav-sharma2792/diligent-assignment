import csv
import os
import random
from datetime import datetime, timedelta


random.seed(42)

DATA_DIR = os.path.join("data")
NUM_CUSTOMERS = 100
NUM_PRODUCTS = 100
NUM_ORDERS = 100
NUM_ORDER_ITEMS = 130
NUM_PAYMENTS = NUM_ORDERS

FIRST_NAMES = [
    "Olivia", "Noah", "Emma", "Liam", "Amelia", "Mason", "Sophia", "Ethan", "Ava", "Logan",
    "Mia", "Lucas", "Isabella", "Aiden", "Charlotte", "Jackson", "Harper", "Sebastian", "Evelyn",
    "Benjamin", "Abigail", "Elijah", "Emily", "James", "Scarlett", "Henry", "Madison", "Daniel",
    "Layla", "Matthew", "Aria", "Samuel", "Chloe", "David", "Mila", "Carter", "Ellie", "Wyatt",
    "Luna"
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez",
    "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor",
    "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez",
    "Clark", "Ramirez", "Lewis", "Robinson", "Walker", "Young", "Allen", "King", "Wright",
    "Scott", "Torres", "Nguyen", "Hill", "Flores"
]

CITIES = [
    "New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio",
    "San Diego", "Dallas", "San Jose", "Austin", "Jacksonville", "San Francisco", "Columbus",
    "Fort Worth", "Indianapolis", "Charlotte", "Seattle", "Denver", "Washington"
]

CATEGORIES = [
    "Electronics", "Home & Kitchen", "Sports & Outdoors", "Fashion", "Beauty & Personal Care",
    "Books", "Toys & Games", "Automotive", "Pet Supplies", "Office Supplies"
]

ADJECTIVES = [
    "Advanced", "Compact", "Premium", "Eco", "Smart", "Wireless", "Portable", "Deluxe",
    "Classic", "Pro", "Ultra", "Lite", "Essential", "Signature", "Colorful"
]

PRODUCT_NOUNS = [
    "Headphones", "Blender", "Backpack", "Sneakers", "Watch", "Camera", "Vacuum", "Mixer",
    "Yoga Mat", "Helmet", "Desk Lamp", "Notebook", "Water Bottle", "Gaming Mouse", "Cookware Set",
    "Drone", "Sunglasses", "Bluetooth Speaker", "Smart Plug", "Fitness Tracker"
]

ORDER_STATUSES = ["Pending", "Processing", "Shipped", "Delivered", "Cancelled", "Returned"]
PAYMENT_MODES = ["Credit Card", "Debit Card", "PayPal", "Bank Transfer", "Gift Card", "Apple Pay"]


def random_date(start_days_ago=730, end_days_ago=1):
    now = datetime.now()
    start_date = now - timedelta(days=start_days_ago)
    end_date = now - timedelta(days=end_days_ago)
    delta = end_date - start_date
    return start_date + timedelta(days=random.randint(0, delta.days), hours=random.randint(0, 23), minutes=random.randint(0, 59))


def slugify_email(name):
    base = name.lower().replace(" ", ".")
    domains = ["example.com", "mail.com", "shopper.io", "retailhub.net"]
    return f"{base}{random.randint(1, 999)}@{random.choice(domains)}"


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def write_csv(path, headers, rows):
    with open(path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def generate_customers():
    customers = []
    for i in range(1, NUM_CUSTOMERS + 1):
        full_name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
        created_at = random_date(900, 30)
        customers.append({
            "customer_id": f"CUST{i:04d}",
            "full_name": full_name,
            "email": slugify_email(full_name),
            "city": random.choice(CITIES),
            "created_at": created_at.strftime("%Y-%m-%d %H:%M:%S")
        })
    return customers


def generate_products():
    products = []
    for i in range(1, NUM_PRODUCTS + 1):
        category = random.choice(CATEGORIES)
        product_name = f"{random.choice(ADJECTIVES)} {random.choice(PRODUCT_NOUNS)}"
        price = round(random.uniform(5.0, 500.0), 2)
        products.append({
            "product_id": f"PROD{i:04d}",
            "product_name": product_name,
            "category": category,
            "price": f"{price:.2f}"
        })
    return products


def generate_orders(customers):
    orders = []
    now = datetime.now()
    for i in range(1, NUM_ORDERS + 1):
        customer = random.choice(customers)
        customer_created = datetime.strptime(customer["created_at"], "%Y-%m-%d %H:%M:%S")
        order_date = customer_created + timedelta(days=random.randint(1, 360))
        if order_date > now:
            order_date = now - timedelta(days=random.randint(0, 14))
        order_status = random.choices(
            ORDER_STATUSES,
            weights=[10, 15, 25, 30, 10, 10],
            k=1
        )[0]
        orders.append({
            "order_id": f"ORD{i:04d}",
            "customer_id": customer["customer_id"],
            "order_date": order_date.strftime("%Y-%m-%d %H:%M:%S"),
            "order_status": order_status
        })
    return orders


def generate_order_items(orders, products):
    items = []
    # Ensure every order has at least one line item
    for order in orders:
        product = random.choice(products)
        items.append({
            "item_id": f"ITEM{len(items)+1:04d}",
            "order_id": order["order_id"],
            "product_id": product["product_id"],
            "quantity": random.randint(1, 4)
        })
    # Add additional items until target count is reached
    while len(items) < NUM_ORDER_ITEMS:
        order = random.choice(orders)
        product = random.choice(products)
        items.append({
            "item_id": f"ITEM{len(items)+1:04d}",
            "order_id": order["order_id"],
            "product_id": product["product_id"],
            "quantity": random.randint(1, 5)
        })
    return items


def generate_payments(orders, order_items, products_lookup):
    item_totals = {order["order_id"]: 0.0 for order in orders}
    for item in order_items:
        price = float(products_lookup[item["product_id"]]["price"])
        item_totals[item["order_id"]] += price * item["quantity"]

    payments = []
    for i, order in enumerate(orders, start=1):
        order_date = datetime.strptime(order["order_date"], "%Y-%m-%d %H:%M:%S")
        payment_date = order_date + timedelta(days=random.randint(0, 7))
        amount = item_totals[order["order_id"]]
        if amount == 0:
            amount = round(random.uniform(10.0, 200.0), 2)
        payments.append({
            "payment_id": f"PAY{i:04d}",
            "order_id": order["order_id"],
            "payment_amount": f"{amount:.2f}",
            "payment_mode": random.choice(PAYMENT_MODES),
            "payment_date": payment_date.strftime("%Y-%m-%d %H:%M:%S")
        })
    return payments


def main():
    ensure_dir(DATA_DIR)
    customers = generate_customers()
    products = generate_products()
    orders = generate_orders(customers)
    order_items = generate_order_items(orders, products)
    payments = generate_payments(orders, order_items, {p["product_id"]: p for p in products})

    write_csv(os.path.join(DATA_DIR, "customers.csv"),
              ["customer_id", "full_name", "email", "city", "created_at"], customers)
    write_csv(os.path.join(DATA_DIR, "products.csv"),
              ["product_id", "product_name", "category", "price"], products)
    write_csv(os.path.join(DATA_DIR, "orders.csv"),
              ["order_id", "customer_id", "order_date", "order_status"], orders)
    write_csv(os.path.join(DATA_DIR, "order_items.csv"),
              ["item_id", "order_id", "product_id", "quantity"], order_items)
    write_csv(os.path.join(DATA_DIR, "payments.csv"),
              ["payment_id", "order_id", "payment_amount", "payment_mode", "payment_date"], payments)


if __name__ == "__main__":
    main()

