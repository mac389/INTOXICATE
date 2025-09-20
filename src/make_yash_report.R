library(rmarkdown)
library(here)

render(
  here("src","for_model","gender_vs_exposure_categorical.rmd"),
  output_format = "pdf_document",
  output_file   = "gender_vs_exposure_categorical.pdf",
  output_dir    = here("notebook","yash"),
  clean         = FALSE   
)
