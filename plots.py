from pandas import DataFrame
from matplotlib.patches import Patch
from collections import Counter
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
import colorsys
import re

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
    cmap = cm.get_cmap("flare_r", len(country_order))
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
    # ax.set_title("Top 10 Países Produtores e suas Top 3 Províncias", fontsize=16, pad=16)

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
                            alpha=0.7, label=f"   └─ Outras províncias")
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
                            alpha=0.7, label=f"   └─ Outras províncias")
            handles_col2.append(other_patch)

    # Create two separate legends side by side
    legend1 = ax.legend(handles=handles_col1, bbox_to_anchor=(1.02, 1), loc='upper left', 
                    title=" ", frameon=False, fontsize=9, title_fontsize=10)
    ax.add_artist(legend1)  # Keep first legend when adding second

    legend2 = ax.legend(handles=handles_col2, bbox_to_anchor=(1.25, 1), loc='upper left', 
                    title=" ", frameon=False, fontsize=9, title_fontsize=10)

    plt.tight_layout()
    plt.savefig('img/top10_countries_with_top3_provinces.png')
    plt.show()

def get_top10_countries_price_distribution(df: pd.DataFrame):
    # Keep only rows with country and price
    df_clean = df.dropna(subset=['country', 'price'])

    # Take top 10 countries by median price
    top10_countries = (
        df_clean.groupby('country')['price']
        .median()
        .sort_values(ascending=False)
        .index[:10]
    )

    # Apply IQR filtering for each country
    def iqr_filter(subdf):
        Q1 = subdf['price'].quantile(0.25)
        Q3 = subdf['price'].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        return subdf[(subdf['price'] >= lower) & (subdf['price'] <= upper)]

    df_filtered = (
        df_clean[df_clean['country'].isin(top10_countries)]
        .groupby('country', group_keys=False)
        .apply(iqr_filter)
    )

    # Plot boxplot
    plt.figure(figsize=(16, 8))
    sns.boxplot(
        data=df_filtered,
        x='country',
        y='price',
        order=top10_countries,
        showcaps=True,
        palette="flare_r",
        whiskerprops={'color': 'black'},
        flierprops={
        'marker': 'D',
        'markerfacecolor': 'black',
        'markersize': 4,
        'linestyle': 'none'
        },        
    )

    # Remove axis labels
    plt.xlabel('')
    plt.ylabel('(USD)')

    # plt.title('Distribuição de Preços de Vinhos por País', fontsize=16, pad=16)
    plt.xticks(fontsize=12, fontweight='bold')
    plt.yticks(fontsize=12, fontweight='bold')
    plt.tight_layout()
    plt.savefig('img/top10_countries_price_distribution.png')
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

    # Rename column to empty string to remove "correlation" text
    corr_matrix.columns = ['']

    # Ordenar pela correlação (descendente)
    corr_matrix_sorted = corr_matrix.sort_values('', ascending=False)

    # Plotar heatmap
    plt.figure(figsize=(8,6))
    sns.heatmap(
        corr_matrix_sorted,
        annot=True,
        cmap='flare',
        center=0,
        cbar=True
    )

    # Remove axis labels
    plt.xlabel('')
    plt.ylabel('')

    plt.savefig('img/top10_countries_price_points_correlation.png')
    plt.show()

def get_price_points_trend_over_years(df: DataFrame):
    # Filtra vinhos com pontos, preço e ano
    wines_clean = df.dropna(subset=['points', 'price', 'year'])

    # Agrupa por ano e calcula média de pontos e preço
    summary_by_year = wines_clean.groupby('year').agg({'points':'mean', 'price':'mean'}).sort_index()

    # Preenche anos faltantes
    all_years = pd.RangeIndex(summary_by_year.index.min(), summary_by_year.index.max() + 1)
    summary_by_year = summary_by_year.reindex(all_years)

    # Paleta flare reversa
    flare_colors = sns.color_palette("flare", 2)
    points_color, price_color = flare_colors[0], flare_colors[1]

    fig, ax1 = plt.subplots(figsize=(12,6))

    # Linha de pontos
    sns.lineplot(
        x=summary_by_year.index,
        y=summary_by_year['points'],
        marker='o',
        color=points_color,
        label='Pontos',
        ax=ax1
    )
    ax1.set_xlabel('')  # Remove "Ano de Safra" label
    ax1.set_ylabel('Pontos', color=points_color)
    ax1.tick_params(axis='y', labelcolor=points_color)

    # Ajusta ticks do eixo X para anos inteiros
    from matplotlib.ticker import MultipleLocator
    ax1.xaxis.set_major_locator(MultipleLocator(1))  # Força intervalos de 1 ano
    plt.xticks(rotation=45, ha='right')

    # Segundo eixo y para preço
    ax2 = ax1.twinx()
    sns.lineplot(
        x=summary_by_year.index,
        y=summary_by_year['price'],
        marker='o',
        color=price_color,
        label='Preço Médio (USD)',
        ax=ax2
    )
    ax2.set_ylabel('Preço Médio (USD)', color=price_color)
    ax2.tick_params(axis='y', labelcolor=price_color)

    # Remove all legends
    ax1.legend().set_visible(False)
    ax2.legend().set_visible(False)

    plt.title('')  # Remove title

    plt.tight_layout()
    plt.savefig('img/price_points_trend_over_years.png')
    plt.show()

def get_description_points_relation(df: DataFrame):
    # Remove linhas com valores nulos em taster_name ou points
    wines_clean = df.dropna(subset=['taster_name', 'points'])

    # Preenche valores nulos em description com string vazia
    wines_clean['description'] = wines_clean['description'].fillna('')

    # Cria coluna com tamanho da descrição
    wines_clean['description_length'] = wines_clean['description'].apply(len)

    plt.figure(figsize=(12,6))
    
    # Usa flare_r como colormap com gradiente baseado nos pontos
    scatter = plt.scatter(
        wines_clean['description_length'], 
        wines_clean['points'],
        c=wines_clean['points'],  # Cor baseada na pontuação
        cmap='flare',           # Paleta flare reversa
        alpha=0.6,
        s=20,                     # Tamanho dos pontos
        edgecolors='white',       # Borda branca sutil
        linewidth=0.1
    )
    
    # Adiciona barra de cores
    cbar = plt.colorbar(scatter)
    cbar.set_label('', rotation=270, labelpad=20)
    
    plt.xlabel('')
    plt.ylabel('')
    # plt.title('Relação entre tamanho da descrição e pontuação', fontsize=14)
    plt.tight_layout()
    plt.savefig('img/description_points_relation.png')
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
        palette='flare_r',
        order=order,
        flierprops={
        'marker': 'D',
        'markerfacecolor': 'black',
        'markersize': 3,
        'linestyle': 'none'
        },   
    )
    plt.xticks(rotation=90)
    #plt.title('Diferença de pontuação entre degustadores (ordenado por mediana)', fontsize=14)
    plt.xlabel('')
    plt.ylabel('')
    plt.tight_layout()
    plt.savefig('img/tasters_points_relation.png')    
    plt.show()

def get_regular_premium_prices_high_quality_relation(df: DataFrame):
    # Filtra os vinhos com pontos > 90
    cols = ['country', 'description', 'designation', 'points', 'price', 'province', 'title', 'variety', 'winery', 'year']
    high_scores = df.loc[df['points'] > 90, cols]

    # Filter data to remove missing prices
    price_data = high_scores[high_scores['price'].notna()].copy()

    # Create price categories with $160 threshold
    price_data['price_category'] = price_data['price'].apply(
        lambda x: 'Premium ($160+)' if x >= 160 else 'Regular ($<160)'
    )

    # VIOLIN PLOT
    plt.figure(figsize=(10, 6))
    sns.violinplot(data=price_data, x='price_category', y='points', palette='flare')
    # plt.title('Vinhos de Preços Regulares X Premium (Alta Qualidade)', fontsize=14, fontweight='bold')
    plt.xlabel('')
    plt.ylabel('')
    plt.tight_layout()
    plt.savefig('img/regular_premium_prices_high_quality_relation.png')    
    plt.show()

def get_year_distribuition_high_quality(df: DataFrame):
    cols = ['country', 'description', 'designation', 'points', 'price', 'province', 'title', 'variety', 'winery', 'year']
    high_scores = df.loc[df['points'] > 90, cols]
    # Prepare year data
    year_data = high_scores[high_scores['year'].notna()].copy()
    year_counts = year_data['year'].value_counts().sort_index().reset_index()
    year_counts.columns = ['year', 'count']

    # BAR PLOT
    plt.figure(figsize=(14, 6))
    sns.barplot(data=year_counts, x='year', y='count', palette='flare')
    #plt.title('Distribuição de Vinhos por Ano (Alta Qualidade)', fontsize=14, fontweight='bold')
    plt.xlabel('')
    plt.ylabel('')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig('img/year_distribuition_high_quality.png')    
    plt.show()

def get_most_common_words_description_high_quality(df: DataFrame):
    cols = ['country', 'description', 'designation', 'points', 'price', 'province', 'title', 'variety', 'winery', 'year']
    high_scores = df.loc[df['points'] > 90, cols]

    # Define common stopwords to exclude
    stopwords = {'the', 'and', 'is', 'it', 'to', 'of', 'a', 'in', 'for', 'are', 'as', 
                'with', 'on', 'this', 'that', 'by', 'from', 'up', 'an', 'be', 'or',
                'at', 'but', 'not', 'have', 'has', 'will', 'more', 'can', 'been', 'very',
                'wine', 'its', 'full', 'through', 'shows', 'years', 'now', 'palate',
                'drink', 'finish', 'structure', 'nose', 'flavors', 'there', '.',
                'rich', 'well', 'long', 'while'}

    # Get all descriptions
    all_descriptions = ' '.join(high_scores['description'].dropna())

    # Extract words and filter out stopwords
    words = [word for word in re.findall(r'\b[a-zA-Z]+\b', all_descriptions.lower()) 
            if word not in stopwords and len(word) > 2]

    # Count frequencies and order descending
    word_counts = Counter(words)
    most_common = word_counts.most_common()  # Remove the limit to get all words

    # Display the results (showing top 25)
    print("Top 25 most common words in high-scoring wine descriptions:")
    for i, (word, count) in enumerate(most_common[:25], 1):
        print(f"{i:2d}. {word:<15} ({count:,} times)")

    from wordcloud import WordCloud

    # Convert to dictionary for WordCloud
    freq_dict = dict(most_common[:25])

    # Generate WordCloud
    wordcloud = WordCloud(width=800, height=400, background_color='white', colormap='flare')\
                .generate_from_frequencies(freq_dict)

    # Plot
    plt.figure(figsize=(12,6))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.savefig('img/most_common_words_description_high_quality.png')    
    plt.show()