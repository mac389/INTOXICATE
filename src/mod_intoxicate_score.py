#!/usr/bin/env python3
"""
INTOXICATE Score Calculator

This script replicates the functionality of the VB macro (macro_v2.vb) to calculate
INTOXICATE scores for patient data in Excel files.

The script reads an input Excel file, applies the INTOXICATE scoring algorithm,
and outputs a new Excel file with the calculated scores and ICU/GMF classifications.

Usage:
    python mod_intoxicate_score.py input.xlsx [endpoint_column] [classification_column]

If no column numbers are specified, defaults to column 12 for endpoint and column 13 for classification.
"""

import pandas as pd
import numpy as np
import argparse
import os
import sys
from pathlib import Path


def round_to_specified_age(age):
    """
    Round age to the nearest specified age value.
    
    Args:
        age (float): The age to round
        
    Returns:
        int: The closest age from the specified ages [20, 30, 40, 50, 60, 70]
    """
    specified_ages = [20, 30, 40, 50, 60, 70]
    
    min_difference = float('inf')
    closest_age = None
    
    for target_age in specified_ages:
        difference = abs(age - target_age)
        if difference < min_difference:
            min_difference = difference
            closest_age = target_age
    
    return closest_age


def calculate_exposure_score(exposure_category):
    """
    Calculate exposure score based on exposure category.
    
    Args:
        exposure_category (str): The exposure category
        
    Returns:
        int: The exposure score
    """
    exposure_scores = {
        "Alcohol": -5,
        "Analgesic": 1,
        "Antidepressants": 0,
        "Street Drugs": 1,
        "Sedatives": -1,
        "CO, As, CN": -6,
        "Unknown ": 2,  # Note: includes trailing space as in VB code
        "Combination": 0
    }
    
    return exposure_scores.get(exposure_category, 0)  # Default to 0 if not found


def calculate_hr_score(hr):
    """
    Calculate heart rate score.
    
    Args:
        hr (float): Heart rate value
        
    Returns:
        int: The heart rate score
    """
    if hr < 75:
        return 0
    elif hr < 85:
        return 1
    elif hr < 95:
        return 2
    elif hr < 105:
        return 3
    else:
        return 4


def calculate_sbp_score(sbp):
    """
    Calculate systolic blood pressure score.
    
    Args:
        sbp (float): Systolic blood pressure value
        
    Returns:
        int: The SBP score
    """
    if sbp >= 140:
        return -3
    elif sbp >= 130:
        return -1
    elif sbp >= 120:
        return 0
    elif sbp >= 110:
        return 1
    elif sbp >= 100:
        return 2
    else:
        return 4


def calculate_gcs_score(gcs):
    """
    Calculate Glasgow Coma Scale score.
    
    Args:
        gcs (float): GCS value
        
    Returns:
        int: The GCS score
    """
    if gcs >= 14:
        return 0
    elif gcs >= 9:
        return 3
    elif gcs >= 6:
        return 7
    else:
        return 9


def calculate_binary_score(value):
    """
    Calculate binary condition score (Yes = 1, No/other = 0).
    
    Args:
        value (str): The binary condition value
        
    Returns:
        int: 1 if "Yes", 0 otherwise
    """
    return 1 if value == "Yes" else 0


def calculate_gender_score(gender):
    """
    Calculate gender score.
    
    Args:
        gender (str): The gender value (F for Female, M for Male)
        
    Returns:
        int: -5 for Female (F), +5 for Male (M), 0 for other values
    """
    if gender == "F":
        return 0
    elif gender == "M":
        return 5
    else:
        return 0


def calculate_intoxicate_score(row):
    """
    Calculate the complete INTOXICATE score for a single patient row.
    
    Args:
        row (pandas.Series): A row of patient data
        
    Returns:
        float: The calculated INTOXICATE endpoint score
    """
    # Extract values from the row (assuming columns are in the same order as VB macro)
    gender = row.iloc[1]  # Column B (index 1)
    exposure_category = row.iloc[2]  # Column C (index 2)
    age = row.iloc[3]  # Column D (index 3)
    hr = row.iloc[4]  # Column E (index 4)
    sbp = row.iloc[5]  # Column F (index 5)
    gcs = row.iloc[6]  # Column G (index 6)
    respiratory_insufficiency = row.iloc[7]  # Column H (index 7)
    cirrhosis = row.iloc[8]  # Column I (index 8)
    dysrhythmia = row.iloc[9]  # Column J (index 9)
    second_icu_reason = row.iloc[10]  # Column K (index 10)
    
    # Round age to specified values
    age = round_to_specified_age(age)
    
    # Calculate individual scores
    exposure_score = calculate_exposure_score(exposure_category)
    hr_score = calculate_hr_score(hr)
    sbp_score = calculate_sbp_score(sbp)
    gcs_score = calculate_gcs_score(gcs)
    gender_score = calculate_gender_score(gender)
    
    # Binary condition scores
    respiratory_score = calculate_binary_score(respiratory_insufficiency) * 8
    cirrhosis_score = calculate_binary_score(cirrhosis) * 7
    dysrhythmia_score = calculate_binary_score(dysrhythmia) * 5
    secondary_diagnosis_score = calculate_binary_score(second_icu_reason) * 7
    
    # Calculate the endpoint score
    endpoint = (exposure_score + 
                ((age - 20) / 5) + 
                hr_score + 
                sbp_score + 
                gcs_score + 
                gender_score +
                respiratory_score + 
                cirrhosis_score + 
#               dysrhythmia_score + 
                secondary_diagnosis_score)
    
    return endpoint


def classify_icu_gmf(endpoint_score):
    """
    Classify patient as ICU or GMF based on endpoint score.
    
    Args:
        endpoint_score (float): The calculated endpoint score
        
    Returns:
        str: "ICU" if score > 6, "GMF" otherwise
    """
    return "ICU" if endpoint_score > 6 else "GMF"


def process_excel_file(input_file, endpoint_col=12, classification_col=13):
    """
    Process an Excel file to calculate INTOXICATE scores and classifications.
    
    Args:
        input_file (str): Path to the input Excel file
        endpoint_col (int): Column number (1-indexed) for endpoint scores
        classification_col (int): Column number (1-indexed) for ICU/GMF classification
        
    Returns:
        str: Path to the output file
    """
    # Read the Excel file from the "INTOXICATE" sheet
    try:
        df = pd.read_excel(input_file, sheet_name="INTOXICATE")
    except Exception as e:
        print(f"Error reading Excel file {input_file} from sheet 'INTOXICATE': {e}")
        sys.exit(1)
    
    # Check if we have enough columns
    if len(df.columns) < 11:
        print(f"Error: Input file must have at least 11 columns, but found {len(df.columns)}")
        sys.exit(1)
    
    # Calculate scores for each row (skip header row)
    endpoint_scores = []
    classifications = []
    
    for index, row in df.iterrows():
        try:
            endpoint_score = calculate_intoxicate_score(row)
            classification = classify_icu_gmf(endpoint_score)
            
            endpoint_scores.append(endpoint_score)
            classifications.append(classification)
        except Exception as e:
            print(f"Error processing row {index + 1}: {e}")
            endpoint_scores.append(np.nan)
            classifications.append("ERROR")
    
    # Add the calculated columns
    # Convert to 0-indexed for pandas
    endpoint_col_idx = endpoint_col - 1
    classification_col_idx = classification_col - 1
    
    # Ensure we have enough columns
    while len(df.columns) <= max(endpoint_col_idx, classification_col_idx):
        df[f'Column_{len(df.columns) + 1}'] = np.nan
    
    # Add the new columns with proper headers
    df.iloc[:, endpoint_col_idx] = endpoint_scores
    df.iloc[:, classification_col_idx] = classifications
    
    # Set column headers for the new columns
    df.columns.values[endpoint_col_idx] = "INTOXICATE SCORE"
    df.columns.values[classification_col_idx] = "Predicted Disposition"
    
    # Generate output filename
    input_path = Path(input_file)
    output_filename = f"{input_path.stem}_rescored{input_path.suffix}"
    output_path = input_path.parent / output_filename
    
    # Write the output file to the "INTOXICATE" sheet
    try:
        df.to_excel(output_path, sheet_name="INTOXICATE", index=False)
        print(f"Successfully processed {input_file}")
        print(f"Output saved to: {output_path}")
        return str(output_path)
    except Exception as e:
        print(f"Error writing output file {output_path}: {e}")
        sys.exit(1)


def main():
    """Main function to handle command line arguments and process files."""
    parser = argparse.ArgumentParser(
        description="Calculate INTOXICATE scores from Excel files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python mod_intoxicate_score.py data.xlsx
    python mod_intoxicate_score.py data.xlsx 12 13
    python mod_intoxicate_score.py /path/to/data.xlsx 15 16
        """
    )
    
    parser.add_argument('input_file', 
                       help='Path to the input Excel file')
    parser.add_argument('endpoint_column', 
                       type=int, 
                       nargs='?', 
                       default=12,
                       help='Column number (1-indexed) for endpoint scores (default: 12)')
    parser.add_argument('classification_column', 
                       type=int, 
                       nargs='?', 
                       default=13,
                       help='Column number (1-indexed) for ICU/GMF classification (default: 13)')
    
    args = parser.parse_args()
    
    # Validate input file exists
    if not os.path.exists(args.input_file):
        print(f"Error: Input file '{args.input_file}' does not exist")
        sys.exit(1)
    
    # Validate column numbers
    if args.endpoint_column < 1 or args.classification_column < 1:
        print("Error: Column numbers must be positive integers")
        sys.exit(1)
    
    if args.endpoint_column == args.classification_column:
        print("Error: Endpoint and classification columns must be different")
        sys.exit(1)
    
    # Process the file
    output_file = process_excel_file(args.input_file, 
                                   args.endpoint_column, 
                                   args.classification_column)
    
    print(f"Processing complete. Output file: {output_file}")


if __name__ == "__main__":
    main()
