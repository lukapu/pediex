# Load required package
library(pedtools)

# Get the file path and additional arguments from the command-line arguments
args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 2) {
  stop("Usage: Rscript FamilyTree.R <input_file> <subject_id> [<founder_ids>]")
}
file_path <- args[1]
subject_id <- args[2]
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

# Save the pedigree plot as a PNG file
output_dir <- "outputs/visualizations/"
if (!dir.exists(output_dir)) {
  dir.create(output_dir, recursive = TRUE)  # Create the directory if it doesn't exist
}
output_file <- paste0(output_dir, "pedigree_tree.png")
png(output_file, width = 1920, height = 1080)
plot(ped, title = paste("Path from:", subject_id, "to founder(s):", paste(founder_ids, collapse = ", ")))
dev.off()