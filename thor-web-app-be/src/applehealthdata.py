# -*- coding: utf-8 -*-
"""
applehealthdata.py: Extract data from Apple Health App's export.xml.

Copyright (c) 2016 Nicholas J. Radcliffe
Licence: MIT

===Modifications===

Copyright (c) 2024 273*

This software includes modifications made by 273* to the original software licensed under the MIT License. 
Modified portions of this software are that I changed some columns to extract only StepCount and SleepAnalysis and store them in a DataFrame.

Licence: MIT
"""

import re
import pandas as pd
from xml.etree import ElementTree
from collections import Counter, OrderedDict
import io


class HealthDataExtractor:
    def __init__(self, binary_data, verbose=True):
        self.verbose = verbose
        self.records = {
            'StepCount': [],
            'SleepAnalysis': []
        }

        # バイナリデータを読み込んでXMLを解析
        self.report('Reading data from binary input... ', end='')
        with io.BytesIO(binary_data) as f:
            self.data = ElementTree.parse(f)
        self.root = self.data.getroot()
        self.nodes = list(self.root)
        self.report('done')

        self.abbreviate_types()
        self.collect_stats()

    def report(self, msg, end='\n'):
        if self.verbose:
            print(msg, end=end)

    def count_tags_and_fields(self):
        self.tags = Counter()
        self.fields = Counter()
        for record in self.nodes:
            self.tags[record.tag] += 1
            for k in record.keys():
                self.fields[k] += 1

    def count_record_types(self):
        self.record_types = Counter()
        self.other_types = Counter()
        for record in self.nodes:
            if record.tag == 'Record':
                self.record_types[record.attrib['type']] += 1
            elif record.tag in ('ActivitySummary', 'Workout'):
                self.other_types[record.tag] += 1

    def collect_stats(self):
        self.count_record_types()
        self.count_tags_and_fields()

    def abbreviate_types(self):
        for node in self.nodes:
            if node.tag == 'Record' and 'type' in node.attrib:
                node.attrib['type'] = abbreviate(node.attrib['type'])

    def write_records(self):
        target_kinds = ['StepCount', 'SleepAnalysis']
        kinds = FIELDS.keys()

        for node in self.nodes:
            if node.tag in kinds:
                attributes = node.attrib
                kind = attributes['type'] if node.tag == 'Record' else node.tag

                if abbreviate(kind) not in target_kinds:
                    continue

                values = {field: format_value(attributes.get(field), datatype)
                          for field, datatype in FIELDS[node.tag].items()}
                self.records[abbreviate(kind)].append(values)

    def extract(self):
        self.write_records()
        self.dataframes = {
            'StepCount': pd.DataFrame(self.records['StepCount']),
            'SleepAnalysis': pd.DataFrame(self.records['SleepAnalysis'])
        }

    def get_dataframes(self):
        return self.dataframes

# 補助関数


def abbreviate(s, enabled=True):
    PREFIX_RE = re.compile(r'^HK.*TypeIdentifier(.+)$')
    m = re.match(PREFIX_RE, s)
    return m.group(1) if enabled and m else s


def format_value(value, datatype):
    if value is None:
        return ''
    elif datatype == 's':
        return value
    elif datatype in ('n', 'd'):
        return value
    else:
        raise KeyError('Unexpected format value: %s' % datatype)


# 定義されているフィールド
FIELDS = {
    'Record': OrderedDict((
        ('sourceVersion', 's'),
        ('device', 's'),
        ('startDate', 'd'),
        ('endDate', 'd'),
        ('value', 'n'),
    )),
    'ActivitySummary': OrderedDict((
        ('dateComponents', 'd'),
        ('activeEnergyBurned', 'n'),
        ('activeEnergyBurnedGoal', 'n'),
        ('activeEnergyBurnedUnit', 's'),
        ('appleExerciseTime', 's'),
        ('appleExerciseTimeGoal', 's'),
        ('appleStandHours', 'n'),
        ('appleStandHoursGoal', 'n'),
    )),
    'Workout': OrderedDict((
        ('sourceVersion', 's'),
        ('device', 's'),
        ('creationDate', 'd'),
        ('startDate', 'd'),
        ('endDate', 'd'),
        ('workoutActivityType', 's'),
        ('duration', 'n'),
        ('durationUnit', 's'),
        ('totalDistance', 'n'),
        ('totalDistanceUnit', 's'),
        ('totalEnergyBurned', 'n'),
        ('totalEnergyBurnedUnit', 's'),
    )),
}
