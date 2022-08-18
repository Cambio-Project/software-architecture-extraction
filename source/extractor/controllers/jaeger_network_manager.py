import json
import requests
import os
from datetime import datetime

URL_ALL_SERVICES = 'http://localhost:16686/api/services'
URL_SERVICE = 'http://localhost:16686/api/traces?service='


class JaegerNetworkManager:
    """
    This class offers the functionality to use the Jaeger HTTP API
    """

    def __init__(self):
        self.traces = {'data': []}

    def get_traces(self):
        """
        A method that retrieves all traces from the Jaeger HTTP API
        """

        # get all services
        services = requests.get(URL_ALL_SERVICES).json()

        # List of all trace IDs used to eliminate duplicate traces
        traceIDs = []

        # get the traces for each service and collect them in the traces array
        for service in services['data']:
            if service != 'jaeger-query':
                url = URL_SERVICE + service
                new_traces = requests.get(url).json()['data']

                # Elimination of duplicate traces
                for trace in new_traces:
                    if trace['traceID'] not in traceIDs:
                        traceIDs.append(trace['traceID'])
                        self.traces['data'].append(trace)

        return self.traces

    def create_backup(self):
        """
        A method that saves all files retrieved from the Jaeger HTTP API as json files in a new backup directory
        """

        # create backup directory
        backup_path = 'backup_{}'.format(datetime.now().strftime("%d-%m-%Y_%H-%M-%S"))
        os.makedirs(backup_path)

        # backup services.json
        services = requests.get(URL_ALL_SERVICES).json()
        handle = open(backup_path + '/services.json', 'w+')
        handle.write(json.dumps(services))
        handle.close()

        # get the traces for each service and collect them in the traces array
        for service in services['data']:
            if service != 'jaeger-query':
                url = URL_SERVICE + service
                handle = open(backup_path + '/' + service + '.json', 'w+')
                handle.write(json.dumps(requests.get(url).json()))
                handle.close()

    def load_backup(self, path):
        """
        A method that loads an existing backup located in the path-directory and returns all the traces
        """
        # get all services from services file
        file = path + '/services.json'
        with open(file) as f:
            services = json.load(f)

        # List of all trace IDs used to eliminate duplicate traces
        traceIDs = []

        # get the traces for each service from the corresponding file and collect them in the traces array
        for service in services['data']:
            if service != 'jaeger-query':
                file_path = path + '/' + service + '.json'
                with open(file_path) as f:
                    file = json.load(f)
                    new_traces = file['data']

                    # Elimination of duplicate traces
                    for trace in new_traces:
                        if trace['traceID'] not in traceIDs:
                            traceIDs.append(trace['traceID'])
                            self.traces['data'].append(trace)

        return self.traces
