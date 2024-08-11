from django.db import connection

def create_payment() -> int:
    with connection.cursor() as cursor:
        cursor.execute("CALL create_payment(NULL::INTEGER);")
        payment_id = cursor.fetchone()[0]
    return payment_id

def add_payment_detail(payment_id: int, product_id: int, quantity: int):
    with connection.cursor() as cursor:
        cursor.execute("CALL add_payment_detail(%s, %s, %s);", [payment_id, product_id, quantity])

def remove_payment_detail(payment_detail_id: int):
    with connection.cursor() as cursor:
        cursor.execute("CALL remove_payment_detail(%s);", [payment_detail_id])

def mark_payment_as_paid(payment_id):
    with connection.cursor() as cursor:
        cursor.execute("CALL mark_payment_as_paid(%s);", [payment_id])

def cancel_payment(payment_id: int):
    with connection.cursor() as cursor:
        cursor.execute("CALL cancel_payment(%s);", [payment_id])

def delete_cancelled_payments(payment_id: int):
    with connection.cursor() as cursor:
        cursor.execute("CALL delete_cancelled_payments(%s);", [payment_id])
