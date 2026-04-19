import pandas as pd
import json

def analyze():
    all_current_path = 'c:/projects/repos/zeric-googleads-localdata/exports/2026-04-17 1009 AllCurrentWithStatsFrom15th16th.csv'
    search_terms_path = 'c:/projects/repos/zeric-googleads-localdata/exports/2026-04-17 1009 SearchTerms15th16th.csv'
    
    try:
        # Trying UTF-16 first, as 'null bytes' error from before might indicate the CSVs are UTF-16
        with open(all_current_path, 'rb') as f:
            head = f.read(2)
            encoding1 = 'utf-16' if head in (b'\xff\xfe', b'\xfe\xff') else 'utf-8'
        all_current = pd.read_csv(all_current_path, sep='\t', encoding=encoding1)
    except Exception as e:
        print('Error reading all_current:', e)
        all_current = pd.DataFrame()

    try:
        with open(search_terms_path, 'rb') as f:
            head = f.read(2)
            encoding2 = 'utf-16' if head in (b'\xff\xfe', b'\xfe\xff') else 'utf-8'
        search_terms = pd.read_csv(search_terms_path, sep='\t', encoding=encoding2)
    except Exception as e:
        print('Error reading search_terms:', e)
        search_terms = pd.DataFrame()

    numeric_cols = ['Clicks', 'Cost', 'Impressions', 'Conversions']
    
    def clean_numeric(df, col):
        if col in df.columns:
            if df[col].dtype == object:
                df[col] = df[col].astype(str).str.replace(',', '').astype(float)
            else:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            df[col] = df[col].fillna(0)

    for df in [all_current, search_terms]:
        if not df.empty:
            for col in numeric_cols:
                clean_numeric(df, col)
            
    if not search_terms.empty and 'Search term' in search_terms.columns:
        st_summary = search_terms.groupby('Search term')[['Clicks', 'Cost', 'Impressions', 'Conversions']].sum().reset_index()
        top_cost_st = st_summary.sort_values('Cost', ascending=False).head(10).to_dict('records')
        top_conv_st = st_summary.sort_values('Conversions', ascending=False).head(10).to_dict('records')
        top_impr_st = st_summary.sort_values('Impressions', ascending=False).head(10).to_dict('records')
    else:
        top_cost_st, top_conv_st, top_impr_st = [], [], []

    if not all_current.empty and 'Campaign' in all_current.columns:
        camp_summary = all_current.groupby('Campaign')[['Clicks', 'Cost', 'Impressions', 'Conversions']].sum().reset_index()
        top_cost_camp = camp_summary.sort_values('Cost', ascending=False).head(10).to_dict('records')
        top_conv_camp = camp_summary.sort_values('Conversions', ascending=False).head(10).to_dict('records')
        overall_totals = {
            'Clicks': float(camp_summary['Clicks'].sum()),
            'Cost': float(camp_summary['Cost'].sum()),
            'Impressions': float(camp_summary['Impressions'].sum()),
            'Conversions': float(camp_summary['Conversions'].sum())
        }
    else:
        top_cost_camp, top_conv_camp, overall_totals = [], [], {}

    output = {
        'overall_totals': overall_totals,
        'top_cost_campaigns': top_cost_camp,
        'top_conv_campaigns': top_conv_camp,
        'top_cost_search_terms': top_cost_st,
        'top_conv_search_terms': top_conv_st,
        'top_impr_search_terms': top_impr_st
    }
    
    print(json.dumps(output, indent=2))

if __name__ == '__main__':
    analyze()
