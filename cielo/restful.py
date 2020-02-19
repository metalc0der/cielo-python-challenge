#!/usr/bin/env python

import argparse
import requests as reqs
import json
import csv

class RestClient:
    basic_url = 'https://jsonplaceholder.typicode.com'
    error_msg = "Something unexpected happened. Closing now..."

    def get(self, endpoint, output, data):
        url = self.basic_url + endpoint
        print('Getting', url)
        try:
            response = reqs.get(url)
            if not str(response.status_code).startswith('2'):
                print(self.error_msg)
                exit()
            
            print('Status Code:', response.status_code)

            if output is None:
                print(response.text)
            else:
                output_pieces = str(output).split('.')
                if len(output_pieces) != 2:
                    print(response.text)

                elif output_pieces[1] == 'json':
                    self.send_to_json(response, output)
                        
                elif output_pieces[1] == 'csv':
                    self.send_to_csv(response, output)

        except Exception as inst:
            print(inst)
            print(self.error_msg)
            exit()

    def post(self, endpoint, output, data):
        url = self.basic_url + endpoint
        print('Posting', url)
        try:
            response = reqs.post(url, json=json.loads(data))

            if not str(response.status_code).startswith('2'):
                print(self.error_msg)
                exit()
            
            print('Status Code:', response.status_code)

            if output is None:
                print(response.text)
            else:
                output_pieces = str(output).split('.')
                if len(output_pieces) != 2:
                    print(response.text)

                elif output_pieces[1] == 'json':
                    self.send_to_json(response, output)
                        
                elif output_pieces[1] == 'csv':
                    self.send_to_csv(response, output)

        except Exception as inst:
            print(inst)
            print(self.error_msg)
            exit()

    def send_to_json(self, response, output):
        json_data = json.loads(response.text)

        with open(output, 'w') as json_file:
            json.dump(json_data, json_file, indent=4)

        json_file.close() 

    def send_to_csv(self, response, output):
        json_data = json.loads(response.text)
        if type(json_data) is not list:
            json_data = [json_data]
        csv_file = open(output, 'w') 
        csv_writer = csv.writer(csv_file)
        count = 0
        for info in json_data: 
            if count == 0: 

                # Writing headers of CSV file 
                header = info.keys() 
                csv_writer.writerow(header) 
                count += 1

            # Writing data of CSV file 
            csv_writer.writerow(info.values()) 

        csv_file.close() 

parser = argparse.ArgumentParser()
   
parser.add_argument('method', choices=['get', 'post'], help="Request method")
parser.add_argument('endpoint', help="Request endpoint URI fragment")
parser.add_argument('-d', '--data', help="Data to send with request")
parser.add_argument('-o', '--output', help="Output to .json or .csv file (default: dump to stdout)")

args = parser.parse_args()

client = RestClient()
method = getattr(client, args.method)
method(args.endpoint, args.output, args.data)


