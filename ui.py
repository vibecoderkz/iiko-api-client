import json


def select_organization(organizations):
    """
    Позволяет пользователю выбрать организацию из списка

    Args:
        organizations (list): Список организаций

    Returns:
        str: ID выбранной организации или None
    """
    if not organizations:
        return None

    print("\nДоступные организации:")
    for i, org in enumerate(organizations, 1):
        print(f"{i}. {org.get('name', 'Без названия')} (ID: {org['id']})")

    while True:
        try:
            choice = input(f"\nВыберите организацию (1-{len(organizations)}): ")
            index = int(choice) - 1
            if 0 <= index < len(organizations):
                return organizations[index]['id']
            else:
                print("Неверный номер организации")
        except ValueError:
            print("Введите число")


def select_terminal_group(terminal_groups):
    """
    Позволяет пользователю выбрать группу терминалов из списка

    Args:
        terminal_groups (list): Список групп терминалов

    Returns:
        str: ID выбранной группы терминалов или None
    """
    if not terminal_groups:
        return None

    all_terminals = []
    for org_terminals in terminal_groups:
        items = org_terminals.get('items', [])
        all_terminals.extend(items)

    if not all_terminals:
        print("Группы терминалов не найдены")
        return None

    print("\nДоступные группы терминалов:")
    for i, terminal in enumerate(all_terminals, 1):
        name = terminal.get('name', 'Без названия')
        address = terminal.get('address', 'Адрес не указан')
        print(f"{i}. {name} - {address} (ID: {terminal['id']})")

    while True:
        try:
            choice = input(f"\nВыберите группу терминалов (1-{len(all_terminals)}): ")
            index = int(choice) - 1
            if 0 <= index < len(all_terminals):
                return all_terminals[index]['id']
            else:
                print("Неверный номер группы терминалов")
        except ValueError:
            print("Введите число")


def select_product_from_menu(products):
    """
    Позволяет пользователю выбрать продукт из меню

    Args:
        products (list): Список продуктов

    Returns:
        dict: Выбранный продукт или None
    """
    if not products:
        return None

    print("\nДоступные продукты (первые 20):")
    display_products = products[:20]

    for i, product in enumerate(display_products, 1):
        price = "Цена не указана"
        if product.get('sizePrices') and len(product['sizePrices']) > 0:
            current_price = product['sizePrices'][0].get('price', {}).get('currentPrice')
            if current_price:
                price = f"{current_price} руб."

        print(f"{i}. {product.get('name', 'Без названия')} - {price}")

    while True:
        try:
            choice = input(f"\nВыберите продукт (1-{len(display_products)}): ")
            index = int(choice) - 1
            if 0 <= index < len(display_products):
                return display_products[index]
            else:
                print("Неверный номер продукта")
        except ValueError:
            print("Введите число")


def display_order_info(order_data):
    """
    Отображает информацию о заказе в удобном формате

    Args:
        order_data (dict): Данные о заказе
    """
    if not order_data:
        print("Нет данных о заказе")
        return

    print(f"\n📋 Информация о заказе:")
    print(f"ID: {order_data.get('id', 'не указан')}")
    print(f"POS ID: {order_data.get('posId', 'не указан')}")
    print(f"Внешний номер: {order_data.get('externalNumber', 'не указан')}")
    print(f"Статус создания: {order_data.get('creationStatus', 'не указан')}")

    if order_data.get('errorInfo'):
        error = order_data['errorInfo']
        print(f"❌ Ошибка: {error.get('message', 'не указана')}")
        print(f"Описание: {error.get('description', 'не указано')}")

    order_details = order_data.get('order')
    if order_details:
        print(f"\n📦 Детали заказа:")
        print(f"Номер: {order_details.get('number', 'не указан')}")
        print(f"Статус: {order_details.get('status', 'не указан')}")
        print(f"Сумма: {order_details.get('sum', 0)} руб.")
        print(f"Время создания: {order_details.get('whenCreated', 'не указано')}")

        customer = order_details.get('customer')
        if customer:
            print(f"Клиент: {customer.get('name', 'не указан')}")

        items = order_details.get('items', [])
        if items:
            print(f"Позиций в заказе: {len(items)}")
            for i, item in enumerate(items, 1):
                print(f"  {i}. Количество: {item.get('amount', 0)}, Статус: {item.get('status', 'не указан')}")

        payments = order_details.get('payments', [])
        if payments:
            print(f"Платежей: {len(payments)}")
            total_paid = sum(p.get('sum', 0) for p in payments)
            print(f"Оплачено: {total_paid} руб.")
    else:
        print("Детали заказа недоступны (возможно, заказ еще обрабатывается)")


def print_menu_stats(menu_result):
    """
    Выводит статистику по меню

    Args:
        menu_result (dict): Результат запроса меню
    """
    if menu_result:
        print("\nМеню получено:")
        print(f"Групп: {len(menu_result.get('groups', []))}")
        print(f"Категорий продуктов: {len(menu_result.get('productCategories', []))}")
        print(f"Продуктов: {len(menu_result.get('products', []))}")
        print(f"Размеров: {len(menu_result.get('sizes', []))}")
        print(f"Ревизия: {menu_result.get('revision', 'не указана')}")


def save_menu_to_file(menu_result, organization_id):
    """
    Сохраняет меню в файл

    Args:
        menu_result (dict): Результат запроса меню
        organization_id (str): ID организации

    Returns:
        str: Имя созданного файла или None
    """
    save_choice = input("\nСохранить полные данные в файл? (y/n): ")
    if save_choice.lower() == 'y':
        filename = f"menu_{organization_id}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(menu_result, f, indent=2, ensure_ascii=False)
        print(f"Меню сохранено в файл: {filename}")
        return filename
    return None


def select_table(restaurant_sections):
    """
    Позволяет пользователю выбрать стол из доступных секций ресторана

    Args:
        restaurant_sections (list): Список секций ресторана с столами

    Returns:
        dict: Выбранный стол с информацией о секции или None
    """
    if not restaurant_sections:
        print("Нет доступных секций ресторана")
        return None

    # Собираем все столы из всех секций
    all_tables = []
    for section in restaurant_sections:
        section_name = section.get('name', 'Без названия')
        tables = section.get('tables', [])
        for table in tables:
            if not table.get('isDeleted', False):  # Исключаем удаленные столы
                table_info = {
                    'table': table,
                    'section': section,
                    'section_name': section_name
                }
                all_tables.append(table_info)

    if not all_tables:
        print("Нет доступных столов")
        return None

    print("\nДоступные столы:")
    for i, table_info in enumerate(all_tables, 1):
        table = table_info['table']
        section_name = table_info['section_name']
        table_name = table.get('name', f"Стол {table.get('number', 'без номера')}")
        capacity = table.get('seatingCapacity', 0)
        print(f"{i}. {table_name} (Секция: {section_name}, Вместимость: {capacity} чел.)")

    while True:
        try:
            choice = input(f"\nВыберите стол (1-{len(all_tables)}): ")
            index = int(choice) - 1
            if 0 <= index < len(all_tables):
                return all_tables[index]
            else:
                print("Неверный номер стола")
        except ValueError:
            print("Введите число")


def get_customer_input():
    """
    Получает данные от пользователя для создания заказа

    Returns:
        tuple: (amount, customer_name)
    """
    amount = input("Введите количество (по умолчанию 1): ")
    try:
        amount = int(amount) if amount else 1
    except ValueError:
        amount = 1

    customer_name = input("Введите имя клиента (по умолчанию 'Тестовый заказ'): ")
    if not customer_name:
        customer_name = "Тестовый заказ"

    return amount, customer_name