# %% [markdown]
# # 🐍 Practice n°2: exploratory data analysis
# ## Preparation
# ### Install & import modules

# %%
! pip install seaborn

# %%
from pathlib import Path

import numpy as np
import pandas as pd
import seaborn as sns

# %% [markdown]
# ### Read remote dataset

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
# ## `df_master` DataFrame

# %% [markdown]
# ### General information
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
df_master.info(memory_usage="deep")  # LINE TO BE REMOVED FOR STUDENTS

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
# - [`pd.DataFrame.fillna`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.fillna.html)
#
# Bonus: fill NaN values with an empty string `""` for a better readability using:

# %%
df_master.describe(include="all").fillna("").T

# %% [markdown]
# ### Quantitative variables
#
# - `review_appearance`
# - `review_aroma`
# - `review_palate`
# - `review_taste`
# - `review_overall`
# - `average_rating`
# - `number_of_reviews`
# - `beer_ABV`

# %% [markdown]
# Methods you'll need:
# - [`pd.DataFrame.describe`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.describe.html)
# - [`pd.Series.hist`](https://pandas.pydata.org/docs/reference/api/pandas.Series.hist.html)
# - [`pd.DataFrame.fillna`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.fillna.html)

# %% [markdown]
# Describe all quantitative variables

# %%
pd.set_option("display.precision", 2)

# %%
quantitative_columns = [
    "review_appearance",
    "review_aroma",
    "review_palate",
    "review_taste",
    "review_overall",
    "average_rating",
    "number_of_reviews",
    "beer_ABV",
]
(
    (df_master)
    .loc[:, quantitative_columns]
    .describe()  # LINE TO BE REMOVED FOR STUDENTS
    .T  # LINE TO BE REMOVED FOR STUDENTS
    .style.background_gradient().set_precision(2)  # LINE TO BE REMOVED FOR STUDENTS
)

# %% [markdown]
# Describe and plot all numeric columns containing reviews: review_* & average_rating

# %%
review_columns = [
    "review_appearance",
    "review_aroma",
    "review_palate",  # LINE TO BE REMOVED FOR STUDENTS
    "review_taste",  # LINE TO BE REMOVED FOR STUDENTS
    "review_overall",  # LINE TO BE REMOVED FOR STUDENTS
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
# Plot `number_of_reviews`

# %%
(
    (df_master)
    .number_of_reviews
    .plot.hist(bins=100)  # LINE TO BE REMOVED FOR STUDENTS
)

# %%
(
    (df_master)
    .number_of_reviews  # LINE TO BE REMOVED FOR STUDENTS
    .plot.hist(bins=100, loglog=True)
)

# %% [markdown]
# If interested, you can read: [Zipf's Law on Wikipedia](https://en.wikipedia.org/wiki/Zipf's_law)

# %% [markdown]
# Plot `beer_ABV`

# %%
(
    (df_master)
    .beer_ABV  # LINE TO BE REMOVED FOR STUDENTS
    .plot.hist(bins=100)
)

# %%
(
    (df_master)
    .beer_ABV  # LINE TO BE REMOVED FOR STUDENTS
    .plot.hist(bins=100, logy=True)
)

# %% [markdown]
# Plot `review_time`

# %%
(
    df_master
    .review_time
    .hist(bins=100)  # LINE TO BE REMOVED FOR STUDENTS
)

# %% [markdown]
# ### Nominal and ordinal variables:
# - `positive_review`
# - `beer_style`
# - `beer_name`
# - `beer_beerId`
# - `beer_brewerId`
# - `review_profileName`

# %% [markdown]
# Describe and plot `positive_review`

# %%
(
    (df_master)
    .positive_review
    .describe()  # LINE TO BE REMOVED FOR STUDENTS
)

# %%
(
    (df_master)
    .positive_review
    .value_counts()  # LINE TO BE REMOVED FOR STUDENTS
    .plot.bar()  # LINE TO BE REMOVED FOR STUDENTS
)

# %% [markdown]
# Describe and plot `beer_style`

# %%
(
    (df_master)
    .beer_style  # LINE TO BE REMOVED FOR STUDENTS
    .describe()
)

# %%
(
    (df_master)
    .beer_style
    .value_counts()
    .plot.bar()  # LINE TO BE REMOVED FOR STUDENTS
)

# %%
(
    (df_master)
    .beer_style
    .value_counts()  # LINE TO BE REMOVED FOR STUDENTS
    .plot.bar(logy=True)
)

# %% [markdown]
# Describe and plot `beer_name`

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
    .plot.bar()  # LINE TO BE REMOVED FOR STUDENTS
)

# %%
(
    (df_master)
    .beer_name  # LINE TO BE REMOVED FOR STUDENTS
    .value_counts()  # LINE TO BE REMOVED FOR STUDENTS
    .value_counts()
    .plot.bar(logy=True)
)

# %%
(
    (df_master)
    .beer_name
    .value_counts()  # LINE TO BE REMOVED FOR STUDENTS
    .value_counts()  # LINE TO BE REMOVED FOR STUDENTS
    .plot(loglog=True, marker=".")
)

# %% [markdown]
# Describe and plot `beer_beerId`

# %%
(
    (df_master)
    .beer_beerId  # LINE TO BE REMOVED FOR STUDENTS
    .describe()
)

# %%
(
    (df_master)
    .beer_beerId  # LINE TO BE REMOVED FOR STUDENTS
    .value_counts()
    .value_counts()
    .plot.bar()
)

# %%
(
    (df_master)
    .beer_beerId  # LINE TO BE REMOVED FOR STUDENTS
    .value_counts()
    .value_counts()
    .plot.bar(logy=True)
)

# %%
(
    (df_master)
    .beer_beerId  # LINE TO BE REMOVED FOR STUDENTS
    .value_counts()
    .value_counts()
    .plot(loglog=True, marker=".")
)

# %%
(
    (df_master)
    .beer_beerId  # LINE TO BE REMOVED FOR STUDENTS
    .value_counts()
    .plot.hist(loglog=True, bins=200)
)

# %% [markdown]
# If interested, you can read: [Zipf's Law on Wikipedia](https://en.wikipedia.org/wiki/Zipf's_law)

# %% [markdown]
# Describe and plot `beer_brewerId`

# %%
(
    (df_master)
    .beer_brewerId  # LINE TO BE REMOVED FOR STUDENTS
    .describe()
)

# %%
(
    (df_master)
    .beer_brewerId
    .value_counts()
    .value_counts()  # LINE TO BE REMOVED FOR STUDENTS
    .plot.bar()
)

# %%
(
    (df_master)
    .beer_brewerId
    .value_counts()  # LINE TO BE REMOVED FOR STUDENTS
    .value_counts()
    .plot.bar(logy=True)
)

# %%
(
    (df_master)
    .beer_brewerId  # LINE TO BE REMOVED FOR STUDENTS
    .value_counts()  # LINE TO BE REMOVED FOR STUDENTS
    .value_counts()
    .plot(loglog=True, marker=".")
)
# %% [markdown]
# If interested, you can read: [Zipf's Law on Wikipedia](https://en.wikipedia.org/wiki/Zipf's_law)

# %% [markdown]
# Describe and plot `review_profileName`

# %%
(
    (df_master)
    .review_profileName
    .describe()  # LINE TO BE REMOVED FOR STUDENTS
)

# %%
(
    (df_master)
    .review_profileName  # LINE TO BE REMOVED FOR STUDENTS
    .value_counts()  # LINE TO BE REMOVED FOR STUDENTS
    .value_counts()
    .plot.bar()
)

# %%
(
    (df_master)
    .review_profileName  # LINE TO BE REMOVED FOR STUDENTS
    .value_counts()  # LINE TO BE REMOVED FOR STUDENTS
    .value_counts()
    .plot.bar(logy=True)
)

# %%
(
    (df_master)
    .review_profileName
    .value_counts()  # LINE TO BE REMOVED FOR STUDENTS
    .value_counts()
    .plot(loglog=True, marker=".")
)

# %% [markdown]
# If interested, you can read: [Zipf's Law on Wikipedia](https://en.wikipedia.org/wiki/Zipf's_law)

# %% [markdown]
# ### Relationship with the target `positive_review`
# #### Quantitative variables

# %% [markdown]
# Plot `review_overall` relationship with `positive_review`

# %%
(
    (df_master)
    .pipe(sns.histplot, x="review_overall", bins=range(21), hue="positive_review")
)

# %% [markdown]
# Plot `review_appearance` relationship with `positive_review`

# %%
(
    (df_master)
    .pipe(sns.histplot, x="review_appearance", bins=range(21), hue="positive_review")  # LINE TO BE REMOVED FOR STUDENTS
)

# %% [markdown]
# Plot `review_aroma` relationship with `positive_review`

# %%
(
    (df_master)
    .pipe(sns.histplot, x="review_aroma", bins=range(21), hue="positive_review")  # LINE TO BE REMOVED FOR STUDENTS
)

# %% [markdown]
# Plot `review_palate` relationship with `positive_review`

# %%
(
    (df_master)  # LINE TO BE REMOVED FOR STUDENTS
    .pipe(sns.histplot, x="review_palate", bins=range(21), hue="positive_review")
)

# %% [markdown]
# Plot `review_taste` relationship with `positive_review`

# %%
(
    (df_master)
    .pipe(sns.histplot, x="review_taste", bins=range(21), hue="positive_review")  # LINE TO BE REMOVED FOR STUDENTS
)

# %% [markdown]
# #### Quantitative variables

# %% [markdown]
# Plot `beer_style` relationship with `positive_review`

# %%
(
    (df_master)  # LINE TO BE REMOVED FOR STUDENTS
    .pipe(sns.histplot, x="beer_style", bins=range(21), hue="positive_review")
)

# %% [markdown]
# #### High cardinality variables

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
# ### Multivariate plots

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
    .pipe(add_jitter)  # LINE TO BE REMOVED FOR STUDENTS
    .pipe(
        pd.plotting.scatter_matrix,
        figsize=(15, 15),
        s=10,  # LINE TO BE REMOVED FOR STUDENTS
        alpha=0.1,  # LINE TO BE REMOVED FOR STUDENTS
        c=df_master.positive_review.head(10000),  # LINE TO BE REMOVED FOR STUDENTS
    )
)

# %% [markdown]
# ### String manipulation
# Using the [`pd.Series.str`](https://pandas.pydata.org/docs/reference/api/pandas.Series.str.html) API

# %% [markdown]
# #### `review_text` column:

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
    .plot.hist(bins=range(2000))  # LINE TO BE REMOVED FOR STUDENTS
)

# %%
(
    (df_master.review_text)
    .str.len()  # LINE TO BE REMOVED FOR STUDENTS
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
    .value_counts()  # LINE TO BE REMOVED FOR STUDENTS
)

# %%
(
    df_most_used_letters
    .head(40)
    .plot.bar()  # LINE TO BE REMOVED FOR STUDENTS
)

# %%
(
    df_most_used_letters
    .head(40)  # LINE TO BE REMOVED FOR STUDENTS
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
    .str.split(" ")  # LINE TO BE REMOVED FOR STUDENTS
    .explode()
    .value_counts()
)
word_frequencies

# %%
(
    word_frequencies
    .head(100)
    .plot.bar(figsize=(12, 4))  # LINE TO BE REMOVED FOR STUDENTS
)

# %%
(
    word_frequencies
    .head(100)  # LINE TO BE REMOVED FOR STUDENTS
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
# ### Detailed text analysis
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
