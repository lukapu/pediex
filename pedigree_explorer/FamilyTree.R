# Load required package
library(pedtools)

# Get the file path and additional arguments from the command-line arguments
args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 2) {
  stop("Usage: Rscript FamilyTree.R <input_file> <subject_id> [<founder_ids>]")
}
file_path <- args[1]
subject_id <- args[2]  # Correctly use the subject_id from the arguments
founder_ids <- if (length(args) > 2) args[3:length(args)] else NULL

# Load the pedigree data
ped_data <- read.table(file_path, header = TRUE, stringsAsFactors = FALSE)

# Ensure the data has the required columns: id, fid, mid, sex
if (!all(c("id", "fid", "mid", "sex") %in% colnames(ped_data))) {
  stop("The input file must contain the columns: id, fid, mid, sex.")
}

# Identify missing parent IDs
all_parents <- unique(c(ped_data$fid, ped_data$mid))  # Combine all father and mother IDs
missing_parents <- setdiff(all_parents, ped_data$id)  # Find parents not in the `id` column
missing_parents <- missing_parents[missing_parents != 0]  # Exclude 0 (unknown parents)

# Create placeholder entries for missing parents
if (length(missing_parents) > 0) {
  placeholder_entries <- data.frame(
    id = missing_parents,
    fid = 0,  # Use 0 for unknown father
    mid = 0,  # Use 0 for unknown mother
    sex = ifelse(missing_parents %in% ped_data$fid, 1, 2)  # Assign sex based on role
  )
  ped_data <- rbind(ped_data, placeholder_entries)
}

# Ensure all individuals have both parents defined or none
for (i in 1:nrow(ped_data)) {
  if (ped_data$fid[i] != 0 && ped_data$mid[i] == 0) {
    new_id <- paste0("M", ped_data$fid[i])  # Unique placeholder ID
    if (!(new_id %in% ped_data$id)) {
      ped_data <- rbind(ped_data, data.frame(id = new_id, fid = 0, mid = 0, sex = 2))
    }
    ped_data$mid[i] <- new_id
  } else if (ped_data$fid[i] == 0 && ped_data$mid[i] != 0) {
    new_id <- paste0("F", ped_data$mid[i])  # Unique placeholder ID
    if (!(new_id %in% ped_data$id)) {
      ped_data <- rbind(ped_data, data.frame(id = new_id, fid = 0, mid = 0, sex = 1))
    }
    ped_data$fid[i] <- new_id
  }
}

# Convert the data into a pedigree object
ped <- ped(id = ped_data$id, fid = ped_data$fid, mid = ped_data$mid, sex = ped_data$sex)

# Load the tst annotation file
tst_data <- read.table("outputs/visualizations/tst_info.txt", header = TRUE, stringsAsFactors = FALSE)

# Define color mapping
tst_colors <- c(
  A = "#550527",
  G = "#688E26",
  P = "#FAA613",
  S = "#1E90FF"  # some nice blue
)

# Create a named vector with colors for each individual, default to gray if not found
ped_colors <- rep("gray80", length(ped$ID))
names(ped_colors) <- ped$ID

# Assign colors based on tst value
for (i in seq_along(ped$ID)) {
  individual_id <- ped$ID[i]
  tst_row <- tst_data[tst_data$id == individual_id, ]
  if (nrow(tst_row) == 1 && tst_row$tst %in% names(tst_colors)) {
    ped_colors[i] <- tst_colors[tst_row$tst]
  }
}


# Save the pedigree plot as a PNG file
output_dir <- "outputs/visualizations/"
if (!dir.exists(output_dir)) {
  dir.create(output_dir, recursive = TRUE)  # Create the directory if it doesn't exist
}
output_file <- paste0(output_dir, "pedigree_tree.png")
png(output_file, width = 1600, height = 900)  # Increase plot dimensions

# Adjust plot margins to make space for the legend
par(mar = c(5, 4, 4, 12))  # Increase the right margin slightly

# Plot your pedigree
plot(
  ped,
  title = paste("Path from:", subject_id, "to founder(s):", paste(founder_ids, collapse = ", ")),
  col = ped_colors,
  lwd = 7
)

# Add a custom legend
legend(
  x = "topright",  # Position the legend at the top-right corner
  inset = c(0, 0),  
  legend = c("G - Genotyped", "P - In project", "S - Available samples for sequencing", "A - All the rest"),
  fill = c("#688E26", "#FAA613", "#1E90FF", "#550527"),
  border = "black",
  bty = "n",  # No border around the legend box
  cex = 1.5,  # Increase the size of the text
  xpd = TRUE  # Allow the legend to be drawn outside the plot area
)

dev.off()