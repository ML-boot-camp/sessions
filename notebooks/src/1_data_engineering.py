# %%
!pip install nb-js-diagrammers

# %%
%load_ext nb_js_diagrammers

# %% [markdown]
# # TD1 : Data Engineering
#
# The objective of this session is to learn about the basics of data engineering. You will have to explore the **Ratebeer** dataset using sql and python.
#
#
# This dataset consists of beer reviews from ratebeer. The data span a period of more than 10 years, including all ~3 million reviews up to November 2011. Each review includes ratings in terms of five "aspects": appearance, aroma, palate, taste, and overall impression. Reviews include product and user information, followed by each of these five ratings, and a plaintext review. We also have reviews from beeradvocate.
#
# *source* [*ratebeer dataset description*](https://snap.stanford.edu/data/web-RateBeer.html)
#
# To avoid high compute time, we are going to work with a sample during the session. Also, the data is already cleaned. 
#
#
# Here are the main steps of the notebook :
#
# 0.   Preparation
# 1.   Data engineering in sql with *duckdb*
# 2.   Data engineering in python with *pandas*
#

# %%
%%mermaid_magic -h 500

flowchart LR
    clean["Cleaned ratebeer\n(parquet)"]-- initialize database -->duck[(duck DB)]
    duck -- part 1: data processing\nusing sql queries --> enriched["enriched ratebeer\n(parquet file)"];
    clean -- part 2: data processing\nusing pandas ---> enriched2["enriched ratebeer\n(parquet file)"];

# %% [markdown]
# Similar data engineering steps will be performed in SQL and Python to make you appreciate the difference between these 2 languages. The output of the 2 parts will be the same, an enriched dataset that will be used in the next sessions.

# %% [markdown]
#  # 0. Preparation
#

# %% [markdown]
# ## Install & import modules

# %%
!pip install duckdb
!pip install pyarrow

# %%
import pandas as pd
import duckdb

pd.set_option("display.max_columns", 100)

# %% [markdown]
# ## Database configuration

# %%
def sql(query):
    return con.execute(query).df()


con = duckdb.connect()
con.execute("PRAGMA threads=2")
con.execute("PRAGMA enable_object_cache")

# %% [markdown]
# ## Read remote dataset

# %% [markdown]
# The data is in this git repository: [ML-boot-camp/ratebeer.git](https://github.com/ML-boot-camp/ratebeer.git).
#
# The data is located in the `ratebeer/data/` folder.
#
#

# %%
file_url = "https://github.com/ML-boot-camp/ratebeer/raw/master/data/ratebeer_sample_clean.parquet"

# %% [markdown]
# # 1. Data engineering in SQL with `duckdb`

# %% [markdown]
# ### Get some doc
#  Open the [w3schools SQL documentation](https://www.w3schools.com/sql/default.asp).

# %% [markdown]
# ### Read data

# %% [markdown]
#  Load the file `ratebeer_sample_clean.parquet` to extract a pandas DataFrame and assign
#  it the variable `table_ratebeer`.  
#  Hint:
#  - [`pd.read_parquet`](https://pandas.pydata.org/docs/reference/api/pandas.read_parquet.html)

# %%
table_ratebeer = pd.read_parquet(file_url)

# %% [markdown]
# ### Explore data

# %% [markdown]
#  Display a few reviews.
#
#  Hint:
#  - `SELECT`
#  - `FROM`
#  - `LIMIT`

# %%
query = """
SELECT *
FROM table_ratebeer
LIMIT 5
"""
sql(query)

# %% [markdown]
# Display only some columns
#
#
#  Hint:
#  - `SELECT` column_name

# %%
query = """
SELECT beer_name, review_text, review_overall --LINE TO BE REMOVED FOR STUDENTS
FROM table_ratebeer
LIMIT 5
"""
sql(query)

# %% [markdown]
# Count the total number of reviews
#
#  Hint:
#  - `COUNT`

# %%
query = """
SELECT COUNT(*) --LINE TO BE REMOVED FOR STUDENTS
FROM table_ratebeer
"""
sql(query)

# %% [markdown]
# Count the distinct number of beer names and renames it as "Number of beer names"
#
#  Hint:
#  - `SELECT`...`AS`
#  - `COUNT`
#  - `DISTINCT`
#

# %%
query = """
SELECT COUNT(DISTINCT beer_name) AS "Number of beer names" --LINE TO BE REMOVED FOR STUDENTS
FROM table_ratebeer
"""
sql(query)

# %% [markdown]
#  Display the number of reviews per beer.
#
#  Hint:
#  - `GROUP BY`
#  - `COUNT`

# %%
query = """
SELECT beer_name, COUNT(beer_name)
FROM table_ratebeer
GROUP BY beer_name
"""
sql(query)

# %% [markdown]
#  Display the 10 beers with the most reviews.
#
#  Hint:
#  - `GROUP BY`
#  - `ORDER BY`...`DESC`

# %%
query = """
SELECT beer_name, count(beer_name)
FROM table_ratebeer
GROUP BY beer_name
ORDER BY count(beer_name) DESC --LINE TO BE REMOVED FOR STUDENTS
LIMIT 10
"""
sql(query)

# %% [markdown]
#  Select the strongest API beers.
#
#  Hint:
# - `WHERE` 
# - `LIKE`
# - `ROUND`
# - `AVG`

# %%
query = """
SELECT beer_style, ROUND(AVG(beer_ABV), 2) as avg_ABV
FROM table_ratebeer
WHERE beer_style LIKE '%IPA%' --LINE TO BE REMOVED FOR STUDENTS
GROUP BY beer_style
ORDER BY avg_ABV DESC
LIMIT 5
"""
sql(query)

# %% [markdown]
# ### Create reviewers table

# %% [markdown]
# Create a `table_reviewers` view which contains for each profile name, his number of reviews and his average rating. 
#
# Hint:
#  - `CREATE VIEW ... AS`

# %%
query = """
CREATE VIEW table_reviewers
AS 
    SELECT 
        review_profileName AS profile_name,
        COUNT(review_profileName) AS number_of_reviews, --LINE TO BE REMOVED FOR STUDENTS
        ROUND(AVG(review_overall), 1) AS average_rating

    FROM table_ratebeer
    GROUP BY review_profileName
"""
sql(query)

# %% [markdown]
#  Verify that the view contains what you want.

# %%
query = """
SELECT *
FROM table_reviewers
"""
sql(query)

# %% [markdown]
# ### Combine tables

# %% [markdown]
# Join the `table_reviewers` with the `table_ratebeer`.
#
#  Hint:
#  - `JOIN`
#  - `INNER`
#  - `ON`

# %%
query = """
SELECT 
  *
FROM table_ratebeer
INNER JOIN table_reviewers
    ON table_ratebeer.review_profileName == table_reviewers.profile_name --LINE TO BE REMOVED FOR STUDENTS
LIMIT 5
"""
sql(query)

# %% [markdown]
# Save that final result to a parquet file named `ratebeer_sample_enriched.parquet`.  
# First, create a view of the table, name `table_ratebeer_enriched`.
#
#  Hint:
#  - `COPY`
#  - `TO`
#  - `FORMAT`

# %%
query = """
CREATE VIEW table_ratebeer_enriched
AS 
    SELECT *
    FROM table_ratebeer
    INNER JOIN table_reviewers
        ON table_ratebeer.review_profileName == table_reviewers.profile_name
"""
sql(query)

# %%
query = """
SELECT *
FROM table_ratebeer_enriched
LIMIT 5
"""
sql(query)

# %%
# save data (optional)

# query = """
# COPY (SELECT * FROM table_ratebeer_enriched)
# TO '/content/ratebeer/data/df_master.parquet' (FORMAT 'parquet')
# """
# sql(query)

# %% [markdown]
#  GOOD JOB 👍
#
#  ![](https://c.tenor.com/Cn6yJ4YTMJgAAAAC/good-job-clapping.gif)

# %% [markdown]
# # 2. Data engineering in python with `pandas`

# %% [markdown]
# ### Get some doc
#  - [pandas doc: main page](https://pandas.pydata.org/docs/index.html)
#  - [pandas doc: API reference](https://pandas.pydata.org/docs/reference/index.html)

# %% [markdown]
# ### Read data

# %% [markdown]
#  Load the file `ratebeer_sample_clean.parquet` to extract a pandas DataFrame and assign
#  it the variable `df_ratebeer`.  
#  Hint:
#  - [`pd.read_parquet`](https://pandas.pydata.org/docs/reference/api/pandas.read_parquet.html)

# %%
df_ratebeer = pd.read_parquet(file_url)

# %% [markdown]
# ### Explore data

# %% [markdown]
# Display a few reviews.  
#

# %%
df_ratebeer

# %% [markdown]
# Display the first 10 rows for some columns only : *beer_name*, *review_text* and *review_overall*
#
# Hint:
#  - [`pandas.DataFrame.head`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.head.html)

# %%
(
    df_ratebeer[["beer_name", "review_text", "review_overall"]]
    .head(10)  # LINE TO BE REMOVED FOR STUDENTS
)

# %% [markdown]
# Display the dimensionality of the dataset.
#
#  Hint:
#  - [`pandas.DataFrame.shape`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.shape.html)

# %%
df_ratebeer.shape  # LINE TO BE REMOVED FOR STUDENTS

# %% [markdown]
#  Check if there are missing values in the data
#
#  Hint:
#  - [`pd.DataFrame.isnull()`](https://pandas.pydata.org/docs/reference/api/pandas.isnull.html)

# %%
df_ratebeer.isnull().sum()

# %% [markdown]
# Generate descriptive statistics on the numerical variables.
#
# Hint:
#  - [`pd.DataFrame.describe`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.describe.html)

# %%
(
    df_ratebeer.describe()  # LINE TO BE REMOVED FOR STUDENTS
)

# %% [markdown]
# Display the distinct beer names and then count the distinct number of beer names.
#
#
# Hint:
#  - [`pd.Series.unique`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.unique.html?highlight=unique#pandas.Series.unique)
#  - [`pd.Series.nunique`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.nunique.html?highlight=nunique#pandas.Series.nunique)
#
#

# %%
(
    df_ratebeer.beer_name
    .unique()
)

# %%
(
    df_ratebeer.beer_name
    .nunique()  # LINE TO BE REMOVED FOR STUDENTS
)

# %% [markdown]
# Display the number of reviews per beer.
#
# Hint:
#  - [`pd.Series.value_counts`](https://pandas.pydata.org/docs/reference/api/pandas.Series.value_counts.html)

# %%
(
    df_ratebeer
    .beer_style
    .value_counts()  # LINE TO BE REMOVED FOR STUDENTS
)

# %% [markdown]
#  Create the following dataframe :
#
#  - Keep only those columns:
#    - `beer_name`,
#    - `beer_ABV`,
#    - `beer_style`,
#    - `review_profileName`,
#    - `review_text`,
#    - `review_appearance`,
#    - `review_aroma`,
#    - `review_palate`,
#    - `review_taste`,
#    - `review_overall`
#  - Keep only rows for which the `beer_style` column contains the string `"Stout"`
#
#  Hint:
#  - [`pd.DataFrame.loc`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.loc.html)
#  - [`pd.Series.str.contains`](https://pandas.pydata.org/docs/reference/api/pandas.Series.str.contains.html)
#

# %%
selected_columns = [
    "beer_name",
    "beer_ABV",
    "beer_style",
    "review_profileName",
    "review_text",
    "review_appearance",
    "review_aroma",
    "review_palate",
    "review_taste",
    "review_overall",
]

df_ratebeer_stout = (
    (df_ratebeer)
    .loc[:, selected_columns]
    .loc[lambda df: df.beer_style.str.contains("Stout")]  # LINE TO BE REMOVED FOR STUDENTS
    .reset_index(drop=True)
)

df_ratebeer_stout

# %% [markdown]
#  Compute the number of occurences of each Stout beers.
#

# %%
df_ratebeer_stout.beer_style.value_counts()

# %% [markdown]
# ### Create reviewers dataframe
#

# %% [markdown]
# Create a `df_reviewers` view which contains for each profile name, his number of reviews and his average rating.
#
# Hint:
#  - [`pandas.core.groupby.DataFrameGroupBy.agg`](https://pandas.pydata.org/pandas-docs/version/0.22/generated/pandas.core.groupby.DataFrameGroupBy.agg.html)
#  - [`pandas.DataFrame.round`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.round.html?highlight=round#pandas.DataFrame.round)
#  - [`pandas.DataFrame.reset_index`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.reset_index.html)

# %%
df_reviewers = (
    df_ratebeer
    .groupby("review_profileName")
    .agg(
        number_of_reviews=('review_profileName', 'count'),
        average_rating=('review_overall', 'mean')  # LINE TO BE REMOVED FOR STUDENTS
    )
    .round(1)
    .reset_index()
)

df_reviewers

# %%
df_ratebeer.head(2)

# %% [markdown]
# ### Combine dataframes

# %% [markdown]
# Create a dataframe combining information from the **df_ratebeer** dataset and the **df_reviewers** dataset, using `merge`.
#
# Merging is the equivalent of SQL's joining.
#
# Hint:
#  - [`pd.DataFrame.merge`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.join.html)

# %%
(
    df_ratebeer
    .merge(df_reviewers, on="review_profileName", how='inner')  # LINE TO BE REMOVED FOR STUDENTS
)

# %% [markdown]
#  If some columns in both the left & right dataframes have the same name, you'll
#  obtain duplicated columns in the merge result. `pandas` adds the suffixes `_x`
#  and `_y` to avoid creating duplicate columns.
#  Use the `suffixes` argument to specify the suffixes to apply to duplicated
#  columns. In this example, there is no common column name in both dataframes.
#
#  We made lots of transformation to our datasets: we want to verify that all
#  values in the "primary keys" columns are indeed unique. Use the `validate`
#  argument to do so.
#
#  Generate the `df_master` dataset by merging the 2 dataframes.
#

# %%
df_master = (
    df_ratebeer
    .merge(
        df_reviewers,
        on="review_profileName",  # LINE TO BE REMOVED FOR STUDENTS
        how='inner',
        validate="m:1"
    )
)

df_master.head(3)

# %% [markdown]
#  Save the final result to a parquet file named `df_master.parquet`.
#
#  Hint:
#  - [`pd.DataFrame.to_parquet`](https://pandas.pydata.org/pandas-docs/version/1.1.5/reference/api/pandas.DataFrame.to_parquet.html)

# %%
# Uncomment the line below to save the dataset to disk
# df_master.to_parquet("df_master.parquet")

# %% [markdown]
#  GOOD JOB 👍
#
#  ![](https://c.tenor.com/PgfvhIRWfrAAAAAd/jim-carrey-yes-sir.gif)


