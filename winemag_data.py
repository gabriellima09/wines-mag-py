from datetime import datetime
import pandas as pd
import re

winesmag = pd.read_csv('data/winemag-data-130k-v2.csv')

# remove empty lines
winesmag = winesmag.dropna(how='all')
# remove empty columns
winesmag = winesmag.dropna(axis=1, how='all')
#drop first index column
winesmag = winesmag.drop(winesmag.columns[0], axis=1)

########################################################################################################################

def add_year_column(wine_df):
    """
    Adds a 'year' column to the wine DataFrame based on the 'title' column.
    The 'year' is extracted from the title, immediately following the winery name.

    Parameters:
    wine_df (pd.DataFrame): DataFrame with a 'title' column containing wine name and year.

    Returns:
    pd.DataFrame: Updated DataFrame with an additional 'year' column.
    """

    def extract_year(title):
        """
        Extracts the year from the wine title by looking for a 4-digit year
        immediately following the winery name.

        Parameters:
        title (str): Wine title string.

        Returns:
        int: Extracted year or None if not found.
        """
        # Match pattern: winery name followed by a space and 4-digit year
        # Assumes winery name is first word(s) before year
        match = re.search(r'winery\s.*?(\d{4})', title, re.IGNORECASE)
        if match:
            return int(match.group(1))
        return None

    wine_df['year'] = wine_df['title'].apply(extract_year)
    return wine_df

winesmag = add_year_column(winesmag)