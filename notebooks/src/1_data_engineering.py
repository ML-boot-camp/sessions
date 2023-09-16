# %% [markdown]
# # 🐍 Practice n°1: data engineering
#
# The objective of this session is to learn about the basics of data engineering. You
# will have to explore the **Ratebeer** dataset using sql and python.
#
#
# This dataset consists of beer reviews from ratebeer. The data span a period of more
# than 10 years, including all ~3 million reviews up to November 2011. Each review
# includes ratings in terms of five "aspects": appearance, aroma, palate, taste, and
# overall impression. Reviews include product and user information, followed by each of
# these five ratings, and a plaintext review. We also have reviews from beeradvocate.
#
# *source* [*ratebeer dataset description*](https://snap.stanford.edu/data/web-RateBeer.html)
#
# To avoid high compute time, we are going to work with a sample during the session.
# Also, the data is already cleaned.
#
#
# Here are the main steps of the notebook :
#
# 1. Preparation
# 1. Data engineering in sql with *duckdb*
# 1. Data engineering in python with *pandas*
#
# ![](https://mermaid.ink/img/pako:eNqNkD1PwzAQhv-KdVMrJYjEjUKNxAAdmWCj7nC1L62F46SOI2ir_nfsoqIOIOHB96G793ntI6hOEwhobPehtugDe36RjsWjLKFbSnhKkTTzGGhN5KV0kx79bqQwlbDKc2acCQatORDTGHCNA7E8f9Cjel9O0s0Wj9PVt-q5jDt9QhXivMB63ykaBuM2UXxMkQ07yyLCGxqSFiPnjdqSjoYu6W-OWGMsJVv3V4_44ZV_83p0GhPqilX-GwYZtORbNDp-5TGhJYQttSRBxFRTg6MNEqQ7xVEcQ_e6dwpE8CNlMPbRFS0Mbjy2IBq0Q-xGR29d116GYgniCJ8g5jdlzYuac16WxYxXVQZ7ELysbuZ3sVnPbks-43V1yuBwFihOXw_WoMg)
#
# <!-- Note for developers: to edit the mermaid diagram, use the mermaid live editor.-->
# <!-- Modify the url to access the live editor:-->
# <!-- modify https://mermaid.ink/img/pako:xxxxxx into https://mermaid.live/edit#pako:xxxxxx-->
#
# This is a data engineering tutorial in Python/pandas, it assumes you have already some
# some knowledge of data engineering in SQL.
#
# ## Preparation
#
# ### Install & import modules

# %%
# !pip install pyarrow

# %%
import pandas as pd

pd.set_option("display.max_columns", 100)

# %% [markdown]
# ## Preparation
# ### Get some doc
# - [pandas doc: main page](https://pandas.pydata.org/docs/index.html)
# - [pandas doc: API reference](https://pandas.pydata.org/docs/reference/index.html)
#
# ### Read data
#
# The data is in this git repository: [ML-boot-camp/ratebeer.git](https://github.com/ML-boot-camp/ratebeer.git).
#
# The data is located in the `ratebeer/data/` folder.

# %%
file_url = "https://github.com/ML-boot-camp/ratebeer/raw/master/data/ratebeer_sample_clean.parquet"

# %% [markdown]
# Load the file `ratebeer_sample_clean.parquet` to extract a pandas DataFrame and
# assign
# it the variable `df_raw`.
# Hint:
# - [`pd.read_parquet`](https://pandas.pydata.org/docs/reference/api/pandas.read_parquet.html)

# %%
df_raw = pd.read_parquet(file_url)

# %% [markdown]
# ## General information
# ### Shape
# Have a first overview of the dataframe size, i.e. number of rows & columns.
#
# Methods you'll need:
# - [`pd.DataFrame.shape`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.shape.html)

# %%
df_raw.shape

# %% [markdown]
# ### Overview
# Get a few information about the content of the dataframe:
# - number of null values per column
# - data type of each column
# - memory usage
#
# Methods you'll need:
# - [`pd.DataFrame.isnull`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.isnull.html)
# - [`pd.DataFrame.sum`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.sum.html)
# - [`pd.DataFrame.dtypes`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.dtypes.html)
# - [`pd.DataFrame.info`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.info.html)

# %%
df_raw.isnull().sum()

# %%
df_raw.dtypes

# %%
df_raw.info(memory_usage="deep")  # LINE TO BE REMOVED FOR STUDENTS

# %% [markdown]
# ### Sample
# Show a sample of the data
#
# Methods you'll need:
# - [`pd.DataFrame.head`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.head.html)
# - [`pd.DataFrame.sample`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.sample.html)

# %%
df_raw.head(5)

# %% [markdown]
# ### Describing statistics
# Compute statistics to understand the content of each column.
#
# Methods you'll need:
# - [`pd.DataFrame.describe`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.describe.html)
#
# Bonus: fill NaN values with an empty string `""` for a better readability using:
# - [`pd.DataFrame.fillna`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.fillna.html)

# %%
df_raw.describe(include="all").fillna("")

# %% [markdown]
# Sometimes you only need the describing statistics for a single column.
# Count and display the distinct beer names.
#
# Hint:
# - [`pd.Series.nunique`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.nunique.html?highlight=nunique#pandas.Series.nunique)
# - [`pd.Series.unique`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.unique.html?highlight=unique#pandas.Series.unique)

# %%
(df_raw.beer).nunique()  # LINE TO BE REMOVED FOR STUDENTS

# %%
(df_raw.beer).unique()  # LINE TO BE REMOVED FOR STUDENTS

# %% [markdown]
# Display the number of reviews per beer type.
#
# Hint:
# - [`pd.Series.value_counts`](https://pandas.pydata.org/docs/reference/api/pandas.Series.value_counts.html)

# %%
(df_raw.type).value_counts()  # LINE TO BE REMOVED FOR STUDENTS

# %% [markdown]
# ### Select data
# Create the following dataframe :
#
# - Keep only those columns:
#   - `beer`
#   - `alcohol`
#   - `type`
#   - `user`
#   - `rating`
# - Keep only rows for which the `type` column contains the string `"Stout"`
#
# Hint:
# - [`pd.DataFrame.loc`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.loc.html)
# - [`pd.Series.str.contains`](https://pandas.pydata.org/docs/reference/api/pandas.Series.str.contains.html)
#

# %%
selected_columns = [
    "beer",
    "alcohol",
    "type",
    "user",
    "rating",
]

df_stout = (
    (df_raw)
    .loc[:, selected_columns]
    .loc[lambda df: df.type.str.contains("Stout")]  # LINE TO BE REMOVED FOR STUDENTS
    .reset_index(drop=True)
)
df_stout

# %% [markdown]
# Compute the number of occurences of each Stout beers.

# %%
df_stout.type.value_counts()

# %% [markdown]
# ## Feature engineering
# ### High cardinality variables
# - `beer`
# - `brewery`
# - `user`
#
# All those high cardinality variables can be thought as links of a network. Indeed, a
# review is an object comprising a beer, a brewery and a user and can be thought as a
# network link between them.
#
# In other words, the review table is the a table describing the links in a network with
# 3 types of nodes: users, beers and breweries.
#
# The first property to compute about each node is its "degree", which is its number of
# connections with other nodes. High degree means "highly connected".
#
# To compute the degree you'll need:
#
# - [`pd.Series.value_counts`](https://pandas.pydata.org/docs/reference/api/pandas.Series.value_counts.html)

# %%
df_beer_degree = (
    (df_raw.beer)
    .value_counts()  # LINE TO BE REMOVED FOR STUDENTS
    .rename("beer_degree")
    .reset_index()
)
df_beer_degree

# %% [markdown]
# Check that this table will merge properly.

# %%
df_tmp = df_raw.merge(
    df_beer_degree,
    on="beer",
    how="outer",
    validate="m:1",
    indicator=True,
)
df_tmp._merge.value_counts()

# %%
df_brewery_degree = (
    (df_raw.brewery)
    .value_counts()  # LINE TO BE REMOVED FOR STUDENTS
    .rename("brewery_degree")
    .reset_index()
)
df_brewery_degree

# %% [markdown]
# Check that this table will merge properly.

# %%
df_tmp = df_raw.merge(
    df_brewery_degree,
    on="brewery",
    how="outer",
    validate="m:1",
    indicator=True,
)
df_tmp._merge.value_counts()

# %%
df_user_degree = (
    (df_raw.user)
    .value_counts()  # LINE TO BE REMOVED FOR STUDENTS
    .rename("user_degree")
    .reset_index()
)
df_user_degree

# %% [markdown]
# Check that this table will merge properly.

# %%
df_tmp = df_raw.merge(
    df_user_degree,
    on="user",
    how="outer",
    validate="m:1",
    indicator=True,
)
df_tmp._merge.value_counts()

# %% [markdown]
# We'll then merge the 3 dataframe at once.

# %% [markdown]
# ### Text length
# Compute the length of the texts in the dataset.
#
# Methods you'll need:
# - [`pd.Series.str.len`](https://pandas.pydata.org/docs/reference/api/pandas.Series.str.len.html)

# %%
text_length = df_raw.text.str.len()
text_length

# %% [markdown]
# ### Convert timestamp

# %%
date = (df_raw.timestamp).astype(int).apply(pd.Timestamp.fromtimestamp)
date

# %% [markdown]
# ### Binary target
# The prediction problem is to predict `rating` based on other information. Since
# `rating` is a numeric variable, it is a regression problem. We'd like also to do a
# classification so we'll create a binary target based on the `rating`.
#
# The `ìs_good` column is True if the rating is above or equal to 16 (expert judgement),
# False otherwise.
#
# Note: also convert the binary target to integer (O or 1) for better readability.
#
# Methods you'll need:
# - [`pd.Series.astype`](https://pandas.pydata.org/docs/reference/api/pandas.Series.astype.html)
#

# %%
is_good = (df_raw.rating >= 16).astype(int)
is_good

# %% [markdown]
# What are the values of this binary target ?

# %%
is_good.value_counts()

# %% [markdown]
# ### Combine dataframes
#
# Create a dataframe combining information from:
# - `df_raw`: the original dataset
# - `df_beer_degree`: merged on `beer` column
# - `df_brewery_degree`: merged on `brewery` column
# - `df_user_degree`: merged on `user` column
# - `text_length`: added as a new column
# - `date`: added as a new column
# - `is_good`: added as a new column
#
# Note: `merge` is the equivalent of `JOIN` in SQL, and it changes the order of the rows
# ! So to add our data columns properly in the dataset, we have 2 options:
# - add the new columns using precomputed arrays, but before merging (not recommended):
#   e.g: `df_raw.text.str.len()`
# - add the new columns using a function (recommended):
#   e.g: `lambda df: df.text.str.len()`
#
# Hint:
# - [`pd.DataFrame.merge`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.merge.html)
# - [`pd.DataFrame.assign`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.assign.html)
#
# Note: If some columns in both the left & right dataframes have the same name, you'll
# obtain duplicated columns in the merge result. `pandas` adds the suffixes `_x`
# and `_y` to avoid creating duplicate columns.
# Use the `suffixes` argument to specify the suffixes to apply to duplicated
# columns. In this example, there is no common column name in both dataframes.
#
# We made lots of transformation to our datasets: we want to verify that all
# values in the "primary keys" columns are indeed unique. Use the `validate`
# argument to do so.
#

# %%
df_main = (
    (df_raw)
    .merge(
        df_beer_degree,
        on="beer",  # LINE TO BE REMOVED FOR STUDENTS
        how="inner",
        validate="m:1",
    )
    .merge(
        df_brewery_degree,
        on="brewery",  # LINE TO BE REMOVED FOR STUDENTS
        how="inner",
        validate="m:1",
    )
    .merge(
        df_user_degree,
        on="user",  # LINE TO BE REMOVED FOR STUDENTS
        how="inner",
        validate="m:1",
    )
    .assign(text_length=lambda df: df.text.str.len())
    .assign(
        date=lambda df: (df.timestamp).astype(int).apply(pd.Timestamp.fromtimestamp)
    )
    .assign(is_good=lambda df: (df.rating >= 16).astype(int))
)
df_main

# %% [markdown]
# Save the final result to a parquet file named `ratebeer_sample_enriched.parquet`.
#
# Hint:
# - [`pd.DataFrame.to_parquet`](https://pandas.pydata.org/pandas-docs/version/1.1.5/reference/api/pandas.DataFrame.to_parquet.html)

# %%
# Uncomment the line below to save the dataset to disk
df_main.to_parquet("ratebeer_sample_enriched.parquet")

# %% [markdown]
#  GOOD JOB 👍
#
#  ![](https://c.tenor.com/Cn6yJ4YTMJgAAAAC/good-job-clapping.gif)
