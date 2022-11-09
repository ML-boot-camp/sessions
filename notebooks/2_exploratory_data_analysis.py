# %% [markdown]
#  # Preparation
#  ## Install & import modules

# %%
! pip install seaborn

# %%
from pathlib import Path
import pandas as pd
import numpy as np
import seaborn as sns

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
)

# %% [markdown]
#  # `df_master` DataFrame

# %% [markdown]
#  ## General information
#  Have a first overview of the dataframe size, i.e. number of rows & columns.
# 
#  Methods you'll need:
#  - [`pd.DataFrame.shape`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.shape.html)

# %%
df_master.shape

# %% [markdown]
#  Get a few information about the content of the dataframe:
#  - number of null values per column
#  - data type of each column
#  - memory usage
# 
#  Methods you'll need:
#  - [`pd.DataFrame.isnull`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.isnull.html)
#  - [`pd.DataFrame.sum`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.sum.html)
#  - [`pd.DataFrame.dtypes`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.dtypes.html)
#  - [`pd.DataFrame.info`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.info.html)

# %%
df_master.isnull().sum()

# %%
df_master.dtypes

# %%
df_master.info(memory_usage="deep")

# %% [markdown]
#  Show a sample of the data
# 
#  Methods you'll need:
#  - [`pd.DataFrame.head`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.head.html)
#  - [`pd.DataFrame.sample`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.sample.html)
# 
#  Bonus: display the transpose of the dataframe for better readability when having lots of columns using:
#  - [`pd.DataFrame.T`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.T.html)

# %%
df_master.head(5)

# %%
df_master.sample(5).T

# %% [markdown]
#  Compute statistics to understand the content of each column.
# 
#  Methods you'll need:
#  - [`pd.DataFrame.describe`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.describe.html)
# 
#  Bonus: fill NaN values with an empty string `""` for a better readability using:
#  - [`pd.DataFrame.fillna`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.fillna.html)

# %%
df_master.describe(include="all").fillna("").T

# %% [markdown]
#  ## Numbers manipulation

# %% [markdown]
#  Count the `review_overall` occurences & plot it a in a bar diagram
# 
#  Hint:
#  - [`pd.Series.value_counts`](https://pandas.pydata.org/docs/reference/api/pandas.Series.value_counts.html)
#  - [`pd.Series.sort_index`](https://pandas.pydata.org/docs/reference/api/pandas.Series.sort_index.html)
#  - [`pd.Series.plot.bar`](https://pandas.pydata.org/docs/reference/api/pandas.Series.plot.bar.html)

# %%
(
    (df_master.review_overall)
    .value_counts()
    .sort_index()
    .plot.bar()
)

# %% [markdown]
#  Plot the `review_overall` histogram
# 
#  Hint:
#  - [`pd.Series.hist`](https://pandas.pydata.org/docs/reference/api/pandas.Series.hist.html)

# %%
(
    (df_master.review_overall)
    .hist(bins=np.arange(-0.5, 20.5, 1))
)

# %% [markdown]
#  Plot the histogram of all `review_*` columns
# 
#  Hint:
#  - [`pd.Series.hist`](https://pandas.pydata.org/docs/reference/api/pandas.Series.hist.html)

# %%
df_master_reviews = df_master.filter(regex="review_")
(
    (df_master_reviews)
    .plot.hist(
        bins=range(21),
        subplots=True,
        figsize=(6, df_master_reviews.shape[1] * 3),
    )
)

# %% [markdown]
#  Plot the histogram of the `number_of_reviews` columns
# 
#  Hint:
#  - [`pd.Series.hist`](https://pandas.pydata.org/docs/reference/api/pandas.Series.hist.html)

# %%
(
    (df_master)
    .number_of_reviews
    .plot.hist(bins=100)
)

# %%
(
    (df_master)
    .number_of_reviews
    .plot.hist(bins=100, loglog=True)
)

# %% [markdown]
#  If interested, you can read: [Zipf's Law on Wikipedia](https://en.wikipedia.org/wiki/Zipf's_law)

# %% [markdown]
#  ## String manipulation
#  Using the [`pd.Series.str`](https://pandas.pydata.org/docs/reference/api/pandas.Series.str.html) API

# %% [markdown]
#  ### `review_text` column:

# %% [markdown]
#  Compute the length of the texts in the dataset.
# 
#  Methods you'll need:
#  - [`pd.Series.str.len`](https://pandas.pydata.org/docs/reference/api/pandas.Series.str.len.html)
#  - [`pd.Series.str`](https://pandas.pydata.org/docs/reference/api/pandas.Series.str..html)
# 
#  Bonus: plot an histogram of the values, with log values, using:
#  - [`pd.Series.plot.hist`](https://pandas.pydata.org/docs/reference/api/pandas.Series.plot.bar.html)
# 
#  Is it a Power law distribution ?

# %%
(
    (df_master.review_text)
    .str.len()
    .plot.hist(bins=range(2000))
)

# %%
(
    (df_master.review_text)
    .str.len()
    .plot.hist(bins=range(2000), logy=True)
)

# %% [markdown]
#  Compute the frequency of the most used letters in the texts
# 
#  Methods you'll need:
#  - [`pd.Series.str.lower`](https://pandas.pydata.org/docs/reference/api/pandas.Series.str.lower.html)
#  - [`pd.Series.str.split`](https://pandas.pydata.org/docs/reference/api/pandas.Series.str.split.html)
#  - [`pd.Series.explode`](https://pandas.pydata.org/docs/reference/api/pandas.Series.explode.html)
#  - [`pd.Series.value_counts`](https://pandas.pydata.org/docs/reference/api/pandas.Series.value_counts.html)
#  - [`pd.Series.head`](https://pandas.pydata.org/docs/reference/api/pandas.Series.head.html)
# 
#  Bonus: plot an histogram of the values, with log values, using:
#  - [`pd.Series.plot.hist`](https://pandas.pydata.org/docs/reference/api/pandas.Series.plot.bar.html)
# 
#  Is it a Power law distribution ?

# %%
df_most_used_letters = (
    (df_master.review_text)
    .str.lower()
    .str.split("")
    .explode()
    .loc[lambda x: x != " "]
    .value_counts()
)

# %%
(
    df_most_used_letters
    .head(40)
    .plot.bar()
)

# %%
(
    df_most_used_letters
    .head(40)
    .plot.bar(logy=True)
)

# %% [markdown]
#  Compute the frequency of the most used words in the texts
# 
#  Methods you'll need:
#  - [`pd.Series.str.len`](https://pandas.pydata.org/docs/reference/api/pandas.Series.str.len.html)
#  - [`pd.Series.str.split`](https://pandas.pydata.org/docs/reference/api/pandas.Series.str.split.html)
#  - [`pd.Series.explode`](https://pandas.pydata.org/docs/reference/api/pandas.Series.explode.html)
#  - [`pd.Series.value_counts`](https://pandas.pydata.org/docs/reference/api/pandas.Series.value_counts.html)
#  - [`pd.Series.head`](https://pandas.pydata.org/docs/reference/api/pandas.Series.head.html)
# 
#  Bonus: plot an histogram of the values, with log values, using:
#  - [`pd.Series.plot.hist`](https://pandas.pydata.org/docs/reference/api/pandas.Series.plot.bar.html)
# 
#  Is it a Power law distribution ?

# %%
word_frequencies = (
    (df_master.review_text)
    # .head(50000)
    .str.lower()
    .str.replace(r"[^a-z\ ]", "")
    .str.replace(r"\ +", " ")
    .str.split(" ")
    .explode()
    .value_counts()
)
word_frequencies

# %%
(
    word_frequencies
    .head(100)
    .plot.bar(figsize=(12, 4))
)

# %%
(
    word_frequencies
    .head(100)
    .plot.bar(logy=True, figsize=(12, 4))
)

# %%
(
    word_frequencies
    .head(1000)
    .reset_index(drop=True)
    .plot(loglog=True)
)

# %% [markdown]
#  ## Multivariate plots

# %% [markdown]
#  Plot a scatter matrix of the numerical variables, colored by the target column
#  `positive_review`.
# 
#  Hint:
#  - [`pd.DataFrame.select_dtypes`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.select_dtypes.html)
#  - [`pd.plotting.scatter_matrix`](https://pandas.pydata.org/docs/reference/api/pandas.plotting.scatter_matrix.html)

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
    .pipe(add_jitter)
    .pipe(
        pd.plotting.scatter_matrix,
        figsize=(15, 15),
        s=10,
        alpha=0.1,
        # c=df_master.positive_review.head(10000),
    )
)

# %% [markdown]
#  Plot a scatter matrix of those columns: `stars_review`, `useful`, `funny`,
#  `cool`, `fans`. Colored by the target column `positive_review`.
# 
#  Hint:
#  - [`pd.plotting.scatter_matrix`](https://pandas.pydata.org/docs/reference/api/pandas.plotting.scatter_matrix.html)

# %%
columns_to_plot = ["stars_review", "useful", "funny", "cool", "fans"]
(
    (df_master)
    .loc[:, columns_to_plot]
    .head(20000)
    .pipe(
        pd.plotting.scatter_matrix,
        figsize=(15, 15),
        s=20,
        alpha=0.5,
        c=df_master.positive_review.head(20000),
    )
)

# %% [markdown]
#  Plot a scatter matrix of those columns: `stars_review`, `useful`, `funny`,
#  `cool`, `fans`. Colored by the target column `positive_review`.
# 
#  Hint:
#  - [`pd.DataFrame.loc`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.loc.html)
#  - [`sns.pairplot`](https://seaborn.pydata.org/generated/seaborn.pairplot.html)

# %%
df_pairplot = (
    (df_master)
    .loc[:, columns_to_plot]
    .head(2000)
    .pipe(lambda df: np.log10(df + 1 + 0.75 * (np.random.rand(*df.shape) - 0.5)))
    .assign(stars_review_no_jitter=df_master.stars_review.head(2000))
)

g = sns.pairplot(
    df_pairplot,
    diag_kind="kde",
    plot_kws=dict(
        size=1,
        alpha=0.1
    ),
    hue="stars_review_no_jitter",
    palette="RdYlGn",
)
g.map_lower(sns.kdeplot, levels=4, color=".2")


# %% [markdown]
#  Plot a scatter matrix of those columns: `stars_review`, `useful`, `funny`,
#  `cool`, `fans`. Colored by the target column `positive_review`.
# 
#  Hint:
#  - [`pd.DataFrame.loc`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.loc.html)
#  - [`sns.pairplot`](https://seaborn.pydata.org/generated/seaborn.pairplot.html)

# %%
df_pairplot = (
    (df_master)
    .loc[:, columns_to_plot]
    .head(2000)
    .pipe(lambda df: np.log10(df + 1 + 0.75 * (np.random.rand(*df.shape) - 0.5)))
    .assign(positive_review=df_master.positive_review.head(2000))
)

g = sns.pairplot(
    df_pairplot,
    diag_kind="kde",
    plot_kws=dict(
        size=1,
        alpha=0.1
    ),
    hue="positive_review",
    palette="RdYlGn",
)
g.map_lower(sns.kdeplot, levels=4, color=".2")


# %% [markdown]
#  Managing overplotting in scatter plots: use jitter, size, alpha

# %%
(
    (df_master)
    .filter(regex="stars")
    .pipe(lambda df: df + 0.45 * (np.random.rand(*df.shape) - 0.5))
    .plot.scatter(
        x="stars_restaurant", y="stars_review", figsize=(6, 6), s=1, alpha=0.01
    )
)


# %%
(
    (df_master)
    .filter(regex="stars")
    .pipe(lambda df: df + 0.45 * (np.random.rand(*df.shape) - 0.5))
    .plot.hexbin(x="stars_restaurant", y="stars_review")
)


# %% [markdown]
#  Managing overplotting in scatter plots: try a heatmap or line plot

# %%
(
    (df_master)
    .assign(dummy=1)
    .pivot_table(
        index="stars_restaurant",
        columns="stars_review",
        values="dummy",
        aggfunc="count",
    )
    .apply(lambda row: row / row.sum(), axis=1)
    .T.sort_index(ascending=False)
    .plot()
    # .pipe(sns.heatmap)
)


# %% [markdown]
#  ## Detailed text analysis
#  Word associated to positive & negative reviews

# %%
(
    df_master
    .head(100000)
    .assign(
        tokenized_text=lambda df: (df.text)
        .str.lower()
        .str.replace(r"[^a-z]", " ")
        .str.replace(r" +", " ")
        .str.split(" ")
    )
    .loc[:, ["stars_review", "tokenized_text"]]
    .explode("tokenized_text")
    .groupby("tokenized_text", as_index=False)
    .agg(["mean", "count"])
    .reset_index()
    .sort_values(by=("stars_review", "count"), ascending=False)
    .head(200)
    .style.background_gradient(cmap="RdYlGn")
)


# %% [markdown]
#  ## Date manipulation
#  Using the [`pd.Series.dt`](https://pandas.pydata.org/docs/reference/api/pandas.Series.dt.html) API

# %% [markdown]
#  ### `date` column

# %% [markdown]
#  Count the occurences of each year in `date` & plot a bar diagram, using the
#  `str` (string) pandas API.
# 
#  Hint:
#  - [`pd.Series.str.slice`](https://pandas.pydata.org/docs/reference/api/pandas.Series.str.slice.html)
#  - [`pd.Series.value_counts`](https://pandas.pydata.org/docs/reference/api/pandas.Series.value_counts.html)
#  - [`pd.Series.sort_index`](https://pandas.pydata.org/docs/reference/api/pandas.Series.sort_index.html)
#  - [`pd.Series.plot.bar`](https://pandas.pydata.org/docs/reference/api/pandas.Series.plot.bar.html)

# %%
(
    (df_master.date)
    .str[0:4]
    .value_counts()
    .sort_index()
    .plot.bar()
)


# %% [markdown]
#  Count the occurences of each year in `date` & plot a bar diagram, using the
#  `dt` (datetime) pandas API.
# 
#  To use the datetime API, you need to convert the column to a datetime dtype.
# 
#  Hint:
#  - [`pd.Series.astype`](https://pandas.pydata.org/docs/reference/api/pandas.Series.astype.html)
#  - [`pd.Series.dt.year`](https://pandas.pydata.org/docs/reference/api/pandas.Series.dt.year.html)
#  - [`pd.Series.value_counts`](https://pandas.pydata.org/docs/reference/api/pandas.Series.value_counts.html)
#  - [`pd.Series.sort_index`](https://pandas.pydata.org/docs/reference/api/pandas.Series.sort_index.html)
#  - [`pd.Series.plot.bar`](https://pandas.pydata.org/docs/reference/api/pandas.Series.plot.bar.html)

# %%
(
    (df_master.date)
    .astype("datetime64[ns]")
    .dt.year
    .value_counts()
    .sort_index()
    .plot.bar()
)


# %% [markdown]
#  Count the occurences of each month in `date` & plot a bar diagram, using the
#  `dt` (datetime) pandas API.
# 
#  Hint:
#  - [`pd.Series.astype`](https://pandas.pydata.org/docs/reference/api/pandas.Series.astype.html)
#  - [`pd.Series.dt.month`](https://pandas.pydata.org/docs/reference/api/pandas.Series.dt.month.html)
#  - [`pd.Series.value_counts`](https://pandas.pydata.org/docs/reference/api/pandas.Series.value_counts.html)
#  - [`pd.Series.sort_index`](https://pandas.pydata.org/docs/reference/api/pandas.Series.sort_index.html)
#  - [`pd.Series.plot.bar`](https://pandas.pydata.org/docs/reference/api/pandas.Series.plot.bar.html)

# %%
(
    (df_master.date)
    .astype("datetime64[ns]")
    .dt.month
    .value_counts()
    .sort_index()
    .plot.bar()
)


# %% [markdown]
#  Count the occurences of each day of the week in `date` & plot a bar diagram,
#  using the `dt` (datetime) pandas API.
# 
#  Hint:
#  - [`pd.Series.astype`](https://pandas.pydata.org/docs/reference/api/pandas.Series.astype.html)
#  - [`pd.Series.dt.dayofweek`](https://pandas.pydata.org/docs/reference/api/pandas.Series.dt.dayofweek.html)
#  - [`pd.Series.value_counts`](https://pandas.pydata.org/docs/reference/api/pandas.Series.value_counts.html)
#  - [`pd.Series.sort_index`](https://pandas.pydata.org/docs/reference/api/pandas.Series.sort_index.html)
#  - [`pd.Series.plot.bar`](https://pandas.pydata.org/docs/reference/api/pandas.Series.plot.bar.html)

# %%
(
    (df_master.date)
    .astype("datetime64[ns]")
    .dt.dayofweek
    .value_counts()
    .sort_index()
    .plot.bar()
)


# %% [markdown]
#  Count the occurences of each hour in `date` & plot a bar diagram, using the
#  `dt` (datetime) pandas API.
# 
#  Maybe it's needed to convert from UTC to local time.
# 
#  Hint:
#  - [`pd.Series.astype`](https://pandas.pydata.org/docs/reference/api/pandas.Series.astype.html)
#  - [`pd.Series.dt.hour`](https://pandas.pydata.org/docs/reference/api/pandas.Series.dt.hour.html)
#  - [`pd.Series.value_counts`](https://pandas.pydata.org/docs/reference/api/pandas.Series.value_counts.html)
#  - [`pd.Series.sort_index`](https://pandas.pydata.org/docs/reference/api/pandas.Series.sort_index.html)
#  - [`pd.Series.plot.bar`](https://pandas.pydata.org/docs/reference/api/pandas.Series.plot.bar.html)

# %%
(
    (df_master.date)
    .astype("datetime64[ns]")
    .dt.hour
    .pipe(lambda s: (s - 6) % 24)
    .value_counts()
    .sort_index()
    .plot.bar()
)


# %% [markdown]
#  Count the percentage of each rating as a function of the year in `date` & plot
#  a line diagram. E.g: in 2020, 55% of ratings were 5, 15% or ratings were 4, ...
# 
#  Hint:
#  - [`pd.Series.astype`](https://pandas.pydata.org/docs/reference/api/pandas.Series.astype.html)
#  - [`pd.Series.dt.year`](https://pandas.pydata.org/docs/reference/api/pandas.Series.dt.year.html)
#  - [`pd.DataFrame.pivot_table`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.pivot_table.html)
#  - [`pd.DataFrame.apply`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.apply.html)

# %%
(
    df_master
    .assign(
        year=lambda df: df.date
        .astype("datetime64[ns]")
        .dt.year
    )
    .assign(dummy=1)
    .pivot_table(index="year", columns="stars_review", values="dummy", aggfunc="count")
    .apply(lambda row: row / row.sum(), axis=1)
    .plot(figsize=(10, 6))
)


