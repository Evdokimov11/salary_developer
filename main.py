import requests
import os

from datetime import date
from dateutil.relativedelta import relativedelta
from terminaltables import AsciiTable
from dotenv import load_dotenv


def predict_salary(salary_from, salary_to):

    if salary_from and salary_to:

        expected_salary = (salary_from + salary_to)/2
    else:

        if salary_from:

            expected_salary = salary_from * 1.2  

        else:

            expected_salary = salary_to * 0.8

    return expected_salary

  
def predict_rub_salary_hh(vacancy):

    expected_salary = None

    if vacancy['salary'] and vacancy['salary']['currency'] == 'RUR':

        expected_salary = predict_salary(vacancy['salary']['from'], vacancy['salary']['to'])
  
    return expected_salary


def predict_rub_salary_sj(vacancy):

    expected_salary = None 
    
    if (vacancy['payment_from'] or vacancy['payment_to']) and vacancy['currency'] == 'rub':

        expected_salary = predict_salary(vacancy['payment_from'], vacancy['payment_to'])
  
    return expected_salary


def print_table(languages_processed_vacancies, title):

    table_data = [['Язык программирования','Вакансий найдено',
                   'Вакансий обработано','Средняя зарплата']]
    
    for language, language_processed_vacancies in languages_processed_vacancies.items():
    
      table_data.append([language,            
                         language_processed_vacancies['vacancies_found'],
                         language_processed_vacancies['vacancies_processed'],
                         language_processed_vacancies['average_salary']
                        ])
      
    table = AsciiTable(table_data, title)
    print(table.table)


def process_languages_hh(programming_languages):

    url = 'https://api.hh.ru/vacancies'

    languages_processed_vacancies = {}

    salaries = []

    for programming_language in programming_languages :
    
        params = {  
                'text' : f'Программист {programming_language}',
                'area' : 1,
                'date_from': date.today() - relativedelta(months=1)
        }
      
        response = requests.get(url, params=params)
      
        response.raise_for_status()
      
        response_formatted = response.json()
      
        sum_vacancies = response_formatted['found']
      
        vacancies = response_formatted['items']
        
        salaries.clear()
      
        for vacancy in vacancies :
      
            expected_salary = predict_rub_salary_hh(vacancy)
      
            if expected_salary:
            
                salaries.append(expected_salary)
              
        if  salaries:
        
            average_salary = sum(salaries)/len(salaries)
      
        else:
      
            average_salary = 'Вакансий не найдено'
        
        languages_processed_vacancies[programming_language] = { 
              "vacancies_found": sum_vacancies,
              "vacancies_processed": len(salaries),
              "average_salary": average_salary
          }
      
    return languages_processed_vacancies


def process_languages_sj(programming_languages, api_key):
      
    url = 'https://api.superjob.ru/2.0/vacancies/'
    
    languages_processed_vacancies= {}
    
    salaries = []
    
    headers = {
       'X-Api-App-Id':api_key, 
      }
    
    for programming_language in programming_languages :
    
        params = {
           'keyword': f'Программист {programming_language}',
           'catalogues':33, 
           'town':4
          }
          
        response = requests.get(url, headers=headers, params=params)
        
        response_formatted = response.json()
        
        vacancies = response_formatted['objects']
        
        average_salary = 0
        
        salaries.clear()
      
        for vacancy in vacancies:
    
            expected_salary = predict_rub_salary_sj(vacancy)
        
            if expected_salary:
              
                 salaries.append(expected_salary)
        
        if len(salaries):
        
            average_salary = sum(salaries) / len(salaries)
    
        else:
    
            average_salary = 'Вакансии не найдены'
        
        languages_processed_vacancies[programming_language] = {
                "average_salary": average_salary,
                "vacancies_found": response_formatted['total'],
                "vacancies_processed": len(salaries)
        }
    
    return languages_processed_vacancies


if __name__ == "__main__":

  load_dotenv()

  api_key_sj = os.environ['API_KEY_SJ']

  programming_languages = ['JavaScript','Java','Python','Ruby','PHP','C++','C#', 'C']

  processed_languages_hh = process_languages_hh(programming_languages)

  processed_languages_sj = process_languages_sj(programming_languages, api_key_sj)

  print_table(processed_languages_hh, 'HeadHunter Moscow')

  print_table(processed_languages_sj, 'SuperJob Moscow')
  











