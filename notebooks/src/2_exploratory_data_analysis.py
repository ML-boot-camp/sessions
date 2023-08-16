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
file_url = "https://github.com/ML-boot-camp/ratebeer/raw/master/data/ratebeer_sample_enriched.parquet"

# %%
df = pd.read_parquet(file_url)

# %% [markdown]
# ## General information
# ### Shape
# Have a first overview of the dataframe size, i.e. number of rows & columns.
#
# Methods you'll need:
# - [`pd.DataFrame.shape`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.shape.html)

# %%
df.shape

# %% [markdown]
# ### Overview
# Get a few information about the content of the dataframe:
# - number of null values per column
# - data type of each column
# - memory usage
#
# Methods you'll need:
# - [`pd.DataFrame.info`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.info.html)

# %%
df.info(memory_usage="deep")  # LINE TO BE REMOVED FOR STUDENTS

# %% [markdown]
# ### Sample
# Show a sample of the data

# %%
df

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
df.describe(include="all").fillna("").T

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
    (df.is_good)
    .value_counts()
    .plot.bar()  # LINE TO BE REMOVED FOR STUDENTS
)

# %%
sns.countplot(
    df,
    x="is_good",  # LINE TO BE REMOVED FOR STUDENTS
)

# %% [markdown]
# ## Quantitative variables
#
# - `alcohol`
# - `date`
# - `rating_appearance`
# - `rating_aroma`
# - `rating_palate`
# - `rating_taste`

# %% [markdown]
# ### `alcohol`
# #### Distribution

# %%
((df.alcohol).plot.hist(bins=100))  # LINE TO BE REMOVED FOR STUDENTS

# %%
sns.displot(
    df,
    x="alcohol",
)

# %%
sns.displot(df, x="alcohol", hue="is_good")

# %%
sns.displot(
    df.loc[lambda df: df.alcohol < 20], x="alcohol", hue="is_good"
)

# %%
sns.displot(
    df.loc[lambda df: df.alcohol < 20],
    x="alcohol",
    hue="is_good",
    kde=True,
)

# %%
sns.displot(
    df.loc[lambda df: df.alcohol < 20],
    x="alcohol",
    hue="is_good",
    multiple="fill",
)

# %% [markdown]
# ### `date`

# %% [markdown]
# #### Distribution

# %%
sns.displot(
    df,
    x="date",  # LINE TO BE REMOVED FOR STUDENTS
)

# %% [markdown]
# #### Relationship with the target

# %%
sns.displot(
    df,
    x="date",  # LINE TO BE REMOVED FOR STUDENTS
    hue="is_good",  # LINE TO BE REMOVED FOR STUDENTS
    kde=True,
)

# %%
sns.displot(
    df,
    x="date",  # LINE TO BE REMOVED FOR STUDENTS
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
df_rating_long = df.melt(id_vars="is_good", value_vars=review_columns)
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
# - `type`
# - `beer`

# %% [markdown]
# ### `type`
# #### Distribution

# %%
(
    (df.type)
    .value_counts()
    .plot.bar()
)

# %% [markdown]
# #### Relationship with the target

# %%
sns.displot(
    df,
    x="type",
    discrete=True,
    hue="is_good",
)

# %%
df_styles = (
    (df)
    .groupby("type")
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
# - `brewery`
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
df_beer_degree = df.loc[:, ["beer", "beer_degree"]].drop_duplicates()
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
sns.displot(df, x="beer_degree", hue="is_good")

# %%
sns.displot(df, x="beer_degree", hue="is_good", log_scale=True)

# %%
sns.displot(
    df,
    x="beer_degree",
    hue="is_good",
    log_scale=True,
    multiple="fill",
)

# %% [markdown]
# ### `brewery`
# #### Distribution

# %%
df_brewery_degree = df.loc[:, ["brewery", "brewery_degree"]].drop_duplicates()
df_brewery_degree

# %%
(
    (df_brewery_degree.brewery_degree)
    .value_counts()
    .reset_index()
    .plot.scatter(  # LINE TO BE REMOVED FOR STUDENTS
        x="brewery_degree",  # LINE TO BE REMOVED FOR STUDENTS
        y="count",  # LINE TO BE REMOVED FOR STUDENTS
        marker=".",  # LINE TO BE REMOVED FOR STUDENTS
    )  # LINE TO BE REMOVED FOR STUDENTS
)

# %%
(
    (df_brewery_degree.brewery_degree)
    .value_counts()
    .reset_index()
    .plot.scatter(  # LINE TO BE REMOVED FOR STUDENTS
        x="brewery_degree",  # LINE TO BE REMOVED FOR STUDENTS
        y="count",  # LINE TO BE REMOVED FOR STUDENTS
        loglog=True,  # LINE TO BE REMOVED FOR STUDENTS
        marker=".",  # LINE TO BE REMOVED FOR STUDENTS
    )  # LINE TO BE REMOVED FOR STUDENTS
)

# %%
plot_rank_size(df_brewery_degree.brewery_degree)

# %% [markdown]
# #### Relationship with target

# %%
sns.displot(df, x="brewery_degree", hue="is_good")

# %%
sns.displot(
    df, x="brewery_degree", hue="is_good", log_scale=True
)

# %%
sns.displot(
    df,
    x="brewery_degree",
    hue="is_good",
    log_scale=True,
    multiple="fill",
)

# %% [markdown]
# ### `user`
# #### Distribution

# %%
df_user_degree = df.loc[:, ["user", "user_degree"]].drop_duplicates()
df_user_degree

# %%
(
    (df_user_degree.user_degree)
    .value_counts()
    .reset_index()
    .plot.scatter(  # LINE TO BE REMOVED FOR STUDENTS
        x="user_degree",  # LINE TO BE REMOVED FOR STUDENTS
        y="count",  # LINE TO BE REMOVED FOR STUDENTS
        marker=".",  # LINE TO BE REMOVED FOR STUDENTS
    )  # LINE TO BE REMOVED FOR STUDENTS
)

# %%
(
    (df_user_degree.user_degree)
    .value_counts()
    .reset_index()
    .plot.scatter(  # LINE TO BE REMOVED FOR STUDENTS
        x="user_degree",  # LINE TO BE REMOVED FOR STUDENTS
        y="count",  # LINE TO BE REMOVED FOR STUDENTS
        loglog=True,  # LINE TO BE REMOVED FOR STUDENTS
        marker=".",  # LINE TO BE REMOVED FOR STUDENTS
    )  # LINE TO BE REMOVED FOR STUDENTS
)

# %%
plot_rank_size(df_user_degree.user_degree)

# %% [markdown]
# #### Relationship with target

# %%
sns.displot(
    df, x="user_degree", hue="is_good"
)

# %%
sns.displot(
    df,
    x="user_degree",
    hue="is_good",
    log_scale=True,
)

# %%
sns.displot(
    df,
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
#
# Is it a Power law distribution ?

# %%
(df.text_length).plot.hist(bins=200)  # LINE TO BE REMOVED FOR STUDENTS

# %%
((df.text_length).plot.hist(bins=200, logy=True))

# %% [markdown]
# #### Relationship with the target

# %%
sns.displot(df, x="text_length")

# %%
sns.displot(
    df,
    x="text_length",
    hue="is_good",
)

# %%
sns.displot(
    df.loc[lambda df: df.text_length < 1500],
    x="text_length",
    hue="is_good",
)

# %%
sns.displot(
    df.loc[lambda df: df.text_length < 1500],
    x="text_length",
    hue="is_good",
    multiple="fill",
)

# %% [markdown]
# ### Words associated to positive & negative reviews (optional)

# %%
(
    (df)
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
    (df.text)
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
    df.loc[lambda df: df.alcohol < 20],
    x="alcohol",
    hue="rating",
    multiple="fill",
    palette="RdYlGn",
    bins=20,
)

# %%
sns.displot(
    df.loc[lambda df: df.alcohol < 20],
    x="alcohol",
    y="rating",
    bins=20,
)

# %% [markdown]
# ### Categorical variable

# %%
sns.displot(
    df,
    x="rating_appearance",
    discrete=True,
    hue="rating",
    multiple="stack",
    palette="RdYlGn",
)

# %%
sns.displot(
    df,
    x="rating_appearance",
    discrete=True,
    hue="rating",
    multiple="fill",
    palette="RdYlGn",
)

# %%
sns.violinplot(
    df,
    x="rating_appearance",
    y="rating",
)
