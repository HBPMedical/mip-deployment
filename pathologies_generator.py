#!/usr/bin/env python3

import sys
import os
import re
import glob
import csv
import json
import chardet
import copy

config = {
            'data':
            {
                'path': 'data',
                'max_recursion_depth': 1,
                'metadata_format': 'json',
                'metadata_filename': 'CDEsMetadata.json',
                'metadata_encoding': 'utf-8',
                'metadata_indent': '  ',
                'metadata_dataset_sync': True,
                'dataset_format': 'csv',
                'dataset_encoding': 'ascii',
                'dataset_delimiter': ',',
                'dataset_quotechar': '"'
            },
            'pathologies':
            {
                'path': 'config',
                'format': 'json',
                'filename': 'pathologies2.json',
                'file_encoding': 'utf-8',
                'file_indent': '  '
            }
        }


class gen_pathologies:
    __config = None
    __metadatas = {}
    __pathologies = []
    __pathologies_ids = {}
    __datasets_codes = {}
    __datasets = {}

    def __init__(self, config):
        check = False
        go_ahead = True
        if isinstance(config, dict):
            keys = {
                        'data':
                            {'keys': ['path', 'max_recursion_depth', 'metadata_format', 'metadata_filename', 'metadata_encoding', 'metadata_indent', 'metadata_dataset_sync', 'dataset_format', 'dataset_encoding', 'dataset_delimiter', 'dataset_quotechar']},
                        'pathologies':
                            {'keys': ['path', 'format', 'filename', 'file_encoding', 'file_indent']}
                    }
            for section in keys:
                if section in config and isinstance(config[section], dict):
                    for key in keys[section]['keys']:
                        if key not in config[section] or (key in config[section] and (config[section][key] is None or config[section][key] == '')):
                            if key in config[section] and config[section][key] is None and re.search(r'encoding', key):
                                pass
                            else:
                                go_ahead = False
                                break
                        if key == 'path':
                            if os.path.isdir(config[section][key]):
                                config[section][key] = os.path.abspath(config[section][key])
                            else:
                                go_ahead = False
                                break
                    if go_ahead:
                        check = True

        if check:
            self.__config = config
        else:
            print("configuration is not consistent! Can't go further...")
            sys.exit(1)

    def __predict_encoding(self, file_path, n_lines=None):
        if n_lines is None:
            nbytes = os.stat(file_path).st_size
            nchars=0
            with open(file_path) as f:
                for line in f:
                    nchars += len(line)
            if nbytes == nchars:
                n_lines = 100
            else:
                n_lines = 5000

        with open(file_path, 'rb') as f:
            rawdata = b''.join([f.readline() for _ in range(n_lines)])

        encoding = chardet.detect(rawdata)['encoding']
        return encoding

    def __get_dict_id(self, dict_list, dict_item, search_value):
        for i, item in enumerate(dict_list):
            if item[dict_item] == search_value:
                return i

    def __get_filtered_dict_list(self, dict_list, key_name):
        return [sub[key_name] for sub in dict_list]

    def __json_file_writer(self, filepath, content, file_encoding, file_indent):
        if file_encoding is None:
            file_encoding = 'utf-8'
        file_ensure_ascii = True
        if file_encoding != 'ascii':
            file_ensure_ascii = False
        print(f"Will write {filepath} in {file_encoding} with indent <{file_indent}>")
        with open(filepath, 'wb') as f:
            f.write(json.dumps(content, indent=file_indent, ensure_ascii=file_ensure_ascii).encode(file_encoding) + "\n")

    def __file_writer(self, filepath, content, file_format='json', file_encoding='utf-8', file_indent='    '):
        if file_format == 'json':
            self.__json_file_writer(filepath, content, file_encoding, file_indent)
        else:
            print(f"WARNING: No pathologies processor for format \"{file_format}\"! I won't be able to write {filepath}")

    def __metadata_file_writer(self, pathology):
        filepath = os.path.join(self.__config['data']['path'], pathology, self.__config['data']['metadata_filename'])
        content = self.__metadatas[pathology]['source']
        file_format = self.__config['data']['metadata_format']
        file_encoding = self.__config['data']['metadata_encoding']
        file_indent = self.__config['data']['metadata_indent']
        self.__file_writer(filepath, content, file_format, file_encoding, file_indent)

    def __metadata_processor(self, pathology):
        pathology_id = self.__pathologies_ids[pathology]
        content = self.__metadatas[pathology]['final']

        metadata_dataset_file_change = False

        datasets = None
        for item in ['code', 'label']:
            if item == 'code' and content[item] == 'root':
                self.__pathologies[pathology_id]['code'] = pathology
            elif item == 'label' and content[item] == '/':
                self.__pathologies[pathology_id]['label'] = pathology.capitalize()
            else:
                self.__pathologies[pathology_id][item] = content[item]
        for i, var_type in enumerate(content['variables']):
            if var_type['code'] == 'dataset':
                metadata_datasets = content['variables'].pop(i)
                metadata_datasets = metadata_datasets['enumerations']

        datasets_codes = [sub['code'] for sub in metadata_datasets]

        missing_datasets = []
        exceeding_datasets = []
        for dataset in self.__datasets_codes[pathology]:
            if dataset in self.__get_filtered_dict_list(metadata_datasets, 'code'):
                dataset_id = self.__get_dict_id(metadata_datasets, 'code', dataset)
                self.__datasets[pathology].append({'code': dataset, 'label': metadata_datasets[dataset_id]['label']})
            else:
                missing_datasets.append(dataset)
                self.__datasets[pathology].append({'code': dataset, 'label': dataset.upper()})
        for dataset in metadata_datasets:
            if dataset['code'] not in self.__datasets_codes[pathology]:
                exceeding_datasets.append(dataset['code'])

        pathology_datasets_codes = [sub['code'] for sub in self.__datasets[pathology]]
        for missing_dataset in missing_datasets:
            missing_dataset_id = self.__get_dict_id(self.__datasets[pathology], 'code', missing_dataset)
            metadata_datasets.append(self.__datasets[pathology][missing_dataset_id])
            if self.__config['data']['metadata_dataset_sync']:
                metadata_dataset_variable_id = self.__get_dict_id(self.__metadatas[pathology]['source']['variables'], 'code', 'dataset')
                self.__metadatas[pathology]['source'][metadata_dataset_variable_id].append(self.__datasets[pathology][dataset_id])
                metadata_dataset_file_change = True
        for exceeding_dataset in exceeding_datasets:
            for i, dataset in enumerate(metadata_datasets):
                if dataset['code'] == exceeding_dataset:
                    metadata_datasets.pop(i)
                    break
            if self.__config['data']['metadata_dataset_sync']:
                for i, dataset in enumerate(self.__metadatas[pathology]['source']['variables']):
                    if dataset['code'] == exceeding_dataset:
                        self.__metadatas[pathology]['source']['variables'].pop(i)
                        metadata_dataset_file_change = True

        if metadata_dataset_file_change:
            self.__metadata_file_writer(pathology)

    def __dataset_processor(self, pathology, file_path):
        datasets = []

        file_encoding = self.__config['data']['dataset_encoding']
        if file_encoding is None:
            file_encoding = self.__predict_encoding(file_path)

        dataset_field_id = None
        with open(file_path, newline='', encoding=file_encoding) as dataset_file:
            if self.__config['data']['dataset_format'] == 'csv':
                datasetreader = csv.reader(dataset_file, delimiter=self.__config['data']['dataset_delimiter'], quotechar=self.__config['data']['dataset_quotechar'])
                for row_id, row in enumerate(datasetreader):
                    if row_id == 0:
                        for field_id, field_name in enumerate(row):
                            if field_name == 'dataset':
                                dataset_field_id = field_id
                                break
                        if dataset_field_id is None:
                            print('WARNING!! Dataset parsing error: Unable to locate "dataset" field in file "%s"!' % file_path)
                            break
                    elif row[dataset_field_id] not in datasets:
                        datasets.append(row[dataset_field_id])
            else:
                print('No dataset processor for format "%s"!' % self.__config['data']['dataset_format'])
                sys.exit(1)
        if len(datasets) > 0:
            if pathology not in self.__datasets_codes:
                self.__datasets_codes[pathology] = []
                self.__datasets[pathology] = []
            for dataset in datasets:
                if dataset not in self.__datasets_codes[pathology]:
                    self.__datasets_codes[pathology].append(dataset)

    def __file_analyser(self, path):
        current_path_element = os.path.basename(path)
        parent_path_element = os.path.split(os.path.dirname(path))[1]
        file_name, file_ext = os.path.splitext(current_path_element)
        if parent_path_element in self.__pathologies_ids:
            pathology = parent_path_element
            pathology_id = self.__pathologies_ids[pathology]
            if current_path_element == self.__config['data']['metadata_filename']:
                metadata_content = None
                file_encoding = self.__config['data']['metadata_encoding']
                if file_encoding is None:
                    file_encoding = self.__predict_encoding(path)
                try:
                    with open(path, encoding=file_encoding) as f:
                        metadata_content = None
                        if self.__config['data']['metadata_format'] == 'json':
                            metadata_content = json.load(f)
                        else:
                            print('No metadata processor for format "%s"!' % self.__config['data']['metadata_format'])
                            sys.exit(1)
                        if metadata_content is not None:
                            self.__metadatas[pathology]['source'] = copy.deepcopy(metadata_content)
                            self.__metadatas[pathology]['final'] = metadata_content
                except Exception as e:
                    print('Error while trying to load %s! Exiting...' % path)
                    sys.exit(1)
            elif file_ext == '.csv':
                self.__dataset_processor(pathology, path)

    def pathologies_generator(self):
        for pathology in self.__pathologies_ids:
            pathology_id = self.__pathologies_ids[pathology]
            if self.__metadatas[pathology]['final'] is not None:
                self.__metadata_processor(pathology)
                self.__pathologies[pathology_id]['metadataHierarchy'] = self.__metadatas[pathology]['final']
            self.__pathologies[pathology_id]['datasets'] = self.__datasets[pathology]

    def pathologies_file_writer(self):
        filepath = os.path.join(self.__config['pathologies']['path'], self.__config['pathologies']['filename'])
        content = self.__pathologies
        file_format = self.__config['pathologies']['format']
        file_encoding = self.__config['pathologies']['file_encoding']
        file_indent = self.__config['pathologies']['file_indent']
        self.__file_writer(filepath, content, file_format, file_encoding, file_indent)

    def get_metadatas(self):
        return self.__metadatas

    def get_pathologies(self):
        return self.__pathologies

    def browse(self, path = None, recursion_depth = None):
        if path is None:
            path = self.__config['data']['path']
            recursion_depth = -1

        if path is not None and recursion_depth is not None:
            recursion_depth += 1
            rel_path_from_data = os.path.relpath(path, self.__config['data']['path'])
            current_path_element = os.path.basename(path)
            parent_path_element = os.path.split(os.path.dirname(path))[1]

            if os.path.isdir(path):
                if recursion_depth == 1:
                    self.__pathologies.append({'code': current_path_element})
                    self.__pathologies_ids[current_path_element] = len(self.__pathologies) - 1
                    self.__metadatas[current_path_element] = {'source': None, 'final': None}

                sub_path_list = sorted(glob.glob(os.path.join(path, '*')))
                for sub_path in sub_path_list:
                    if recursion_depth <= self.__config['data']['max_recursion_depth']:
                        self.browse(sub_path, recursion_depth)
            elif os.path.isfile(path):
                self.__file_analyser(path)

def main():
    pathologies = gen_pathologies(config)
    pathologies.browse()
    pathologies.pathologies_generator()
    pathologies.pathologies_file_writer()

if __name__ == '__main__':
    main()
