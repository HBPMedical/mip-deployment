#!/usr/bin/env python3

import sys
import os
import argparse
import glob
import csv
import json
import copy
import chardet
import requests
import re

class gen_pathologies:
    __config = None
    __metadatas = {}
    __pathologies = []
    __pathologies_ids = {}
    __datasets_codes = {}
    __datasets = {}

    def __init__(self, args):
        args_dict = vars(args)
        config = {'data': {}, 'pathologies': {}}
        for key in args_dict:
            if key.startswith('data_'):
                config['data'][key[5:]] = args_dict[key]
            elif key.startswith('pathologies_'):
                config['pathologies'][key[12:]] = args_dict[key]

        for section in ['data', 'pathologies']:
            keyname = 'metadata_indent'
            if section == 'pathologies':
                keyname = 'file_indent'
            config[section][keyname] = ''
            for i in range(config[section][keyname+'_count']):
                config[section][keyname] += config[section][keyname+'_char']

        config['data']['metadata_dataset_sync'] = True
        if config['data']['metadata_dataset_unsync']:
            config['data']['metadata_dataset_sync'] = False

        for section in ['data', 'pathologies']:
            if config[section]['path'] is not None:
                path = config[section]['path']
            else:
                path = os.path.dirname(__file__)
                if section == 'data':
                    path = os.path.join(path, '../data')
            if os.path.isdir(path):
                config[section]['path'] = os.path.abspath(path)
            else:
                sys.exit('Invalid directory: %s' % path)

        config['data']['metadata_datacatalogue_headers'] = {'Content-Type': 'application/json', 'X-Requested-With': 'XMLHttpRequest'}
        config['data']['metadata_datacatalogue_version'] = None
        self.__config = config

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
        result = None
        for i, item in enumerate(dict_list):
            if item[dict_item] == search_value:
                result = i
                break

        return result

    def __get_filtered_dict_list(self, dict_list, key_name):
        return [sub[key_name] for sub in dict_list]

    def __replace_values(self, content, replacements = None, encoding = None):
        new_content = None

        if isinstance(content, dict):
            new_content = {}
            for k, v in content.items():
                new_content[k] = self.__replace_values(v, replacements, encoding)
        elif isinstance(content, list):
            new_content = []
            for i, item in enumerate(content):
                new_content.append(self.__replace_values(item, replacements, encoding))
        elif isinstance(content, str):
            if replacements is not None:
                for replacement in replacements:
                    if new_content is None:
                        new_content = content.replace(replacement['search_value'], replacement['replace_value'])
                    else:
                        new_content = new_content.replace(replacement['search_value'], replacement['replace_value'])
            if encoding is not None and encoding == 'utf-8':
                for match in re.findall(r"\\u[\da-f]{4}", content):
                    code = match[2:]
                    char = eval('u"\\u%s"' %(code))
                    if new_content is None:
                        new_content = content.replace(match, char)
                    else:
                        new_content = new_content.replace(match, char)
                if new_content is None:
                    new_content = content
        else:
            new_content = content

        return new_content

    def __relabel(self, label, text = None):
        result = label
        if self.__config['data']['force_relabel']:
            if text is None:
                text = "New label? [%s] " %(label)
            newlabel = input(text)
            if newlabel != '':
                result = newlabel

        return result

    def __json_file_writer(self, filepath, content, file_encoding, file_indent):
        if file_encoding is None:
            file_encoding = 'utf-8'
        file_ensure_ascii = True
        if file_encoding != 'ascii':
            file_ensure_ascii = False
        file_indent = file_indent.replace('\\t', '\t').replace('\\n', '\n').replace('\\r', '\r')
        with open(filepath, 'wb') as f:
            f.write(json.dumps(content, indent=file_indent, ensure_ascii=file_ensure_ascii).encode(file_encoding) + b"\n")

    def __file_writer(self, filepath, content, file_format='json', file_encoding='utf-8', file_indent='    '):
        if file_format == 'json':
            self.__json_file_writer(filepath, content, file_encoding, file_indent)
        else:
            print("WARNING: No pathologies processor for format \"%s\"! I won't be able to write %s" %(file_format, filepath))

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
                label = pathology.capitalize()
                label = self.__relabel(label, "Relabel pathology '%s'? [%s] " %(pathology, label))
                self.__pathologies[pathology_id]['label'] = label
            elif item == 'label':
                label = content[item]
                label = self.__relabel(label, "Relabel pathology '%s'? [%s] " %(pathology, label))
                self.__pathologies[pathology_id][item] = label
            else:
                self.__pathologies[pathology_id][item] = content[item]

        for i, var_type in enumerate(content['variables']):
            if var_type['code'] == 'dataset':
                metadata_datasets = content['variables'][i]
                if not self.__config['pathologies']['preserve_dataset_var']:
                    content['variables'].pop(i)
                metadata_datasets = metadata_datasets['enumerations']

        datasets_codes = [sub['code'] for sub in metadata_datasets]

        missing_datasets = []
        changed_datasets = []
        exceeding_datasets = []
        for dataset in self.__datasets_codes[pathology]:
            if dataset in self.__get_filtered_dict_list(metadata_datasets, 'code'):
                dataset_id = self.__get_dict_id(metadata_datasets, 'code', dataset)
                label = metadata_datasets[dataset_id]['label']
                newlabel = self.__relabel(label, "Pathology '%s': Relabel dataset '%s'? [%s] " %(pathology, dataset, label))
                if newlabel != label:
                    changed_datasets.append(dataset)
                label = newlabel
                self.__datasets[pathology].append({'code': dataset, 'label': label})
            else:
                missing_datasets.append(dataset)
                label = dataset.upper()
                label = self.__relabel(label, "Pathology '%s': Relabel dataset '%s'? [%s] " %(pathology, dataset, label))
                self.__datasets[pathology].append({'code': dataset, 'label': label})
        for dataset in metadata_datasets:
            if dataset['code'] not in self.__datasets_codes[pathology]:
                exceeding_datasets.append(dataset['code'])

        for missing_dataset in missing_datasets:
            missing_dataset_id = self.__get_dict_id(self.__datasets[pathology], 'code', missing_dataset)
            metadata_datasets.append(self.__datasets[pathology][missing_dataset_id])
            if self.__config['data']['metadata_dataset_sync']:
                metadata_dataset_variable_id = self.__get_dict_id(self.__metadatas[pathology]['source']['variables'], 'code', 'dataset')
                self.__metadatas[pathology]['source']['variables'][metadata_dataset_variable_id]['enumerations'].append(self.__datasets[pathology][missing_dataset_id])
                metadata_dataset_file_change = True
        for changed_dataset in changed_datasets:
            changed_dataset_id = self.__get_dict_id(self.__datasets[pathology], 'code', changed_dataset)
            metadata_dataset_variable_id = self.__get_dict_id(self.__metadatas[pathology]['source']['variables'], 'code', 'dataset')
            for i, dataset in enumerate(self.__metadatas[pathology]['source']['variables'][metadata_dataset_variable_id]['enumerations']):
                if dataset['code'] == changed_dataset:
                    self.__metadatas[pathology]['source']['variables'][metadata_dataset_variable_id]['enumerations'][i] = self.__datasets[pathology][changed_dataset_id]
                    self.__metadatas[pathology]['final']['variables'][metadata_dataset_variable_id]['enumerations'][i] = self.__datasets[pathology][changed_dataset_id]
                    metadata_dataset_file_change = True
        for exceeding_dataset in exceeding_datasets:
            for i, dataset in enumerate(metadata_datasets):
                if dataset['code'] == exceeding_dataset:
                    metadata_datasets.pop(i)
                    break
            if self.__config['data']['metadata_dataset_sync']:
                metadata_dataset_variable_id = self.__get_dict_id(self.__metadatas[pathology]['source']['variables'], 'code', 'dataset')
                for i, dataset in enumerate(self.__metadatas[pathology]['source']['variables'][metadata_dataset_variable_id]['enumerations']):
                    if dataset['code'] == exceeding_dataset:
                        self.__metadatas[pathology]['source']['variables'][metadata_dataset_variable_id]['enumerations'].pop(i)
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
        if datasets:
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
                            # Enforce utf-8 encoding of remaining non-encoded characters (typically \u2019, \u03b2, and \u03c4 in dementia CDE)
                            metadata_content = self.__replace_values(metadata_content, None, file_encoding)
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
                hierarchyName = 'metadataHierarchy'
                if self.__config['pathologies']['mip5_compatibility']:
                    hierarchyName = 'hierarchy'
                self.__pathologies[pathology_id][hierarchyName] = self.__metadatas[pathology]['final']
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
                    if self.__config['data']['metadata_online_sync']:
                        metadata_version = 'latest_cde_version'
                        if self.__config['data']['metadata_datacatalogue_version'] is not None:
                            metadata_version = self.__config['data']['metadata_datacatalogue_version']
                        datacatalogue_uri = '/pathology/allPathologies/%s/%s' %(current_path_element, metadata_version)
                        # Old datacatalogue API URL was: http://195.251.252.222:2448
                        response = requests.get(self.__config['data']['metadata_datacatalogue_api_url'] + datacatalogue_uri, headers=self.__config['data']['metadata_datacatalogue_headers'])
                        if response.status_code == 200:
                            file_encoding = self.__config['data']['metadata_encoding']
                            content = None
                            try:
                                if file_encoding is not None:
                                    content = json.loads(response.content.decode(file_encoding))
                                else:
                                    content = json.loads(response.content)
                                if 'jsonString' in content:
                                    if file_encoding is not None:
                                        content = json.loads(content['jsonString'].encode().decode(file_encoding))
                                    else:
                                        content = json.loads(content['jsonString'])
                            except Exception as e:
                                content = None
                                raise e
                            if content is not None:
                                if os.path.isfile(os.path.join(path, self.__config['data']['metadata_filename'])):
                                    os.rename(os.path.join(path, self.__config['data']['metadata_filename']), os.path.join(path, self.__config['data']['metadata_filename'] + '.bak'))
                                self.__file_writer(os.path.join(path, self.__config['data']['metadata_filename']), content, 'json', file_encoding, self.__config['data']['metadata_indent'])

                sub_path_list = sorted(glob.glob(os.path.join(path, '*')))
                for sub_path in sub_path_list:
                    if recursion_depth <= self.__config['data']['max_recursion_depth']:
                        self.browse(sub_path, recursion_depth)
            elif os.path.isfile(path):
                self.__file_analyser(path)

def main():
    argsparser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    argsparser.add_argument('-d', '--data-path', dest='data_path', help='Data base directory path', type=str)
    argsparser.add_argument('-r', '--max-recursion-depth', dest='data_max_recursion_depth', default=1, help='Maximum level of recursion for data directory analysis', type=int)
    argsparser.add_argument('-w', '--force-relabel', dest='data_force_relabel', default=False, action='store_true', help='Force relabeling pathologies and datasets in CDE metadata files and pathologies file')
    argsparser.add_argument('-s', '--metadata-online-sync', dest='data_metadata_online_sync', default=False, action='store_true', help='Download CDE metadata content from online Data Catalogue')
    argsparser.add_argument('-z', '--metadata-datacatalogue-api-url', dest='data_metadata_datacatalogue_api_url', default='http://datacatalogue.mip.ebrains.eu:8086', help='Online CDE metadata datacatalogue API URL', type=str)
    argsparser.add_argument('-f', '--metadata-format', dest='data_metadata_format', default='json', help='CDE metadata files format', type=str)
    argsparser.add_argument('-m', '--metadata-filename', dest='data_metadata_filename', default='CDEsMetadata.json', help='CDE metadata file name', type=str)
    argsparser.add_argument('-e', '--metadata-encoding', dest='data_metadata_encoding', default='utf-8', help='CDE metadata files encoding', type=str)
    argsparser.add_argument('-i', '--metadata-indent-char', dest='data_metadata_indent_char', default=' ', help='CDE metadata files indentation character', type=str)
    argsparser.add_argument('-c', '--metadata-indent-count', dest='data_metadata_indent_count', default=2, help='CDE metadata files indentation character count', type=int)
    argsparser.add_argument('-u', '--metadata-dataset-unsync', dest='data_metadata_dataset_unsync', default=False, action='store_true', help='Do NOT synchronize CDE metadata files datasets enumeration with dataset files content')
    argsparser.add_argument('-t', '--dataset-format', dest='data_dataset_format', default='csv', help='Dataset files format', type=str)
    argsparser.add_argument('-o', '--dataset-encoding', dest='data_dataset_encoding', default='ascii', help='Dataset files encoding', type=str)
    argsparser.add_argument('-l', '--dataset-delimiter', dest='data_dataset_delimiter', default=',', help='Dataset files fields delimiter', type=str)
    argsparser.add_argument('-q', '--dataset-quotechar', dest='data_dataset_quotechar', default='"', help='Dataset files fields quote character', type=str)
    argsparser.add_argument('-p', '--pathologies-path', dest='pathologies_path', help='Directory path where to save pathologies file', type=str)
    argsparser.add_argument('-g', '--pathologies-format', dest='pathologies_format', default='json', help='Pathologies file format', type=str)
    argsparser.add_argument('-a', '--pathologies-filename', dest='pathologies_filename', default='pathologies.json', help='Pathologies file name', type=str)
    argsparser.add_argument('-b', '--pathologies-encoding', dest='pathologies_file_encoding', default='utf-8', help='Pathologies file encoding', type=str)
    argsparser.add_argument('-j', '--pathologies-indent-char', dest='pathologies_file_indent_char', default=' ', help='Pathologies file indentation character', type=str)
    argsparser.add_argument('-k', '--pathologies-indent-count', dest='pathologies_file_indent_count', default=2, help='Pathologies file indentation character count', type=int)
    argsparser.add_argument('-n', '--pathologies-preserve-dataset-var', dest='pathologies_preserve_dataset_var', default=False, action='store_true', help='Preserve dataset variable in pathologies file')
    argsparser.add_argument('-5', '--pathologies-mip5-ok', dest='pathologies_mip5_compatibility', default=False, action='store_true', help='Generate MIP5 compatible pathologies file')

    args = argsparser.parse_args()

    pathologies = gen_pathologies(args)
    pathologies.browse()
    pathologies.pathologies_generator()
    pathologies.pathologies_file_writer()

if __name__ == '__main__':
    main()
