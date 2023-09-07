from elasticsearch import Elasticsearch
import elastic_transport
import sys
import warnings

from client import app_flow

elastic_url = 'xxx'
elastic_user = 'xxx'
elastic_pass = 'xxx'

warnings.filterwarnings('ignore', category=elastic_transport.SecurityWarning)

try:
    client = Elasticsearch(
        elastic_url, basic_auth=(elastic_user, elastic_pass),
        verify_certs=False)
except elastic_transport.ConnectionError as e:
    print(e)
    sys.exit(e)


if __name__ == '__main__':
    app_flow(client)


