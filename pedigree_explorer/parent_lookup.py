import csv

def get_parent_info(subject_ids, allanimals_path, output_file="outputs/paths/shortest_paths_info.txt"):
    """
    Extract parent information for the given subject IDs from AllAnimals.v1.TxT and save it to a file.

    Args:
        subject_ids (set): A set of subject IDs to look up.
        allanimals_path (str): Path to the AllAnimals.v1.TxT file.
        output_file (str): Path to the output file where the information will be saved.

    Returns:
        dict: A dictionary where keys are subject IDs and values are tuples (father_id, mother_id).
    """
    parent_info = {}
    with open(allanimals_path, "r") as f, open(output_file, "w") as out_f:
        reader = csv.DictReader(f, delimiter="\t")
        out_f.write("id fid mid sex\n")  # Write the header to the output file
        for row in reader:
            if row["TierID"] in subject_ids:
                father_id = row["VaterID"]
                mother_id = row["MutterID"]
                sex = row["Sex"]
                parent_info[row["TierID"]] = (father_id, mother_id)
                # Write the information to the output file
                out_f.write(f"{row['TierID']} {father_id} {mother_id} {sex}\n")
    return parent_info