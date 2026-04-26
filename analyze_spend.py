import pandas as pd

try:
    print('--- Search Terms Report (April 16-20) ---')
    df_st = pd.read_csv('exports/2026-04-21 1210 SearchTerms 4.16-4.20.csv', sep='\t', encoding='utf-16', low_memory=False)
    df_st['Cost'] = pd.to_numeric(df_st['Cost'].astype(str).str.replace(',', ''), errors='coerce').fillna(0)
    df_st['Conversions'] = pd.to_numeric(df_st['Conversions'].astype(str).str.replace(',', ''), errors='coerce').fillna(0)
    
    brand_terms = df_st[df_st['Search term'].str.contains('spavia', case=False, na=False)]
    non_brand_terms = df_st[~df_st['Search term'].str.contains('spavia', case=False, na=False)]
    
    brand_cost = brand_terms['Cost'].sum()
    brand_conv = brand_terms['Conversions'].sum()
    
    total_cost = df_st['Cost'].sum()
    total_conv = df_st['Conversions'].sum()
    
    print(f'Total Spend: ${total_cost:.2f}')
    print(f'Branded Spend: ${brand_cost:.2f} ({(brand_cost/total_cost)*100:.1f}%)')
    print(f'Non-Branded Spend: ${total_cost - brand_cost:.2f} ({((total_cost - brand_cost)/total_cost)*100:.1f}%)')
    print(f'\nTotal Conversions: {total_conv}')
    if total_conv > 0:
        print(f'Branded Conversions: {brand_conv} ({(brand_conv/total_conv)*100:.1f}%)')
        print(f'Non-Branded Conversions: {total_conv - brand_conv} ({((total_conv - brand_conv)/total_conv)*100:.1f}%)')

    print('\nTop 5 Branded Search Terms by Cost:')
    print(brand_terms.groupby('Search term')['Cost'].sum().nlargest(5))
except Exception as e:
    print(f"Error reading Search Terms: {e}")

try:
    print('\n--- CurrentWithStats (April 1-20) ---')
    df_cs = pd.read_csv('exports/2026-04-21 1210 CurrentWithStats 4.1-4.20.csv', sep='\t', encoding='utf-16', low_memory=False)
    df_cs['Cost'] = pd.to_numeric(df_cs['Cost'].astype(str).str.replace(',', ''), errors='coerce').fillna(0)
    df_cs['Conversions'] = pd.to_numeric(df_cs['Conversions'].astype(str).str.replace(',', ''), errors='coerce').fillna(0)
    
    # Let's find keyword spend
    if 'Keyword' in df_cs.columns:
        keywords = df_cs[df_cs['Keyword'].notna()]
        kw_total_cost = keywords['Cost'].sum()
        if kw_total_cost > 0:
            brand_kw = keywords[keywords['Keyword'].str.contains('spavia', case=False, na=False)]
            brand_kw_cost = brand_kw['Cost'].sum()
            print(f'\nTotal Keyword Level Spend: ${kw_total_cost:.2f}')
            print(f'Branded Keyword Spend: ${brand_kw_cost:.2f} ({(brand_kw_cost/kw_total_cost)*100:.1f}%)')
            
            print('\nTop Branded Keywords by Cost:')
            print(brand_kw.groupby('Keyword')['Cost'].sum().nlargest(5))

    # Campaign level spend
    campaign_rows = df_cs[df_cs['Campaign'].notna() & df_cs['Ad Group'].isna() & df_cs['Keyword'].isna()]
    if not campaign_rows.empty:
        print('\nSpend by Campaign (Total April 1-20):')
        campaign_cost = campaign_rows.groupby('Campaign')['Cost'].sum()
        print(campaign_cost[campaign_cost > 0].sort_values(ascending=False))
except Exception as e:
    print(f"Error reading CurrentWithStats: {e}")
