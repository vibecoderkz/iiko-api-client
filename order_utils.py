import uuid
from datetime import datetime


def build_simple_order(product_id, product_size_id, price, amount=1, customer_name="Тестовый заказ", order_type_id=None, price_category_id=None, table_ids=None):
    """
    Создает простой заказ с одним продуктом

    Args:
        product_id (str): ID продукта
        product_size_id (str): ID размера продукта
        price (float): Цена за единицу
        amount (int): Количество
        customer_name (str): Имя клиента
        order_type_id (str): ID типа заказа
        price_category_id (str): ID категории цен
        table_ids (list): Список ID столов

    Returns:
        dict: Данные заказа
    """
    order_id = str(uuid.uuid4())

    item = {
        "productId": product_id,
        "price": price,
        "type": "Product",
        "amount": amount,
        "comment": ""
    }

    # Добавляем productSizeId только если он не None
    if product_size_id is not None:
        item["productSizeId"] = product_size_id

    order = {
        "id": order_id,
        "externalNumber": f"TEST-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
        "customer": {
            "id": str(uuid.uuid4()),
            "name": customer_name,
            "gender": "NotSpecified",
            "type": "one_time"
        },
        "phone": "77777777777",
        "guestCount": 1,
        "guests": {
            "count": 1
        },
        "items": [item],
        "combos": [],
        "payments": [],
        "tips": [],
        "sourceKey": "api-test"
    }

    if order_type_id:
        order["orderTypeId"] = order_type_id

    if price_category_id:
        order["priceCategoryId"] = price_category_id

    if table_ids:
        order["tableIds"] = table_ids

    return order


def get_product_size_and_price(selected_product):
    """
    Извлекает ID размера продукта и цену из выбранного продукта

    Args:
        selected_product (dict): Выбранный продукт

    Returns:
        tuple: (product_size_id, price)
    """
    product_size_id = None
    price = 0

    if selected_product.get('sizePrices') and len(selected_product['sizePrices']) > 0:
        size_info = selected_product['sizePrices'][0]
        # Если sizeId есть и не null, используем его
        if size_info.get('sizeId') is not None:
            product_size_id = size_info['sizeId']
        else:
            # Если sizeId равен null, НЕ указываем productSizeId вообще
            # Для продуктов без размеров это поле должно отсутствовать
            product_size_id = None

        # Получаем цену из sizePrices
        price_info = size_info.get('price', {})
        price = price_info.get('currentPrice', 0)
    else:
        # Если sizePrices отсутствует, также не указываем productSizeId
        product_size_id = None

    return product_size_id, price