from django.db import models

# !/usr/bin/env python3
# -*- coding: utf-8 -*-


class Projects(models.Model):
    """
    Создаем таблицу, в которой будут храниться названия проектов
    """
    id = models.IntegerField(primary_key=True)
    name = models.TextField(blank=True)

    def __str__(self):
        return f"{self.id} // {self.name}"


class StructureStatistic(models.Model):
    """
    Создаем таблицу, в которой будут храниться данные о патологии у субъекта:
    """
    id = models.IntegerField(primary_key=True)
    name = models.TextField(null=True)
    NVoxels = models.IntegerField(null=True)
    Volume_mm3 = models.FloatField(null=True)
    normMean = models.FloatField(null=True)
    normStdDev = models.FloatField(null=True)
    normMin = models.FloatField(null=True)
    normMax = models.FloatField(null=True)
    normRange = models.FloatField(null=True)

    def __str__(self):
        return f"{self.id}// {self.name} // {self.NVoxels} // {self.Volume_mm3} " \
               f"// {self.normMean} // {self.normStdDev} // {self.normMin} // {self.normMax}" \
               f"// {self.normRange}"


class MainStatistic(models.Model):
    """
    Создание таблицы main_statistic.
    В таблице содержатся основные статистические характеристики ГМ субъекта
    """
    id = models.IntegerField(primary_key=True)
    BrainSegVol = models.FloatField(null=True)
    VentricleChoroidVol = models.FloatField(null=True)
    lhCortexVol = models.FloatField(null=True)
    rhCortexVol = models.FloatField(null=True)
    CortexVol = models.FloatField(null=True)
    lhCerebralWhiteMatterVol = models.FloatField(null=True)
    rhCerebralWhiteMatterVol = models.FloatField(null=True)
    CerebralWhiteMatterVol = models.FloatField(null=True)
    SubCortGrayVol = models.FloatField(null=True)
    TotalGrayVol = models.FloatField(null=True)
    SupraTentorialVol = models.FloatField(null=True)
    eTIV = models.FloatField(null=True)

    def __str__(self):
        return f"{self.id} // {self.BrainSegVol} // {self.VentricleChoroidVol} // {self.lhCortexVol}" \
               f"// {self.rhCortexVol} // {self.CortexVol} // {self.lhCerebralWhiteMatterVol} " \
               f"// {self.rhCerebralWhiteMatterVol} // {self.CerebralWhiteMatterVol} " \
               f"// {self.SubCortGrayVol} // {self.TotalGrayVol} // {self.SupraTentorialVol}"


class Pathology(models.Model):
    """
    Создаем таблицу, в которой будут храниться данные о патологии у субъекта:
    """
    id = models.IntegerField(primary_key=True)
    name = models.TextField()

    def __str__(self):
        return f"{self.id} // {self.name}"


class Subjects(models.Model):
    """
    Создаем таблицу, в которой будут храниться данные субъекта:
    имя (name), пол (sex), дата рождения, (date_of_birth), дата исследования (date_of_study)
    """
    id = models.IntegerField(primary_key=True)
    name = models.CharField(null=True, max_length=30)
    sex = models.TextField(null=True)
    date_of_birth = models.DateField(null=True)
    date_of_study = models.DateField(null=True)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE, null=True, blank=True)
    pathology = models.ForeignKey(Pathology, on_delete=models.CASCADE, null=True, blank=True)
    statistic = models.ManyToManyField('StructureStatistic', blank=True)
    main_statistic = models.ManyToManyField('MainStatistic', blank=True)

    def __str__(self):
        return f"Имя: {self.name}, Дата иссл: {self.date_of_study}"
