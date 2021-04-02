from ..models import Subjects


class CompareData:
    def __init__(self, subj_vol_id1: int, subj_vol_id2: int):
        """
        :param subj_vol_id1: id данных первого сравниваемого субъекта
        :param subj_vol_id2: id данных второго сравниваемого субъекта
        """
        self.subject = Subjects.objects.get(id=subj_vol_id1)
        self.stats = self.subject.statistic.all()
        self.mn_sts = self.subject.main_statistic.all()

        self.compare_subject = Subjects.objects.get(id=subj_vol_id2)
        self.compare_stats = self.compare_subject.statistic.all()
        self.cmp_mn_sts = self.compare_subject.main_statistic.all()

    def compare_volumes(self) -> list:
        """
        Создание списка словарей с данными сравнения двух исследований
        :return: список словарей
        """
        list1 = []
        zone_name_list = [
            "eTIV", "BrainSeg", "VentricleChoroid", "Cortex", "lhCortex", "rhCortex",
            "lhCerebralWhiteMatter", "rhCerebralWhiteMatter", "CerebralWhiteMatter", "TotalGray",
            "SupraTentorial"
        ]
        for mn_st in self.mn_sts:
            for cmp_mn_st in self.cmp_mn_sts:
                list1.append(self.det_cmp_sts(mn_st.eTIV, cmp_mn_st.eTIV, mn_st.eTIV, cmp_mn_st.eTIV, "eTIV"))
                list1.append(
                    self.det_cmp_sts(mn_st.eTIV, cmp_mn_st.eTIV, mn_st.BrainSegVol, cmp_mn_st.BrainSegVol, "BrainSeg"))
                list1.append(
                    self.det_cmp_sts(mn_st.eTIV, cmp_mn_st.eTIV, mn_st.VentricleChoroidVol,
                                     cmp_mn_st.VentricleChoroidVol, "VentricleChoroid"))
                list1.append(
                    self.det_cmp_sts(mn_st.eTIV, cmp_mn_st.eTIV, mn_st.CortexVol, cmp_mn_st.CortexVol, "Cortex"))
                list1.append(
                    self.det_cmp_sts(mn_st.eTIV, cmp_mn_st.eTIV, mn_st.lhCortexVol, cmp_mn_st.lhCortexVol, "lhCortex"))
                list1.append(
                    self.det_cmp_sts(mn_st.eTIV, cmp_mn_st.eTIV, mn_st.rhCortexVol, cmp_mn_st.rhCortexVol, "rhCortex"))
                list1.append(self.det_cmp_sts(mn_st.eTIV, cmp_mn_st.eTIV, mn_st.lhCerebralWhiteMatterVol,
                                              cmp_mn_st.lhCerebralWhiteMatterVol,
                                              "lhCerebralWhiteMatter"))
                list1.append(self.det_cmp_sts(mn_st.eTIV, cmp_mn_st.eTIV, mn_st.rhCerebralWhiteMatterVol,
                                              cmp_mn_st.rhCerebralWhiteMatterVol,
                                              "rhCerebralWhiteMatter"))
                list1.append(self.det_cmp_sts(mn_st.eTIV, cmp_mn_st.eTIV, mn_st.CerebralWhiteMatterVol,
                                              cmp_mn_st.CerebralWhiteMatterVol,
                                              "CerebralWhiteMatter"))
                list1.append(self.det_cmp_sts(mn_st.eTIV, cmp_mn_st.eTIV, mn_st.TotalGrayVol, cmp_mn_st.TotalGrayVol,
                                              "TotalGray"))
                list1.append(
                    self.det_cmp_sts(mn_st.eTIV, cmp_mn_st.eTIV, mn_st.SupraTentorialVol, cmp_mn_st.SupraTentorialVol,
                                     "SupraTentorial"))
        return list1

    @staticmethod
    def create_stat_list(name_stat_query) -> list:
        """
        Принимает queryset, итерирует его и преобразует в список
        :param name_stat_query: название query (данные таблицы)
        :return:
        """
        name_stat_list = []
        for stat in name_stat_query:
            name_stat_list.append(stat)
        return name_stat_list

    def compare_structure_volume(self) -> dict:
        """
        Генерируем цикл с запуском сравнения сравнения по каждой структурной зоне ГМ и
        из возвращенного словаря сверяем ratio, далее отправляем данный словарь в соответствующий результатам список:
        positive_list, negative_list, origin_list
        :return:
        """
        positive_list = []
        negative_list = []
        origin_list = []

        stat_list = self.create_stat_list(self.stats)
        compare_stat_list = self.create_stat_list(self.compare_stats)

        length_stats = len(stat_list)
        for i in range(length_stats):
            result = self.compare_structure_stats(
                stat_list[i].Volume_mm3, compare_stat_list[i].Volume_mm3, compare_stat_list[i].name
            )
            if result['ref_diff'] >= 0.01:
                negative_list.append(result)
            elif result['ref_diff'] <= -0.01:
                positive_list.append(result)
            else:
                origin_list.append(result)

        compare_struct_dict = {
            'pos_list': positive_list, 'neg_list': negative_list, 'orig_list': origin_list
        }
        return compare_struct_dict

    def compare_structure_stats(self, stat_1: float, stat_2: float, zone: str) -> dict:
        """
        Сравнение данных двух исследований и создание словаря с результатами сравнения для таблиц структурных данных
        :param stat_1: Значение первого исследования
        :param stat_2: Значение второго исследования
        :param zone: Название области ГМ
        :return: словарь с результатами сравнения
        """
        for mn_sts in self.mn_sts:
            for cmp_mn_sts in self.cmp_mn_sts:
                if stat_1 != 0 and stat_2 != 0:
                    ref_vol1 = stat_1 / mn_sts.eTIV * 100
                    ref_vol2 = stat_2 / cmp_mn_sts.eTIV * 100
                    ratio = ref_vol1 / ref_vol2
                    difference = stat_1 - stat_2
                    ref_diff = ref_vol1 - ref_vol2
                    diction = {
                        'ratio': round(ratio, 2),
                        'zone': zone,
                        'param1': round(stat_1 / 1000, 2),
                        'param2': round(stat_2 / 1000, 2),
                        'ref_vol1': round(ref_vol1, 2),
                        'ref_vol2': round(ref_vol2, 2),
                        'diff': round(difference / 1000, 2),
                        'ref_diff': round(ref_diff, 2),
                    }
                    return diction
                else:
                    diction = {
                        'ratio': 0, 'zone': zone, 'param1': 0,
                        'param2': 0, 'ref_vol1': 0, 'ref_vol2': 0, 'diff': 0, 'ref_diff': 0
                    }
                    return diction

    @staticmethod
    def det_cmp_sts(etiv1: float, etiv2: float, stat_1: float, stat_2: float, zone: str) -> dict:
        """
        Сравнение данных двух исследований и создание словаря с результатами сравнения
        :param etiv1: Значение всего объема ГМ первого исследования
        :param etiv2: Значение всего объема ГМ второго исследования
        :param stat_1: Значение первого исследования
        :param stat_2: Значение второго исследования
        :param zone: Название области ГМ
        :return: словарь с результатами сравнения
        """
        ref_vol1 = stat_1 / etiv1 * 100
        ref_vol2 = stat_2 / etiv2 * 100
        ref_diff = abs(ref_vol1 - ref_vol2)

        if ref_diff <= -0.01:
            report = "Увеличение объёма"
        elif ref_diff >= 0.01:
            report = "Снижение объёма"
        elif ref_diff == 0 and zone == 'eTIV':
            report = ""
        else:
            report = "Без изменений"

        diction = {
            'zone': zone,
            'report': report,
            'param1': round(stat_1 / 1000, 2),
            'param2': round(stat_2 / 1000, 2),
            'ref_vol1': round(ref_vol1, 2),
            'ref_vol2': round(ref_vol2, 2),
        }
        return diction


class ReleaseResults:
    def __init__(self, subj_id1: int):
        """
        :param subj_id1: id данных первого сравниваемого субъекта
        """
        self.subject = Subjects.objects.get(id=subj_id1)
        self.stats = self.subject.statistic.all()
        self.mn_sts = self.subject.main_statistic.all()
        self.cd = CompareData

    @staticmethod
    def release_stat_results(etiv: float, structure_data: dict):
        """
        Расчёт референсного объема структуры ГМ
        :param etiv: Значение всего объема ГМ
        :param structure_data: Словарь с данными структуры ГМ из БД в виде списка
        """
        volume = round(structure_data.Volume_mm3 / 1000, 3)
        ref_vol = round(structure_data.Volume_mm3 / etiv * 100, 2)
        dict_ = {
            'name': structure_data.name,
            'NVoxels': structure_data.NVoxels,
            'Volume_mm3': f"{volume} ({ref_vol}%)",
            'normMean': structure_data.normMean,
            'normStdDev': structure_data.normStdDev,
            'normMin': structure_data.normMin,
            'normMax': structure_data.normMax,
            'normRange': structure_data.normRange
        }
        return dict_

    def concatenate_stats(self):
        """
        Создание списка словарей для вывода на странице со статистикой
        :return:
        """
        list_ = []
        stat_list = self.cd.create_stat_list(self.stats)
        length_stats = len(stat_list)
        for index in range(length_stats):
            for mn_st in self.mn_sts:
                list_.append(self.release_stat_results(mn_st.eTIV, stat_list[index]))
        return list_

    @staticmethod
    def release_main_stat_result(etiv: float, stat: float, zone: str) -> dict:
        ref_vol = stat / etiv * 100
        diction = {
            'name': zone,
            'parameter': round(stat / 1000, 2),
            'ref_vol': round(ref_vol, 2),
        }
        return diction

    def concatanate_main_stats(self) -> list:
        main_stat_list = []
        for mn_st in self.mn_sts:
            main_stat_list.append(self.release_main_stat_result(mn_st.eTIV, mn_st.eTIV, "eTIV"))
            main_stat_list.append(
                self.release_main_stat_result(mn_st.eTIV, mn_st.BrainSegVol, "BrainSeg"))
            main_stat_list.append(
                self.release_main_stat_result(mn_st.eTIV, mn_st.VentricleChoroidVol, "VentricleChoroid"))
            main_stat_list.append(
                self.release_main_stat_result(mn_st.eTIV, mn_st.CortexVol, "Cortex"))
            main_stat_list.append(
                self.release_main_stat_result(mn_st.eTIV, mn_st.lhCortexVol, "lhCortex"))
            main_stat_list.append(
                self.release_main_stat_result(mn_st.eTIV, mn_st.rhCortexVol, "rhCortex"))
            main_stat_list.append(
                self.release_main_stat_result(mn_st.eTIV, mn_st.lhCerebralWhiteMatterVol, "lhCerebralWhiteMatter"))
            main_stat_list.append(
                self.release_main_stat_result(mn_st.eTIV, mn_st.rhCerebralWhiteMatterVol, "rhCerebralWhiteMatter"))
            main_stat_list.append(
                self.release_main_stat_result(mn_st.eTIV, mn_st.CerebralWhiteMatterVol, "CerebralWhiteMatter"))
            main_stat_list.append(self.release_main_stat_result(mn_st.eTIV, mn_st.TotalGrayVol,
                                                                "TotalGray"))
            main_stat_list.append(
                self.release_main_stat_result(mn_st.eTIV, mn_st.SupraTentorialVol,
                                              "SupraTentorial"))
        return main_stat_list
