import csv

def load_subjects(csv_path, filters=None):
    people = {}
    with open(csv_path) as f:
        # Specify delimiter as tab for TSV files
        for row in csv.DictReader(f, delimiter='\t'):
            if filters:
                if any(row[k] != v for k, v in filters.items()):
                    continue
            people[row["TierID"]] = {  # Adjusted key to match the column name in AllAnimals.v1.TxT
                "father": row["VaterID"],
                "mother": row["MutterID"],
                "descriptors": {k: row[k] for k in row if k not in ["TierID", "VaterID", "MutterID"]}
            }
    return people