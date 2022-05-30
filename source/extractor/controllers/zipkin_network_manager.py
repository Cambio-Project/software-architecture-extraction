import json
import requests
from datetime import datetime

URL_Traces = 'http://localhost:9411/api/v2/traces?limit='


class ZipkinNetworkManager:
    """
    This class offers the functionality to use the Zipkin HTTP API
    """

    def __init__(self):
        self.traces = None

    def get_traces(self, limit: int):
        """
        A method that retrieves all traces up to the limit from the Zipkin HTTP API
        """
        if not int(limit):
            # take default value if input is invalid
            limit = 10

        self.traces = requests.get(URL_Traces + str(limit)).json()
        return self.traces

    def create_backup(self, limit):
        """
        A method that saves all Traces up to the limit retrieved from the Zipkin HTTP API in json file
        """
        if not int(limit):
            # take default value if input is invalid
            limit = 10

        if self.traces is None:
            self.get_traces(limit)

        backup_path = 'backup_{}'.format(datetime.now().strftime("%d-%m-%Y_%H-%M-%S"))
        handle = open(backup_path + '.json', 'w+')
        handle.write(json.dumps(self.traces))
        handle.close()
