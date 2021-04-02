from .json_worker import Json

import datetime


class Log:
    def __init__(self):
        self.js = Json()
        self.error_log_file = '/home/lg/PycharmProjects/FSWeb/web/fsweb/Logs/error_logs.txt'

    def write_subject_data_to_json(self, project_key: str, diction: dict):
        """
        Запись названия проекта и данных субъекта в json
        :param project_key: название проекта
        :param diction: словарь с данными субъекта исследования
        :return: None
        """
        dict_to_json = self.js.read_json()
        dict_to_json[project_key] = diction
        self.js.write_json(dict_to_json)

    def error_log(self, message: str):
        """
        Запись ошибок в log
        :param message: сообщение об ошибке
        :return: None
        """
        file = open(self.error_log_file, 'a')
        file.write(f"{datetime.datetime.now()}: {message} \n")
        file.close()
