import psycopg2


def create_list_vacs(employer_ids) -> list:
    """
    Метод преобразования полученных данных из апи
    в необходимы нам формат с необходимыми полями.
    Если зарплата в вакансии не указана - возвращает 0.
    """
    data = []
    for employer_id in employer_ids:
        data.append({
            'company_id': employer_id.get('employer').get('id'),
            'company_name': employer_id.get('employer').get('name'),
            'vac_title': employer_id.get('name'),
            'vac_city': employer_id.get('area').get('name'),
            'vac_salary_from': employer_id.get('salary').get('from') if employer_id["salary"] is not None else 0,
            'vac_salary_to': employer_id.get('salary').get('to') if employer_id["salary"] is not None else 0,
            'link': employer_id.get('alternate_url'),
        })
    return data


def create_list_comps(companies):
    """ Метод преобразования полученных данных по компаниям. """
    data = []
    for company in companies:
        data.append({
            'company_id': company.get('employer_id'),
            'company_name': company.get('name'),
            'vacancies_url': company.get('vacancies_url'),
            'open_vacancies': company.get('open_vacancies')
        })
    return data


def create_database(database_name: str, params: dict):
    """ Метод создания БД. """
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True  # каждый sql-запрос будет коммититься
    cur = conn.cursor()
    cur.execute(f'DROP DATABASE IF EXISTS {database_name}')
    cur.execute(f'CREATE DATABASE {database_name}')
    cur.close()
    conn.close()


def create_tables(database_name: str, params: dict) -> None:
    """ Метод создания таблицы в БД. """
    conn = psycopg2.connect(dbname=database_name, **params)
    with conn.cursor() as cur:
        cur.execute("""
                CREATE TABLE vacancies (
                    company_id VARCHAR(50),
                    company_name VARCHAR(100),
                    vacancy_title TEXT,
                    city VARCHAR(100),
                    salary_from INTEGER,
                    salary_to INTEGER,
                    link_on TEXT
                    );
                CREATE TABLE companies (
                    company_id VARCHAR(50),
                    company_name VARCHAR(100),
                    vacancies_url TEXT,
                    open_vacancies INTEGER
                    );
            """)
    conn.commit()
    conn.close()


def save_to_table_vacs(data: list[dict], database_name: str, params: dict) -> None:
    """ Метод заполнения таблицы БД. """
    conn = psycopg2.connect(dbname=database_name, **params)
    with conn.cursor() as cur:
        for item in data:
            cur.execute(
                """
                INSERT INTO vacancies VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (item.get('company_id'),
                 item.get('company_name'),
                 item.get('vac_title'),
                 item.get('vac_city'),
                 item.get('vac_salary_from'),
                 item.get('vac_salary_to'),
                 item.get('link'))
            )
    conn.commit()
    conn.close()


def save_to_table_comps(data: list[dict], database_name: str, params: dict) -> None:
    """ Метод заполнения таблицы компании БД. """
    conn = psycopg2.connect(dbname=database_name, **params)
    with conn.cursor() as cur:
        for item in data:
            cur.execute(
                """
                INSERT INTO companies
                (company_id, company_name, vacancies_url, open_vacancies)
                VALUES (%s, %s, %s, %s)
                """,
                (item.get('company_id'),
                 item.get('company_name'),
                 item.get('vacancies_url'),
                 item.get('open_vacancies'))
            )
    conn.commit()
    conn.close()
    