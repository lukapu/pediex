# Pediex

**Pediex** is a scalable toolset for parsing, analyzing, and visualizing pedigree trees from large datasets. It is designed to trace ancestry paths, extract parent information, and generate pedigree visualizations with color-coded annotations.

---

## Features

- **Trace Ancestry Paths**: Identify the shortest paths from a subject to specified founders.
- **Parent Information Extraction**: Extract parent and sex information from a dataset.
- **ID Renaming**: Replace raw IDs with TierLIDs for consistency.
- **Pedigree Visualization**: Generate pedigree plots with color-coded annotations based on tst values.
- **Configurable Workflows**: Use a YAML configuration file to customize inputs, outputs, and processing options.

---

## Installation

### Prerequisites
- Install Mamba (a faster alternative to Conda):
  ```bash
  conda install -n base -c conda-forge mamba

Clone the Repository

```bash
git clone https://github.com/your-username/pediex.git
cd pediex
```

Create and Activate the Environment
Use Mamba to create the environment and install all dependencies:

```bash
mamba env create -f environment.yml
mamba activate pediex
```

## Prepare Input Data

Place your input dataset (e.g., AllAnimals.v2.TxT) in the data/ folder. Update the configs/config.yaml file with the appropriate paths and parameters.
Configuration

The configs/config.yaml file controls the behavior of the tool. Below is an example configuration:

data_format:
  file_type: ".txt"
  columns:
    - TierID
    - tst
    - TierLID
    - gDat
    - Sex
    - VaterID
    - MutterID
    - Rasse

### Config example

```yaml
input_data: "data/AllAnimals.v2.TxT"
filter_by_descriptors:  # Optional filters (leave empty if not needed)
  # Sex: "2"  # Example: Filter for females
subject_id: "276000950288532"  # Example subject ID
founders:
  - "000009073000300"  # Example founder ID
max_generations: 20
output:
  enable_visualization: true
  visualization_folder: "outputs/visualizations"
  visualization_format: "png"
```

## Usage
Run the Main Script

```bash
python3 main.py
```
Outputs

    Parent Information:
        outputs/visualizations/parent_info.txt: Extracted parent information.
        outputs/visualizations/parent_info_renamed.txt: Parent information with renamed IDs.
    tst Information:
        outputs/visualizations/tst_info.txt: tst values for visualization.
    Pedigree Plot:
        outputs/visualizations/pedigree_tree.png: Pedigree visualization.

## How It Works

    Load Configuration:
    The main.py script reads the config.yaml file to determine input paths, subject IDs, founders, and other parameters.

    Trace Ancestry Paths:
    The trace_to_founders function finds the shortest paths from the subject to the founders.

    Extract Parent Information:
    The get_parent_info function extracts parent and sex information for all individuals in the ancestry paths.

    Rename IDs:
    The rename function replaces raw IDs with TierLIDs and collects tst values.

    Visualize Pedigree:
    The FamilyTree.R script generates a pedigree plot with color-coded annotations based on tst values.

## Visualization

The pedigree plot is generated using the FamilyTree.R script. Boxes are color-coded based on tst values:

    G (Genotyped): #688E26 (Green)
    P (In Project): #FAA613 (Yellow)
    S (Available Samples): #1E90FF (Blue)
    A (All the Rest): #550527 (Dark Red)

Example Workflow

    Input Data:
        AllAnimals.v2.TxT contains columns like TierID, VaterID, MutterID, Sex, and TierLID.

    Configuration:
        Specify the subject_id and founders in config.yaml.

    Run the Script:
        Execute main.py to generate outputs.

    Output:
        View the pedigree plot in outputs/visualizations/pedigree_tree.png.

Troubleshooting

    Legend Cutoff in Pedigree Plot:
    Adjust the par(mar = c(...)) and legend() parameters in FamilyTree.R to ensure the legend fits within the plot.

    Missing IDs:
    Ensure all fid and mid values in parent_info_renamed.txt are present in the id column.

    R Script Errors:
    Verify that the tst_info.txt file matches the IDs in parent_info_renamed.txt.

# For graphing  [pedtools](https://github.com/magnusdv/pedtools).
