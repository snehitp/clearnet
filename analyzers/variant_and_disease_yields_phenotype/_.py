from bson.objectid import ObjectId


class VaultQuery:

    def hub_query(self, parameters, db):
        """
        Case vault query to return results to the hub.

        For this variant and this disease, what are the phenotypes (i.e. symptoms, clinical presentations)
        that have been associated with the cases?

        :param parameters:  A dict, we expect it to have the keys ['variant', 'disease']
        :param db:
        :return:
        """

        variant = parameters['variant']
        mondo_id = parameters['disease']

        variant_collection = db['variants']
        case_collection = db['cases']

        cursor = variant_collection.find({'variants': variant})

        cases = [v for v in cursor]
        if not cases:
            return []

        try:
            cases = [ObjectId(c['caseId']) for c in cases]
        except KeyError as e:
                print('Expecting a {} key, did not find it'.format(e))

        query = {'$and': [
            {'_id': {'$in': cases}},
            {'diseases.diseases.id': mondo_id}
        ]}
        cursor = case_collection.find(query)
        cases = [d for d in cursor]

        if not cases:
            return []

        phenotypes = []
        for case in cases:
            try:
                p = case['phenotypes']
            except KeyError as e:
                print('Expecting a {} key, did not find it'.format(e))
                continue
            if p:
                these_phenotypes = p['phenotypes']
                for this_phenotype in these_phenotypes:
                    phenotypes.append(this_phenotype)

        num_phenotypes = len(phenotypes)
        phenotype_counts = {}

        for p in phenotypes:
            try:
                hpo_id = p['id']
            except KeyError as e:
                print('Expecting a {} key, did not find it'.format(e))
                continue
            if hpo_id not in phenotype_counts.keys():
                p['count'] = 1
                phenotype_counts[hpo_id] = p
            else:
                phenotype_counts[hpo_id]['count'] += 1

        """
        Just some cosmetic reshaping of the data; we want to return something like this:
        [
            {count: 10, data: {...}},
            {count: 3, data: {...}}
        ]
        """
        details = []
        for key in phenotype_counts.keys():
            phenotype = phenotype_counts[key]
            count = phenotype.pop('count')
            details.append({
                'count': count,
                'data': phenotype
            })

        return num_phenotypes, details

    def casevault_query(self, parameters):
        """
        Execute the query and return more detailed results for the case vault.

        :param parameters: A dict, we expect it to have the keys ['variant', 'mondo_id']
        :return:
        """
