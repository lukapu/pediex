import os
import subprocess
from pedigree_explorer.config import load_config, resolve_id
from pedigree_explorer.loader import load_subjects
from pedigree_explorer.ancestry_tracer import trace_to_founders
from pedigree_explorer.graph_builder import build_graph
from pedigree_explorer.parent_lookup import get_parent_info
from pedigree_explorer.rename import rename
from pedigree_explorer.validator import check_for_duplicates


def main():
    # Load configuration
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "configs/config.yaml")
    config = load_config(config_path)

    # Set the path for the input data relative to the script location
    allanimals_path = os.path.join(script_dir, config["input_data"])

    # Resolve subject_id and founders to regular IDs
    print("Resolving subject ID and founder IDs...")
    subject_id = resolve_id(config["subject_id"], allanimals_path)
    founders = {resolve_id(founder, allanimals_path) for founder in config["founders"]}

    # Load subjects from the input data
    print("Loading subjects from input data...")
    subjects = load_subjects(allanimals_path, config.get("filter_by_descriptors"))

    # Find the shortest paths to each founder and process them separately
    print("Tracing shortest paths to each founder...")
    for founder in founders:
        print(f"Processing founder: {founder}")
        
        # Find paths to the current founder
        paths = trace_to_founders(
            graph=build_graph(subjects),
            subject_id=subject_id,
            founders={founder},  # Only consider the current founder
            max_depth=config["max_generations"]
        )
        
        if paths:
            # Filter and print only the shortest paths for this founder
            print(f"Shortest paths to founder {founder}:")
            min_length = min(len(path) for path in paths)
            shortest_paths = [path for path in paths if len(path) == min_length]
            for path in shortest_paths:
                print(" -> ".join(path))
            
            # Extract all unique subject IDs from the shortest paths
            subject_ids = set(node for path in shortest_paths for node in path)

            # Check for duplicates in the database
            print(f"Checking for duplicate subjects in the database for founder {founder}...")
            check_for_duplicates(subject_ids, allanimals_path)

            # Create dynamic folder structure for each subject_founder combination
            subject_founder_folder = os.path.join(script_dir, f"outputs/{subject_id}_{founder}")
            paths_folder = os.path.join(subject_founder_folder, "paths")
            os.makedirs(subject_founder_folder, exist_ok=True)
            os.makedirs(paths_folder, exist_ok=True)

            # Define paths for parent info and renamed files
            parent_info_file = os.path.join(paths_folder, f"parent_info_{founder}.txt")
            renamed_parent_info_file = os.path.join(paths_folder, f"parent_info_renamed_{founder}.txt")
            tst_file = os.path.join(paths_folder, f"tst_info_{founder}.txt")

            # Debugging paths
            print(f"Input file: {parent_info_file}")
            print(f"Output file: {renamed_parent_info_file}")
            print(f"Database file: {allanimals_path}")

            # Extract parent information for the subject IDs
            print(f"Extracting parent information for founder {founder}...")
            parent_info = get_parent_info(subject_ids, allanimals_path, output_file=parent_info_file)

            # Save parent information to a .txt file for R
            print(f"Saving parent information to {parent_info_file}...")
            with open(parent_info_file, "w") as f:
                f.write("id\tfid\tmid\tsex\n")
                for subject_id, (father_id, mother_id) in parent_info.items():
                    # Fetch the sex information from the original data if needed
                    sex = subjects[subject_id]["descriptors"].get("Sex", "unknown")
                    f.write(f"{subject_id}\t{father_id}\t{mother_id}\t{sex}\n")

            # Rename IDs in the parent_info file using TierLIDs and collect tst values
            print("Renaming IDs in the parent_info file and collecting tst values...")
            tst_dict = rename(
                input_file=parent_info_file,
                output_file=renamed_parent_info_file,
                database_file=allanimals_path
            )

            # Save tst_dict to a file for the R script
            print(f"Saving TST information to {tst_file}...")
            with open(tst_file, "w") as f:
                f.write("id\ttst\n")
                for id_, tst in tst_dict.items():
                    f.write(f"{id_}\t{tst}\n")

            print(f"TST information saved to {tst_file}.")

            # Save the pedigree plot as a PNG file directly in the subject_founder_folder
            output_file = os.path.join(subject_founder_folder, f"shortest_paths_{subject_id}_{founder}.png")
            print(f"Calling R script for pedigree visualization for founder {founder}...")
            r_script_path = os.path.join(script_dir, "pedigree_explorer/FamilyTree.R")
            try:
                # Define the renamed parent info file path
                renamed_parent_info_file = os.path.join(paths_folder, f"parent_info_renamed_{founder}.txt")
                subprocess.run(
                    ["Rscript", r_script_path, renamed_parent_info_file, subject_id, str(founder), output_file],
                    check=True
                )
                print(f"Pedigree visualization for founder {founder} completed. Saved to {output_file}.")
            except subprocess.CalledProcessError as e:
                print(f"Error while running R script for founder {founder}: {e}")
        else:
            print(f"No ancestry paths found for founder {founder}.")

if __name__ == "__main__":
    main()