from pandas import DataFrame
from matplotlib.patches import Patch
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np
import colorsys

def get_top10_countries_with_top3_provinces(df: DataFrame):

    # --- Prepare data: top 10 countries; top 3 provinces per country ---
    top10 = df['country'].value_counts().head(10).index.tolist()
    df10 = df[df['country'].isin(top10)].copy()

    # full totals per country (used for sorting & annotation)
    totals = df10['country'].value_counts().sort_values(ascending=False)

    # counts by country+province
    counts = df10.groupby(['country', 'province']).size().reset_index(name='count')

    # keep top 3 provinces per country (for plotting)
    top3 = counts.sort_values(['country', 'count'], ascending=[True, False]).groupby('country').head(3)

    # ensure country order = full totals descending
    country_order = totals.index.tolist()

    # --- magma base colors per country ---
    cmap = cm.get_cmap("magma", len(country_order))
    country_base_rgb = {c: cmap(i)[:3] for i, c in enumerate(country_order)}

    # --- build per-country & per-province shades
    color_map = {}  # (country, province) -> rgb
    for country in country_order:
        pr = (top3[top3['country'] == country]
            .sort_values('count', ascending=True)   # ascending inside bar (small -> large)
            .reset_index(drop=True))
        n = len(pr)
        # lightness values (small -> light, large -> dark)
        lightness_vals = np.linspace(0.85, 0.35, n) if n > 0 else []
        base_rgb = country_base_rgb[country]
        # convert to HLS so we can change lightness
        h, l, s = colorsys.rgb_to_hls(*base_rgb)
        for i, province in enumerate(pr['province']):
            lv = float(lightness_vals[i])
            shade_rgb = colorsys.hls_to_rgb(h, lv, s)
            color_map[(country, province)] = shade_rgb

    # --- Plot ---
    fig, ax = plt.subplots(figsize=(14, 9))

    # draw stacked bars: each country as one horizontal stacked bar (provinces ascending inside)
    for country in country_order:
        pr = (top3[top3['country'] == country]
            .sort_values('count', ascending=True)   # ascending inside bar
            .reset_index(drop=True))
        
        # Calculate displayed total (sum of top 3 provinces) and remaining
        displayed_total = pr['count'].sum()
        full_total = int(totals.get(country, 0))
        remaining = full_total - displayed_total
        
        left = 0
        # Draw the top 3 provinces
        for _, row in pr.iterrows():
            prov = row['province']
            val = row['count']
            ax.barh(country, val, left=left,
                    color=color_map.get((country, prov), (0.7,0.7,0.7)),
                    edgecolor='white', height=0.6)
            left += val
        
        # Add "remaining" segment if there are other provinces
        if remaining > 0:
            ax.barh(country, remaining, left=left,
                    color=(0.9, 0.9, 0.9),  # light gray for "others"
                    edgecolor='white', height=0.6, alpha=0.7)
            left += remaining

        # annotate full country total to the right of the complete bar
        x_pos = left + totals.max() * 0.01
        ax.text(x_pos, country, f"{full_total:,}", va='center', ha='left', fontsize=9, fontweight='bold')

    # invert so largest country (first in country_order) is on top
    ax.invert_yaxis()

    # Remove axis ticks, labels, spines and grid to keep only the title + country names
    ax.xaxis.set_visible(False)
    ax.set_xlabel("")  # remove x label
    ax.set_ylabel("")  # remove y label (country names remain)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.grid(False)

    # Title only
    ax.set_title("Top 10 Countries with Their Top 3 Provinces", fontsize=16, pad=16)

    # --- Create two separate legends for better grouping ---
    # Split countries into two groups for two columns
    mid_point = len(country_order) // 2
    col1_countries = country_order[:mid_point + len(country_order) % 2]  # first half (+ 1 if odd)
    col2_countries = country_order[mid_point + len(country_order) % 2:]   # second half

    # Create handles for column 1
    handles_col1 = []
    for country in col1_countries:
        # country header patch (use base color)
        header_patch = Patch(facecolor=country_base_rgb[country], edgecolor='black', label=country)
        handles_col1.append(header_patch)

        # provinces in DESCENDING order in legend (largest -> smallest)
        pr_desc = (top3[top3['country'] == country]
                .sort_values('count', ascending=False))
        for _, row in pr_desc.iterrows():
            prov = row['province']
            prov_patch = Patch(facecolor=color_map.get((country, prov), (0.85,0.85,0.85)),
                            edgecolor='black', label=f"   └─ {prov}")
            handles_col1.append(prov_patch)
        
        # Add "Other provinces" entry if there are remaining provinces
        displayed_total = top3[top3['country'] == country]['count'].sum()
        full_total = int(totals.get(country, 0))
        if full_total > displayed_total:
            other_patch = Patch(facecolor=(0.9, 0.9, 0.9), edgecolor='black', 
                            alpha=0.7, label=f"   └─ Other provinces")
            handles_col1.append(other_patch)

    # Create handles for column 2
    handles_col2 = []
    for country in col2_countries:
        # country header patch (use base color)
        header_patch = Patch(facecolor=country_base_rgb[country], edgecolor='black', label=country)
        handles_col2.append(header_patch)

        # provinces in DESCENDING order in legend (largest -> smallest)
        pr_desc = (top3[top3['country'] == country]
                .sort_values('count', ascending=False))
        for _, row in pr_desc.iterrows():
            prov = row['province']
            prov_patch = Patch(facecolor=color_map.get((country, prov), (0.85,0.85,0.85)),
                            edgecolor='black', label=f"   └─ {prov}")
            handles_col2.append(prov_patch)
        
        # Add "Other provinces" entry if there are remaining provinces
        displayed_total = top3[top3['country'] == country]['count'].sum()
        full_total = int(totals.get(country, 0))
        if full_total > displayed_total:
            other_patch = Patch(facecolor=(0.9, 0.9, 0.9), edgecolor='black', 
                            alpha=0.7, label=f"   └─ Other provinces")
            handles_col2.append(other_patch)

    # Create two separate legends side by side
    legend1 = ax.legend(handles=handles_col1, bbox_to_anchor=(1.02, 1), loc='upper left', 
                    title=" ", frameon=False, fontsize=9, title_fontsize=10)
    ax.add_artist(legend1)  # Keep first legend when adding second

    legend2 = ax.legend(handles=handles_col2, bbox_to_anchor=(1.25, 1), loc='upper left', 
                    title=" ", frameon=False, fontsize=9, title_fontsize=10)

    plt.tight_layout()
    plt.show()