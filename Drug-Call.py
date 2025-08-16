import requests


#for testing (all drug names are in uppercase)
drugs = ["ASPIRIN", "CLOPIDOGREL"]



class Drug:
    query_limit = 20
    def __init__(self, drugs:list):
        self.drugs = drugs

    def get_drug_FDA(self, drug_1, limit=None):
        if limit is None:
            limit = self.query_limit
        base_url = "https://api.fda.gov/drug/event.json"
        search_query = (
        f'patient.drug.medicinalproduct:"{drug_1}*"'
    )
        params = {
    'search': search_query,
    'limit': limit  #100 maximum and 240 per minute
}
            
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            return response.json().get('results', [])
        else:
            print("Error fetching data:", response.status_code, response.text)
            return None
        

    def get_FDA_overlap(self, drug1, drug2, limit=None):
        reports1 = self.get_drug_FDA(drug1, limit)
        reports2 = self.get_drug_FDA(drug2, limit)

        ids1 = {r["safetyreportid"]: r for r in reports1}
        ids2 = {r["safetyreportid"]: r for r in reports2}

        overlap_ids = ids1.keys() & ids2.keys()

        if not overlap_ids:
            print(f"No overlapping reports found for {drug1} and {drug2}.")
            return None


        return [ids1[i] for i in overlap_ids]
            


    def filter_events_FDA(self, events):
        filtered = []
        for event in events:
            filtered.append({
                "id": event.get("safetyreportid"),
                "date": event.get("receivedate"),
                "drugs": [d.get("medicinalproduct") for d in event.get("patient", {}).get("drug", [])],
                "reactions": [r.get("reactionmeddrapt") for r in event.get("patient", {}).get("reaction", [])]
            })
        return filtered














model = Drug(drugs)


# Example usage
report = model.get_FDA_overlap(model.drugs[0], model.drugs[1])
if report is not None:
    print(model.filter_events_FDA(report))

    
