import elasticsearch


def fetch_data(client, query=None, sort=None, size=500):
    """
    Diese Funktion lädt Daten aus einer gegebenen Datenbank.
    Die Daten können gefiltert und nach Attributen sortiert werden.
    """
    if query is None:
        query = {
            "bool": {
                "must": [
                    {
                        "match": {
                            "deprecated": 0
                        }
                    }
                ]
            }
        }
    if sort is None:
        sort = {}
    try:
        return client.search(index="real_estate", query=query, size=size, sort=sort)['hits']['hits']
    except elasticsearch.NotFoundError:
        return ''


def get_query_for_zip(zip):
    """
    Diese Funktion gibt eine Suchanfrage für die Datenbank zurück, mit der nur Daten einer gegebenen Postleitzahl
    zurückgeliefert werden.
    """
    query = {
        "bool": {
            "must": [
                {
                    "match": {
                        "zip": zip
                    }
                },
                {
                    "match": {
                        "deprecated": 0
                    }
                }
            ]
        }
    }
    return query
