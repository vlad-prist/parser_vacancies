import psycopg2


class DB_Manager:
    """  Класс, который будет подключаться к БД PostgreSQL. """

    def __init__(self):
        self.data_base = 'hh_parsing'

    def get_companies_and_vacancies_count(self, data_base, params):
        """ Получает список всех компаний и кол-во вакансий у каждой компании. """
        with psycopg2.connect(dbname=data_base, **params) as conn:
            with conn.cursor() as cur:
                cur.execute("""SELECT company_name, COUNT(vacancy_title)
                            FROM vacancies GROUP BY company_name""")
                query = cur.fetchall()
        conn.close()
        return query

    def get_all_vacancies(self, data_base, params):
        """ Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию. """
        with psycopg2.connect(dbname=data_base, **params) as conn:
            with conn.cursor() as cur:
                cur.execute("""SELECT company_name, vacancy_title, salary_from, link_on
                            FROM vacancies""")
                query = cur.fetchall()
        conn.close()
        return query

    def get_avg_salary(self, data_base, params):
        """ Получает среднюю зарплату по вакансиям. """
        with psycopg2.connect(dbname=data_base, **params) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT AVG(salary_from) FROM vacancies")
                query = cur.fetchall()
        conn.close()
        return query

    def get_vacancies_with_higher_salary(self, data_base, params):
        """ Получает топ 10 высокооплачиваемых вакансий. """
        with psycopg2.connect(dbname=data_base, **params) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT company_name, vacancy_title, salary_from, link_on\n"
                            "                FROM vacancies\n"
                            "                WHERE salary_from not in (0)\n"
                            "                ORDER BY salary_from DESC\n"
                            "                LIMIT 10")
                query = cur.fetchall()
        conn.close()
        return query

    def get_vacancies_with_keyword(self, data_base, params, user_query):
        """ Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python. """
        with psycopg2.connect(dbname=data_base, **params) as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT company_name, vacancy_title, salary_from, link_on"
                            f" FROM vacancies WHERE vacancy_title LIKE '%{user_query}%'")
                query = cur.fetchall()
        conn.close()
        return query
