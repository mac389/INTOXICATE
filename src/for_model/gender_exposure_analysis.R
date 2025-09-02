"Add exposure by gender category chi-square analysis

- Initial exercise for examining relationship between gender and exposure types
- Includes contingency tables, chi-square test, and visualizations
- Handles zero categories and assumption checking"
# Ingestion by Gender Analysis - Starter Exercise
# Chi-square test to examine relationship between gender and exposure categories

# 1. Load Required Libraries
library(dplyr)
library(ggplot2)
library(readxl)
library(knitr)
library(stringr) # for wrapping long labels

# 2. Load Excel Data (update path if needed)
data <- read_excel("Downloads/Tox Book.v2.xlsx", sheet = "INTOXICATE")

# 3. Clean Data
clean_data <- function(data) {
  data_clean <- data %>%
    filter(!is.na(Gender), !is.na(`Exposure Category`)) %>%
    mutate(
      Gender = trimws(Gender),
      `Exposure Category` = trimws(`Exposure Category`)
    ) %>%
    filter(Gender %in% c("M", "F"))
  return(data_clean)
}

# 3b. Collapse Rare Categories
collapse_categories <- function(data) {
  rare_cats <- c("Antipsychotic", "Chlorine Gas", "clorox bleach", "Sedative (Combination)")
  data <- data %>%
    mutate(`Exposure Category` = ifelse(
      `Exposure Category` %in% rare_cats,
      paste0("Other (", paste(rare_cats, collapse = ", "), ")"),
      `Exposure Category`
    ))
  return(data)
}

# 3c. Reorder Categories
reorder_categories <- function(data) {
  categories <- unique(data$`Exposure Category`)
  other_cat <- grep("^Other", categories, value = TRUE)
  categories <- categories[!categories %in% c(other_cat, "Unknown")]
  categories <- c(categories, other_cat, "Unknown")
  data$`Exposure Category` <- factor(data$`Exposure Category`, levels = categories)
  return(data)
}

# 4. Create Contingency Table
create_contingency_table <- function(clean_data) {
  cont_table <- table(clean_data$`Exposure Category`, clean_data$Gender)
  print(knitr::kable(as.data.frame.matrix(cont_table),
                     caption = "Exposure Category by Gender"))
  return(cont_table)
}

# 5. Chi-square + Fisher's Exact Test (simulated)
perform_tests <- function(cont_table) {
  chi <- chisq.test(cont_table)
  low_expected <- sum(chi$expected < 5)
  if (low_expected > 0) {
    message("⚠️ Warning: Some expected frequencies are < 5. Chi-square may be unreliable.")
  }
  
  fisher <- fisher.test(cont_table, simulate.p.value = TRUE, B = 10000)
  
  summary_df <- data.frame(
    Test = c("Chi-square", "Fisher (Simulated)"),
    Statistic = c(round(chi$statistic, 3), NA),
    DF = c(chi$parameter, NA),
    P_Value = c(signif(chi$p.value, 4), signif(fisher$p.value, 4))
  )
  
  print(knitr::kable(summary_df, caption = "Test Results Summary"))
  
  return(list(chi_result = chi, fisher_result = fisher, summary = summary_df))
}

# 6. Visualization (wrapped labels + cleaner bar spacing)
create_visualization <- function(data) {
  # Wrap long labels at ~20 characters
  data <- data %>%
    mutate(`Exposure Category` = str_wrap(as.character(`Exposure Category`), width = 20))
  
  # Count plot
  p1 <- ggplot(data, aes(x = `Exposure Category`, fill = Gender)) +
    geom_bar(position = position_dodge(width = 0.8), width = 0.7) +
    theme_minimal(base_size = 12) +
    labs(title = "Exposure Category by Gender (Count)", 
         x = "Exposure Category", y = "Count") +
    theme(axis.text.x = element_text(angle = 45, hjust = 1, size = 10))
  print(p1)
  
  # Proportion plot
  p2 <- ggplot(data, aes(x = `Exposure Category`, fill = Gender)) +
    geom_bar(position = "fill", width = 0.7) +
    theme_minimal(base_size = 12) +
    labs(title = "Exposure Category by Gender (Proportion)", 
         x = "Exposure Category", y = "Proportion") +
    theme(axis.text.x = element_text(angle = 45, hjust = 1, size = 10))
  print(p2)
  
  return(list(count_plot = p1, proportion_plot = p2))
}

# 7. Main Function
run_analysis <- function() {
  cleaned <- clean_data(data)
  collapsed <- collapse_categories(cleaned)
  reordered <- reorder_categories(collapsed)
  cont_table <- create_contingency_table(reordered)
  test_results <- perform_tests(cont_table)
  plots <- create_visualization(reordered)
  
  return(list(
    cleaned_data = reordered,
    contingency_table = cont_table,
    chi_result = test_results$chi_result,
    fisher_result = test_results$fisher_result,
    summary = test_results$summary,
    plots = plots
  ))
}

# 8. Run Analysis
results <- run_analysis()

# 9. Optional Views
results$summary             # Clean summary table
results$contingency_table
results$plots$count_plot
results$plots$proportion_plot
