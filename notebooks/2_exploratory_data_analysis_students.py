# %% [markdown]
# # Preparation
# ## Install & import modules

# %%
! pip install seaborn

# %%
from pathlib import Path

import numpy as np
import pandas as pd
import seaborn as sns

# %% [markdown]
# ## Read remote dataset

# %% [markdown]
# The data is in this git repository: [ML-boot-camp/ratebeer.git](https://github.com/ML-boot-camp/ratebeer.git).
#
# The data is located in the `ratebeer/data/` folder.
#

# %%
file_url = "https://github.com/ML-boot-camp/ratebeer/raw/master/data/ratebeer_sample_clean.parquet"

# %%
df_ratebeer = pd.read_parquet(file_url)

# %%
df_reviewers = (
    df_ratebeer
    .groupby("review_profileName")
    .agg(
        number_of_reviews=('review_profileName', 'count'),
        average_rating=('review_overall', 'mean')
    )
    .round(1)
    .reset_index()
)

# %%
df_master = (
    df_ratebeer
    .merge(
        df_reviewers,
        on="review_profileName",
        how='inner',
        validate="m:1"
    )
    .assign(
        review_time=lambda df: df.review_time.astype(int)
        .apply(pd.Timestamp.fromtimestamp)
    )
    .assign(
        positive_review=lambda df: (df.review_overall >= df.review_overall.median()).astype(int)
    )
)

# %% [markdown]
# # `df_master` DataFrame

# %% [markdown]
# ## General information
# Have a first overview of the dataframe size, i.e. number of rows & columns.
#
# Methods you'll need:
# - [`pd.DataFrame.shape`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.shape.html)

# %%
df_master.shape

# %% [markdown]
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
df_master.isnull().sum()

# %%
df_master.dtypes

# %%
*** FILL THE MISSING LINE ***

# %% [markdown]
# Show a sample of the data
#
# Methods you'll need:
# - [`pd.DataFrame.head`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.head.html)
# - [`pd.DataFrame.sample`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.sample.html)
#
# Bonus: display the transpose of the dataframe for better readability when having lots of columns using:
# - [`pd.DataFrame.T`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.T.html)

# %%
df_master.head(5)

# %%
df_master.sample(5).T

# %% [markdown]
# Compute statistics to understand the content of each column.
#
# Methods you'll need:
# - [`pd.DataFrame.describe`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.describe.html)
# - [`pd.Series.hist`](https://pandas.pydata.org/docs/reference/api/pandas.Series.hist.html)
# - [`pd.DataFrame.fillna`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.fillna.html)
#
# Bonus: fill NaN values with an empty string `""` for a better readability using:

# %%
df_master.describe(include="all").fillna("").T

# %% [markdown]
# ## Quantitative variables

# %% [markdown]
# `review_overall`

# %% [markdown]
# all numeric columns containing reviews: review_* & average_rating

# %%
review_columns = [
    "review_appearance",
    "review_aroma",
    *** FILL THE MISSING LINE ***
    *** FILL THE MISSING LINE ***
    *** FILL THE MISSING LINE ***
    "average_rating",
]
HISTOGRAM_SIZE = (6, 3)
(
    (df_master)
    .loc[:, review_columns]
    .plot.hist(
        bins=range(21),
        subplots=True,
        figsize=(HISTOGRAM_SIZE[0], len(review_columns) * HISTOGRAM_SIZE[1]),
    )
)

# %% [markdown]
# `number_of_reviews`

# %%
(
    (df_master)
    .number_of_reviews
    *** FILL THE MISSING LINE ***
)

# %%
(
    (df_master)
    *** FILL THE MISSING LINE ***
    .plot.hist(bins=100, loglog=True)
)

# %% [markdown]
# If interested, you can read: [Zipf's Law on Wikipedia](https://en.wikipedia.org/wiki/Zipf's_law)

# %% [markdown]
# `beer_ABV`

# %%
(
    (df_master)
    *** FILL THE MISSING LINE ***
    .plot.hist(bins=100)
)

# %%
(
    (df_master)
    *** FILL THE MISSING LINE ***
    .plot.hist(bins=100, logy=True)
)

# %% [markdown]
# `review_time` column

# %%
(
    (df_master)
    *** FILL THE MISSING LINE ***
    .describe()
)

# %%
(
    df_master
    .review_time
    *** FILL THE MISSING LINE ***
)

# %%
(
    df_master
    .pipe(sns.histplot, x="review_time", bins=100, hue="positive_review")
)

# %% [markdown]
# ## Nominal and ordinal variables:
# - `positive_review`
# - `beer_style`
# - `beer_name`
# - `beer_beerId`
# - `beer_brewerId`
# - `review_profileName`

# %% [markdown]
# `positive_review`

# %%
(
    (df_master)
    .positive_review
    .describe()
)

# %%
(
    (df_master)
    .positive_review
    .value_counts()
    .plot.bar()
)

# %% [markdown]
# `beer_style`

# %%
(
    (df_master)
    *** FILL THE MISSING LINE ***
    .describe()
)

# %%
(
    (df_master)
    .beer_style
    .value_counts()
    *** FILL THE MISSING LINE ***
)

# %%
(
    (df_master)
    .beer_style
    *** FILL THE MISSING LINE ***
    .plot.bar(logy=True)
)

# %% [markdown]
# `beer_name`

# %%
(
    (df_master)
    .beer_name
    .describe()
)

# %%
(
    (df_master)
    .beer_name
    .value_counts()
    .value_counts()
    *** FILL THE MISSING LINE ***
)

# %%
(
    (df_master)
    *** FILL THE MISSING LINE ***
    *** FILL THE MISSING LINE ***
    .value_counts()
    .plot.bar(logy=True)
)

# %%
(
    (df_master)
    .beer_name
    *** FILL THE MISSING LINE ***
    *** FILL THE MISSING LINE ***
    .plot(loglog=True, marker=".")
)

# %% [markdown]
# `beer_beerId`

# %%
(
    (df_master)
    *** FILL THE MISSING LINE ***
    .describe()
)

# %%
(
    (df_master)
    *** FILL THE MISSING LINE ***
    .value_counts()
    .value_counts()
    .plot.bar()
)

# %%
(
    (df_master)
    .beer_beerId
    *** FILL THE MISSING LINE ***
    *** FILL THE MISSING LINE ***
    .plot.bar(logy=True)
)

# %% [markdown]
# `beer_brewerId`

# %%
(
    (df_master)
    *** FILL THE MISSING LINE ***
    .describe()
)

# %%
(
    (df_master)
    .beer_brewerId
    .value_counts()
    *** FILL THE MISSING LINE ***
    .plot.bar()
)

# %%
(
    (df_master)
    .beer_brewerId
    *** FILL THE MISSING LINE ***
    .value_counts()
    .plot.bar(logy=True)
)

# %%
(
    (df_master)
    *** FILL THE MISSING LINE ***
    *** FILL THE MISSING LINE ***
    .value_counts()
    .plot(loglog=True, marker=".")
)

# %% [markdown]
# `review_profileName`

# %%
(
    (df_master)
    .review_profileName
    *** FILL THE MISSING LINE ***
)

# %%
(
    (df_master)
    *** FILL THE MISSING LINE ***
    *** FILL THE MISSING LINE ***
    .value_counts()
    .plot.bar()
)

# %%
(
    (df_master)
    *** FILL THE MISSING LINE ***
    *** FILL THE MISSING LINE ***
    .value_counts()
    .plot.bar(logy=True)
)

# %%
(
    (df_master)
    .review_profileName
    *** FILL THE MISSING LINE ***
    .value_counts()
    .plot(loglog=True, marker=".")
)

# %% [markdown]
# Plot the histogram of the `review_time` column
#
# Hint:
# - [`pd.Series.hist`](https://pandas.pydata.org/docs/reference/api/pandas.Series.hist.html)

# %% [markdown]
# `review_overall`

# %%
(
    (df_master)
    .pipe(sns.histplot, x="review_overall", bins=range(21), hue="positive_review")
)

# %% [markdown]
# `review_appearance`

# %%
(
    (df_master)
    *** FILL THE MISSING LINE ***
)

# %% [markdown]
# `review_aroma`

# %%
(
    (df_master)
    *** FILL THE MISSING LINE ***
)

# %% [markdown]
# `review_palate`

# %%
(
    *** FILL THE MISSING LINE ***
    .pipe(sns.histplot, x="review_palate", bins=range(21), hue="positive_review")
)

# %% [markdown]
# `review_taste`

# %%
(
    (df_master)
    *** FILL THE MISSING LINE ***
)

# %% [markdown]
# `beer_style`

# %%
(
    *** FILL THE MISSING LINE ***
    .pipe(sns.histplot, x="beer_style", bins=range(21), hue="positive_review")
)

# %% [markdown]
# ## High cardinality variables

# %%
(
    (df_master)
    .sample(10000)
    .assign(beer_beerId_noccurences=lambda df: df.beer_beerId.pipe(lambda s: s.replace(s.value_counts().to_dict())))
    .pipe(sns.histplot, x="beer_beerId_noccurences", bins=range(21), hue="positive_review")
)

# %%
(
    (df_master)
    .sample(10000)
    .assign(beer_brewerId_noccurences=lambda df: df.beer_brewerId.pipe(lambda s: s.replace(s.value_counts().to_dict())))
    .pipe(sns.histplot, x="beer_brewerId_noccurences", bins=range(21), hue="positive_review")
)
# %%
(
    (df_master)
    .sample(10000)
    .assign(review_profileName_noccurences=lambda df: df.review_profileName.pipe(lambda s: s.replace(s.value_counts().to_dict())))
    .pipe(sns.histplot, x="review_profileName_noccurences", bins=range(21), hue="positive_review")
)

# %% [markdown]
# ## Multivariate plots

# %% [markdown]
# Plot a scatter matrix of the numerical variables, colored by the target column
# `positive_review`.
#
# Hint:
# - [`pd.DataFrame.select_dtypes`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.select_dtypes.html)
# - [`pd.plotting.scatter_matrix`](https://pandas.pydata.org/docs/reference/api/pandas.plotting.scatter_matrix.html)

# %%
review_columns = [
    "review_appearance",
    "review_aroma",
    "review_palate",
    "review_taste",
    "review_overall",
]

def add_jitter(df, jitter=0.4):
    return df + np.random.uniform(low=-jitter, high=jitter, size=df.shape)

(
    (df_master)
    .loc[:, review_columns]
    .head(10000)
    *** FILL THE MISSING LINE ***
    .pipe(
        pd.plotting.scatter_matrix,
        figsize=(15, 15),
        *** FILL THE MISSING LINE ***
        *** FILL THE MISSING LINE ***
        *** FILL THE MISSING LINE ***
    )
)

# %% [markdown]
# ## String manipulation
# Using the [`pd.Series.str`](https://pandas.pydata.org/docs/reference/api/pandas.Series.str.html) API

# %% [markdown]
# ### `review_text` column:

# %% [markdown]
# Compute the length of the texts in the dataset.
#
# Methods you'll need:
# - [`pd.Series.str.len`](https://pandas.pydata.org/docs/reference/api/pandas.Series.str.len.html)
# - [`pd.Series.str`](https://pandas.pydata.org/docs/reference/api/pandas.Series.str..html)
#
# Bonus: plot an histogram of the values, with log values, using:
# - [`pd.Series.plot.hist`](https://pandas.pydata.org/docs/reference/api/pandas.Series.plot.bar.html)
#
# Is it a Power law distribution ?

# %%
(
    (df_master.review_text)
    .str.len()
    *** FILL THE MISSING LINE ***
)

# %%
(
    (df_master.review_text)
    *** FILL THE MISSING LINE ***
    .plot.hist(bins=range(2000), logy=True)
)

# %% [markdown]
# Compute the frequency of the most used letters in the texts
#
# Methods you'll need:
# - [`pd.Series.str.lower`](https://pandas.pydata.org/docs/reference/api/pandas.Series.str.lower.html)
# - [`pd.Series.str.split`](https://pandas.pydata.org/docs/reference/api/pandas.Series.str.split.html)
# - [`pd.Series.explode`](https://pandas.pydata.org/docs/reference/api/pandas.Series.explode.html)
# - [`pd.Series.value_counts`](https://pandas.pydata.org/docs/reference/api/pandas.Series.value_counts.html)
# - [`pd.Series.head`](https://pandas.pydata.org/docs/reference/api/pandas.Series.head.html)
#
# Bonus: plot an histogram of the values, with log values, using:
# - [`pd.Series.plot.hist`](https://pandas.pydata.org/docs/reference/api/pandas.Series.plot.bar.html)
#
# Is it a Power law distribution ?

# %%
df_most_used_letters = (
    (df_master.review_text)
    .str.lower()
    .str.split("")
    .explode()
    .loc[lambda x: x != " "]
    *** FILL THE MISSING LINE ***
)

# %%
(
    df_most_used_letters
    .head(40)
    *** FILL THE MISSING LINE ***
)

# %%
(
    df_most_used_letters
    *** FILL THE MISSING LINE ***
    .plot.bar(logy=True)
)

# %% [markdown]
# Compute the frequency of the most used words in the texts
#
# Methods you'll need:
# - [`pd.Series.str.len`](https://pandas.pydata.org/docs/reference/api/pandas.Series.str.len.html)
# - [`pd.Series.str.split`](https://pandas.pydata.org/docs/reference/api/pandas.Series.str.split.html)
# - [`pd.Series.explode`](https://pandas.pydata.org/docs/reference/api/pandas.Series.explode.html)
# - [`pd.Series.value_counts`](https://pandas.pydata.org/docs/reference/api/pandas.Series.value_counts.html)
# - [`pd.Series.head`](https://pandas.pydata.org/docs/reference/api/pandas.Series.head.html)
#
# Bonus: plot an histogram of the values, with log values, using:
# - [`pd.Series.plot.hist`](https://pandas.pydata.org/docs/reference/api/pandas.Series.plot.bar.html)
#
# Is it a Power law distribution ?

# %%
word_frequencies = (
    (df_master.review_text)
    .str.lower()
    .str.replace(r"[^a-z\ ]", "")
    .str.replace(r"\ +", " ")
    *** FILL THE MISSING LINE ***
    .explode()
    .value_counts()
)
word_frequencies

# %%
(
    word_frequencies
    .head(100)
    *** FILL THE MISSING LINE ***
)

# %%
(
    word_frequencies
    *** FILL THE MISSING LINE ***
    .plot.bar(logy=True, figsize=(12, 4))
)

# %%
(
    word_frequencies
    .head(1000)
    .reset_index(drop=True)
    .plot(loglog=True, marker=".")
)

# %% [markdown]
# ## Detailed text analysis
# Word associated to positive & negative reviews

# %%
(
    df_master
    .head(100000)
    .assign(
        tokenized_text=lambda df: (df.review_text)
        .str.lower()
        .str.replace(r"[^a-z]", " ")
        .str.replace(r" +", " ")
        .str.split(" ")
    )
    .loc[:, ["review_overall", "tokenized_text"]]
    .explode("tokenized_text")
    .groupby("tokenized_text", as_index=False)
    .agg(["mean", "count"])
    .reset_index()
    .sort_values(by=("review_overall", "count"), ascending=False)
    .head(200)
    .style.background_gradient(cmap="RdYlGn")
)
# %% [markdown]
# Count the occurences of each day of the week in `date` & plot a bar diagram,
# using the `dt` (datetime) pandas API.
#
# Hint:
# - [`pd.Series.astype`](https://pandas.pydata.org/docs/reference/api/pandas.Series.astype.html)
# - [`pd.Series.dt.dayofweek`](https://pandas.pydata.org/docs/reference/api/pandas.Series.dt.dayofweek.html)
# - [`pd.Series.value_counts`](https://pandas.pydata.org/docs/reference/api/pandas.Series.value_counts.html)
# - [`pd.Series.sort_index`](https://pandas.pydata.org/docs/reference/api/pandas.Series.sort_index.html)
# - [`pd.Series.plot.bar`](https://pandas.pydata.org/docs/reference/api/pandas.Series.plot.bar.html)

# %%
(
    (df_master.review_time)
    *** FILL THE MISSING LINE ***
    .value_counts()
    .sort_index()
    .plot.bar()
)

# %% [markdown]
# Count the percentage of each rating as a function of the `date` & plot
# a line diagram. E.g: in 2020, 55% of ratings were 5, 15% or ratings were 4, ...
#
# Hint:
# - [`sns.displot`]()

# %%
(
    df_master
    .pipe(sns.displot, x="review_time", hue="review_overall", multiple="fill", kind="kde")
)

# %%
