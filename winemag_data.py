import pandas as pd

winesmag = pd.read_csv('data/winemag-data-130k-v2.csv')

# remove empty lines
winesmag = winesmag.dropna(how='all')
# remove empty columns
winesmag = winesmag.dropna(axis=1, how='all')
#drop first index column
winesmag = winesmag.drop(winesmag.columns[0], axis=1)

########################################################################################################################

# create year column based on title combined content
import re

def add_year_column(wine_df):
    """
    Adds a 'year' column to the wine DataFrame based on the 'title' column.
    The 'year' is extracted from the title, following the winery name.

    Parameters:
    wine_df (pd.DataFrame): DataFrame with a 'title' column containing wine name and year.

    Returns:
    pd.DataFrame: Updated DataFrame with an additional 'year' column.
    """

    def extract_year(title):
        """
        Extracts the year from the wine title by looking for a 4-digit year.

        Parameters:
        title (str): Wine title string.

        Returns:
        int: Extracted year or None if not found.
        """
        # Regular expression to match a 4-digit number following the winery name
        match = re.search(r'(\d{4})\s', title)  # Match 4-digit year followed by a space

        if match:
            return int(match.group(1))  # Return the year as an integer
        return None  # If no year is found, return None

    # Apply the function to extract the year and add it as a new column
    wine_df['year'] = wine_df['title'].apply(extract_year)

    return wine_df

winesmag = add_year_column(winesmag)