import requests


#for testing (all drug names are in uppercase)
drugs = ["ASPIRIN", "CLOPIDOGREL"]



class Drug:
    def __init__(self, drugs:list):
        self.drugs = drugs

    def get_drug_FDA(self, drug_1, limit, endpoint):
        # Map endpoint to base URL and search field
        self.status = endpoint
        base_urls = {
            "event": "https://api.fda.gov/drug/event.json",
            "label": "https://api.fda.gov/drug/label.json",
            "drugsfda": "https://api.fda.gov/drug/drugsfda.json"
        }
        
        search_fields = {
            "event": f'patient.drug.medicinalproduct:"{drug_1}*"',
            "label": f'openfda.brand_name:"{drug_1}*"',
            "drugsfda": f'products.brand_name:"{drug_1}*"'
        }
        
        url = base_urls[self.status]
        search_query = search_fields[self.status]
        
        params = {
            "search": search_query,
            "limit": limit
        }
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()["results"]
        else:
            print(f"Error: {response.status_code}")
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
        if self.status == "event":
            for event in events:
                filtered.append({
                    "id": event.get("safetyreportid"),
                    "date": event.get("receivedate"),
                    "drugs": [d.get("medicinalproduct") for d in event.get("patient", {}).get("drug", [])],
                    "reactions": [r.get("reactionmeddrapt") for r in event.get("patient", {}).get("reaction", [])]
                })


        if self.status == "label":
            for label in events:
                filtered.append({
                    "id": label.get("id"),
                    "brand_name": label.get("openfda", {}).get("brand_name", []),
                    "generic_name": label.get("openfda", {}).get("generic_name", []),
                    "substance_name": label.get("openfda", {}).get("substance_name", []),
                    "purpose": label.get("purpose"),
                    "indications": label.get("indications_and_usage"),
                    "warnings": label.get("warnings"),
                    "adverse_reactions": label.get("adverse_reactions")
                })

        if self.status == "drugsfda":
            for drug in events:
                filtered.append({
                    "application_number": drug.get("application_number"),
                    "sponsor_name": drug.get("sponsor_name"),
                    "products": [
                        {
                            "brand_name": p.get("brand_name"),
                            "generic_name": p.get("generic_name"),
                            "route": p.get("route"),
                            "marketing_status": p.get("marketing_status")
                        }
                        for p in drug.get("products", [])
                    ],
                    "submission_type": drug.get("submission_type"),
                    "approval_date": drug.get("approval_date")
                })
            
        return filtered














model = Drug(drugs)


# Example usage



report3 = model.get_drug_FDA("Aspirin", 1, "drugsfda")


print("label")  #by far the most important
report1 = model.get_drug_FDA("Aspirin", 1, "label")
print(model.filter_events_FDA(report1))

print("event")

report2 = model.get_drug_FDA("Aspirin", 1, "event")
print(model.filter_events_FDA(report2))

print("brand")
report3 = model.get_drug_FDA("Aspirin", 1, "drugsfda")
print(model.filter_events_FDA(report3))

    
