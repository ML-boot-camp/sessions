# %% [markdown]
# # 🐍 Practice n°2: exploratory data analysis
# ## Preparation
# ### Install & import modules

# %%
# ! pip install seaborn

# %%
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

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
    (df_ratebeer)
    .groupby("review_profileName")
    .agg(
        number_of_reviews=("review_profileName", "count"),
        average_rating=("review_overall", "mean"),
    )
    .round(1)
    .reset_index()
)

# %%
df_master = (
    (df_ratebeer)
    .merge(
        df_reviewers, on="review_profileName", how="inner", validate="m:1"
    )
    .assign(
        review_time=lambda df: df.review_time.astype(int).apply(
            pd.Timestamp.fromtimestamp
        )
    )
    .assign(
        positive_review=lambda df: (
            df.review_overall >= df.review_overall.median()
        ).astype(int)
    )
)

# %% [markdown]
# ## General information
# ### Shape
# Have a first overview of the dataframe size, i.e. number of rows & columns.
#
# Methods you'll need:
# - [`pd.DataFrame.shape`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.shape.html)

# %%
df_master.shape

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
df_master.isnull().sum()

# %%
df_master.dtypes

# %%
df_master.info(memory_usage="deep")  # LINE TO BE REMOVED FOR STUDENTS

# %% [markdown]
# ### Sample
# Show a sample of the data
#
# Methods you'll need:
# - [`pd.DataFrame.head`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.head.html)
# - [`pd.DataFrame.sample`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.sample.html)
#
# Bonus: display the transpose of the dataframe for better readability when having lots
# of columns using:
# - [`pd.DataFrame.T`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.T.html)

# %%
df_master.head(5)

# %%
df_master.sample(5).T

# %% [markdown]
# ### Describing statistics
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
# ## Quantitative variables
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
# ### Describe quantitative variables
# 
# Methods you'll need:
# - [`pd.DataFrame.describe`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.describe.html)
# - [`pd.Series.hist`](https://pandas.pydata.org/docs/reference/api/pandas.Series.hist.html)
# - [`pd.DataFrame.fillna`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.fillna.html)

# %%
pd.set_option("display.precision", 2)
sns.set_style("whitegrid")
sns.set_context(rc = {'patch.linewidth': 0.15})

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
    .T.style.background_gradient()  # LINE TO BE REMOVED FOR STUDENTS
    .format(precision=2)  # LINE TO BE REMOVED FOR STUDENTS
)

# %% [markdown]
# ### Plot rating columns: review_* & average_rating

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
# ### Plot `beer_ABV`

# %%
(
    (df_master)
    .beer_ABV
    .plot.hist(bins=100)  # LINE TO BE REMOVED FOR STUDENTS
)

# %% [markdown]
# ### Plot `review_time`

# %%
(
    (df_master)
    .review_time
    .hist(bins=100)  # LINE TO BE REMOVED FOR STUDENTS
)

# %% [markdown]
# ## Nominal and ordinal variables
# - `positive_review`
# - `beer_style`
# - `beer_name`
# - `beer_beerId`
# - `beer_brewerId`
# - `review_profileName`

# %% [markdown]
# ### Describe and plot `positive_review`

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
    .value_counts()
    .plot.bar()  # LINE TO BE REMOVED FOR STUDENTS
)

# %%
sns.countplot(
    df_master,
    x="positive_review",   # LINE TO BE REMOVED FOR STUDENTS
)

# %% [markdown]
# ### Describe and plot `beer_style`

# %%
(
    (df_master)
    .beer_style
    .describe()  # LINE TO BE REMOVED FOR STUDENTS
)

# %%
(
    (df_master)
    .beer_style
    .value_counts()
    .plot.bar()  # LINE TO BE REMOVED FOR STUDENTS
)

# %% [markdown]
# ### Describe and plot `beer_name`

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
    .plot(marker=".")  # LINE TO BE REMOVED FOR STUDENTS
)

# %% [markdown]
# The distribution is highly skewed. But is there an underlying structure ?

# %%
(
    (df_master)
    .beer_name
    .value_counts()
    .value_counts()
    .plot(loglog=True, marker=".")
)

# %% [markdown]
# Haha ! ☝️🙂 This linear relationship is interesting. See at the end of the notebook for
# more info.

# %% [markdown]
# ### Describe and plot `beer_beerId`

# %%
(
    (df_master)
    .beer_beerId
    .describe()  # LINE TO BE REMOVED FOR STUDENTS
)

# %%
(
    (df_master)
    .beer_beerId
    .value_counts()
    .plot(marker=".")  # LINE TO BE REMOVED FOR STUDENTS
)

# %%
(
    (df_master)
    .beer_beerId
    .value_counts()
    .value_counts()
    .plot(loglog=True, marker=".")
)

# %% [markdown]
# `beer_beerId` seems to have the same underlying structure as `beer_name`.
# See at the end of the notebook for more info.

# %% [markdown]
# ### Describe and plot `beer_brewerId`

# %%
(
    (df_master)
    .beer_brewerId
    .describe()  # LINE TO BE REMOVED FOR STUDENTS
)

# %%
(
    (df_master)
    .beer_brewerId
    .value_counts()
    .plot(marker=".")  # LINE TO BE REMOVED FOR STUDENTS
)


# %%
(
    (df_master)
    .beer_brewerId
    .value_counts()
    .value_counts()
    .plot(loglog=True, marker=".")
)

# %% [markdown]
# Same for this one: see at the end of the notebook for more info.

# %% [markdown]
# ### Describe and plot `review_profileName`

# %%
(
    (df_master)
    .review_profileName
    .describe()  # LINE TO BE REMOVED FOR STUDENTS
)

# %%
(
    (df_master)
    .review_profileName
    .value_counts()
    .plot(marker=".")  # LINE TO BE REMOVED FOR STUDENTS
)

# %%
(
    (df_master)
    .review_profileName
    .value_counts()
    .value_counts()
    .plot(loglog=True, marker=".")
)

# %% [markdown]
# ## Relationship with the target `positive_review`

# %% [markdown]
# ### Plot `review_overall` relationship with `positive_review`

# %%
sns.histplot(
    df_master,
    x="review_overall",
    discrete=True,
    hue="positive_review"
)

# %% [markdown]
# ### Plot `review_appearance` relationship with `positive_review`

# %%
sns.histplot(
    df_master,
    x="review_appearance",
    discrete=True,
    hue="positive_review",
)

# %%
sns.histplot(
    df_master,
    x="review_appearance",
    discrete=True,
    hue="positive_review",
    multiple="fill"
)

# %% [markdown]
# ### Plot `review_aroma` relationship with `positive_review`

# %%
sns.histplot(
    df_master,
    x="review_aroma",
    discrete=True,
    hue="positive_review",
)

# %%
sns.histplot(
    df_master,
    x="review_aroma",
    discrete=True,
    hue="positive_review",
    multiple="fill"
)

# %% [markdown]
# ### Plot `review_palate` relationship with `positive_review`

# %%
sns.histplot(
    df_master,
    x="review_palate",
    discrete=True,
    hue="positive_review",
)

# %%
sns.histplot(
    df_master,
    x="review_palate",
    discrete=True,
    hue="positive_review",
    multiple="fill",
)

# %% [markdown]
# ### Plot `review_taste` relationship with `positive_review`

# %%
sns.histplot(
    df_master,
    x="review_taste",
    discrete=True,
    hue="positive_review",
)

# %%
sns.histplot(
    df_master,
    x="review_taste",
    discrete=True,
    hue="positive_review",
    multiple="fill",
)

# %% [markdown]
# ### Plot `beer_style` relationship with `positive_review`

# %%
sns.histplot(
    df_master,
    x="beer_style",
    discrete=True,
    hue="positive_review",
)

# %%
df_beer_styles = (
    df_master
    .groupby("beer_style")
    .positive_review
    .agg(["count", "mean"])
    .add_prefix("review_")
    .reset_index()
    .sort_values(by="review_mean", ascending=False)
    .reset_index(drop=True)
    .assign(bar_left_position=lambda df:
        df.review_count.cumsum().shift(1, fill_value=0))
)
df_beer_styles

# %%
plt.bar(
    x=df_beer_styles.bar_left_position,
    height=df_beer_styles.review_mean,
    width=df_beer_styles.review_count,
    align="edge",
    alpha=0.5,
    edgecolor="k",
    linewidth=0.5
)

# %% [markdown]
# ## High cardinality variables
# ### `beer_beerIds`

# %%
df_beer_beerIds = (
    df_master
    .merge(
        df_master
        .beer_beerId
        .value_counts()
        .rename("beer_beerId_review_count")
        .reset_index(),
        on="beer_beerId"
    )
    .loc[:, ["beer_beerId", "beer_beerId_review_count", "positive_review"]]
)
df_beer_beerIds

# %%
sns.histplot(df_beer_beerIds, x="beer_beerId_review_count", hue="positive_review")

# %%
sns.histplot(df_beer_beerIds, x="beer_beerId_review_count", hue="positive_review", log_scale=True)

# %%
sns.histplot(df_beer_beerIds, x="beer_beerId_review_count", hue="positive_review", log_scale=True, multiple="fill")

# %% [markdown]
# ### `beer_brewerIds`

# %%
df_beer_brewerIds = (
    df_master
    .merge(
        df_master
        .beer_brewerId
        .value_counts()
        .rename("beer_brewerId_review_count")
        .reset_index(),
        on="beer_brewerId"
    )
    .loc[:, ["beer_brewerId", "beer_brewerId_review_count", "positive_review"]]
)
df_beer_brewerIds

# %%
sns.histplot(df_beer_brewerIds, x="beer_brewerId_review_count", hue="positive_review")

# %%
sns.histplot(df_beer_brewerIds, x="beer_brewerId_review_count", hue="positive_review", log_scale=True, bins=50)

# %%
sns.histplot(df_beer_brewerIds, x="beer_brewerId_review_count", hue="positive_review", log_scale=True, bins=50, multiple="fill")

# %% [markdown]
# ### `review_profileName`

# %%
df_review_profileNames = (
    df_master
    .merge(
        df_master
        .review_profileName
        .value_counts()
        .rename("review_profileName_review_count")
        .reset_index(),
        on="review_profileName"
    )
    .loc[:, ["review_profileName", "review_profileName_review_count", "positive_review"]]
)
df_review_profileNames

# %%
sns.histplot(df_review_profileNames, x="review_profileName_review_count", hue="positive_review")

# %%
sns.histplot(df_review_profileNames, x="review_profileName_review_count", hue="positive_review", log_scale=True, bins=50)

# %%
sns.histplot(df_review_profileNames, x="review_profileName_review_count", hue="positive_review", log_scale=True, bins=50, multiple="fill")

# %% [markdown]
# ## Review text
# Using the [`pd.Series.str`](https://pandas.pydata.org/docs/reference/api/pandas.Series.str.html) API

# %% [markdown]
# ### Text length

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
    .plot.hist(bins=200)  # LINE TO BE REMOVED FOR STUDENTS
)

# %%
(
    (df_master.review_text)
    .str.len()  # LINE TO BE REMOVED FOR STUDENTS
    .plot.hist(bins=200, logy=True)
)

# %% [markdown]
# ### Word frequencies
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
df_word_frequencies = (
    (df_master.review_text)
    .str.lower()
    .str.replace(r"[^a-z\ ]", "")
    .str.replace(r"\ +", " ")
    .str.split(" ")  # LINE TO BE REMOVED FOR STUDENTS
    .explode()
    .loc[lambda x: x != ""]
    .value_counts(normalize=True)
    .rename("word_frequency")
    .rename_axis(index="word")
    .reset_index()
    .assign(rank=lambda df: range(1, 1 + df.shape[0]))
)
df_word_frequencies

# %%
(
    df_word_frequencies
    .head(10000)
    .plot(x="rank", y="word_frequency", marker=".")
)

# %%
(
    df_word_frequencies
    .head(10000)
    .plot(x="rank", y="word_frequency", loglog=True, marker=".")
)

# %% [markdown]
# ### Words associated to positive & negative reviews

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
    .loc[lambda df: df.tokenized_text != ""]
    .groupby("tokenized_text", as_index=False)
    .agg(["mean", "count"])
    .reset_index()
    .sort_values(by=("review_overall", "count"), ascending=False)
    .head(200)
    .style.background_gradient(cmap="RdYlGn")
)

# %% [markdown]
# ### Date
# Count the percentage of each rating as a function of the `date` & plot
# a line diagram. E.g: in 2020, 55% of ratings were 5, 15% or ratings were 4, ...
#
# Hint:
# - [`sns.displot`]()

# %%
sns.displot(
    df_master,
    x="review_time",
    hue="positive_review",
)

# %%
sns.displot(
    df_master,
    x="review_time",
    hue="positive_review",
    multiple="fill",
)

# %%
sns.displot(
    df_master,
    x="review_time",
    hue="review_overall",
    multiple="fill",
    kind="kde",
    palette="RdYlGn",
)

# %% [markdown]
# ## Advanced analytics
# 
# %% [markdown]
# ### Analysis of `number_of_reviews`:
#
# As this column has been joined from another table, it has lots of duplicates. To
# retrieve the original data, we must deduplicate the records.
#
# For the sake of clarity, we can rename:
# - `review_profileName` as `user`
# - `number_of_reviews` as `user_degree`. We refer here to the concept of *degree* in a
# social network, i.e. for a node, its degree is its number of connections.
#
# In other words, users are connecting to beers and breweries thanks to their reviews,
# which forms a network.

# %%
df_users_degree = (
    (df_master)
    .loc[:, ["review_profileName", "number_of_reviews"]]
    .drop_duplicates()
    .sort_values(by="number_of_reviews", ascending=False)
    .reset_index(drop=True)
    .rename(columns={"review_profileName": "user", "number_of_reviews": "user_degree"})
)
df_users_degree

# %% [markdown]
# Many networks are [scale free networks](https://en.wikipedia.org/wiki/Scale-free_network):
# ![](https://www.researchgate.net/profile/Leonardo-Riella/publication/234031137/figure/fig1/AS:282612053626890@1444391372899/Structure-of-networks-A-biological-network-is-not-randomly-wired-similar-number-of.png)
#
# Meaning that the node's degree distribution follows a [power law
# distribution](https://en.wikipedia.org/wiki/Power_law):
# ![](https://upload.wikimedia.org/wikipedia/commons/3/3b/Degree_distribution_for_a_network_with_150000_vertices_and_mean_degree_%3D_6_created_using_the_Barabasi-Albert_model..png)
#
# To compute the distribution you'll need:
# - [`pd.Series.value_counts`](https://pandas.pydata.org/docs/reference/api/pandas.Series.value_counts.html)
#

# %%
df_users_degree_distribution = (
    df_users_degree.user_degree.value_counts(normalize=True)
    .rename("user_degree_frequency")
    .reset_index()
)
df_users_degree_distribution

# %%
df_users_degree_distribution.plot(
    kind="scatter",
    x="user_degree",
    y="user_degree_frequency",
)

# %%
df_users_degree_distribution.plot(
    kind="scatter",
    x="user_degree",
    y="user_degree_frequency",
    loglog=True,
)

# %% [markdown]
# Another way to visualize the power law distribution is to visualize the [rank-frequency plot](https://en.wikipedia.org/wiki/Rank%E2%80%93size_distribution).
# 
# Instead of plotting the frequency as a function of the value (like in a normal
# distribution plot), we plot the frequency as a function of its rank. Note: It's always
# monotonically decreasing.
# 
# Power law distributions exhibit also a distinctive visual pattern in the
# rank-frequency plot, known as the [Zipf's law]():
# ![](https://upload.wikimedia.org/wikipedia/commons/d/d9/Zipf-engl-0_English_-_Culpeper_herbal_and_War_of_the_Worlds.svg)
# 
# Let's compute the 

# %%
df_users_degree_rank_frequency = df_users_degree_distribution.assign(
    rank=lambda df: range(1, 1 + df.shape[0])
)
df_users_degree_rank_frequency

# %%
df_users_degree_rank_frequency.plot(
    loglog=True, x="rank", y="user_degree_frequency", marker="."
)

# %%
