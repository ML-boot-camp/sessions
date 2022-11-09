# %% [markdown]
#  # Preparation
#  ## Install & import modules

# %%
!pip install boto3
!pip install duckdb


# %%
from pathlib import Path
import pandas as pd
import duckdb
import sys
import urllib3
import boto3
from boto3.s3.transfer import TransferConfig
import threading
import os
import numpy as np
import seaborn as sns



# %% [markdown]
#  ## Utility functions & configuration

# %%
def multipart_download(key, bucket_name, s3_client):
    config = TransferConfig(
        max_concurrency=15,
        use_threads=True,
    )
    s3_client.download_file(
        bucket_name,
        key,
        key,
        Config=config, Callback=Progress(key)
    )


def format_bytes(size):
    power = 2**10
    n = 0
    power_labels = {0: '', 1: 'k', 2: 'M', 3: 'G', 4: 'T'}
    while size > power:
        size /= power
        n += 1
    return "{:.2f} {}".format(size, power_labels[n]+'B')


class Progress(object):
    def __init__(self, filename):
        self.filename = filename
        self.seen_so_far = 0
        self.lock = threading.Lock()

    def __call__(self, bytes_amount):
        with self.lock:
            self.seen_so_far += bytes_amount
            sys.stdout.write(
                "\r{} {}".format(self.filename, format_bytes(self.seen_so_far))
            )
            sys.stdout.flush()


def download_files_if_missing(files, bucket_name, s3_client, gdrive_dir=None):
    for file in files:
        if Path(file).exists():
            print(f"{file}: ✅ OK")
        elif gdrive_dir:
            print(f"{file}: ❌ missing. Linking from drive directory.")
            os.symlink(f"{gdrive_dir}/{file}", file)
        else:
            print(f"{file}: ❌ missing. Downloading from S3.")
            multipart_download(file, bucket_name, s3_client)
            print()


def sql(query):
    return con.execute(query).df()


pd.set_option("display.max_columns", 100)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

con = duckdb.connect()
con.execute("PRAGMA threads=2")
con.execute("PRAGMA enable_object_cache")

bucket_name = "yelp-dataset-parquet"
ACCESS_KEY = "AKIASOLI5AWTXR6HOPFE"
SECRET_KEY = "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"
s3_client = boto3.client(
    "s3",
    region_name='eu-west-3',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    verify=False
)


# %% [markdown]
#  ## Mount google drive

# %%
from google.colab import drive
drive.mount('/content/gdrive')
gdrive_dir = "gdrive/MyDrive/datasets - PUBLIC/"
# gdrive_dir = None


# %% [markdown]
#  # Exploratory data analysis

# %% [markdown]
#  ## Download data files

# %%
files = [
    "df_master.parquet",
]
download_files_if_missing(files, bucket_name, s3_client)


# %%
df_master = pd.read_parquet("df_master.parquet")


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
#  Count the `stars_review` occurences & plot it a in a bar diagram
# 
#  Hint:
#  - [`pd.Series.value_counts`](https://pandas.pydata.org/docs/reference/api/pandas.Series.value_counts.html)
#  - [`pd.Series.sort_index`](https://pandas.pydata.org/docs/reference/api/pandas.Series.sort_index.html)
#  - [`pd.Series.plot.bar`](https://pandas.pydata.org/docs/reference/api/pandas.Series.plot.bar.html)

# %%
(
    (df_master.stars_review)
    .value_counts()
    .sort_index()
    .plot.bar()
)


# %% [markdown]
#  Plot the `stars_review` histogram
# 
#  Hint:
#  - [`pd.Series.hist`](https://pandas.pydata.org/docs/reference/api/pandas.Series.hist.html)

# %%
(
    (df_master.stars_review)
    .hist(bins=np.arange(-0.5, 6.5, 1))
)


# %% [markdown]
#  Plot the histogram of every integer-type columns
# 
#  Hint:
#  - [`pd.Series.hist`](https://pandas.pydata.org/docs/reference/api/pandas.Series.hist.html)

# %%
df_master_integers = df_master.select_dtypes(include=["int64"])
(
    (df_master_integers).plot.hist(
        bins=range(1000),
        loglog=True,
        subplots=True,
        figsize=(6, df_master_integers.shape[1] * 4),
    )
)


# %% [markdown]
#  If interested, you can read: [Zipf's Law on Wikipedia](https://en.wikipedia.org/wiki/Zipf's_law)

# %% [markdown]
#  ## String manipulation
#  Using the [`pd.Series.str`](https://pandas.pydata.org/docs/reference/api/pandas.Series.str.html) API

# %% [markdown]
#  ### `text` column:

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
    (df_master.text)
    .str.len()
    .plot.hist(bins=range(5000), logy=True)
)


# %% [markdown]
#  Compute the frequency of the most used letters in the texts
#  (use only the first 100000 texts).
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
(
    (df_master.text)
    .head(100000)
    .str.lower()
    .str.split("")
    .explode()
    .loc[lambda x: x != " "]
    .value_counts()
    .head(40)
    .plot.bar(logy=True)
)


# %% [markdown]
#  Compute the frequency of the most used words in the texts
#  (use only the first 100000 texts).
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
    (df_master.text)
    .head(50000)
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
(
    (df_master)
    .select_dtypes(["int64", "float64"])
    .head(10000)
    .pipe(
        pd.plotting.scatter_matrix,
        figsize=(15, 15),
        s=10,
        alpha=0.5,
        c=df_master.positive_review.head(10000),
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



