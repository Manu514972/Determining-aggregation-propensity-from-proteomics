# Determining aggregation propensity from proteomics data
## What does this project do?
This program will take in a list of proteins and will compute the aggregation propensity of the proteins in that list. It will do this by comparing the input list of protein to two published datasets which measured protein aggregation propensity in two different ways: 
1. Ciryam et al. (_Ciryam, Prajwal, et al. "Widespread aggregation and neurodegenerative diseases are associated with supersaturated proteins." Cell reports 5.3 (2013): 781-790._) computed the supersaturation score (SS) of all proteins in the human proteome. The program will compare the input list of proteins to the SS list published by Ciryam et al. and will output two results: (1) the average SS for the entire list and (2) all the proteins in the input list and their associated SS in descending order. This will be done for both the unfolded SS (SSu) and folded SS (SSf) (see technical notes). 
2. Jarzab et al. (_Jarzab, Anna, et al. "Meltome atlas—thermal proteome stability across the tree of life." Nature methods 17.5 (2020): 495-503._) measured the thermal stability of proteins using a method called thermal proteome profiling (TPP) and determined the "melting temperature" (Tm) of the entire proteome (see technical notes). The program will compare the input list of proteins to the TPP list published by Jarzab et al. and will output two results: (1) the average Tm for the entire list and (2) all the proteins in the input list and their associated SS in descending order.

## Why is this useful?
- Understanding the biophysical properties of a given sample of proteins can be useful in interpretting proteomics data. This project focuses on two interesting properties (supersaturation and melting temperature), but can be easily expanded to compare and match proteins with other databases of interest. 

## Technical notes
1. A protein's intrinsic aggregation propensity can be computed based on it's primary amino acid sequence. Some proteins are observed to be expressed higher than their intrinsic aggregation propensity would predict. These are termed super saturated (SS) proteins. Ciryam et al. calculated the SS for all proteins by combining their intrinsic aggregation propensity with their measured expression level.
2. TPP measures protein thermal stability by exposing cells to an increasing gradient of heat stress, and then performing mass spectrometry on the soluble proteome of the cells at each temperature. The "melting temperature" (Tm) is defined as the temperature at which 50% of the protein becomes insoluble in the cell. 

## Input and output
Inputs:
1. A list of proteins whos aggregation properties we want to determine.
2. The supersaturation database from Ciryam et al.
3. The Tm database from Jarzab et al.
   
Output:
- The matched proteins with along with the average supersaturation score and Tm for the entire list.

## How to run
- Make sure pandas and numpy are installed.
- Run the script from the terminal providing (1) the list of proteins to be checked, (2) the supersaturation list, (3) the Tm list as arguments.
- In the terminal run the script using the following line: python Protein_aggregation.py Proteins.csv SS.xlsx Tm.xlsx. Make sure all four files are in the working directory. 
- The output excel file named "matched_proteins_output" will be added to the working directory.

This project was developed as part of the Python programming course at the Weizmann Institute of Science.
