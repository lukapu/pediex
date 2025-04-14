def check_for_duplicates(subject_ids, allanimals_path):
    """
    Check for duplicate subjects in the database where a TierLID is also presented as a regular ID
    with differing parent information. Warn the user if such duplicates are found.
    """
    # Load the database
    relevant_data = []
    with open(allanimals_path, "r") as f:
        for line in f:
            columns = line.strip().split("\t")
            if len(columns) < 8:  # Ensure there are enough columns
                continue
            regular_id, tierlid, fid, mid = columns[0], columns[2], columns[6], columns[7]
            if regular_id in subject_ids or tierlid in subject_ids:
                relevant_data.append((regular_id, tierlid, fid, mid))
    
    # Create a mapping of TierLIDs and regular IDs to their parent information
    id_to_parents = {}
    for regular_id, tierlid, fid, mid in relevant_data:
        if regular_id:
            id_to_parents[regular_id] = (fid, mid)
        if tierlid:
            id_to_parents[tierlid] = (fid, mid)
    
    # Check for duplicates where a TierLID is also a regular ID with differing parents
    duplicates = []
    for regular_id, tierlid, fid, mid in relevant_data:
        if tierlid and tierlid in id_to_parents:
            tierlid_parents = id_to_parents[tierlid]
            if (fid, mid) != tierlid_parents:
                duplicates.append((tierlid, regular_id, tierlid_parents, (fid, mid)))
    
    # Warn the user if duplicates are found
    if duplicates:
        print("WARNING: Duplicate subjects found in the database with differing parents:")
        for dup in duplicates:
            print(f"  TierLID {dup[0]} is also listed as regular ID {dup[1]} with:")
            print(f"    TierLID parents: fid={dup[2][0]}, mid={dup[2][1]}")
            print(f"    Regular ID parents: fid={dup[3][0]}, mid={dup[3][1]}")