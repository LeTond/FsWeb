from ..Backend.add_to_sqlite import AddToSQL
from ..Backend.json_worker import Json
from ..Backend.log_files import Log
from ..Backend.parsing_aseg_stats import ParsingResults
from ..Configuration.key_words_and_directories_list import home_directory, projects_paths

import os


class Obs:
    """
    Запускаем обсервер, который будет отслеживать состояние в директории с данными субъектов исследования и
    по-необходимости добавлять обсчитанные данные в БД.
    """
    def __init__(self):
        self.projects_paths = projects_paths
        self.home_directory = home_directory
        self.lg = Log()
        self.json = Json()
        self.sql = AddToSQL()
        self.pr = ParsingResults()
        self.structure_statistic = self.pr.structure_statistic_data
        self.main_statistic = self.pr.main_statistic_data

    def search_existing_projects(self) -> list:
        """
        Просматриваем и создает список с имеющимися обработанными исследованиями
        :return: Возвращает список с местонахождением файлов со статистикой (aseg.stats)
        """
        directs_list = []
        for directs, direct, files in os.walk(self.home_directory):
            for file in files:
                if 'aseg.stats' == file:
                    directs_list.append(directs)
        return directs_list

    def search_aseg_stats(self):
        """
        Просматривает наличие новых обработанных данных, добавляет их в спискок учета проектов (list_projects_path) и
        вызывает БД для сохранения статистических данных.
        :return: None
        """
        list_projects_paths = open(self.projects_paths, 'r')    # Открываем лог с сохранёнными проектами
        list_of_projects_path = list_projects_paths.read().split('\n')
        for project_path in self.search_existing_projects():
            if project_path not in list_of_projects_path:
                try:
                    self.save_new_project(self.pr.project_name(project_path), project_path)
                    write_to_list = open(self.projects_paths, 'a')
                    write_to_list.write(project_path + '\n')
                except ConnectionError:
                    self.lg.error_log_file(f"ConnectionError: {project_path}")
                    print("Ошибка подключения к БД")

    def save_new_project(self, project_key: str, project_path: str):
        """
        После прочтения json отправляем данные субъекта в базу данных, после чего удаляем эти данные
        из json файла с информацией о проектах по ключю project_name
        :param project_key: название проекта (ключ в json)
        :param project_path: путь к list_projects_paths.txt с информацией об исследованиях, сохраненных в БД
        :return: None
        """
        project_name = self.json.read_subject_data()[project_key]["project"]
        pathology_name = self.json.read_subject_data()[project_key]["pathology"]

        project_id = self.sql.project(project_name)
        pathology_id = self.sql.pathology(pathology_name)
        subject_id = self.sql.subject(project_key, project_id, pathology_id)

        self.sql.structure_statistic(project_path, subject_id)
        self.sql.main_statistic(project_path, subject_id)

        # self.json.delete_subject_data_from_json(project_name)
