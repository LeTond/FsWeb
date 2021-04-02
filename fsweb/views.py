from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect, HttpResponseNotFound, HttpResponseBadRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import View
from django.db.models import Q

from .Backend.compare_data import CompareData, ReleaseResults
from .Backend.add_to_sqlite import AddToSQL
from .models import Projects, Subjects
from .Backend.startup_scripts import FreeScripts, DataSearcher
from .Backend.log_files import Log
from .Backend.observer import Obs

import time


def common_search(request, model, query):
    page_num = request.GET.get('page', 1)
    if query is not None:
        model_list = model.objects.filter(Q(name__icontains=query) |
                                          Q(id__icontains=query)).all()
    else:
        model_list = model.objects.all()
    p = Paginator(model_list, 25)
    try:
        page = p.page(page_num)
    except PageNotAnInteger:
        page = p.page(1)
    except EmptyPage:
        page = p.page(1)
    return page


class IndexView(View):
    def get(self, request):
        """
        Открытие домашней страницы
        :param request: request
        :return: index.html
        """
        obs = Obs()
        obs.search_aseg_stats()
        return render(request, "index.html")


class CreateProjectView(View):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.fr = FreeScripts()
        self.lg = Log()
        self.ds = DataSearcher()

    def get(self, request):
        """
        Вывод информации на странице с выбором доступных файлов для обработки и
        :param request: request
        :return: страницу new_project.html с доступными файлами и параметрами для обработки
        """
        files = self.ds.search_files()
        parameters = self.ds.start_up_parameter()
        sex_s = self.ds.sex_list()
        return render(request, "new_project.html", {"files": files,
                                                    "parameters": parameters,
                                                    "sex_s": sex_s})

    def post(self, request):
        """
        Отправление запроса на запуск процесса обработки данных МР-морфометрии, в котором
        parameter - параметр обработки, file_name - имя файла с МР-морфометрией пациента, project_name -
        название для создания нового проекта с обсчитанными данными.
        :param request: request
        :return: если все хорошо, то возвращается текущая страница, иначе - возврат ошибки
        """
        try:
            project_name = request.POST.get("project_name")
            file_name = request.POST.get("files")
            parameter = request.POST.get("parameters")
            subject_name = request.POST.get("subject_name")
            sex_s = request.POST.get("sex_s")
            date_of_birth = request.POST.get("date_of_birth")
            date_of_study = request.POST.get("date_of_study")
            pathology = request.POST.get("pathology_name")

            key = f"{project_name}_{subject_name}_{time.time()}"

            self.fr.start_up_preprocessing(f'{parameter} '
                                           f'{file_name}.nii '
                                           f'{key} '
                                           f'-3t')
            diction = {'project': project_name, 'subject': subject_name, 'sex': sex_s,
                       'date_of_birth': date_of_birth, 'date_of_study': date_of_study, 'pathology': pathology}
            self.lg.write_subject_data_to_json(key, diction)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        except Exception:
            return HttpResponseNotFound("<h2>Ошибка при создании проекта</h2>")


class ProjectsView(View):
    @staticmethod
    def get(request):
        """
        Получение списка проектов
        :param request: request
        :return: None
        """
        query = request.GET.get('q1')
        page = common_search(request, Projects, query)
        context = {'project_list': page}
        return render(request, 'projects_list.html', context)


class SubjectsView(View):
    @staticmethod
    def get(request):
        """
        Получение списка всех проектов
        :param request: request
        """
        query = request.GET.get('q1')
        page_num = request.GET.get('page', 1)
        if query is not None:
            subject_list = Subjects.objects.filter(Q(name__icontains=query) |
                                                   Q(sex__icontains=query) |
                                                   Q(date_of_birth__icontains=query) |
                                                   Q(date_of_study__icontains=query)).all()
        else:
            subject_list = Subjects.objects.all()
        p = Paginator(subject_list, 25)
        try:
            page = p.page(page_num)
        except PageNotAnInteger:
            page = p.page(1)
        except EmptyPage:
            page = p.page(1)
        context = {'subject_list': page,
                   'project_subjects': subject_list}

        return render(request, 'subjects_list.html', context)


class StatisticView(View):
    @staticmethod
    def get(request, subject_id):
        """
        Получение списка проектов в проекте
        :param request: request
        :param subject_id: id проекта
        """
        try:
            subject = Subjects.objects.get(id=subject_id)
            project_subjects = Subjects.objects.filter(project=subject.project)
            pathology = subject.pathology
            rr = ReleaseResults(subject_id)
            release_stat_list = rr.concatenate_stats()
            release_main_stat_list = rr.concatanate_main_stats()
            context = {'subject': subject,
                       'project_subjects': project_subjects,
                       'pathology': pathology,
                       'release_stat': release_stat_list,
                       'main_stats': release_main_stat_list}
            return render(request, 'statistic_list.html', context)
        except ConnectionError:
            return HttpResponseNotFound("<h2>Ошибка подключения</h2>")


class InstructionsView(View):
    @staticmethod
    def get(request):
        """
        Вывод страницы с инструкциями по взаимодействию с веб-приложением
        :return: instructions.html
        """
        return render(request, 'instructions.html')


class ProjectEditView(View):
    @staticmethod
    def get(request, project_id):
        """
        Получение данных проекта для редактирования
        :param request: request
        :param project_id: id проекта
        """
        try:
            project = Projects.objects.get(id=project_id)
            return render(request, "edit_project.html", {"project": project})
        except Projects.DoesNotExist:
            return render(request, 'projects_list.html')

    @staticmethod
    def post(request, project_id):
        """
        Отправка отредактированного проекта в БД
        :param request: request
        :param project_id: id проекта
        """
        project = Projects.objects.get(id=project_id)
        project.name = request.POST.get("name")
        project.save()
        project_list = Projects.objects.filter(id=project_id)
        context = {'project_list': project_list}
        return render(request, "projects_list.html", context)


class SubjectEditView(View):
    @staticmethod
    def get(request, subject_id):
        """
        Получение субъекта для редактирования
        :param request: request
        :param subject_id: id субъекта
        """
        try:
            subject = Subjects.objects.get(id=subject_id)
            return render(request, "edit_subject.html", {"subject": subject})
        except Subjects.DoesNotExist:
            return render(request, 'subjects_list.html')

    @staticmethod
    def post(request, subject_id):
        """
        Отправка отредактированного субъекта в БД
        :param request: request
        :param subject_id: id проекта
        """
        ads = AddToSQL()
        subject = Subjects.objects.get(id=subject_id)
        subject.name = request.POST.get("name")
        subject.sex = request.POST.get("sex")
        subject.date_of_birth = request.POST.get("date_of_birth")
        subject.date_of_study = request.POST.get("date_of_study")

        pathology = request.POST.get("pathology")
        pathology_id = ads.pathology(pathology)
        subject.pathology = pathology_id
        subject.save()
        subject_list = Subjects.objects.filter(id=subject_id)
        context = {'subject_list': subject_list}
        return render(request, "subjects_list.html", context)


class SubjectsInProjectView(View):
    @staticmethod
    def get(request, project_id):
        """
        Получение списка субъектов в проекте
        :param request: request
        :param project_id: id проекта
        """
        page_num = request.GET.get('page', 1)
        subject_list = Subjects.objects.filter(Q(project__id=project_id)).all()
        p = Paginator(subject_list, 15)
        try:
            page = p.page(page_num)
        except PageNotAnInteger:
            page = p.page(1)
        except EmptyPage:
            page = p.page(1)
        context = {'subject_list': page,
                   'project_subjects': subject_list}
        return render(request, 'subjects_list.html', context)


class ProjectDeleteView(View):
    @staticmethod
    def post(request, project_id):
        """
        Удаление проекта из БД
        :param request: request
        :param project_id: id проекта
        """
        try:
            Projects.objects.get(id=project_id).delete()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        except TypeError:
            return HttpResponseNotFound("<h2>Возможно, вы пытаетесь удалить проект, в котором есть исследования. "
                                        "Перед удалением проекта, убедитесь, что все исследования в нем удалены</h2>")
        except Projects.DoesNotExist:
            return HttpResponseNotFound("<h2>Project not found</h2>")


class SubjectDeleteView(View):
    @staticmethod
    def post(request, subject_id):
        """
        Удаление субъекта из БД
        :param request: request
        :param subject_id: id субъекта
        """
        try:
            subject = Subjects.objects.get(id=subject_id)
            subject.statistic.all().delete()
            subject.main_statistic.all().delete()
            subject.delete()

            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        except Projects.DoesNotExist:
            return HttpResponseNotFound("<h2>Subject not found</h2>")


class CompareSubjectsView(View):
    @staticmethod
    def post(request):
        """
        Запуск алгоритма сравнения двух исследований
        :param request: request
        :return: compare_list.html
        """
        subject_id = request.POST.get("subject_id")
        compare_subject_id = request.POST.get("compare_subject_id")
        subject = Subjects.objects.get(id=subject_id)
        compare_subject = Subjects.objects.get(id=compare_subject_id)

        cd = CompareData(subject_id, compare_subject_id)
        compare_list = cd.compare_volumes()
        compare_structure_list = cd.compare_structure_volume()

        context = {'compare_list': compare_list,
                   'pos_list': compare_structure_list['pos_list'],
                   'neg_list': compare_structure_list['neg_list'],
                   'orig_list': compare_structure_list['orig_list'],
                   'subject': subject,
                   'compare_subject': compare_subject}
        return render(request, "compare_list.html", context)


class InfoView(View):
    @staticmethod
    def get(request):
        """
        Открываем страницу с контактной информацией
        :param request: request
        :return: info.html
        """
        return render(request, "info.html")


class ViewerView(View):
    @staticmethod
    def get(request):
        """
        При обращении вызывает открытие просмотровщика freeview
        :param request: request
        :return: Возвращает текущую страницу
        """
        fr = FreeScripts()
        fr.start_up_freeview('freeview')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class LieViewerView(View):
    @staticmethod
    def get(request):
        """
        Открываем страницу с "просмотровщиком"
        :param request: request
        :return: lie_viewer.html
        """
        return render(request, "lie_viewer.html")
