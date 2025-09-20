from pandas import DataFrame
from matplotlib.patches import Patch
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np
import colorsys
import seaborn as sns
import pandas as pd

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

def get_top10_countries_price_distribution(df: DataFrame):
    # Keep only rows with country and price
    df_clean = df.dropna(subset=['country', 'price'])

    # Take top 10 countries by median price
    top10_countries = df_clean.groupby('country')['price'].median().sort_values(ascending=False).index[:10]

    # Create boxplot with points overlay (no y-axis limit, so outliers included)
    plt.figure(figsize=(16, 8))
    sns.boxplot(
        data=df_clean[df_clean['country'].isin(top10_countries)],
        x='country',
        y='price',
        order=top10_countries,
        showcaps=True,
        showfliers=True,  # include outliers
        boxprops={'facecolor': 'lightblue', 'edgecolor': 'black'},
        medianprops={'color': 'red', 'linewidth': 2},
        whiskerprops={'color': 'black'}
    )

    # Overlay wine quality (points) as jittered scatter
    sns.stripplot(
        data=df_clean[df_clean['country'].isin(top10_countries)],
        x='country',
        y='price',
        order=top10_countries,
        hue='points',
        dodge=False,
        jitter=0.3,
        size=3,
        alpha=0.4,
        palette='viridis'
    )

    plt.title('Wine Price Distribution by Country with Quality Overlay', fontsize=16, pad=16)
    plt.xlabel('Country', fontsize=12)
    plt.ylabel('Price', fontsize=12)
    plt.legend(title='Points', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()

def get_top10_countries_price_points_correlation(df: DataFrame):
    # Keep only rows with country and price
    df_clean = df.dropna(subset=['country', 'price', 'points'])

    # Get top 10 countries
    top_countries = df_clean['country'].value_counts().nlargest(10).index
    df_top = df_clean[df_clean['country'].isin(top_countries)]

    # OK Calcular correlação entre price e points para cada país
    corr_by_country = (
        df_top.groupby('country', group_keys=False)
        .apply(lambda g: g['price'].corr(g['points']))
        .reset_index(name='correlation')
    )

    # Transformar em matriz para heatmap
    corr_matrix = corr_by_country.set_index('country')[['correlation']]

    # Ordenar pela correlação (descendente)
    corr_matrix_sorted = corr_matrix.sort_values('correlation', ascending=False)

    # Plotar heatmap com palette 'flare'
    plt.figure(figsize=(8,6))
    sns.heatmap(
        corr_matrix_sorted,
        annot=True, cmap='rocket_r', center=0, cbar=True
    )
    plt.title('Correlation between Price and Points by Country (Sorted)', fontsize=14)
    plt.show()

def get_price_points_trend_over_years(df: DataFrame):
    # Filtra vinhos com pontos, preço e ano
    wines_clean = df.dropna(subset=['points', 'price', 'year'])

    # Agrupa por ano e calcula média de pontos e preço
    summary_by_year = wines_clean.groupby('year').agg({'points':'mean', 'price':'mean'}).sort_index()

    # Preenche anos faltantes
    all_years = pd.RangeIndex(summary_by_year.index.min(), summary_by_year.index.max() + 1)
    summary_by_year = summary_by_year.reindex(all_years)

    fig, ax1 = plt.subplots(figsize=(12,6))

    sns.lineplot(x=summary_by_year.index, y=summary_by_year['points'], marker='o', color='blue', label='Média de Pontos', ax=ax1)
    ax1.set_xlabel('Ano de Safra')
    ax1.set_ylabel('Média de Pontos', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')

    # Ticks do eixo X a cada ano
    plt.xticks(ticks=summary_by_year.index, labels=summary_by_year.index, rotation=45)

    # Segundo eixo y para preço
    ax2 = ax1.twinx()
    sns.lineplot(x=summary_by_year.index, y=summary_by_year['price'], marker='o', color='green', label='Preço Médio', ax=ax2)
    ax2.set_ylabel('Preço Médio (USD)', color='green')
    ax2.tick_params(axis='y', labelcolor='green')

    plt.title('Comparativo: Média de Pontos vs Preço Médio por Ano de Safra')
    plt.tight_layout()
    plt.show()

def get_description_points_relation(df: DataFrame):
    # Remove linhas com valores nulos em taster_name ou points
    wines_clean = df.dropna(subset=['taster_name', 'points'])

    # Preenche valores nulos em description com string vazia
    wines_clean['description'] = wines_clean['description'].fillna('')

    # Cria coluna com tamanho da descrição
    wines_clean['description_length'] = wines_clean['description'].apply(len)

    plt.figure(figsize=(12,6))
    sns.scatterplot(data=wines_clean, x='description_length', y='points', alpha=0.3)
    plt.xlabel('Tamanho da Descrição', fontsize=12)
    plt.ylabel('Pontuação', fontsize=12)
    plt.title('Relação entre tamanho da descrição e pontuação', fontsize=14)
    plt.tight_layout()
    plt.show()

def get_tasters_points_relation(df: DataFrame):
    # Remove linhas com valores nulos em taster_name ou points
    wines_clean = df.dropna(subset=['taster_name', 'points'])

    # Preenche valores nulos em description com string vazia
    wines_clean['description'] = wines_clean['description'].fillna('')

    # Boxplot ordenado pela mediana
    # Calcula a mediana das pontuações por degustador
    medians = wines_clean.groupby('taster_name')['points'].median().sort_values(ascending=False)

    # Lista dos degustadores ordenada pela mediana
    order = medians.index

    plt.figure(figsize=(12,6))
    sns.boxplot(
        data=wines_clean,
        x='taster_name',
        y='points',
        palette='flare',
        order=order  # passa a ordem aqui
    )
    plt.xticks(rotation=90)
    plt.title('Diferença de pontuação entre degustadores (ordenado por mediana)', fontsize=14)
    plt.xlabel('Degustador', fontsize=12)
    plt.ylabel('Pontuação', fontsize=12)
    plt.tight_layout()
    plt.show()



