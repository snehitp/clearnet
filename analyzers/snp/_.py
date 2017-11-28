def hub_query(self, parameters, db):
    """ Case vault query to return results to the hub
    :param db:
    :param parameters:
    """

    # Query cases matching a specific snp
    # Using the cases returned and the additional filter criteria query
    # for cases

    variant_string = parameters['variant']

    variant_collection = db['variants']

    cursor = variant_collection.find(
            {'variants': variant_string}
        )

    return sum(1 for i in cursor), {}

def casevault_query(self, parameters):
    """ Execute the query and return detailed results for the case vault
    :param parameters:
    """
