import os

from ..Backend.log_files import Log


class ParsingResults:
    def __init__(self):
        self.lg = Log()

    @staticmethod
    def open_aseg_stat_file(project_path: str) -> list:
        """
        Прочитывает файл со статистикой и возвращает его в виде списка
        :param project_path:
        :return: список статистических данных
        """
        for directs, direct, files in os.walk(project_path):
            for file in files:
                if 'aseg.stats' == file:
                    with open(directs + '/' + file, 'r', encoding='utf-8') as f:
                        split_statistic_list = f.read().split('\n')
        return split_statistic_list

    def project_name(self, project_path: str) -> str:
        """
        Определяем имя обработанного субъекта
        :return: возвращаем имя субъекта
        """
        project_name = ''
        for i in self.open_aseg_stat_file(project_path):
            if '# subjectname' in i:
                j_list = i.split(' ')
                project_name = j_list[2]
        return project_name

    def main_statistic_data(self, project_path: str) -> list:
        """
        Определяем основные статистические параметры и передаем их для записи в БД
        :param project_path: путь к файлу со статистикой
        :return:
        """
        m_s_dict = {}
        for i in self.open_aseg_stat_file(project_path):
            if '# Measure' in i:
                j_list = i.split(', ')
                j = [k for k in j_list if k != '']
                try:
                    m_s_dict[j[1]] = j[3]
                except IndexError:
                    print('Ошибка')
                    self.lg.error_log_file(f"IndexError: Ошибка создания словаря main_statistic")
                else:
                    pass
        main_stat = [
            m_s_dict['BrainSegVol'], m_s_dict['VentricleChoroidVol'], m_s_dict['lhCortexVol'],
            m_s_dict['rhCortexVol'], m_s_dict['CortexVol'], m_s_dict['lhCerebralWhiteMatterVol'],
            m_s_dict['rhCerebralWhiteMatterVol'], m_s_dict['CerebralWhiteMatterVol'],
            m_s_dict['SubCortGrayVol'], m_s_dict['TotalGrayVol'], m_s_dict['SupraTentorialVol'],
            m_s_dict['eTIV']
        ]
        return main_stat

    def structure_statistic_data(self, project_path: str) -> list:
        """
        Поиск статистических параметров субъекта и возврат их в виде списка
        :param project_path: путь к файлу со статистикой
        :return: список статистических данных
        """
        statistic_list = []
        for i in self.open_aseg_stat_file(project_path):
            if i == "":
                pass
            elif '#' not in i:
                j_list = i.split(' ')
                j = [k for k in j_list if k != '']
                try:
                    statistic_list.append(
                        [j[4], int(j[2]), float(j[3]), float(j[5]), float(j[6]),
                         float(j[7]), float(j[8]), float(j[9])]
                    )
                except IndexError:
                    self.lg.error_log_file(f"IndexError: Ошибка создания списка statistic")
                    print('Ошибка')
                else:
                    pass
        return statistic_list
