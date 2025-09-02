"Add gender by exposure category chi-square analysis

- Initial starter exercise for examining relationship between gender and exposure types
- Includes contingency tables, chi-square test, and visualizations
- Handles zero categories and assumption checking"
# Gender by Ingestion Analysis - Starter Exercise
# Chi-square test to examine relationship between gender and exposure categories

# Load required libraries
library(dplyr)
library(ggplot2)
library(knitr)

# Step 1: Load your data from Excel
library(readxl)
# Replace 'your_file.xlsx' with actual filename
# data <- read_excel("your_file.xlsx", sheet = "Dashboard")

# Step 2: Explore the data structure
# Uncomment these lines once you load your data
# str(data)
# head(data)
# summary(data)

# Step 3: Check column names for gender and ingestion variables
# Look for columns that might represent gender (M/F, Male/Female, etc.)
# and ingestion/exposure categories
# colnames(data)

# Step 4: Clean and prepare data
# Gender is in Column C (values: M or F)
# Exposure Category is in Column D (8 categories: Alcohol, Analgesic, Antidepressants, Street Drugs, Sedatives, CO/As/CN, Unknown, Combination)

clean_data <- function(data) {
  # Remove rows with missing gender or exposure data
  clean <- data %>%
    filter(!is.na(Gender) & !is.na(`Exposure Category`)) %>%
    # Standardize gender coding 
    mutate(
      Gender = case_when(
        Gender == "M" ~ "Male",
        Gender == "F" ~ "Female",
        TRUE ~ as.character(Gender)
      ),
      # Clean up exposure categories if needed
      `Exposure Category` = trimws(`Exposure Category`)  # Remove any extra whitespace
    )
  
  return(clean)
}

# Step 5: Create contingency table
create_contingency_table <- function(data) {
  # Create cross-tabulation using correct column names
  cont_table <- table(data$Gender, data# Gender by Ingestion Analysis - Starter Exercise
# Chi-square test to examine relationship between gender and exposure categories

# Load required libraries
library(dplyr)
library(ggplot2)
library(knitr)

# Step 1: Load your data from Excel
library(readxl)
# Replace 'your_file.xlsx' with actual filename
# data <- read_excel("your_file.xlsx", sheet = "Dashboard")

# Step 2: Explore the data structure
# Uncomment these lines once you load your data
# str(data)
# head(data)
# summary(data)

# Step 3: Check column names for gender and ingestion variables
# Look for columns that might represent gender (M/F, Male/Female, etc.)
# and ingestion/exposure categories
# colnames(data)

# Step 4: Clean and prepare data
# Gender is in Column C (values: M or F)
# Exposure Category is in Column D (8 categories: Alcohol, Analgesic, Antidepressants, Street Drugs, Sedatives, CO/As/CN, Unknown, Combination)

clean_data <- function(data) {
  # Remove rows with missing gender or exposure data
  clean <- data %>%
    filter(!is.na(Gender) & !is.na(`Exposure Category`)) %>%
    # Standardize gender coding 
    mutate(
      Gender = case_when(
        Gender == "M" ~ "Male",
        Gender == "F" ~ "Female",
        TRUE ~ as.character(Gender)
      ),
      # Clean up exposure categories if needed
      `Exposure Category` = trimws(`Exposure Category`)  # Remove any extra whitespace
    )
  
  return(clean)
}

# Step 5: Create contingency table
Exposure Category`)
  
  # Print the table
  print("Contingency Table: Gender by Exposure Category")
  print(cont_table)
  
  # Convert to data frame for easier viewing
  cont_df <- as.data.frame.matrix(cont_table)
  print(knitr::kable(cont_df, caption = "Gender by Exposure Category"))
  
  return(cont_table)
}

# Step 6: Handle zero categories
examine_zero_categories <- function(cont_table) {
  # Check for categories with zero counts
  zero_counts <- which(cont_table == 0, arr.ind = TRUE)
  
  if(nrow(zero_counts) > 0) {
    print("Categories with zero counts:")
    print(zero_counts)
    print("Consider combining categories or excluding empty ones")
  }
  
  # Show row and column totals
  print("Row totals (by gender):")
  print(rowSums(cont_table))
  print("Column totals (by exposure):")
  print(colSums(cont_table))
  
  return(zero_counts)
}

# Step 7: Perform chi-square test
perform_chi_square <- function(cont_table) {
  # Chi-square test
  chi_result <- chisq.test(cont_table)
  
  print("Chi-square Test Results:")
  print(chi_result)
  
  # Check assumptions
  expected_freq <- chi_result$expected
  low_expected <- sum(expected_freq < 5)
  
  print(paste("Cells with expected frequency < 5:", low_expected))
  
  if(low_expected > 0) {
    print("Warning: Some expected frequencies < 5. Consider:")
    print("1. Combining categories")
    print("2. Using Fisher's exact test")
    print("3. Monte Carlo simulation")
  }
  
  return(chi_result)
}

# Step 8: Alternative tests if assumptions violated
perform_alternative_tests <- function(data) {
  # Fisher's exact test (for small samples)
  fisher_result <- fisher.test(table(data$Gender, data# Gender by Ingestion Analysis - Starter Exercise
# Chi-square test to examine relationship between gender and exposure categories

# Load required libraries
library(dplyr)
library(ggplot2)
library(knitr)

# Step 1: Load your data from Excel
library(readxl)
# Replace 'your_file.xlsx' with actual filename
# data <- read_excel("your_file.xlsx", sheet = "Dashboard")

# Step 2: Explore the data structure
# Uncomment these lines once you load your data
# str(data)
# head(data)
# summary(data)

# Step 3: Check column names for gender and ingestion variables
# Look for columns that might represent gender (M/F, Male/Female, etc.)
# and ingestion/exposure categories
# colnames(data)

# Step 4: Clean and prepare data
# Gender is in Column C (values: M or F)
# Exposure Category is in Column D (8 categories: Alcohol, Analgesic, Antidepressants, Street Drugs, Sedatives, CO/As/CN, Unknown, Combination)

clean_data <- function(data) {
  # Remove rows with missing gender or exposure data
  clean <- data %>%
    filter(!is.na(Gender) & !is.na(`Exposure Category`)) %>%
    # Standardize gender coding 
    mutate(
      Gender = case_when(
        Gender == "M" ~ "Male",
        Gender == "F" ~ "Female",
        TRUE ~ as.character(Gender)
      ),
      # Clean up exposure categories if needed
      `Exposure Category` = trimws(`Exposure Category`)  # Remove any extra whitespace
    )
  
  return(clean)
}

# Step 5: Create contingency table
create_contingency_table <- function(data) {
  # Create cross-tabulation using correct column names
  cont_table <- table(data$Gender, data# Gender by Ingestion Analysis - Starter Exercise
# Chi-square test to examine relationship between gender and exposure categories

# Load required libraries
library(dplyr)
library(ggplot2)
library(knitr)

# Step 1: Load your data from Excel
library(readxl)
# Replace 'your_file.xlsx' with actual filename
# data <- read_excel("your_file.xlsx", sheet = "Dashboard")

# Step 2: Explore the data structure
# Uncomment these lines once you load your data
# str(data)
# head(data)
# summary(data)

# Step 3: Check column names for gender and ingestion variables
# Look for columns that might represent gender (M/F, Male/Female, etc.)
# and ingestion/exposure categories
# colnames(data)

# Step 4: Clean and prepare data
# Gender is in Column C (values: M or F)
# Exposure Category is in Column D (8 categories: Alcohol, Analgesic, Antidepressants, Street Drugs, Sedatives, CO/As/CN, Unknown, Combination)

clean_data <- function(data) {
  # Remove rows with missing gender or exposure data
  clean <- data %>%
    filter(!is.na(Gender) & !is.na(`Exposure Category`)) %>%
    # Standardize gender coding 
    mutate(
      Gender = case_when(
        Gender == "M" ~ "Male",
        Gender == "F" ~ "Female",
        TRUE ~ as.character(Gender)
      ),
      # Clean up exposure categories if needed
      `Exposure Category` = trimws(`Exposure Category`)  # Remove any extra whitespace
    )
  
  return(clean)
}

# Step 5: Create contingency table
Exposure Category`)
  
  # Print the table
  print("Contingency Table: Gender by Exposure Category")
  print(cont_table)
  
  # Convert to data frame for easier viewing
  cont_df <- as.data.frame.matrix(cont_table)
  print(knitr::kable(cont_df, caption = "Gender by Exposure Category"))
  
  return(cont_table)
}

# Step 6: Handle zero categories
examine_zero_categories <- function(cont_table) {
  # Check for categories with zero counts
  zero_counts <- which(cont_table == 0, arr.ind = TRUE)
  
  if(nrow(zero_counts) > 0) {
    print("Categories with zero counts:")
    print(zero_counts)
    print("Consider combining categories or excluding empty ones")
  }
  
  # Show row and column totals
  print("Row totals (by gender):")
  print(rowSums(cont_table))
  print("Column totals (by exposure):")
  print(colSums(cont_table))
  
  return(zero_counts)
}

# Step 7: Perform chi-square test
perform_chi_square <- function(cont_table) {
  # Chi-square test
  chi_result <- chisq.test(cont_table)
  
  print("Chi-square Test Results:")
  print(chi_result)
  
  # Check assumptions
  expected_freq <- chi_result$expected
  low_expected <- sum(expected_freq < 5)
  
  print(paste("Cells with expected frequency < 5:", low_expected))
  
  if(low_expected > 0) {
    print("Warning: Some expected frequencies < 5. Consider:")
    print("1. Combining categories")
    print("2. Using Fisher's exact test")
    print("3. Monte Carlo simulation")
  }
  
  return(chi_result)
}

Exposure Category`))
  print("Fisher's Exact Test:")
  print(fisher_result)
  
  # If you want to try Monte Carlo simulation
  # chi_mc <- chisq.test(table(data$Gender, data# Gender by Ingestion Analysis - Starter Exercise
# Chi-square test to examine relationship between gender and exposure categories

# Load required libraries
library(dplyr)
library(ggplot2)
library(knitr)

# Step 1: Load your data from Excel
library(readxl)
# Replace 'your_file.xlsx' with actual filename
# data <- read_excel("your_file.xlsx", sheet = "Dashboard")

# Step 2: Explore the data structure
# Uncomment these lines once you load your data
# str(data)
# head(data)
# summary(data)

# Step 3: Check column names for gender and ingestion variables
# Look for columns that might represent gender (M/F, Male/Female, etc.)
# and ingestion/exposure categories
# colnames(data)

# Step 4: Clean and prepare data
# Gender is in Column C (values: M or F)
# Exposure Category is in Column D (8 categories: Alcohol, Analgesic, Antidepressants, Street Drugs, Sedatives, CO/As/CN, Unknown, Combination)

clean_data <- function(data) {
  # Remove rows with missing gender or exposure data
  clean <- data %>%
    filter(!is.na(Gender) & !is.na(`Exposure Category`)) %>%
    # Standardize gender coding 
    mutate(
      Gender = case_when(
        Gender == "M" ~ "Male",
        Gender == "F" ~ "Female",
        TRUE ~ as.character(Gender)
      ),
      # Clean up exposure categories if needed
      `Exposure Category` = trimws(`Exposure Category`)  # Remove any extra whitespace
    )
  
  return(clean)
}

# Step 5: Create contingency table
create_contingency_table <- function(data) {
  # Create cross-tabulation using correct column names
  cont_table <- table(data$Gender, data# Gender by Ingestion Analysis - Starter Exercise
# Chi-square test to examine relationship between gender and exposure categories

# Load required libraries
library(dplyr)
library(ggplot2)
library(knitr)

# Step 1: Load your data from Excel
library(readxl)
# Replace 'your_file.xlsx' with actual filename
# data <- read_excel("your_file.xlsx", sheet = "Dashboard")

# Step 2: Explore the data structure
# Uncomment these lines once you load your data
# str(data)
# head(data)
# summary(data)

# Step 3: Check column names for gender and ingestion variables
# Look for columns that might represent gender (M/F, Male/Female, etc.)
# and ingestion/exposure categories
# colnames(data)

# Step 4: Clean and prepare data
# Gender is in Column C (values: M or F)
# Exposure Category is in Column D (8 categories: Alcohol, Analgesic, Antidepressants, Street Drugs, Sedatives, CO/As/CN, Unknown, Combination)

clean_data <- function(data) {
  # Remove rows with missing gender or exposure data
  clean <- data %>%
    filter(!is.na(Gender) & !is.na(`Exposure Category`)) %>%
    # Standardize gender coding 
    mutate(
      Gender = case_when(
        Gender == "M" ~ "Male",
        Gender == "F" ~ "Female",
        TRUE ~ as.character(Gender)
      ),
      # Clean up exposure categories if needed
      `Exposure Category` = trimws(`Exposure Category`)  # Remove any extra whitespace
    )
  
  return(clean)
}

# Step 5: Create contingency table
Exposure Category`)
  
  # Print the table
  print("Contingency Table: Gender by Exposure Category")
  print(cont_table)
  
  # Convert to data frame for easier viewing
  cont_df <- as.data.frame.matrix(cont_table)
  print(knitr::kable(cont_df, caption = "Gender by Exposure Category"))
  
  return(cont_table)
}

# Step 6: Handle zero categories
examine_zero_categories <- function(cont_table) {
  # Check for categories with zero counts
  zero_counts <- which(cont_table == 0, arr.ind = TRUE)
  
  if(nrow(zero_counts) > 0) {
    print("Categories with zero counts:")
    print(zero_counts)
    print("Consider combining categories or excluding empty ones")
  }
  
  # Show row and column totals
  print("Row totals (by gender):")
  print(rowSums(cont_table))
  print("Column totals (by exposure):")
  print(colSums(cont_table))
  
  return(zero_counts)
}

# Step 7: Perform chi-square test
perform_chi_square <- function(cont_table) {
  # Chi-square test
  chi_result <- chisq.test(cont_table)
  
  print("Chi-square Test Results:")
  print(chi_result)
  
  # Check assumptions
  expected_freq <- chi_result$expected
  low_expected <- sum(expected_freq < 5)
  
  print(paste("Cells with expected frequency < 5:", low_expected))
  
  if(low_expected > 0) {
    print("Warning: Some expected frequencies < 5. Consider:")
    print("1. Combining categories")
    print("2. Using Fisher's exact test")
    print("3. Monte Carlo simulation")
  }
  
  return(chi_result)
}

Exposure Category`), 
  #                      simulate.p.value = TRUE, B = 10000)
  # print("Chi-square with Monte Carlo simulation:")
  # print(chi_mc)
}

# Step 9: Visualize the relationship
create_visualization <- function(data) {
  # Bar plot
  p1 <- ggplot(data, aes(x = `Exposure Category`, fill = Gender)) +
    geom_bar(position = "dodge") +
    theme_minimal() +
    labs(title = "Distribution of Gender by Exposure Category",
         x = "Exposure Category",
         y = "Count",
         fill = "Gender") +
    theme(axis.text.x = element_text(angle = 45, hjust = 1))
  
  print(p1)
  
  # Proportional bar plot
  p2 <- ggplot(data, aes(x = `Exposure Category`, fill = Gender)) +
    geom_bar(position = "fill") +
    theme_minimal() +
    labs(title = "Proportion of Gender by Exposure Category",
         x = "Exposure Category",
         y = "Proportion",
         fill = "Gender") +
    theme(axis.text.x = element_text(angle = 45, hjust = 1))
  
  print(p2)
}

# Step 10: Main analysis function
run_gender_ingestion_analysis <- function(data) {
  # Clean data
  clean_data_result <- clean_data(data)
  
  # Create contingency table
  cont_table <- create_contingency_table(clean_data_result)
  
  # Examine zero categories
  zero_cats <- examine_zero_categories(cont_table)
  
  # Perform chi-square test
  chi_result <- perform_chi_square(cont_table)
  
  # Create visualizations
  create_visualization(clean_data_result)
  
  # If assumptions violated, run alternative tests
  if(any(chi_result$expected < 5)) {
    perform_alternative_tests(clean_data_result)
  }
  
  return(list(
    contingency_table = cont_table,
    chi_square_result = chi_result,
    clean_data = clean_data_result
  ))
}

# Example usage (uncomment and modify once you have your data):
# results <- run_gender_ingestion_analysis(your_data)

# Debugging tips:
# 1. Start by examining your column names: colnames(data)
# 2. Check unique values: unique(data$gender), unique(data$exposure_category)
# 3. Look for missing data: sum(is.na(data$gender)), sum(is.na(data$exposure_category))
# 4. If you get errors, check data types: class(data$gender), class(data$exposure_category)
