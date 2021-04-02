import os
import subprocess

from typing import AnyStr


class DataSearcher:
    @staticmethod
    def search_files() -> list:
        """
        Поиск готовых к обработке файлов с расширением NifTy
        :return: Список файлов
        """
        subjects_list = []
        for file in os.listdir('/home/lg/Science/freesurfer/subjects'):
            if '.nii' in file:
                subjects_list.append(file.strip('.nii'))
        return subjects_list

    @staticmethod
    def start_up_parameter() -> list:
        """
        Создаем список со сценариями обработки данных
        :return: список с параметрами
        """
        start_up_parameter = [
            "-all",
            "-all -3t",
            "-autorecon2",
            "-autorecon-segstats ",
        ]
        return start_up_parameter

    @staticmethod
    def sex_list() -> list:
        """
        Создание списка для выбора пола субъекта
        :return: список полов
        """
        sex_list_ = [
            "Муж.",
            "Жен.",
            "Другое",
        ]
        return sex_list_


class FreeScripts:
    @staticmethod
    def start_up_freeview(cmd: AnyStr) -> None:
        """
        Вызов скрипта для запуска встроенного во freesurfer просмотровщика
        :param cmd: имя программы (freeview) для запуска
        :return: None
        """
        command_list = [f'./home/lg/Science/freesurfer/Startup_freeview.sh {cmd}']
        subprocess.Popen(command_list,
                         shell=True,
                         executable='/bin/bash',
                         cwd='/')

    @staticmethod
    def start_up_preprocessing(data: AnyStr) -> None:
        """
        Вызов скрипта для запуска процесса обсчета данных МР-морфометрии
        :param data: параметры для запуска программы
        :return: None
        """
        command_list = [f'./home/lg/Science/freesurfer/Startup_freesurfer.sh {data}']
        subprocess.Popen(command_list,
                         shell=True,
                         executable='/bin/bash',
                         cwd='/')
