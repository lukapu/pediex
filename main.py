import os
import subprocess
from pedigree_explorer.config import load_config
from pedigree_explorer.loader import load_subjects
from pedigree_explorer.ancestry_tracer import trace_to_founders
from pedigree_explorer.graph_builder import build_graph
from pedigree_explorer.parent_lookup import get_parent_info
from pedigree_explorer.rename import rename

def main():
    # Load configuration
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "configs/config.yaml")
    config = load_config(config_path)

    # Set the path for the input data relative to the script location
    allanimals_path = os.path.join(script_dir, config["input_data"])

    # Load subjects from the input data
    print("Loading subjects from input data...")
    subjects = load_subjects(allanimals_path, config.get("filter_by_descriptors"))

    # Find the shortest paths to the founders
    print("Tracing shortest paths to founders...")
    paths = trace_to_founders(
        graph=build_graph(subjects),
        subject_id=config["subject_id"],
        founders=set(config["founders"]),
        max_depth=config["max_generations"]
    )

    if paths:
        # Filter and print only the shortest paths
        print("Shortest paths to the founders:")
        min_length = min(len(path) for path in paths)
        shortest_paths = [path for path in paths if len(path) == min_length]
        for path in shortest_paths:
            print(" -> ".join(path))

        # Extract all unique subject IDs from the shortest paths
        subject_ids = set(node for path in shortest_paths for node in path)

        # Get parent information for all subjects in the shortest paths
        print("Fetching parent information and saving to file...")
        parent_info = get_parent_info(subject_ids, allanimals_path)

        # Save parent information to a .txt file for R
        parent_info_file = os.path.join(script_dir, "outputs/visualizations/parent_info.txt")
        os.makedirs(os.path.dirname(parent_info_file), exist_ok=True)  # Ensure the directory exists
        with open(parent_info_file, "w") as f:
            f.write("id\tfid\tmid\tsex\n")
            for subject_id, (father_id, mother_id) in parent_info.items():
                # Fetch the sex information from the original data if needed
                sex = subjects[subject_id]["descriptors"].get("Sex", "unknown")
                f.write(f"{subject_id}\t{father_id}\t{mother_id}\t{sex}\n")

                # Rename IDs in the parent_info file using TierLIDs and collect tst values
        print("Renaming IDs in the parent_info file and collecting tst values...")
        renamed_parent_info_file = os.path.join(script_dir, "outputs/visualizations/parent_info_renamed.txt")
        tst_dict = rename(parent_info_file, renamed_parent_info_file, allanimals_path)
        # Save tst_dict to a file for the R script
        tst_file = os.path.join(script_dir, "outputs/visualizations/tst_info.txt")
        with open(tst_file, "w") as f:
            f.write("id\ttst\n")
            for id_, tst in tst_dict.items():
                f.write(f"{id_}\t{tst}\n")

        # Call the R script for pedigree visualization using the renamed file and tst info
        print("Calling R script for pedigree visualization...")
        r_script_path = os.path.join(script_dir, "pedigree_explorer/FamilyTree.R")
        try:
            subprocess.run(
                ["Rscript", r_script_path, renamed_parent_info_file, config["subject_id"]] + config["founders"],
                check=True
            )
            print("Pedigree visualization completed.")
        except subprocess.CalledProcessError as e:
            print(f"Error while running R script: {e}")
    else:
        print("No ancestry paths found.")

if __name__ == "__main__":
    main()