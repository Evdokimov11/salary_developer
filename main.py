import requests
import os

from datetime import date
from dateutil.relativedelta import relativedelta
from terminaltables import AsciiTable
from dotenv import load_dotenv


def predict_salary(salary_from, salary_to):

  if salary_from and salary_to:
      return (salary_from + salary_to) / 2
  if not salary_from:
      return salary_to * 0.8
  if not salary_to:
      return salary_from * 1.2


def predict_rub_salary_hh(vacancy):

  expected_salary = None
  if vacancy['salary'] and vacancy['salary']['currency'] == 'RUR':
      expected_salary = predict_salary(vacancy['salary']['from'],vacancy['salary']['to'])

  return expected_salary


def predict_rub_salary_sj(vacancy):

  expected_salary = None
  if (vacancy['payment_from'] or vacancy['payment_to']) and vacancy['currency'] == 'rub':
      expected_salary = predict_salary(vacancy['payment_from'],vacancy['payment_to'])

  return expected_salary


def print_table(languages_processed_vacancies, title):

  table_vacancies_statistics = [[
    'Язык программирования', 'Вакансий найдено', 
    'Вакансий обработано','Средняя зарплата'
    ]]

  for language, language_processed_vacancies in languages_processed_vacancies.items():

      table_vacancies_statistics.append([
        language, language_processed_vacancies['vacancies_found'],
        language_processed_vacancies['vacancies_processed'],
        language_processed_vacancies['average_salary']
        ])

  table = AsciiTable(table_vacancies_statistics, title)
  print(table.table)


def process_languages_hh(programming_languages):

  hh_url = 'https://api.hh.ru/vacancies'
  languages_processed_vacancies = {}

  for programming_language in programming_languages:

      page = 0
      pages_number = 1
      hh_salaries = []
      hh_salaries.clear()

      while page < pages_number:

          hh_params = {
            'text': f'Программист {programming_language}',
            'area': 1,
            'date_from': date.today() - relativedelta(months=1),
            'page': page
            }
          hh_response = requests.get(hh_url, params=hh_params)
          hh_response.raise_for_status()
          hh_formatted_response = hh_response.json()
          pages_number = hh_formatted_response['pages']
          page += 1
          sum_vacancies = hh_formatted_response['found']
          vacancies = hh_formatted_response['items']

          for vacancy in vacancies:

              expected_salary = predict_rub_salary_hh(vacancy)
              if expected_salary:
                  hh_salaries.append(expected_salary)

      if hh_salaries:
          average_salary = sum(hh_salaries) / len(hh_salaries)
      else:
          average_salary = 'Вакансий не найдено'

      languages_processed_vacancies[programming_language] = {
        "vacancies_found": sum_vacancies,
        "vacancies_processed": len(hh_salaries),
        "average_salary": average_salary
        }

  return languages_processed_vacancies


def process_languages_sj(programming_languages, api_key):

  sj_url = 'https://api.superjob.ru/2.0/vacancies/'
  languages_processed_vacancies = {}
  sj_headers = {
    'X-Api-App-Id': api_key,
    }

  for programming_language in programming_languages:

      sj_salaries = []
      page = 0
      more_results = True
      sj_salaries.clear()
  
      while more_results:
  
          sj_params = {
            'keyword': f'Программист {programming_language}',
            'catalogues': 33,
            'town': 4,
            'page': page
            }
          sj_response = requests.get(sj_url, headers=sj_headers, params=sj_params)
          sj_formatted_response = sj_response.json()
          more_results = sj_formatted_response['more']
          vacancies = sj_formatted_response['objects']
          page += 1
    
          for vacancy in vacancies:
  
              expected_salary = predict_rub_salary_sj(vacancy)
              if expected_salary:
                sj_salaries.append(expected_salary)
  
      if len(sj_salaries):
          average_salary = sum(sj_salaries) / len(sj_salaries)
      else:
          average_salary = 'Вакансии не найдены'
  
      languages_processed_vacancies[programming_language] = {
        "average_salary": average_salary,
        "vacancies_found": sj_formatted_response['total'],
        "vacancies_processed": len(sj_salaries)
        }

  return languages_processed_vacancies


if __name__ == "__main__":

  load_dotenv()
  sj_api_key = os.environ['SJ_API_KEY']
  programming_languages = [
    'JavaScript', 'Java', 'Python', 'Ruby', 'PHP', 'C++', 'C#', 'C'
    ]
  processed_languages_hh = process_languages_hh(programming_languages)
  processed_languages_sj = process_languages_sj(programming_languages,sj_api_key)
  print_table(processed_languages_hh, 'HeadHunter Moscow')
  print_table(processed_languages_sj, 'SuperJob Moscow')
