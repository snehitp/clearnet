from bson.objectid import ObjectId


class VaultQuery:

    def hub_query(self, parameters, db):

        """
        Case vault query to return results to the hub
        For this variant and this disease, how many variant carriers are unaffected family members?

        :param db: The database object
        :param parameters: A dict, we expect it to have the keys ['variant', 'mondo_id']
        """

        # Query cases matching a specific snp
        # Using the cases returned and the additional filter criteria query
        # for cases

        variant = parameters['variant']
        mondo_id = parameters['disease']

        variant_collection = db['variants']
        cases_collection = db['cases']

        cursor = variant_collection.find(
                {'variants': variant}
            )

        case_ids = [v for v in cursor]
        if not case_ids:
            return 0, {}
        else:
            try:
                case_ids = [ObjectId(v['caseId']) for v in case_ids]
            except KeyError as e:
                print('Expecting a {} key, did not find it'.format(e))

        query = {'$and': [
            {'_id': {
                '$in': case_ids}
            },
            {'diseases.diseases.id': {'$nin': [mondo_id]}},
            {'pedigree.familyMembers.caseId': {'$in': case_ids}}
        ]}
        cursor = cases_collection.find(query)
        res = [i for i in cursor]

        return sum(1 for i in res), {}

    def casevault_query(self, parameters):
        """ Execute the query and return detailed results for the case vault
        :param parameters:
        """
