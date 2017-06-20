#!/usr/bin/env python
#
# Authors:
# David Huynh (@dfhuynh)
# Pablo Castellano (@PabloCastellano)

import argparse
import os.path
import time
import requests


class Refine:
    def __init__(self, server='http://127.0.0.1:3333'):
        self.server = server[0, -1] if server.endswith('/') else server

    def new_project(self, file_path, options=None):
        file_name = os.path.split(file_path)[-1]
        project_name = options['project_name'] if options != None and 'project_name' in options else file_name

        files = {'file': (file_name, open(file_path, 'rb'), 'application/vnd.ms-excel', {'Expires': '0'})}

        r = requests.post(self.server + '/command/core/create-project-from-upload', files=files)
        if '?project=' in r.request.path_url:
            _id = r.request.path_url.split('?project=')[1]
            return RefineProject(self.server, _id, project_name)

        # TODO: better error reporting
        return None


class RefineProject:
    def __init__(self, server, id, project_name):
        self.server = server
        self.id = id
        self.project_name = project_name

    def wait_until_idle(self, polling_delay=0.5):
        while True:
            r = requests.get(self.server + '/command/core/get-processes?project=' + self.id)
            response_json = r.json()
            if 'processes' in response_json and len(response_json['processes']) > 0:
                time.sleep(polling_delay)
            else:
                return

    def apply_operations(self, file_path, wait=True):
        fd = open(file_path)
        operations_json = fd.read()

        data = {
            'operations': operations_json
        }
        r = requests.post(self.server + '/command/core/apply-operations?project=' + self.id, data)
        response_json = r.json()
        if response_json['code'] == 'error':
            raise Exception(response_json['message'])
        elif response_json['code'] == 'pending':
            if wait:
                self.wait_until_idle()
                return 'ok'

        return response_json['code']  # can be 'ok' or 'pending'

    def export_rows(self, format='tsv', printColumnHeader=True):
        data = {
            'engine': '{"facets":[],"mode":"row-based"}',
            'project': self.id,
            'format' : format,
            'printColumnHeader': printColumnHeader
        }
        r = requests.post(self.server + '/command/core/export-rows/' + self.project_name + '.' + format, data)
        return r.content.decode("utf-8")

    def export_project(self, format='openrefine.tar.gz'):
        data = {
            'project' : self.id,
            'format' : format
        }
        response = urllib2.urlopen(self.server + '/command/core/export-project/' + self.project_name + '.' + format, data)
        return response.read()

    def delete_project(self):
        data = {
            'project': self.id
        }
        r = requests.post(self.server + '/command/core/delete-project', data)
        response_json = r.json()
        return response_json.get('code', '') == 'ok'


def main(args):
    r = Refine()
    p = r.new_project(args.input)
    p.apply_operations(args.operations)
    print(p.export_rows())
    p.delete_project()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Apply operations to a CSV file by using the OpenRefine API')
    parser.add_argument("input", help="Input CSV")
    parser.add_argument("operations", help="Operations CSV")
    args = parser.parse_args()

    main(args)
