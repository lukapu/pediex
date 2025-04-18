# Pediex

**Pediex** is designed to trace ancestry paths, and generate pedigree visualizations with the help of [pedtools](https://github.com/magnusdv/pedtools).

---

## Features

- **Trace Ancestry Paths**: Identify the shortest paths from a subject to specified founders.
- **Pedigree Visualization**: Generate pedigree plots with color-coded annotations based on tst values.
- **Configurable Workflows**: Use a YAML configuration file to customize inputs, outputs, and processing options.

---

## Installation

Clone the Repository

```bash
git clone https://github.com/lukapu/pediex.git
cd pediex
```

Create and Activate the Environment
Use Mamba to create the environment and install all dependencies:

```bash
mamba env create -f environment.yml
mamba activate pediex
```
Download the [pedtools](https://github.com/magnusdv/pedtools) package
```bash
R -e "install.packages('pedtools', repos='https://cran.rstudio.com/')"
```
## Prepare Input Data

Remove the example datasets and place your input dataset (e.g., AllAnimals.v2.TxT) in the data/ folder. Update the configs/config.yaml file with the appropriate paths and parameters.
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
subject_id: "276000950288532"  # Example subject ID or TierLID
founders:
  - "000009073000300"  # Example founder ID or TierLID
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
    
    Check for possible duplicates:
    Check whether there are 2 individuals with the same ID but different parents.

    Extract Parent Information:
    The get_parent_info function extracts parent and sex information for all individuals in the ancestry paths.

    Rename IDs:
    The rename function replaces raw IDs with TierLIDs and collects tst values.

    Visualize Pedigree:
    The FamilyTree.R script generates a pedigree plot with color-coded annotations based on tst values.

## Visualization

The pedigree plot is generated using the FamilyTree.R script. Boxes are color-coded based on tst values. These values and colors can be changed in the R script:

    G (Genotyped): #688E26 (Green)
    P (In Project): #FAA613 (Yellow)
    S (Available Samples): #1E90FF (Blue)
    A (All the Rest): #550527 (Dark Red)

Example Workflow

    Input Data:
        AllAnimals.v2.TxT contains columns like ID, tst, TierLID, VaterID, MutterID, Sex and rasse.

    Configuration:
        Specify the subject_id and founders in config.yaml.

    Run the Script:
        Execute main.py to generate outputs.

    Output:
        View the pedigree plot in outputs/subjectid_founderid/.

Troubleshooting

    Legend Cutoff in Pedigree Plot:
    Adjust the par(mar = c(...)) and legend() parameters (mainly position "topright","bottomleft",..) in FamilyTree.R to ensure the legend fits within the      plot.

    Missing IDs:
    Ensure all fid and mid values in parent_info_renamed.txt are present in the id column.

    R Script Errors:
    Verify that the tst_info.txt file matches the IDs in parent_info_renamed.txt.

# Graphical visualization of the shortest is achieved with [pedtools](https://github.com/magnusdv/pedtools).
