import yaml

def load_config(config_path="config.yaml"):
    with open(config_path, "r") as file:
        return yaml.safe_load(file)
    
def resolve_id(input_id, allanimals_path):
    """
    Resolves whether the input ID is a TierLID or a regular ID.
    If it's a TierLID, returns the corresponding regular ID.
    If it's already a regular ID, returns it as is.
    """
    with open(allanimals_path, "r") as f:
        for line in f:
            columns = line.strip().split("\t")
            if len(columns) < 2:
                continue
            regular_id, tierlid = columns[0], columns[2]
            if input_id == tierlid:
                return regular_id
            elif input_id == regular_id:
                return regular_id
    raise ValueError(f"ID '{input_id}' not found in the database.")