import json
from iiko_api import (
    get_iiko_access_token,
    get_organizations,
    get_nomenclature,
    get_terminal_groups,
    get_available_restaurant_sections,
    create_order,
    get_order_by_id
)
from ui import (
    select_organization,
    select_terminal_group,
    select_table,
    select_product_from_menu,
    display_order_info,
    print_menu_stats,
    save_menu_to_file,
    get_customer_input
)
from order_utils import (
    build_simple_order,
    get_product_size_and_price
)


def main():
    print("iiko API Client")
    print("=" * 30)

    api_login = input("Введите apiLogin: ")

    if not api_login:
        print("API логин не может быть пустым!")
        return

    print("Получение токена доступа...")
    token_result = get_iiko_access_token(api_login)

    if not token_result or 'token' not in token_result:
        print("Не удалось получить токен")
        return

    token = token_result['token']
    print(f"Токен получен: {token_result['correlationId']}")

    print("\nПолучение списка организаций...")
    organizations_result = get_organizations(token)

    if not organizations_result or 'organizations' not in organizations_result:
        print("Не удалось получить список организаций")
        return

    organizations = organizations_result['organizations']
    organization_id = select_organization(organizations)

    if not organization_id:
        print("Организация не выбрана")
        return

    print(f"\nПолучение меню для организации {organization_id}...")
    menu_result = get_nomenclature(token, organization_id)

    if menu_result:
        print_menu_stats(menu_result)
        save_menu_to_file(menu_result, organization_id)

        create_test_order = input("\nСоздать тестовый заказ? (y/n): ")
        if create_test_order.lower() == 'y':
            products = menu_result.get('products', [])
            if not products:
                print("В меню нет продуктов для заказа")
                return

            print("\nПолучение групп терминалов...")
            terminal_groups_result = get_terminal_groups(token, [organization_id])

            if not terminal_groups_result or 'terminalGroups' not in terminal_groups_result:
                print("Не удалось получить группы терминалов")
                return

            terminal_groups = terminal_groups_result['terminalGroups']
            terminal_group_id = select_terminal_group(terminal_groups)

            if not terminal_group_id:
                print("Группа терминалов не выбрана")
                return

            print("\nПолучение доступных столов...")
            sections_result = get_available_restaurant_sections(token, [terminal_group_id])

            selected_table_info = None
            if sections_result and sections_result.get('restaurantSections'):
                restaurant_sections = sections_result['restaurantSections']
                selected_table_info = select_table(restaurant_sections)

                if not selected_table_info:
                    print("Стол не выбран, заказ будет создан без привязки к столу")
            else:
                print("Не удалось получить информацию о столах, заказ будет создан без привязки к столу")

            selected_product = select_product_from_menu(products)
            if not selected_product:
                print("Продукт не выбран")
                return

            product_size_id, price = get_product_size_and_price(selected_product)

            if product_size_id is not None:
                print(f"Используемый productSizeId: {product_size_id}")
            else:
                print("ProductSizeId не указывается (продукт без размеров)")
            print(f"Цена продукта: {price}")

            amount, customer_name = get_customer_input()

            # Подготавливаем список ID столов если стол выбран
            table_ids = None
            if selected_table_info:
                table_ids = [selected_table_info['table']['id']]
                table_name = selected_table_info['table'].get('name', f"Стол {selected_table_info['table'].get('number', 'без номера')}")
                print(f"Заказ будет привязан к столу: {table_name}")

            print(f"\nСоздание заказа с продуктом: {selected_product['name']}")
            order_data = build_simple_order(
                selected_product['id'],
                product_size_id,
                price,
                amount,
                customer_name,
                table_ids=table_ids
            )

            order_result = create_order(token, organization_id, terminal_group_id, order_data)

            if order_result:
                print("\nЗаказ создан успешно!")
                order_info = order_result.get('orderInfo')

                if order_info:
                    print(f"ID заказа: {order_info.get('id', 'не указан')}")
                    print(f"Статус создания: {order_info.get('creationStatus', 'не указан')}")

                    order_details = order_info.get('order')
                    if order_details:
                        print(f"Номер заказа: {order_details.get('number', 'не указан')}")
                    else:
                        print("Номер заказа: не указан")

                    if order_info.get('errorInfo'):
                        print(f"Ошибка: {order_info['errorInfo'].get('message', 'Неизвестная ошибка')}")
                else:
                    print("Информация о заказе отсутствует в ответе")

                print("\nПолный ответ:")
                print(json.dumps(order_result, indent=2, ensure_ascii=False))

                # Предложить проверить статус заказа
                if order_info and order_info.get('id'):
                    check_status = input("\nПроверить статус заказа? (y/n): ")
                    if check_status.lower() == 'y':
                        order_id = order_info['id']
                        print(f"\nПроверка статуса заказа {order_id}...")

                        status_result = get_order_by_id(
                            token,
                            order_ids=[order_id],
                            organization_ids=[organization_id]
                        )

                        if status_result and status_result.get('orders'):
                            orders = status_result['orders']
                            if orders:
                                display_order_info(orders[0])
                            else:
                                print("Заказ не найден")
                        else:
                            print("Не удалось получить статус заказа")
            else:
                print("Не удалось создать заказ")
        else:
            print("\nПример данных:")
            print(json.dumps({
                "correlationId": menu_result.get('correlationId'),
                "revision": menu_result.get('revision'),
                "groups_count": len(menu_result.get('groups', [])),
                "products_count": len(menu_result.get('products', []))
            }, indent=2, ensure_ascii=False))
    else:
        print("Не удалось получить меню")


if __name__ == "__main__":
    main()