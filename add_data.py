# import requests
# import psycopg2
# import uuid
# from datetime import datetime
# from decouple import config


# # Insert into PostgreSQL
# conn = psycopg2.connect(
#     dbname=config('DB_NAME'),
#     user=config('DB_USER'),
#     password=config('DB_PASSWORD'),
#     host="localhost",
#     port="5432"
# )

# cur = conn.cursor()


# # Step 1: Fetch and clean data
# response = requests.get("https://dummyjson.com/products")
# products = response.json()['products']

# def get_category_id(category_name):
#     cur.execute("SELECT category_id FROM categories WHERE LOWER(category_name) = LOWER(%s)", (category_name,))
#     result = cur.fetchone()
#     if result:
#         return result[0]
#     else:
#         # Insert category if it doesn't exist
#         cur.execute("INSERT INTO categories (category_name) VALUES (%s) RETURNING category_id", (category_name,))
#         new_id = cur.fetchone()[0]
#         conn.commit()
#         return new_id

# for product in products:
#     category_name = product.get("category", "Uncategorized")
#     category_id = get_category_id(category_name)

#     title = product["title"]
#     price = float(product["price"])
#     description = product["description"][:500]
#     reviews = product.get("reviews", [])
#     review_comments = "; ".join([r["comment"] for r in reviews])[:600]
#     featured = product["stock"] > 50  # or set False by default
#     quantity = product["stock"]
#     rating_avg = round(float(product.get("rating", 0.0)), 2)
#     rating_count = len(reviews)

#     cur.execute("""
#         INSERT INTO products (category_id, product_name, price, description, prod_reviews, featured, quantity, rating_average, rating_count)
#         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
#     """, (
#         category_id, title, price, description, review_comments, featured, quantity, rating_avg, rating_count
#     ))

# conn.commit()
# cur.close()
# conn.close()
# print("Products inserted successfully.")
