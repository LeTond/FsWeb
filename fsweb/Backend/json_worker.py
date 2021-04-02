import json


class Json:
    def __init__(self):
        self.add_project_log = \
            '/home/lg/PycharmProjects/FSWeb/web/fsweb/Logs/created_project_names.json'

    def read_json(self) -> dict:
        """
        Чтение данных из json
        :return:
        """
        with open(self.add_project_log) as file:
            return json.load(file)

    def write_json(self, value: dict):
        """
        Запись данных в json
        :param value: словарь с данными для записи
        :return: None
        """
        with open(self.add_project_log, 'w') as file:
            json.dump(value, file)

    def read_subject_data(self) -> dict:
        """
        Чтение jsоn файла с информацией о субъекте
        :return:
        """
        diction = self.read_json()
        return diction

    def delete_subject_data(self, project_name: str):
        """
        Удаление из json данных о субъекте, записанных в БД
        :param project_name: название проекта
        """
        diction = self.read_json()
        for project in diction:
            if project == project_name:
                diction.pop(project_name)
                self.write_json(diction)
                break
