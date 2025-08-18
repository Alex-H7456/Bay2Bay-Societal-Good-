import requests


#for testing (all drug names are in uppercase)
drugs = ["ASPIRIN", "CLOPIDOGREL"]



class Drug:


    def get_drug_FDA(self, drug_1, limit, endpoint):
        # Map endpoint to base URL and search field

        if drug_1 != None:
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
        else:
            print("No meaningful search results found")

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

        if self.status == "None":
            return None
            
        return filtered
    
    def summarise_drug_info(self, drug_entry):
        summaries = []

        for entry in drug_entry:
            brand = ", ".join(entry.get("brand_name", [])) or "Unknown"
            generic = ", ".join(entry.get("generic_name", [])) or "Unknown"
            substance = ", ".join(entry.get("substance_name", [])) or "Unknown"

            purpose = entry.get("purpose") or ["Not specified"]
            if isinstance(purpose, list):
                purpose = " ".join(purpose)

            indications = entry.get("indications") or ["Not specified"]
            if isinstance(indications, list):
                indications = " ".join(indications)

            warnings = entry.get("warnings") or ["Not specified"]
            if isinstance(warnings, list):
                warnings = " ".join(warnings)

            adverse_reactions = entry.get("adverse_reactions") or ["Not specified"]
            if isinstance(adverse_reactions, list):
                adverse_reactions = " ".join(adverse_reactions)

            # Limit adverse reactions length for readability
            adverse_summary = adverse_reactions[:800] + ("..." if len(adverse_reactions) > 800 else "")

            summaries.append(f"""
    **{brand} ({generic})**

    **Active Substance(s):** {substance}

    **Purpose:**  
    {purpose.strip()}

    **Indications/Usage:**  
    {indications.strip()}

    **Warnings/Precautions:**  
    {warnings.strip()}

    **Adverse Reactions:**  
    {adverse_summary.strip()}
    """.strip())

        return "\n\n---\n\n".join(summaries)






# Example usage


if __name__ == "__main__":
    model = Drug()

    print("label")  #by far the most important
    report1 = model.get_drug_FDA("Diamox", 1, "label")
    report1 = model.filter_events_FDA(report1)
    print(model.summarise_drug_info(report1))

    
