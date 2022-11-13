# %% [markdown]
# # Preparation
# ## Install & import modules

# %%
import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import RidgeClassifier
from sklearn.dummy import DummyClassifier

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


def feature_engineering_per_group(df, groupby="review_profileName", target="review_overall"):
    target_mean_column = f"feature_{groupby}_{target}_mean"
    count_column = f"feature_{groupby}_count"
    print(groupby)

    def _compute_expanding_values(group):
        df = group.sort_values(by="review_time")
        df[target_mean_column] = df[target].expanding().mean().shift(1)
        df[count_column] = df[target].expanding().count()
        return df

    def _fillna_in_expanding_values(df):
        return df.fillna({target_mean_column: df[target].mean()})

    return (
        (df)
        .groupby("review_profileName", as_index=False)
        .apply(_compute_expanding_values)
        .pipe(_fillna_in_expanding_values)
        .reset_index(drop=True)
    )


def target_engineering(df):
    target = "target_positive_review"
    df[target] = (df.review_overall >= df.review_overall.median()).astype(int)
    return df


def feature_engineering_time(df):
    return df.assign(feature_review_time=lambda df: df.review_time.astype(int).apply(pd.Timestamp.fromtimestamp))


def feature_engineering_reviews(df):
    for review in [
        "review_appearance",
        "review_aroma",
        "review_palate",
        "review_taste",
    ]:
        df[f"feature_{review}"] = df[review]
    return df


df_master = (
    (df_ratebeer)
    .pipe(feature_engineering_time)
    .pipe(feature_engineering_per_group, groupby="review_profileName")
    .pipe(feature_engineering_per_group, groupby="beer_beerId")
    .pipe(feature_engineering_per_group, groupby="beer_brewerId")
    .pipe(feature_engineering_reviews)
    .pipe(target_engineering)
)

# %%
features_correlation_with_target = (df_master).filter(regex="(feature|target)").corr().target_positive_review
features_correlation_with_target

# %%
sns.histplot(df_master, x="feature_review_profileName_review_overall_mean", bins=range(21), hue="target_positive_review")

# %%
sns.histplot(df_master, x="feature_beer_beerId_review_overall_mean", bins=range(21), hue="target_positive_review")

# %%
sns.histplot(df_master, x="feature_beer_brewerId_review_overall_mean", bins=range(21), hue="target_positive_review")

# %%
sns.histplot(df_master, x="feature_review_profileName_count", bins=200, hue="target_positive_review", log_scale=(True, True))

# %%
sns.histplot(df_master, x="feature_beer_beerId_count", bins=200, hue="target_positive_review", log_scale=(True, True))

# %%
sns.histplot(df_master, x="feature_beer_brewerId_count", bins=200, hue="target_positive_review", log_scale=(True, True))

# %%
features_to_drop = features_correlation_with_target.loc[lambda x: x.abs() < 0.1].index.tolist() + ["feature_review_time"]

df_X = df_master.filter(regex="feature").drop(features_to_drop, axis=1)
df_y = df_master.filter(regex="target")

df_X_train, df_X_test, df_y_train, df_y_test = train_test_split(df_X, df_y, test_size=0.1, random_state=42)

# %%
print("DummyClassifier: ", DummyClassifier().fit(df_X_train, df_y_train).score(df_X_test, df_y_test))
print("RidgeClassifier: ", RidgeClassifier().fit(df_X_train, df_y_train).score(df_X_test, df_y_test))
print("RandomForestClassifier: ", RandomForestClassifier().fit(df_X_train, df_y_train).score(df_X_test, df_y_test))
print("GradientBoostingClassifier: ", GradientBoostingClassifier().fit(df_X_train, df_y_train).score(df_X_test, df_y_test))

# %%
