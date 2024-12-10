import requests


@staticmethod
def get_company(company_list) -> list:
    """
    Статикметод, который получает данные о работодателях с апи по определенным параметрам,
    если код ответа верный, то формирует список данных по определенным ключам.
    """
    url = 'https://api.hh.ru/employers'
    comp_list = []
    for company in company_list:
        response = requests.get(url, params={
            'text': company,
            'page': 0,
            'per_page': 100,
            'area': 113,
            'only_with_vacancies': True,
            'only_with_salary': True
        })
        if response.status_code != 200:
            print(f"Ошибка {response.status_code}")
        else:
            companies = response.json()['items']
            for item in companies:
                comp_list.append({
                    'employer_id': item['id'],
                    'name': item['name'],
                    'url': item['alternate_url'],
                    'vacancies_url': item['vacancies_url'],
                    'open_vacancies': item['open_vacancies'],
                })
    return comp_list


@staticmethod
def get_company_vacancies(companies_list) -> list:
    """
    Статикметод, который получает вакансии с ранее полученных данных о работодателях,
    если код ответа верный, то формирует список данных по определенным ключам.
    """
    vacs_list = []
    for company in companies_list:
        vacancies_url = company['vacancies_url']
        response = requests.get(vacancies_url)
        if response.status_code != 200:
            print(f'Ошибка {response.status_code}')
        else:
            vacs = response.json()['items']
            for item in vacs:
                vacs_list.append(item)
    return vacs_list
