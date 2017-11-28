class VaultQuery():
    
    def hub_query(self, parameters, db):
        """ Case vault query to return results to the hub """

        # Query cases matching a specific snp
        # Using the casses returned and the additional filter criteria query
        # for cases

        variant_string = parameters['variant']

        # fix this...
        variant_collection = db['hgvs.samples']

        cursor = variant_collection.find(
                {'variants': parameters['variant']}
            )

        return sum(1 for i in cursor), None

    def casevault_query(self, parameters, db):
        """ Execute the query and return detailed results for the case vault """
