import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pandas as pd
import seaborn as sns
import colorsys
import matplotlib.cm as cm
from matplotlib.patches import Patch
from scipy.stats import f_oneway

import plots
from winemag_data import winesmag

# pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
# print(winesmag.info())
# print(winesmag.head())

# Plots generation
# plots.get_top10_countries_with_top3_provinces(winesmag)
# plots.get_top10_countries_price_distribution(winesmag)
# plots.get_top10_countries_price_points_correlation(winesmag)
# plots.get_price_points_trend_over_years(winesmag)
# plots.get_description_points_relation(winesmag)
# plots.get_tasters_points_relation(winesmag)




# DATA ANALISYS AND VISUALIZATION SAMPLES

# #top 10 mais caros 
# print('CAROS')
# df_clean = winesmag.dropna(subset=['title', 'price', 'points', 'country'])
# print(df_clean[['title', 'price', 'points', 'country']].sort_values('price', ascending=False).head(10))

# #top 5 mais baratos 
# print('BARATOS')
# df_clean = winesmag.dropna(subset=['title', 'price', 'country', 'points']).groupby('title').first().reset_index()
# print(df_clean[['title', 'price', 'country', 'points']].sort_values(['price', 'points']).head())

# #top 5 vinhos por pontos c menor preço
# print('PONTOS c menor preço')
# print(winesmag[['title', 'points', 'price', 'country']].sort_values(['points', 'price'], ascending=[False, True]).head())

# Vinhos com maior qualidade por avaialiação
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

# print("\Designação dos vinhos:")
# print(high_scores['designation'].value_counts().head())



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

# # Scatter: descrição x pontos
# sns.scatterplot(data=wines_clean, x='description_length', y='points')
# plt.xlabel('Tamanho da Descrição')
# plt.ylabel('Pontuação')
# plt.title('Relação entre tamanho da descrição e pontuação')
# plt.show()

# # Boxplot: pontuação por degustador
# sns.boxplot(data=wines_clean, x='taster_name', y='points')
# plt.xticks(rotation=90)
# plt.title('Diferença de pontuação entre degustadores')
# plt.show()


# # =============================
# # Limpeza dos dados
# # =============================
# # Remove linhas com valores nulos em taster_name ou points
# wines_clean = winesmag.dropna(subset=['taster_name', 'points'])

# # Preenche valores nulos em description com string vazia
# wines_clean['description'] = wines_clean['description'].fillna('')

# # =============================
# # Média de pontos por degustador
# # =============================
# avg_points_by_taster = wines_clean.groupby('taster_name')['points'].mean().sort_values(ascending=False)
# print("Média de pontos por degustador:\n", avg_points_by_taster)

# # =============================
# # Comprimento das descrições
# # =============================
# wines_clean['description_length'] = wines_clean['description'].apply(len)

# # Top 10 descrições mais longas
# longest_descriptions = wines_clean.sort_values('description_length', ascending=False).head(10)
# print("\nTop 10 descrições mais longas:\n", longest_descriptions[['taster_name', 'points', 'description_length']])

# # =============================
# # Scatter plot: descrição x pontos (gradiente Flare)
# # =============================
# plt.figure(figsize=(10,6))

# # Cria objeto Axes
# ax = sns.scatterplot(
#     data=wines_clean,
#     x='description_length',
#     y='points',
#     hue='description_length',  # Gradiente baseado no tamanho da descrição
#     palette='flare',
#     edgecolor='k',
#     alpha=0.7,
#     legend=False
# )

# # Adiciona colorbar corretamente
# norm = mpl.colors.Normalize(vmin=wines_clean['description_length'].min(),
#                             vmax=wines_clean['description_length'].max())
# sm = mpl.cm.ScalarMappable(cmap='flare', norm=norm)
# sm.set_array([])
# plt.colorbar(sm, ax=ax, label='Tamanho da Descrição')

# ax.set_xlabel('Tamanho da Descrição', fontsize=12)
# ax.set_ylabel('Pontuação', fontsize=12)
# ax.set_title('Relação entre tamanho da descrição e pontuação', fontsize=14)
# plt.tight_layout()
# plt.show()

# # =============================
# # Boxplot ordenado pela mediana
# # =============================

# # Calcula a mediana das pontuações por degustador
# medians = wines_clean.groupby('taster_name')['points'].median().sort_values(ascending=False)

# # Lista dos degustadores ordenada pela mediana
# order = medians.index

# plt.figure(figsize=(12,6))
# sns.boxplot(
#     data=wines_clean,
#     x='taster_name',
#     y='points',
#     palette='flare',
#     order=order  # passa a ordem aqui
# )
# plt.xticks(rotation=90)
# plt.title('Diferença de pontuação entre degustadores (ordenado por mediana)', fontsize=14)
# plt.xlabel('Degustador', fontsize=12)
# plt.ylabel('Pontuação', fontsize=12)
# plt.tight_layout()
# plt.show()

# Teste ANOVA para diferença entre degustadores
# groups = [group['points'].values for name, group in wines_clean.groupby('taster_name')]
# f_stat, p_val = f_oneway(*groups)
# print(f"\nTeste ANOVA: F-statistic = {f_stat:.2f}, p-value = {p_val:.4f}")

# # Calcula correlação entre comprimento da descrição e pontuação
# correlation = wines_clean['description_length'].corr(wines_clean['points'])
# print(f"Correlação entre tamanho da descrição e pontuação: {correlation:.2f}")