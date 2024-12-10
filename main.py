from src.staticmethod import get_company, get_company_vacancies
from src.config import config
from src.utils import (create_list_vacs,
                       create_database,
                       create_tables,
                       save_to_table_vacs,
                       save_to_table_comps,
                       create_list_comps)
from src.db import DB_Manager


def main():
    params = config()
    list_company = ['Т-Банк', 'Яндекс', 'Аэрофлот', 'S7 Airlines']

    companies = get_company(list_company)
    vacancies = get_company_vacancies(companies)
    new_vacs = create_list_vacs(vacancies)
    new_comp = create_list_comps(companies)
    create_database('hh_parsing', params)
    create_tables('hh_parsing', params)
    save_to_table_comps(new_comp, 'hh_parsing', params)
    save_to_table_vacs(new_vacs, 'hh_parsing', params)

    db = DB_Manager()
    print('Список всех компаний и количество вакансий у каждой компании: ')
    for query in db.get_companies_and_vacancies_count('hh_parsing', params):
        print(f'Наименование компании: "{query[0]}" - открытых вакансий: {query[1]}')

    print('\nОбщий список вакансий')
    for query in db.get_all_vacancies('hh_parsing', params):
        print(f'Наименование компании: "{query[0]}".'
              f'Вакансия: {query[1]}. Зарплата от: {query[2]}.'
              f'Ссылка на вакансию: {query[3]} ')

    for query in db.get_avg_salary('hh_parsing', params):
        print(f'\nСредняя зарплата по вакансиям: "{int(query[0])}".')

    print('\nТоп-10 высокооплачиваемых вакансий: ')
    for query in db.get_vacancies_with_higher_salary('hh_parsing', params):
        print(f'Наименование компании: "{query[0]}".'
              f'Вакансия: {query[1]}. Зарплата от: {query[2]}.'
              f'Ссылка на вакансию: {query[3]} ')

    user_query = input("Введите интересующую вас вакансию: ").strip().lower()
    for query in db.get_vacancies_with_keyword('hh_parsing', params, user_query):
        if user_query in query[1]:
            print(f'Наименование компании: "{query[0]}".'
                  f' Вакансия: {query[1]}. Зарплата от: {query[2]}. '
                  f'Ссылка на вакансию: {query[3]} ')
        elif user_query not in query[1]:
            print("Извините, такой вакансии нет")


if __name__ == '__main__':
    main()
