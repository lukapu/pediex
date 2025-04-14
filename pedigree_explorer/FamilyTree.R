# Load required package
library(pedtools)

# Get the file path and additional arguments from the command-line arguments
args <- commandArgs(trailingOnly = TRUE)

if (length(args) < 4) {
  stop("Usage: Rscript FamilyTree.R <input_file> <subject_id> <founder_ids> <output_file>")
}

# Parse arguments
file_path <- args[1]
subject_id <- args[2]
founder_ids <- args[3]
output_file <- args[4]


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
# Load the .tst file to determine node colors
tst_file <- file.path(dirname(file_path), paste0("tst_info_", founder_ids, ".txt"))
if (!file.exists(tst_file)) {
  stop("The .tst file is missing: ", tst_file)
}

# Read the .tst file
tst_data <- read.table(tst_file, header = TRUE, stringsAsFactors = FALSE)

# Define color mapping
tst_colors <- c(
  A = "#550527",  # Red for others
  G = "#688E26",  # Green for genotyped
  P = "#FAA613",  # Orange for in project
  S = "#1E90FF"   # Blue for available samples
)

# Create a named vector with colors for each individual, default to gray if not found
node_colors <- rep("gray80", length(ped_data$id))  # Default to gray
names(node_colors) <- ped_data$id

# Assign colors based on tst value
for (i in seq_along(ped_data$id)) {
  individual_id <- ped_data$id[i]
  tst_row <- tst_data[tst_data$id == individual_id, ]
  if (nrow(tst_row) == 1 && tst_row$tst %in% names(tst_colors)) {
    node_colors[i] <- tst_colors[tst_row$tst]
  }
}

# Convert the data into a pedigree object
ped <- ped(id = ped_data$id, fid = ped_data$fid, mid = ped_data$mid, sex = ped_data$sex)

# Save the pedigree plot as a PNG file
png(output_file, width = 1200, height = 800)

# Plot pedigree
plot(
  ped,
  margin = c(3, 4, 4, 4),  # Set fixed margins (bottom, left, top, right)
  title = paste("Shortest path from:", subject_id, "to founder:", founder_ids),
  col = node_colors,  # Apply the colors
  lwd = 7
)

# Add the legend
legend(
  x = "bottomleft",
  legend = c("G - Genotyped", "P - In project", "S - Available samples for sequencing", "A - All the rest"),
  fill = c("#688E26", "#FAA613", "#1E90FF", "#550527"),
  border = "black",
  bty = "n",
  cex = 1.5,
  xpd = TRUE,
  inset = c(-0.05, 0)
)

dev.off()