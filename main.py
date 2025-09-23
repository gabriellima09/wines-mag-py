import pandas as pd
from scipy.stats import f_oneway

import plots
from winemag_data import winesmag

# pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
# print(winesmag.info())
# print(winesmag.head())

# Plots generation
plots.get_top10_countries_with_top3_provinces(winesmag)
plots.get_top10_countries_price_distribution(winesmag)
plots.get_top10_countries_price_points_correlation(winesmag)
plots.get_price_points_trend_over_years(winesmag)
plots.get_description_points_relation(winesmag)
plots.get_tasters_points_relation(winesmag)
plots.get_regular_premium_prices_high_quality_relation(winesmag)
plots.get_year_distribuition_high_quality(winesmag)
plots.get_most_common_words_description_high_quality(winesmag)

######## DATA ANALISYS AND VISUALIZATION SAMPLES
# print(winesmag[winesmag['country'] == 'Argentina'].describe())
# print(winesmag[winesmag['country'] == 'Argentina']['price'].median())

# # Calcula a variância
# price_variance = winesmag['price'].dropna().var()  # Por padrão, usa amostra (n-1)
# print("Variância dos preços dos vinhos:", price_variance)

# #top 10 mais caros 
# print('CAROS')
# df_clean = winesmag.dropna(subset=['title', 'price', 'country', 'points'])
# print(df_clean[['title', 'price', 'country', 'points']].sort_values('price', ascending=False).head(10))

# #top 5 mais baratos 
# print('BARATOS')
# df_clean = winesmag.dropna(subset=['title', 'price', 'country', 'points']).groupby('title').first().reset_index()
# print(df_clean[['title', 'price', 'country', 'points']].sort_values(['price', 'points']).head())

# ############## Vinhos com maior qualidade por avalialiação
# # Filtra os vinhos com pontos > 90
# cols = ['country', 'description', 'designation', 'points', 'price', 'province', 'title', 'variety', 'winery', 'year']
# high_scores = winesmag.loc[winesmag['points'] > 90, cols]

# # Contagem de vinhos por país
# print("\nQuantidade de vinhos por país:")
# print(high_scores['country'].value_counts().head(10))  # top 10 países

# # Contagem de variedades de uva mais comuns
# print("\nVariedades mais frequentes:")
# print(high_scores['variety'].value_counts().head(10))

# # Preço médio por país
# print("\nPreço médio dos vinhos por país:")
# print(high_scores.groupby('country')['price'].mean().sort_values(ascending=False).head(10))

# # Distribuição por ano de produção
# print("\nDistribuição dos vinhos por ano:")
# print(high_scores['year'].value_counts().sort_index())

# print("\Descrições dos vinhos:")
# print(high_scores['description'].value_counts().head(10))

# # Normalize designation column
# winesmag['designation_normalized'] = winesmag['designation'].dropna().str.title()

# # Merge Reserve/Reserva/Riserva
# winesmag['designation_grouped'] = winesmag['designation_normalized'].replace({
#     'Reserva': 'Reserve',
#     'Riserva': 'Reserve'
# })

# # Count and calculate percentage
# designation_counts = winesmag['designation_grouped'].value_counts()
# designation_percent = (designation_counts / designation_counts.sum()) * 100

# # Média de pontos por degustador
# # Filtra apenas linhas sem valores nulos em taster_name e points
# wines_clean = winesmag.dropna(subset=['taster_name', 'points'])

# # Agrupa por degustador e calcula a média das pontuações
# avg_points_by_taster = wines_clean.groupby('taster_name')['points'].mean().sort_values(ascending=False)

# print(avg_points_by_taster)

# # Cria coluna com tamanho da descrição
# wines_clean['description_length'] = wines_clean['description'].fillna('').apply(len)

# # Top 10 descrições mais longas
# longest_descriptions = wines_clean.sort_values('description_length', ascending=False).head(10)
# print(longest_descriptions[['taster_name', 'points', 'description_length']])

# # Teste ANOVA para diferença entre degustadores
# groups = [group['points'].values for name, group in wines_clean.groupby('taster_name')]
# f_stat, p_val = f_oneway(*groups)
# print(f"\nTeste ANOVA: F-statistic = {f_stat:.2f}, p-value = {p_val:.4f}")

# # Calcula correlação entre comprimento da descrição e pontuação
# correlation = wines_clean['description_length'].corr(wines_clean['points'])
# print(f"Correlação entre tamanho da descrição e pontuação: {correlation:.2f}")


