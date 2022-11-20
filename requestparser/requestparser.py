from configparser import ConfigParser
import definitions
from pathlib import Path
import json
from collections import OrderedDict
import csv


class RequestParser:

    def __init__(self,request_csv, response_csv, json_template, rules_config):
        self.request = request_csv
        self.response = response_csv
        self.json_template = json_template
        self.rules_config = rules_config

    def get_response(self):
        temp_list = []
        response_csv_header = self.json_template.keys()
        for each_line in self.request:

            if float(each_line.get('Quantity')) % float(self.rules_config.get('rule1','quantity')) == 0:
                self.json_template["ResponseType"] = "NEW_ORDER_CONFIRM"
            else:
                self.json_template["ResponseType"] = "REJECT"

            if each_line.get('Symbol') == self.rules_config.get('rule2','symbol'):
                self.json_template["ResponseType"] = "NEW_ORDER_CONFIRM"

            if (each_line.get('Symbol') == self.rules_config.get('rule3','symbol')) and (float(each_line.get('price')) > float(self.rules_config.get('rule3','price')) ):
                self.json_template["ResponseType"] = "REJECT"
            else:
                self.json_template["ResponseType"] = "NEW_ORDER_CONFIRM"

            if (float(each_line.get('price')) > float(self.rules_config.get('rule3','price')) ):
                self.json_template["ResponseType"] = "REJECT"
            else:
                self.json_template["ResponseType"] = "NEW_ORDER_CONFIRM"

            temp_list.append(self.json_template)

        self.response.writerows(temp_list)







if __name__ == '__main__':
    config_file_path = Path().joinpath(definitions.root_dir, 'config.ini')
    rules_config_file_path = Path().joinpath(definitions.root_dir, 'rules.ini')
    config = ConfigParser()
    config.read(config_file_path)
    rules_config = ConfigParser()
    rules_config.read(rules_config_file_path)

    input_file_path = Path().joinpath(definitions.root_dir, 'requestdata',
                                      config.get('projectdetails', 'requestfilename'))
    output_file_path = Path().joinpath(definitions.root_dir, 'responsedata',
                                       config.get('projectdetails', 'responsefilename'))
    output_temp_file_path = Path().joinpath(definitions.root_dir, 'responsedata',
                                       config.get('projectdetails', 'jsontempfilename'))

    """
    # read input file
    with open(input_file_path,'r') as file:
        csv_file = csv.DictReader(file)
        for line in csv_file:
            print(line)
            print(line.get('OrderID'))

    """

    """
    # write output JSON
        with open(output_file_path, 'w', newline='') as out_file:
        response = csv.DictWriter(out_file, fieldnames=header_fields)
        response.writeheader()
        response.writerows(rows)
    """
    """
        with open(output_temp_file_path,'r') as json_temp:
        temp_json = json.load(json_temp)
        print(temp_json)
        temp_json = OrderedDict(temp_json)
        print(type(temp_json))
        print(list(temp_json.keys()))
    """
    temp_json = open(output_temp_file_path,'r')
    json_temp = json.load(temp_json)
    temp_json_od = OrderedDict(json_temp)
    output_header = list(temp_json_od.keys())
    input_CSV = open(input_file_path,'r')
    request_csv = csv.DictReader(input_CSV)
    out_file = open(output_file_path, 'w', newline='')
    response = csv.DictWriter(out_file, fieldnames=output_header)
    response.writeheader()
    RequestParser(request_csv, response, temp_json_od,rules_config).get_response()