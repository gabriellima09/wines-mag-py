import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import colorsys
from matplotlib.patches import Patch
import matplotlib.cm as cm

import plots
from winemag_data import winesmag

pd.set_option('display.max_columns', None)
print(winesmag.info())
print(winesmag.head(10))

# Plots generation
#plots.get_top10_countries_with_top3_provinces(winesmag)

#top 10 mais caros 
df_clean = winesmag.dropna(subset=['title', 'price', 'points', 'country'])
print(df_clean[['title', 'price', 'points', 'country']].sort_values('price', ascending=False).head(10))

#top 5 mais baratos 
df_clean = winesmag.dropna(subset=['title', 'price', 'points', 'country'])
print(df_clean[['title', 'price', 'points', 'country']].sort_values('price').head())

#top 5 vinhos por pontos
print(winesmag[['title', 'points', 'price', 'country']].sort_values('points', ascending=False).head())


### BOXPLOT OK
# # Keep only rows with country and points
# df_clean = winesmag.dropna(subset=['country', 'points', 'price'])

# # Get top 10 countries by number of reviews
# top_countries = df_clean['country'].value_counts().nlargest(10).index
# df_top = df_clean[df_clean['country'].isin(top_countries)]

# # Sort countries by median price
# median_price = df_top.groupby('country')['price'].median().sort_values(ascending=False)
# sorted_countries = median_price.index
# df_top['country'] = pd.Categorical(df_top['country'], categories=sorted_countries, ordered=True)

# # Customize outliers
# flierprops = dict(marker='D', color='white', markersize=3, 
#                   markeredgecolor='black', markerfacecolor='black')

# # --- BOXPLOT ---
# plt.figure(figsize=(14,8))
# sns.boxplot(
#     data=df_top,
#     x='country',
#     y='price',
#     palette='flare',
#     flierprops=flierprops
# )
# plt.title('Price Distribution by Top 10 Countries (Sorted by Median)', fontsize=16)
# plt.xlabel('Country')
# plt.ylabel('Price')
# plt.show()
# ### BOXPLOT OK


# # Keep only rows with country, points, price
# df_clean = winesmag.dropna(subset=['country','points','price'])

# # Top 10 countries by number of reviews
# top_countries = df_clean['country'].value_counts().nlargest(10).index
# df_top = df_clean[df_clean['country'].isin(top_countries)]

# # Sort countries by median points
# median_points = df_top.groupby('country')['points'].median().sort_values(ascending=False)
# sorted_countries = median_points.index
# df_top['country'] = pd.Categorical(df_top['country'], categories=sorted_countries, ordered=True)

# sns.lineplot(df_top)
# plt.show()





# print(winesmag.info())
# print(winesmag[['title', 'year']].head(100))

# tratar dados de países desconhecidos
# tratar pontos não informados

# country_points = winesmag[['country', 'points']].groupby('country').mean().sort_values('points', ascending=False)
# print(country_points)

# wine_points = (
#     winesmag[['designation', 'province', 'region_1', 'variety', 'winery', 'points']]
#     .groupby(['designation', 'province', 'region_1', 'variety', 'winery'])
#     .mean()
#     .sort_values('points', ascending=False))
#
# print(wine_points)

#show all numeric values
# sns.pairplot(winesmag.head(1000), hue='country')
# plt.show()

# sns.violinplot(data=winesmag[['country', 'price']].head(1000), x = 'country', y = 'price', order=winesmag.groupby("country")["price"].median().sort_values(ascending=False).index)
# #sns.violinplot(data=winesmag.head(1000), x = 'country', y = 'points')
# plt.title("Wine Price Distribution by Country")
# plt.show()

# df_clean = winesmag.dropna(subset=["country", "price", "points"])

# # Take top 10 countries by median price
# top10_countries = df_clean.groupby("country")["price"].median().sort_values(ascending=False).index[:10]

# # Create boxplot with points overlay (no y-axis limit, so outliers included)
# plt.figure(figsize=(16, 8))
# sns.boxplot(
#     data=df_clean[df_clean["country"].isin(top10_countries)],
#     x="country",
#     y="price",
#     order=top10_countries,
#     showcaps=True,
#     showfliers=True,  # include outliers
#     boxprops={"facecolor": "lightblue", "edgecolor": "black"},
#     medianprops={"color": "red", "linewidth": 2},
#     whiskerprops={"color": "black"}
# )

# # Overlay wine quality (points) as jittered scatter
# # sns.stripplot(
# #     data=df_clean[df_clean["country"].isin(top10_countries)],
# #     x="country",
# #     y="price",
# #     order=top10_countries,
# #     hue="points",
# #     dodge=False,
# #     jitter=0.3,
# #     size=3,
# #     alpha=0.4,
# #     palette="viridis"
# # )

# plt.ylim(0, 200)  # cap extreme outliers

# plt.xticks(rotation=45, ha="right")
# plt.title("Wine Price Distribution by Country (Top 10 by Median Price)")
# plt.ylabel("Price (USD)")
# plt.xlabel("Country")
# plt.show()


#print(winesmag[winesmag['country'] == 'China'].head())

# df_clean = winesmag.dropna(subset=["country", "points"])

# # Take top 10 countries by median points
# top10_countries = df_clean.groupby("country")["points"].median().sort_values(ascending=False).index[:10]

# # Create boxplot with points overlay (no y-axis limit, so outliers included)
# plt.figure(figsize=(16, 8))
# sns.boxplot(
#     data=df_clean[df_clean["country"].isin(top10_countries)],
#     x="country",
#     y="points",
#     order=top10_countries,
#     showcaps=True,
#     showfliers=True,  # include outliers
#     boxprops={"facecolor": "lightblue", "edgecolor": "black"},
#     medianprops={"color": "red", "linewidth": 2},
#     whiskerprops={"color": "black"}
# )

# plt.xticks(rotation=45, ha="right")
# plt.title("Wine Points Distribution by Country (Top 10 by Median Points)")
# plt.ylabel("Points (USD)")
# plt.xlabel("Country")
# plt.show()