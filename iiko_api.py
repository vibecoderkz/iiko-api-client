import requests
import json


def get_iiko_access_token(api_login):
    """
    Получает токен доступа от iiko API

    Args:
        api_login (str): API логин для iiko

    Returns:
        dict: Ответ от API с correlationId и token
    """
    url = "https://api-ru.iiko.services/api/1/access_token"

    payload = {
        "apiLogin": api_login
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе: {e}")
        return None


def get_organizations(token, organization_ids=None, return_additional_info=True,
                     include_disabled=True, return_external_data=None):
    """
    Получает список организаций от iiko API

    Args:
        token (str): Токен доступа
        organization_ids (list): Список ID организаций (опционально)
        return_additional_info (bool): Возвращать дополнительную информацию
        include_disabled (bool): Включать отключенные организации
        return_external_data (list): Список внешних данных для возврата

    Returns:
        dict: Ответ от API со списком организаций
    """
    url = "https://api-ru.iiko.services/api/1/organizations"

    payload = {
        "returnAdditionalInfo": return_additional_info,
        "includeDisabled": include_disabled
    }

    if organization_ids:
        payload["organizationIds"] = organization_ids

    if return_external_data:
        payload["returnExternalData"] = return_external_data

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе организаций: {e}")
        return None


def get_nomenclature(token, organization_id, start_revision="0"):
    """
    Получает меню (номенклатуру) от iiko API

    Args:
        token (str): Токен доступа
        organization_id (str): ID организации
        start_revision (str): Начальная ревизия (по умолчанию "0")

    Returns:
        dict: Ответ от API с меню (группы, продукты, размеры)
    """
    url = "https://api-ru.iiko.services/api/1/nomenclature"

    payload = {
        "organizationId": organization_id,
        "startRevision": start_revision
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе меню: {e}")
        return None


def get_terminal_groups(token, organization_ids, include_disabled=True, return_external_data=None):
    """
    Получает список групп терминалов от iiko API

    Args:
        token (str): Токен доступа
        organization_ids (list): Список ID организаций
        include_disabled (bool): Включать отключенные группы терминалов
        return_external_data (list): Список внешних данных для возврата

    Returns:
        dict: Ответ от API со списком групп терминалов
    """
    url = "https://api-ru.iiko.services/api/1/terminal_groups"

    payload = {
        "organizationIds": organization_ids,
        "includeDisabled": include_disabled
    }

    if return_external_data:
        payload["returnExternalData"] = return_external_data

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе групп терминалов: {e}")
        return None


def create_order(token, organization_id, terminal_group_id, order_data, settings=None):
    """
    Создает заказ через iiko API

    Args:
        token (str): Токен доступа
        organization_id (str): ID организации
        terminal_group_id (str): ID группы терминалов
        order_data (dict): Данные заказа
        settings (dict): Настройки создания заказа

    Returns:
        dict: Ответ от API с информацией о созданном заказе
    """
    url = "https://api-ru.iiko.services/api/1/order/create"

    if settings is None:
        settings = {
            "servicePrint": False,
            "transportToFrontTimeout": 0,
            "checkStopList": False
        }

    payload = {
        "organizationId": organization_id,
        "terminalGroupId": terminal_group_id,
        "order": order_data,
        "createOrderSettings": settings
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    try:
        print("Отправляемые данные заказа:")
        print(json.dumps(payload, indent=2, ensure_ascii=False))

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code != 200:
            print(f"Ошибка HTTP {response.status_code}: {response.reason}")
            try:
                error_data = response.json()
                print("Детали ошибки:")
                print(json.dumps(error_data, indent=2, ensure_ascii=False))
            except:
                print("Текст ошибки:", response.text)
            return None

        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при создании заказа: {e}")
        return None


def get_available_restaurant_sections(token, terminal_group_ids, return_schema=True, revision=0):
    """
    Получает доступные секции ресторана и столы от iiko API

    Args:
        token (str): Токен доступа
        terminal_group_ids (list): Список ID групп терминалов
        return_schema (bool): Возвращать схему расположения
        revision (int): Ревизия для обновления

    Returns:
        dict: Ответ от API с секциями ресторана и столами
    """
    url = "https://api-ru.iiko.services/api/1/reserve/available_restaurant_sections"

    payload = {
        "terminalGroupIds": terminal_group_ids,
        "returnSchema": return_schema,
        "revision": revision
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе секций ресторана: {e}")
        return None


def get_order_by_id(token, order_ids=None, organization_ids=None, pos_order_ids=None, source_keys=None, return_external_data_keys=None):
    """
    Получает заказы по ID от iiko API

    Args:
        token (str): Токен доступа
        order_ids (list): Список ID заказов
        organization_ids (list): Список ID организаций
        pos_order_ids (list): Список POS ID заказов
        source_keys (list): Список ключей источников
        return_external_data_keys (list): Ключи внешних данных для возврата

    Returns:
        dict: Ответ от API с информацией о заказах
    """
    url = "https://api-ru.iiko.services/api/1/order/by_id"

    payload = {}

    if order_ids:
        payload["orderIds"] = order_ids
    if organization_ids:
        payload["organizationIds"] = organization_ids
    if pos_order_ids:
        payload["posOrderIds"] = pos_order_ids
    if source_keys:
        payload["sourceKeys"] = source_keys
    if return_external_data_keys:
        payload["returnExternalDataKeys"] = return_external_data_keys

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе заказа: {e}")
        return None