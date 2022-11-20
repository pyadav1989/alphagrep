from configparser import ConfigParser
import definitions
from pathlib import Path
import json
from collections import OrderedDict
import csv
from requestparser import requestparser


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
temp_json = open(output_temp_file_path,'r')
json_temp = json.load(temp_json)
temp_json_od = OrderedDict(json_temp)
output_header = list(temp_json_od.keys())
input_CSV = open(input_file_path,'r')
request_csv = csv.DictReader(input_CSV)
out_file = open(output_file_path, 'w', newline='')
response = csv.DictWriter(out_file, fieldnames=output_header)
response.writeheader()
requestparser.RequestParser(request_csv, response, temp_json_od,rules_config).get_response()