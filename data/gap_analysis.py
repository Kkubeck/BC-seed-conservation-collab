import pandas as pd
import os

# Paths
DATA_DIR = "/home/hevek/projects/BC-seed-conservation-collab/data"
TAXON_PATH = os.path.join(DATA_DIR, "vascan/taxon.txt")
DIST_PATH = os.path.join(DATA_DIR, "vascan/distribution.txt")
UBC_PATH = os.path.join(DATA_DIR, "database.csv")

OUT_MASTER = os.path.join(DATA_DIR, "bc_native_vascan_master.csv")
OUT_SUMMARY = os.path.join(DATA_DIR, "gap_analysis_summary.txt")
OUT_UNMATCHED = os.path.join(DATA_DIR, "ubc_unmatched.csv")

def run_analysis():
    print("Loading VASCAN data...")
    # 1. Load VASCAN taxon.txt
    try:
        taxon = pd.read_csv(TAXON_PATH, sep='\t', low_memory=False)
    except UnicodeDecodeError:
        taxon = pd.read_csv(TAXON_PATH, sep='\t', encoding='latin-1', low_memory=False)
    
    print(f"Taxon rows: {len(taxon)}")
    
    # Filter to accepted and specific ranks
    taxon_filtered = taxon[
        (taxon['taxonomicStatus'] == 'accepted') & 
        (taxon['taxonRank'].isin(['species', 'subspecies', 'variety']))
    ].copy()
    print(f"Filtered taxon rows (accepted + rank): {len(taxon_filtered)}")

    # 2. Load distribution.txt
    try:
        dist = pd.read_csv(DIST_PATH, sep='\t', low_memory=False)
    except UnicodeDecodeError:
        dist = pd.read_csv(DIST_PATH, sep='\t', encoding='latin-1', low_memory=False)
    
    print(f"Distribution rows: {len(dist)}")
    
    # Filter to BC native present
    dist_bc = dist[
        (dist['locality'] == 'British Columbia') & 
        (dist['occurrenceStatus'] == 'present') & 
        (dist['establishmentMeans'] == 'native')
    ].copy()
    print(f"Filtered BC native records: {len(dist_bc)}")

    # 3. Join
    # Use 'id' from both
    bc_native_master = taxon_filtered.merge(dist_bc[['id']], on='id', how='inner')
    print(f"Master BC native list size: {len(bc_native_master)}")
    
    # Save master
    cols_to_save = ['id', 'scientificName', 'family', 'genus', 'specificEpithet', 'infraspecificEpithet', 'taxonRank', 'scientificNameAuthorship']
    bc_native_master[cols_to_save].to_csv(OUT_MASTER, index=False)

    # 4. Load UBC database.csv
    ubc = pd.read_csv(UBC_PATH)
    print(f"UBC collection rows: {len(ubc)}")

    # 5. Matching
    # Normalize for matching
    bc_native_master['genus_lower'] = bc_native_master['genus'].str.lower().str.strip()
    bc_native_master['species_lower'] = bc_native_master['specificEpithet'].str.lower().str.strip()
    
    ubc['genus_lower'] = ubc['Genus'].str.lower().str.strip()
    ubc['species_lower'] = ubc['Species'].str.lower().str.strip()

    # Join UBC to Master
    matched = ubc.merge(
        bc_native_master[['genus_lower', 'species_lower', 'id', 'scientificName']], 
        on=['genus_lower', 'species_lower'], 
        how='left'
    )
    
    ubc_matched = matched[matched['id'].notna()]
    ubc_unmatched = matched[matched['id'].isna()]
    
    # The Gap: VASCAN BC natives not in UBC
    # We need to be careful with double-counting subspecies if UBC only lists species
    # Let's count by unique genus/species combinations for the basic gap
    vascan_taxa_set = set(zip(bc_native_master['genus_lower'], bc_native_master['species_lower']))
    ubc_taxa_set = set(zip(ubc['genus_lower'], ubc['species_lower']))
    
    gap_taxa = bc_native_master[~bc_native_master.set_index(['genus_lower', 'species_lower']).index.isin(ubc_taxa_set)]

    # Statistics
    total_bc_native = len(bc_native_master)
    species_count = len(bc_native_master[bc_native_master['taxonRank'] == 'species'])
    sub_var_count = len(bc_native_master[bc_native_master['taxonRank'].isin(['subspecies', 'variety'])])
    
    count_ubc_matched = len(ubc_matched)
    count_ubc_unmatched = len(ubc_unmatched)
    count_gap = len(gap_taxa)
    
    # Family summary
    family_gap = gap_taxa['family'].value_counts().head(10)
    
    # Write summary
    with open(OUT_SUMMARY, 'w') as f:
        f.write("VASCAN Gap Analysis Summary: BC Native Vascular Plants vs UBC Collection\n")
        f.write("========================================================================\n\n")
        f.write(f"Total BC-native taxa in VASCAN: {total_bc_native}\n")
        f.write(f"  - Species: {species_count}\n")
        f.write(f"  - Subspecies/Varieties: {sub_var_count}\n\n")
        f.write(f"UBC Collection Coverage (from {len(ubc)} total UBC taxa):\n")
        f.write(f"  - Matches VASCAN BC-native list: {count_ubc_matched}\n")
        f.write(f"  - No match in VASCAN BC-native list: {count_ubc_unmatched}\n\n")
        f.write(f"The Gap (VASCAN BC-native taxa NOT in UBC collection): {count_gap}\n\n")
        f.write("Top 10 Families with largest gaps (number of missing taxa):\n")
        for fam, count in family_gap.items():
            f.write(f"  - {fam}: {count}\n")

    # Save unmatched for investigation
    ubc_unmatched[['FamilyEx', 'Genus', 'Species', 'AccessionList']].to_csv(OUT_UNMATCHED, index=False)
    
    print("\nAnalysis Complete.")
    print(f"Summary written to {OUT_SUMMARY}")
    print(f"Master list written to {OUT_MASTER}")
    print(f"Unmatched UBC taxa written to {OUT_UNMATCHED}")

if __name__ == "__main__":
    run_analysis()
