import pandas as pd
import numpy as np
import sys

def load_human_protein_data(xlsx_file):
    header_row = 18254
    df = pd.read_excel(xlsx_file, sheet_name=0, header=header_row)
    df = df[['Uniprot ID', 'σf', 'σu']].copy()
    df['Protein'] = df['Uniprot ID'].str.replace('_human', '', regex=False).str.upper()
    return df

def load_melting_point_data(tm_file):
    df = pd.read_excel(tm_file, sheet_name='ma_0024')
    df['Protein'] = df['Protein ID'].str.split('_').str[0].str.upper()
    df = df[['Protein', 'Melting point [°C]']]
    df.rename(columns={'Melting point [°C]': 'Tm'}, inplace=True)
    return df

def match_proteins(input_csv, ss_xlsx, tm_xlsx, output_xlsx="matched_proteins_output.xlsx"):
    # Load input proteins
    input_proteins = pd.read_csv(input_csv, header=None)
    input_proteins.columns = ['Protein']
    input_proteins['Protein'] = input_proteins['Protein'].str.strip().str.upper()

    # --- Supersaturation Matching ---
    ss_data = load_human_protein_data(ss_xlsx)
    ss_merged = pd.merge(input_proteins, ss_data[['Protein', 'σf', 'σu']], on='Protein', how='left')
    ss_merged.rename(columns={'σf': 'SSf', 'σu': 'SSu'}, inplace=True)
    ss_merged['SSf'] = ss_merged['SSf'].where(ss_merged['SSf'].notna(), 'No data')
    ss_merged['SSu'] = ss_merged['SSu'].where(ss_merged['SSu'].notna(), 'No data')

    # Compute SS averages
    valid_ssf = pd.to_numeric(ss_merged['SSf'], errors='coerce')
    valid_ssu = pd.to_numeric(ss_merged['SSu'], errors='coerce')
    avg_ssf = valid_ssf.mean()
    avg_ssu = valid_ssu.mean()

    ss_merged['Average SSf'] = ""
    ss_merged['Average SSu'] = ""
    avg_row_ss = pd.DataFrame({
        'Protein': ['Average'],
        'SSf': [""],
        'SSu': [""],
        'Average SSf': [avg_ssf],
        'Average SSu': [avg_ssu]
    })
    ss_final = pd.concat([ss_merged, avg_row_ss], ignore_index=True)

    # --- Melting Point Matching ---
    tm_data = load_melting_point_data(tm_xlsx)
    tm_merged = pd.merge(input_proteins, tm_data, on='Protein', how='left')
    tm_merged['Tm'] = tm_merged['Tm'].where(tm_merged['Tm'].notna(), 'No data')

    # Compute Tm average
    valid_tm = pd.to_numeric(tm_merged['Tm'], errors='coerce')
    avg_tm = valid_tm.mean()

    tm_merged['Average Tm'] = ""
    avg_row_tm = pd.DataFrame({
        'Protein': ['Average'],
        'Tm': [""],
        'Average Tm': [avg_tm]
    })
    tm_final = pd.concat([tm_merged, avg_row_tm], ignore_index=True)

    # --- Output both sheets ---
    with pd.ExcelWriter(output_xlsx) as writer:
        ss_final.to_excel(writer, sheet_name="Supersaturation", index=False)
        tm_final.to_excel(writer, sheet_name="Melting Points", index=False)

    print(f"✅ Output saved to: {output_xlsx} with 2 sheets")

def load_melting_point_data(tm_file):
    df = pd.read_excel(tm_file, sheet_name='ma_0024')
    # Extract protein name after underscore
    df['Protein'] = df['Protein ID'].astype(str).str.split('_').str[1].str.upper()
    df = df[['Protein', 'Melting point [°C]']]
    df.rename(columns={'Melting point [°C]': 'Tm'}, inplace=True)
    return df

# --- Command-line interface ---
if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python match_proteins.py input_proteins.csv SS.xlsx Tm.xlsx [output.xlsx]")
        sys.exit(1)

    input_csv = sys.argv[1]
    ss_xlsx = sys.argv[2]
    tm_xlsx = sys.argv[3]
    output_file = sys.argv[4] if len(sys.argv) > 4 else "matched_proteins_output.xlsx"

    match_proteins(input_csv, ss_xlsx, tm_xlsx, output_file)
    