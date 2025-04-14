def clean_id(identifier):
    """Clean the ID by stripping whitespace and removing non-printable characters."""
    return identifier.strip()

def find_tierlid(database_file, target_id, tst_dict):
    """Find the TierLID for a given ID by searching the database file and store its tst."""
    target_id = clean_id(target_id)  # Clean the target_id
    if not target_id:  # If the target_id is empty after cleaning, return it as is
        return target_id
    with open(database_file, "r") as db_file:
        for line in db_file:
            parts = line.strip().split("\t")
            if len(parts) >= 3:  # Ensure there are at least 3 columns (ID, tst, TierLID)
                db_id = clean_id(parts[0])  # Clean the database ID
                tst = clean_id(parts[1])  # Extract the tst value
                tierlid = clean_id(parts[2])  # Clean the TierLID
                if db_id == target_id:  # Match found
                    if tierlid:  # If TierLID is not empty
                        tst_dict[tierlid] = tst  # Store the tst value using TierLID as the key
                        return tierlid
                    else:  # If TierLID is empty, keep the original ID
                        tst_dict[target_id] = tst  # Store the tst value using the original ID as the key
                        return target_id
    return target_id  # Return the original ID if no match is found

def rename(input_file, output_file, database_file):
    """Rename IDs in the input file using the database file for lookups and collect tst values."""
    tst_dict = {}  # Dictionary to store tst values for each ID
    with open(input_file, "r") as infile, open(output_file, "w") as outfile:
        # Read the header and write it to the output file
        header = infile.readline()
        outfile.write(header)
        
        # Process each line in the input file
        for line_number, line in enumerate(infile, start=1):
            parts = line.strip().split("\t")
            # Ensure the line has at least four columns
            while len(parts) < 4:  # Ensure there are at least 4 columns (id, fid, mid, sex)
                parts.append("")  # Add empty columns if missing
            # Perform lookups in the database file for each ID
            parts[0] = find_tierlid(database_file, parts[0], tst_dict) if parts[0].strip() else parts[0]  # Replace id
            parts[1] = find_tierlid(database_file, parts[1], tst_dict) if parts[1].strip() else parts[1]  # Replace fid
            parts[2] = find_tierlid(database_file, parts[2], tst_dict) if parts[2].strip() else parts[2]  # Replace mid
            # Write the updated line to the output file
            outfile.write("\t".join(parts) + "\n")
    return tst_dict  # Return the tst dictionary