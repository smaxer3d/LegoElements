from os import listdir
from os.path import isfile, join, isdir, dirname
from requests import Session
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings

import sys
import time
import pandas as pd
import re

disable_warnings(InsecureRequestWarning)

URL = 'https://rebrickable.com/api/v3/'
SEP = ';'

file = ''
file_dir = '.\\'


def get_api(url, endpoint, params='', headers=None, token=''):
    if not headers:
        headers = {
            'Authorization': token,
            # "Content-Type": "application/json"
        }

    uri = url + endpoint + params

    with Session() as session:
        try:
            response = session.get(
                uri,
                headers=headers,
                verify=False
            )
            if response.status_code == 200:
                res = response.json()
            else:
                res = response.text
            return response.status_code, res

        except Exception as e:
            print("API GET / Parse Error:  {}".format(e))
            return None


def get_element(token, element_id):
    res_stat, res = get_api(
        token='key ' + token,
        url=URL,
        endpoint=f'lego/elements/{str(element_id)}'
    )
    if res_stat != 200:
        print(f'Status: {res_stat}')
        print(res)
    return res


def get_data_write_csv_file(source: list, csv_file: str, key: str) -> None:
    """
    Gets a specific list of quantity and Lego elements from the corresponding API and writes it to a specific csv-file

    :param source: list of quantity and Lego elements
    :param csv_file: file to write the data to
    :param key: Key needed for the ReBrickable API
    :return: Nothing
    """

    if not key:
        return

    output = open(csv_file, 'w', encoding='utf-8')
    output.write(f'quantity{SEP}Element-id{SEP}part{SEP}color{SEP}Description{SEP}Image{SEP}Remark\n')

    for line in source:
        line = line.strip()

        if not line:
            continue

        try:
            quantity, element_id = line.split('\t')
        except ValueError:
            print(f'Error: {line}')
            continue

        print(f'Processing: {element_id} ({quantity} pieces)')

        info = get_element(key, element_id)
        output.write(
            quantity + SEP +
            element_id + SEP +
            str(info['part']['part_num']) + SEP +
            str(info['color']['name']) + SEP +
            str(info['part']['name']) + SEP +
            str(info['element_img_url']) + SEP + ' \n'
        )

        time.sleep(1)

    output.close()


def csv_to_html() -> None:
    """
    Read CSV-file and write it to an HTML table

    :return: Nothing
    """

    csv_files = [f for f in listdir(file_dir) if isfile(join(file_dir, f)) and f.endswith('.csv')]

    html = \
        '<!DOCTYPE html>\n' \
        '<html>\n' \
        '<head>\n' \
        '<title>Lego checklist</title>\n' \
        '<style>\n' \
        'body {font-family: Arial, Helvetica, sans-serif}\n' \
        '.column {\n' \
        '  float: left;\n' \
        '  padding: 5px;\n' \
        '}\n' \
        '.row:after {\n' \
        '  content: "";\n' \
        '  display: table;\n' \
        '  clear: both;\n' \
        '}\n' \
        'table {\n' \
        '  border: 2px solid gray;\n' \
        '  border-collapse: collapse;\n' \
        '}\n' \
        'td, th {\n' \
        '  border: 1px solid lightgray;\n' \
        '  padding: 3px;\n' \
        '}\n' \
        'th {\n' \
        '  padding-top: 8px;\n' \
        '  padding-bottom: 8px;\n' \
        '  background-color: gray;\n' \
        '  color: white;\n' \
        '}\n' \
        'tr:hover {background-color: darkgray;}\n' \
        'td:last-child {width: 100%}\n' \
        'td:nth-child(2) {min-width: 90px}\n' \
        'td:nth-child(5) {min-width: 180px}\n' \
        '</style>\n' \
        '</head>\n' \
        '<body>\n'

    for csv_file in csv_files:

        nums = re.findall(r'\d+', csv_file)

        df = pd.read_csv(join(file_dir, csv_file), sep=SEP)
        df.rename(columns={
            'quantity': 'Pcs',
            'part': 'Part',
            'color': 'Color'
        }, inplace=True)
        df['Image'] = '<img src="' + df['Image'] + '" width="80">'

        table = df.to_html(render_links=True, escape=False, index=False, justify='center')
        table = table.replace(' border="1" ', ' ')

        # color = df['Color'].value_counts().to_dict()
        color = df.groupby('Color').agg(['sum', 'count'])['Pcs'].T.to_dict()  # {'Trans-Clear': {'sum': 1, 'count': 1}, 'White': {'sum': 3, 'count': 2}}

        html += f'<h2>{csv_file.split(".")[0]}</h2>\n' \
                f'{table}\n' \
                '<div class="row">\n' \
                '  <div class="column">\n' \
                '    <br>\n'

        for key in color.keys():
            html += f'    {key}<br>\n'

        html += '    Total\n' \
                '  </div>\n' \
                '  <div class="column">\n' \
                '    Count<br>\n'

        for value in color.values():
            html += f'    {value["count"]}<br>\n'

        html += f'    {df["Pcs"].count()}\n' \
                '  </div>\n' \
                '  <div class="column">\n' \
                '    Sum<br>\n'

        for value in color.values():
            html += f'    {value["sum"]}<br>\n'

        html += f'    {df["Pcs"].sum()}\n' \
                '  </div>\n' \
                '</div>\n'

    html += '</body>\n</html>'

    with open(join(file_dir, 'Lego checklist.html'), 'w') as html_file:
        html_file.writelines(html)


def options() -> dict:
    """
    Process the commandline arguments

    :return: Dictionary of options
    """
    output = {}
    args = sys.argv[1:]

    i = 0
    while i < len(args)-1:
        if args[i].startswith('-'):
            output[args[i][1]] = args[i+1]
            i = i+2
        else:
            i = i+1

    if 'i' in output.keys():
        global file
        global file_dir

        if isfile(output['i']):
            file = output['i']
            if isdir(dirname(file)):
                file_dir = dirname(file)
            print(f'Using file {file}')

        elif isdir(output['i']):
            file_dir = output['i']
            print(f'Using dir {file_dir}')

        else:
            print(output['i'])

    if 'k' in output.keys():
        if isfile(output['k']):
            with open(output['k'], 'r') as key:
                output['k'] = key.readlines()
    else:
        print('Missing key, continue without API-get')

    # if 'i' in output.keys():
    #     if not exists(output['i']):
    #         print(f'File {output["i"]} does not exist')
    #         return {}

    return output


if __name__ == '__main__':

    option = options()

    if file:
        file_base = file.split('.')[-2]

        with open(file, 'r') as f:
            lines = f.readlines()

        if 'k' in option.keys():
            get_data_write_csv_file(lines, file_base + '.csv', option['k'])

    csv_to_html()
