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

# %%
pd.set_option("display.precision", 2)
sns.set_style("whitegrid")
sns.set_context(rc={"patch.linewidth": 0.15})

# %% [markdown]
# ### Read remote dataset
#
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
    .merge(df_reviewers, on="review_profileName", how="inner", validate="m:1")
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
#
# Bonus: fill NaN values with an empty string `""` for a better readability using:
# - [`pd.DataFrame.fillna`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.fillna.html)

# %%
df_master.describe(include="all").fillna("").T

# %% [markdown]
# ## Target
#
# The dataset contains 2 possible targets:
# - review_overall: an ordinal variable, which can be used to define a regression
# - positive_review: a binary variable, which can be used to define a classification
#
# In the follow-up of the exploratory data analysis, for the sake of clariy, we'll
# consider only the binary target (classification). Some plots would be different for
# numeric target.

# %% [markdown]
# ### `positive_review`

# %%
(
    (df_master.positive_review)
    .value_counts()
    .plot.bar()  # LINE TO BE REMOVED FOR STUDENTS
)

# %%
sns.countplot(
    df_master,
    x="positive_review",  # LINE TO BE REMOVED FOR STUDENTS
)

# %% [markdown]
# ## Quantitative variables
#
# - `beer_ABV`
# - `review_time`
# - `review_appearance`
# - `review_aroma`
# - `review_palate`
# - `review_taste`
# - `average_rating`

# %% [markdown]
# ### `beer_ABV`
# #### Distribution

# %%
((df_master.beer_ABV).plot.hist(bins=100))  # LINE TO BE REMOVED FOR STUDENTS

# %%
sns.displot(
    df_master,
    x="beer_ABV",
)

# %%
sns.displot(df_master, x="beer_ABV", hue="positive_review")

# %%
sns.displot(
    df_master.loc[lambda df: df.beer_ABV < 20], x="beer_ABV", hue="positive_review"
)

# %%
sns.displot(
    df_master.loc[lambda df: df.beer_ABV < 20],
    x="beer_ABV",
    hue="positive_review",
    kde=True,
)

# %%
sns.displot(
    df_master.loc[lambda df: df.beer_ABV < 20],
    x="beer_ABV",
    hue="positive_review",
    multiple="fill",
)

# %% [markdown]
# ### `review_time`

# %% [markdown]
# #### Distribution

# %%
sns.displot(
    df_master,
    x="review_time",  # LINE TO BE REMOVED FOR STUDENTS
)

# %% [markdown]
# #### Relationship with the target

# %%
sns.displot(
    df_master,
    x="review_time",  # LINE TO BE REMOVED FOR STUDENTS
    hue="positive_review",  # LINE TO BE REMOVED FOR STUDENTS
    kde=True,
)

# %%
sns.displot(
    df_master,
    x="review_time",  # LINE TO BE REMOVED FOR STUDENTS
    hue="positive_review",  # LINE TO BE REMOVED FOR STUDENTS
    multiple="fill",
)

# %% [markdown]
# ### All rating columns: review_* & average_rating
# #### Distribution

# %%
review_columns = [
    "review_appearance",
    "review_aroma",
    "review_palate",  # LINE TO BE REMOVED FOR STUDENTS
    "review_taste",  # LINE TO BE REMOVED FOR STUDENTS
    "average_rating",
]
df_rating_long = df_master.melt(id_vars="positive_review", value_vars=review_columns)
df_rating_long

# %%
sns.displot(
    df_rating_long,
    x="value",
    row="variable",
    discrete=True,
    height=3,
    aspect=2,
)

# %% [markdown]
# #### Relationship with the target

# %%
sns.displot(
    df_rating_long,
    x="value",
    hue="positive_review",
    row="variable",
    discrete=True,
    height=3,
    aspect=2,
)

# %%
sns.displot(
    df_rating_long,
    x="value",
    hue="positive_review",
    row="variable",
    discrete=True,
    height=3,
    aspect=2,
    multiple="fill",
)

# %% [markdown]
# ## Categorical variables
# - `beer_style`
# - `beer_name`

# %% [markdown]
# ### `beer_style`
# #### Distribution

# %%
((df_master).beer_style.value_counts().plot.bar())  # LINE TO BE REMOVED FOR STUDENTS

# %% [markdown]
# #### Relationship with the target

# %%
sns.histplot(
    df_master,
    x="beer_style",
    discrete=True,
    hue="positive_review",
)

# %%
df_beer_styles = (
    df_master.groupby("beer_style")
    .positive_review.agg(["count", "mean"])
    .add_prefix("review_")
    .reset_index()
    .sort_values(by="review_mean", ascending=False)
    .reset_index(drop=True)
    .assign(
        bar_left_position=lambda df: df.review_count.cumsum().shift(1, fill_value=0)
    )
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
    linewidth=0.5,
)

# %% [markdown]
# ## High cardinality variables
# - `beer_name`
# - `beer_beerId`
# - `beer_brewerId`
# - `review_profileName`

# %% [markdown]
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
# As we cannot the high cardinality variables, we'll rather analyse the degree of the
# nodes.
#
# To compute the degree you'll need:
# - [`pd.Series.value_counts`](https://pandas.pydata.org/docs/reference/api/pandas.Series.value_counts.html)

# %% [markdown]
# ### `beer_name` degree
# #### Distribution

# %%
df_beer_name_degree = (
    (df_master.beer_name).value_counts().rename("beer_name_degree").reset_index()
)
df_beer_name_degree

# %%
(
    (df_beer_name_degree)
    .beer_name_degree.value_counts()
    .reset_index()
    .plot.scatter(
        x="beer_name_degree", y="count", marker="."
    )  # LINE TO BE REMOVED FOR STUDENTS
)

# %% [markdown]
# Many networks are [scale free networks](https://en.wikipedia.org/wiki/Scale-free_network):
# ![](https://www.researchgate.net/profile/Leonardo-Riella/publication/234031137/figure/fig1/AS:282612053626890@1444391372899/Structure-of-networks-A-biological-network-is-not-randomly-wired-similar-number-of.png)
#
# Meaning that the node's degree distribution follows a [power law
# distribution](https://en.wikipedia.org/wiki/Power_law), which is better visualized
# using a **log-log scale**:
# ![](https://upload.wikimedia.org/wikipedia/commons/3/3b/Degree_distribution_for_a_network_with_150000_vertices_and_mean_degree_%3D_6_created_using_the_Barabasi-Albert_model..png)
#

# %%
(
    (df_beer_name_degree)
    .beer_name_degree.value_counts()
    .reset_index()
    .plot.scatter(
        x="beer_name_degree", y="count", loglog=True, marker="."
    )  # LINE TO BE REMOVED FOR STUDENTS
)

# %% [markdown]
# Another way to visualize the power law distribution is to visualize the
# [rank-frequency plot](https://en.wikipedia.org/wiki/Rank%E2%80%93size_distribution).
#
# Instead of plotting the frequency as a function of the value (like in a normal
# distribution plot), we plot the frequency as a function of its rank. Note: It's always
# monotonically decreasing.
#
# Power law distributions exhibit also a distinctive visual pattern in the
# rank-frequency plot, known as the [Zipf's law]():
# ![](https://upload.wikimedia.org/wikipedia/commons/d/d9/Zipf-engl-0_English_-_Culpeper_herbal_and_War_of_the_Worlds.svg)
#


# %%
def plot_rank_size(series):
    return (
        (series)
        .rename("")
        .value_counts()
        .reset_index()
        .assign(rank=lambda df: range(1, 1 + df.shape[0]))
        .plot(x="rank", y="count", loglog=True, marker=".")
    )


# %%
plot_rank_size(df_beer_name_degree.beer_name_degree)

# %% [markdown]
# #### Relationship with target

# %%
df_beer_names = (
    (df_master)
    .merge(
        df_beer_name_degree,
        on="beer_name",
    )
    .loc[:, ["beer_name", "beer_name_degree", "positive_review"]]
)
df_beer_names

# %%
sns.histplot(df_beer_names, x="beer_name_degree", hue="positive_review")

# %%
sns.histplot(df_beer_names, x="beer_name_degree", hue="positive_review", log_scale=True)

# %%
sns.histplot(
    df_beer_names,
    x="beer_name_degree",
    hue="positive_review",
    log_scale=True,
    multiple="fill",
)

# %% [markdown]
# ### `beer_beerId`
# #### Distribution

# %%
df_beer_beerId_degree = (
    (df_master.beer_beerId).value_counts().rename("beer_beerId_degree").reset_index()
)
df_beer_beerId_degree

# %%
(
    (df_beer_beerId_degree)
    .beer_beerId_degree.value_counts()
    .reset_index()
    .plot.scatter(
        x="beer_beerId_degree", y="count", marker="."
    )  # LINE TO BE REMOVED FOR STUDENTS
)

# %%
(
    (df_beer_beerId_degree)
    .beer_beerId_degree.value_counts()
    .reset_index()
    .plot.scatter(
        x="beer_beerId_degree", y="count", loglog=True, marker="."
    )  # LINE TO BE REMOVED FOR STUDENTS
)

# %% [markdown]
# #### Relationship with target

# %%
plot_rank_size(df_beer_beerId_degree.beer_beerId_degree)

# %%
df_beer_beerIds = (
    (df_master)
    .merge(
        df_beer_beerId_degree,
        on="beer_beerId",
    )
    .loc[:, ["beer_beerId", "beer_beerId_degree", "positive_review"]]
)
df_beer_beerIds

# %%
sns.histplot(df_beer_beerIds, x="beer_beerId_degree", hue="positive_review")

# %%
sns.histplot(
    df_beer_beerIds, x="beer_beerId_degree", hue="positive_review", log_scale=True
)

# %%
sns.histplot(
    df_beer_beerIds,
    x="beer_beerId_degree",
    hue="positive_review",
    log_scale=True,
    multiple="fill",
)

# %% [markdown]
# ### `beer_brewerId`
# #### Distribution

# %%
df_beer_brewerId_degree = (
    (df_master.beer_brewerId)
    .value_counts()
    .rename("beer_brewerId_degree")
    .reset_index()
)
df_beer_brewerId_degree

# %%
(
    (df_beer_brewerId_degree)
    .beer_brewerId_degree.value_counts()
    .reset_index()
    .plot.scatter(
        x="beer_brewerId_degree", y="count", marker="."
    )  # LINE TO BE REMOVED FOR STUDENTS
)

# %%
(
    (df_beer_brewerId_degree)
    .beer_brewerId_degree.value_counts()
    .reset_index()
    .plot.scatter(
        x="beer_brewerId_degree", y="count", loglog=True, marker="."
    )  # LINE TO BE REMOVED FOR STUDENTS
)

# %% [markdown]
# #### Relationship with target

# %%
plot_rank_size(df_beer_brewerId_degree.beer_brewerId_degree)

# %%
df_beer_brewerIds = (
    (df_master)
    .merge(
        df_beer_brewerId_degree,
        on="beer_brewerId",
    )
    .loc[:, ["beer_brewerId", "beer_brewerId_degree", "positive_review"]]
)
df_beer_brewerIds

# %%
sns.histplot(df_beer_brewerIds, x="beer_brewerId_degree", hue="positive_review")

# %%
sns.histplot(
    df_beer_brewerIds, x="beer_brewerId_degree", hue="positive_review", log_scale=True
)

# %%
sns.histplot(
    df_beer_brewerIds,
    x="beer_brewerId_degree",
    hue="positive_review",
    log_scale=True,
    multiple="fill",
)

# %% [markdown]
# ### `review_profileName`
# #### Distribution

# %%
df_review_profileName_degree = (
    (df_master.review_profileName)
    .value_counts()
    .rename("review_profileName_degree")
    .reset_index()
)
df_review_profileName_degree

# %%
(
    (df_review_profileName_degree)
    .review_profileName_degree.value_counts()
    .reset_index()
    .plot.scatter(
        x="review_profileName_degree", y="count", marker="."
    )  # LINE TO BE REMOVED FOR STUDENTS
)

# %%
(
    (df_review_profileName_degree)
    .review_profileName_degree.value_counts()
    .reset_index()
    .plot.scatter(
        x="review_profileName_degree", y="count", loglog=True, marker="."
    )  # LINE TO BE REMOVED FOR STUDENTS
)

# %% [markdown]
# #### Relationship with target

# %%
plot_rank_size(df_review_profileName_degree.review_profileName_degree)

# %%
df_review_profileNames = (
    (df_master)
    .merge(
        df_review_profileName_degree,
        on="review_profileName",
    )
    .loc[:, ["review_profileName", "review_profileName_degree", "positive_review"]]
)
df_review_profileNames

# %%
sns.histplot(
    df_review_profileNames, x="review_profileName_degree", hue="positive_review"
)

# %%
sns.histplot(
    df_review_profileNames,
    x="review_profileName_degree",
    hue="positive_review",
    log_scale=True,
)

# %%
sns.histplot(
    df_review_profileNames,
    x="review_profileName_degree",
    hue="positive_review",
    log_scale=True,
    multiple="fill",
)


# %% [markdown]
# ## Text variable
# Using the [`pd.Series.str`](https://pandas.pydata.org/docs/reference/api/pandas.Series.str.html) API

# %% [markdown]
# ### Text length
# #### Distribution

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
df_review_text_len = df_master.assign(
    review_text_len=lambda df: df.review_text.str.len()
)

# %%
(
    (df_review_text_len.review_text_len).plot.hist(
        bins=200
    )  # LINE TO BE REMOVED FOR STUDENTS
)

# %%
((df_review_text_len.review_text_len).plot.hist(bins=200, logy=True))

# %% [markdown]
# #### Relationship with the target

# %%
sns.displot(
    df_review_text_len,
    x="review_text_len",
)

# %%
sns.displot(
    df_review_text_len,
    x="review_text_len",
    hue="positive_review",
)

# %%
sns.displot(
    df_review_text_len.loc[lambda df: df.review_text_len < 1500],
    x="review_text_len",
    hue="positive_review",
)

# %%
sns.displot(
    df_review_text_len.loc[lambda df: df.review_text_len < 1500],
    x="review_text_len",
    hue="positive_review",
    multiple="fill",
)

# %% [markdown]
# ### Words associated to positive & negative reviews

# %%
(
    (df_master)
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
# ### Word frequencies (optional)
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
df_word_frequencies.head(10000).plot(x="rank", y="word_frequency", marker=".")

# %%
df_word_frequencies.head(10000).plot(
    x="rank", y="word_frequency", loglog=True, marker="."
)

# %% [markdown]
# ## And if it's a regression ?
# We show those plot examples to explain what would be an exploratory data analysis for
# a regression problem.
#
# ### Continuous variable

# %%
sns.displot(
    df_master.loc[lambda df: df.beer_ABV < 20],
    x="beer_ABV",
    hue="review_overall",
    multiple="fill",
    palette="RdYlGn",
    bins=20,
)

# %%
sns.displot(
    df_master.loc[lambda df: df.beer_ABV < 20],
    x="beer_ABV",
    y="review_overall",
    bins=20,
)

# %% [markdown]
# ### Categorical variable

# %%
sns.histplot(
    df_master,
    x="review_appearance",
    discrete=True,
    hue="review_overall",
    multiple="stack",
    palette="RdYlGn",
)

# %%
sns.histplot(
    df_master,
    x="review_appearance",
    discrete=True,
    hue="review_overall",
    multiple="fill",
    palette="RdYlGn",
)

# %%
sns.violinplot(
    df_master,
    x="review_appearance",
    y="review_overall",
)

# %%
