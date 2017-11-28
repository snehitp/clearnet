from bson.objectid import ObjectId


class VaultQuery:

    def hub_query(self, parameters, db):

        """
        Case vault query to return results to the hub
        For this variant and this disease, how many segregations were observed?
        (Segregation = direct transmission of BOTH disease and variant from parent to child)


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

        cases = [v for v in cursor]
        case_ids = []
        if not cases:
            return 0, {}
        else:
            for case in cases:
                if 'caseId' in case.keys():
                    case_ids.append(ObjectId(case['caseId']))

        # The main query.  It is important to note the optimization wherein instead of
        # constructing a family tree, we look only for the relation 'MOTHER' or 'FATHER'.
        # This implementation assumes a fully-formed pedigree object
        query = {'$and': [
            {'_id': {
                '$in': case_ids}
            },
            {'diseases.diseases.id': {'$in': [mondo_id]}},
            {'pedigree.familyMembers.caseId': {'$in': [str(i) for i in case_ids]}},
            {'pedigree.familyMembers.relation': {'$in': ['Mother', 'Father']}}
        ]}
        cursor = cases_collection.find(query)
        res = [i for i in cursor]

        return sum(1 for i in res), {}

    def casevault_query(self, parameters):
        """ Execute the query and return detailed results for the case vault
        :param parameters:
        """
