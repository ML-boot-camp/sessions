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
df_master = (
    (df_ratebeer)
    .assign(
        time=lambda df: df.time.astype(int).apply(
            pd.Timestamp.fromtimestamp
        )
    )
    .assign(
        is_good=lambda df: (
            df.rating >= df.rating.median()
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
# - `rating`: an ordinal variable, which can be used to define a regression
# - `is_good`: a binary variable, which can be used to define a classification
#
# In the follow-up of the exploratory data analysis, for the sake of clariy, we'll
# consider only the binary target (classification). Some plots would be different for
# numeric target.

# %% [markdown]
# ### `is_good`

# %%
(
    (df_master.is_good)
    .value_counts()
    .plot.bar()  # LINE TO BE REMOVED FOR STUDENTS
)

# %%
sns.countplot(
    df_master,
    x="is_good",  # LINE TO BE REMOVED FOR STUDENTS
)

# %% [markdown]
# ## Quantitative variables
#
# - `alcohol`
# - `time`
# - `rating_appearance`
# - `rating_aroma`
# - `rating_palate`
# - `rating_taste`
# - `average_rating`

# %% [markdown]
# ### `alcohol`
# #### Distribution

# %%
((df_master.alcohol).plot.hist(bins=100))  # LINE TO BE REMOVED FOR STUDENTS

# %%
sns.displot(
    df_master,
    x="alcohol",
)

# %%
sns.displot(df_master, x="alcohol", hue="is_good")

# %%
sns.displot(
    df_master.loc[lambda df: df.alcohol < 20], x="alcohol", hue="is_good"
)

# %%
sns.displot(
    df_master.loc[lambda df: df.alcohol < 20],
    x="alcohol",
    hue="is_good",
    kde=True,
)

# %%
sns.displot(
    df_master.loc[lambda df: df.alcohol < 20],
    x="alcohol",
    hue="is_good",
    multiple="fill",
)

# %% [markdown]
# ### `time`

# %% [markdown]
# #### Distribution

# %%
sns.displot(
    df_master,
    x="time",  # LINE TO BE REMOVED FOR STUDENTS
)

# %% [markdown]
# #### Relationship with the target

# %%
sns.displot(
    df_master,
    x="time",  # LINE TO BE REMOVED FOR STUDENTS
    hue="is_good",  # LINE TO BE REMOVED FOR STUDENTS
    kde=True,
)

# %%
sns.displot(
    df_master,
    x="time",  # LINE TO BE REMOVED FOR STUDENTS
    hue="is_good",  # LINE TO BE REMOVED FOR STUDENTS
    multiple="fill",
)

# %% [markdown]
# ### All rating columns: review_* & average_rating
# #### Distribution

# %%
review_columns = [
    "rating_appearance",
    "rating_aroma",
    "rating_palate",  # LINE TO BE REMOVED FOR STUDENTS
    "rating_taste",  # LINE TO BE REMOVED FOR STUDENTS
]
df_rating_long = df_master.melt(id_vars="is_good", value_vars=review_columns)
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
    hue="is_good",
    row="variable",
    discrete=True,
    height=3,
    aspect=2,
)

# %%
sns.displot(
    df_rating_long,
    x="value",
    hue="is_good",
    row="variable",
    discrete=True,
    height=3,
    aspect=2,
    multiple="fill",
)

# %% [markdown]
# ## Categorical variables
# - `style`
# - `beer`

# %% [markdown]
# ### `style`
# #### Distribution

# %%
(
    (df_master["style"])
    .value_counts()
    .plot.bar()
)

# %% [markdown]
# #### Relationship with the target

# %%
sns.displot(
    df_master,
    x="style",
    discrete=True,
    hue="is_good",
)

# %%
df_styles = (
    (df_master)
    .groupby("style")
    .is_good.agg(["count", "mean"])
    .add_prefix("review_")
    .reset_index()
    .sort_values(by="review_mean", ascending=False)
    .reset_index(drop=True)
    .assign(
        bar_left_position=lambda df: df.review_count.cumsum().shift(1, fill_value=0)
    )
)
df_styles

# %%
plt.bar(
    x=df_styles.bar_left_position,
    height=df_styles.review_mean,
    width=df_styles.review_count,
    align="edge",
    alpha=0.5,
    edgecolor="k",
    linewidth=0.5,
)

# %% [markdown]
# ## High cardinality variables
# - `beer`
# - `beer_ID`
# - `brewery_ID`
# - `user`

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
# Analyse the degree of the nodes is a way to answer the following questions:
# - is an experienced user more severe ?
# - is a new user more forgiving ?
# - is a popular beer (or a big brewery) disadvantaged by a "boreness factor" ?
# - is a new beer (a small brewery) benefitting from a "novelty factor" ?
#
# To compute the degree you'll need:
#
# - [`pd.Series.value_counts`](https://pandas.pydata.org/docs/reference/api/pandas.Series.value_counts.html)

# %% [markdown]
# ### `beer` degree
# #### Distribution

# %%
df_beer_degree = (
    (df_master.beer)
    .value_counts()  # LINE TO BE REMOVED FOR STUDENTS
    .rename("beer_degree")
    .reset_index()
)
df_beer_degree

# %%
(
    (df_beer_degree.beer_degree)
    .value_counts()
    .reset_index()
    .plot.scatter(
        x="beer_degree", y="count", marker="."  # LINE TO BE REMOVED FOR STUDENTS
    )
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
    (df_beer_degree.beer_degree)
    .value_counts()
    .reset_index()
    .plot.scatter(  # LINE TO BE REMOVED FOR STUDENTS
        x="beer_degree",  # LINE TO BE REMOVED FOR STUDENTS
        y="count",  # LINE TO BE REMOVED FOR STUDENTS
        loglog=True,  # LINE TO BE REMOVED FOR STUDENTS
        marker="."  # LINE TO BE REMOVED FOR STUDENTS
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
plot_rank_size(df_beer_degree.beer_degree)

# %% [markdown]
# #### Relationship with target

# %%
df_beers = (
    (df_master)
    .merge(
        df_beer_degree,
        on="beer",
    )
    .loc[:, ["beer", "beer_degree", "is_good"]]
)
df_beers

# %%
sns.displot(df_beers, x="beer_degree", hue="is_good")

# %%
sns.displot(df_beers, x="beer_degree", hue="is_good", log_scale=True)

# %%
sns.displot(
    df_beers,
    x="beer_degree",
    hue="is_good",
    log_scale=True,
    multiple="fill",
)

# %% [markdown]
# ### `beer_ID`
# #### Distribution

# %%
df_beer_ID_degree = (
    (df_master.beer_ID).value_counts().rename("beer_ID_degree").reset_index()
)
df_beer_ID_degree

# %%
(
    (df_beer_ID_degree.beer_ID_degree)
    .value_counts()
    .reset_index()
    .plot.scatter(
        x="beer_ID_degree", y="count", marker="."  # LINE TO BE REMOVED FOR STUDENTS
    )
)

# %%
(
    (df_beer_ID_degree.beer_ID_degree)
    .value_counts()
    .reset_index()
    .plot.scatter(  # LINE TO BE REMOVED FOR STUDENTS
        x="beer_ID_degree",  # LINE TO BE REMOVED FOR STUDENTS
        y="count",  # LINE TO BE REMOVED FOR STUDENTS
        loglog=True,  # LINE TO BE REMOVED FOR STUDENTS
        marker=".",  # LINE TO BE REMOVED FOR STUDENTS
    )  # LINE TO BE REMOVED FOR STUDENTS
)

# %% [markdown]
# #### Relationship with target

# %%
plot_rank_size(df_beer_ID_degree.beer_ID_degree)

# %%
df_beer_IDs = (
    (df_master)
    .merge(
        df_beer_ID_degree,
        on="beer_ID",
    )
    .loc[:, ["beer_ID", "beer_ID_degree", "is_good"]]
)
df_beer_IDs

# %%
sns.displot(df_beer_IDs, x="beer_ID_degree", hue="is_good")

# %%
sns.displot(
    df_beer_IDs, x="beer_ID_degree", hue="is_good", log_scale=True
)

# %%
sns.displot(
    df_beer_IDs,
    x="beer_ID_degree",
    hue="is_good",
    log_scale=True,
    multiple="fill",
)

# %% [markdown]
# ### `brewery_ID`
# #### Distribution

# %%
df_brewery_ID_degree = (
    (df_master.brewery_ID)
    .value_counts()
    .rename("brewery_ID_degree")
    .reset_index()
)
df_brewery_ID_degree

# %%
(
    (df_brewery_ID_degree)
    .brewery_ID_degree.value_counts()
    .reset_index()
    .plot.scatter(  # LINE TO BE REMOVED FOR STUDENTS
        x="brewery_ID_degree",  # LINE TO BE REMOVED FOR STUDENTS
        y="count",  # LINE TO BE REMOVED FOR STUDENTS
        marker=".",  # LINE TO BE REMOVED FOR STUDENTS
    )  # LINE TO BE REMOVED FOR STUDENTS
)

# %%
(
    (df_brewery_ID_degree)
    .brewery_ID_degree.value_counts()
    .reset_index()
    .plot.scatter(  # LINE TO BE REMOVED FOR STUDENTS
        x="brewery_ID_degree",  # LINE TO BE REMOVED FOR STUDENTS
        y="count",  # LINE TO BE REMOVED FOR STUDENTS
        loglog=True,  # LINE TO BE REMOVED FOR STUDENTS
        marker=".",  # LINE TO BE REMOVED FOR STUDENTS
    )  # LINE TO BE REMOVED FOR STUDENTS
)

# %% [markdown]
# #### Relationship with target

# %%
plot_rank_size(df_brewery_ID_degree.brewery_ID_degree)

# %%
df_brewery_IDs = (
    (df_master)
    .merge(
        df_brewery_ID_degree,
        on="brewery_ID",
    )
    .loc[:, ["brewery_ID", "brewery_ID_degree", "is_good"]]
)
df_brewery_IDs

# %%
sns.displot(df_brewery_IDs, x="brewery_ID_degree", hue="is_good")

# %%
sns.displot(
    df_brewery_IDs, x="brewery_ID_degree", hue="is_good", log_scale=True
)

# %%
sns.displot(
    df_brewery_IDs,
    x="brewery_ID_degree",
    hue="is_good",
    log_scale=True,
    multiple="fill",
)

# %% [markdown]
# ### `user`
# #### Distribution

# %%
df_user_degree = (
    (df_master.user)
    .value_counts()
    .rename("user_degree")
    .reset_index()
)
df_user_degree

# %%
(
    (df_user_degree)
    .user_degree.value_counts()
    .reset_index()
    .plot.scatter(  # LINE TO BE REMOVED FOR STUDENTS
        x="user_degree",  # LINE TO BE REMOVED FOR STUDENTS
        y="count",  # LINE TO BE REMOVED FOR STUDENTS
        marker=".",  # LINE TO BE REMOVED FOR STUDENTS
    )  # LINE TO BE REMOVED FOR STUDENTS
)

# %%
(
    (df_user_degree)
    .user_degree.value_counts()
    .reset_index()
    .plot.scatter(  # LINE TO BE REMOVED FOR STUDENTS
        x="user_degree",  # LINE TO BE REMOVED FOR STUDENTS
        y="count",  # LINE TO BE REMOVED FOR STUDENTS
        loglog=True,  # LINE TO BE REMOVED FOR STUDENTS
        marker=".",  # LINE TO BE REMOVED FOR STUDENTS
    )  # LINE TO BE REMOVED FOR STUDENTS
)

# %% [markdown]
# #### Relationship with target

# %%
plot_rank_size(df_user_degree.user_degree)

# %%
df_users = (
    (df_master)
    .merge(
        df_user_degree,
        on="user",
    )
    .loc[:, ["user", "user_degree", "is_good"]]
)
df_users

# %%
sns.displot(
    df_users, x="user_degree", hue="is_good"
)

# %%
sns.displot(
    df_users,
    x="user_degree",
    hue="is_good",
    log_scale=True,
)

# %%
sns.displot(
    df_users,
    x="user_degree",
    hue="is_good",
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
df_text_len = df_master.assign(
    text_len=lambda df: df.text.str.len()
)

# %%
(
    (df_text_len.text_len).plot.hist(
        bins=200
    )  # LINE TO BE REMOVED FOR STUDENTS
)

# %%
((df_text_len.text_len).plot.hist(bins=200, logy=True))

# %% [markdown]
# #### Relationship with the target

# %%
sns.displot(
    df_text_len,
    x="text_len",
)

# %%
sns.displot(
    df_text_len,
    x="text_len",
    hue="is_good",
)

# %%
sns.displot(
    df_text_len.loc[lambda df: df.text_len < 1500],
    x="text_len",
    hue="is_good",
)

# %%
sns.displot(
    df_text_len.loc[lambda df: df.text_len < 1500],
    x="text_len",
    hue="is_good",
    multiple="fill",
)

# %% [markdown]
# ### Words associated to positive & negative reviews

# %%
(
    (df_master)
    .head(100000)
    .assign(
        tokenized_text=lambda df: (df.text)
        .str.lower()
        .str.replace(r"[^a-z]", " ")
        .str.replace(r" +", " ")
        .str.split(" ")
    )
    .loc[:, ["rating", "tokenized_text"]]
    .explode("tokenized_text")
    .loc[lambda df: df.tokenized_text != ""]
    .groupby("tokenized_text", as_index=False)
    .agg(["mean", "count"])
    .reset_index()
    .sort_values(by=("rating", "count"), ascending=False)
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
    (df_master.text)
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
    df_master.loc[lambda df: df.alcohol < 20],
    x="alcohol",
    hue="rating",
    multiple="fill",
    palette="RdYlGn",
    bins=20,
)

# %%
sns.displot(
    df_master.loc[lambda df: df.alcohol < 20],
    x="alcohol",
    y="rating",
    bins=20,
)

# %% [markdown]
# ### Categorical variable

# %%
sns.displot(
    df_master,
    x="rating_appearance",
    discrete=True,
    hue="rating",
    multiple="stack",
    palette="RdYlGn",
)

# %%
sns.displot(
    df_master,
    x="rating_appearance",
    discrete=True,
    hue="rating",
    multiple="fill",
    palette="RdYlGn",
)

# %%
sns.violinplot(
    df_master,
    x="rating_appearance",
    y="rating",
)
