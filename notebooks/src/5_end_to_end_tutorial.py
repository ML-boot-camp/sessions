# %% [markdown]
# # Plan du TD
#
# - Intro: **(30m)**
#   - accueil **(10m)**
#   - la baseline: workflow global end-to-end **(10m)**
#   - l'objectif: description des metriques de qualité, matrice de confusion, f1-score... **(10m)**
#
# - Data explo: **(30m)**
#   - data explo: petit exemple pour rappel **(5m)**
#   - data explo: travaux individuels **(25m)**
#
# - Feature engineering text: **(30m)**
#   - Présentation feature engineering existant & évaluation performance **(10m)**
#   - Travaux individuels: faire des expérimentations pour optimiser la perfo en fonction des hyperparamètres de feature engineering (threshold positive / negative word, taille du vocabulaire, rajouter des features (ex: `very_positive_words_set`)) **(20m)**
#
# - Pause **(15m)**
#
# - Pipeline: **(1h10m)**
#
#   - Data prep: Normalization (StandardScaler, Powertransform): **(20m)**
#     - Présentation **(10m)**
#     - Travaux individuels **(10m)**
#
#   - Modèle - Logistic Regression - expérimentations **(50m)**:
#
#     - Hyperparameter tuning manuel: (Régularisation (l1 ou l2 ou elastic), class weight): **(30m)**
#       - présentation des paramètres **(10m)**
#       - travaux individuels (tuner les hyperparamètres du modèle + ceux de la data prep) **(20m)**
#
#     - Courbe precision-recall (est-ce qu'une autre threshold est plus pertinente ?): **(20m)**
#       - Predict_proba + choix de threshold **(10m)**
#       - Travaux individuels **(10m)**

# %% [markdown]
#  # Preparation
#  ## Install & import modules

# %%
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import (
    linear_model,
    preprocessing,
    pipeline,
    model_selection,
    metrics,
    decomposition,
)
import numpy as np
# from wordcloud import STOPWORDS
import pandas as pd

# %%
file_url = "https://github.com/ML-boot-camp/ratebeer/raw/master/data/ratebeer_sample_enriched.parquet"

# %% [markdown]
#  ## Load data & describe

# %%
df_master = pd.read_parquet(file_url)

# %%
df_master


# %% [markdown]
#  # Data exploration
#  Instructions:
#  - create 3 charts and/or indicators which show interesting facts about the
#  dataset
#
#  Hint:
#  - [pandas plotting](https://pandas.pydata.org/pandas-docs/stable/user_guide/visualization.html)
#  - [seaborn](https://seaborn.pydata.org/examples/index.html)

# %% [markdown]
#  # Data preparation & feature engineering
#
#  Select only a subset of the data (only 100k lines)

# %%
df_features_and_target = (df_master).sample(100000, random_state=42)


# %% [markdown]
#  ## Target

# %%
df_features_and_target["positive_review"] = (
    df_features_and_target.review_overall.pipe(lambda s: s >= s.quantile(0.5))
)


# %%
df_features_and_target.positive_review.value_counts()


# %% [markdown]
#  ## Features
#  Instructions:
#  - add new features to add them to the training set and try to improve the
#  model performance.
#  - try different hyper-parameters to change the way those features are computed
#  and see if performance improves.

# %%


# def tokenize(serie):
#     return (
#         (serie)
#         .str.lower()
#         .str.replace(r"[^a-z]", " ")
#         .str.replace(r" +", " ")
#         .str.split(" ")
#     )


# df_words_count = (
#     (df_master)
#     .head(300000)
#     .assign(tokenized_text=lambda df: tokenize(df.text))
#     .loc[:, ["stars_review", "tokenized_text"]]
#     .explode("tokenized_text")
#     .groupby("tokenized_text", as_index=False)
#     .agg(["mean", "count"])
#     .reset_index()
#     .sort_values(by=("stars_review", "count"), ascending=False)
#     .loc[lambda df: ~df.tokenized_text.isin(list(STOPWORDS))]
#     .loc[lambda df: df.tokenized_text.str.len() > 1]
#     .head(1000)
# )


# %% [markdown]
#  ### Mean word rating
#  Compute the "word ratings" dictionary containing the mean review for each word
#  Compute the "mean word ratings" of each text

# %%
# word_mean_review = (
#     df_words_count.set_index("tokenized_text").stars_review["mean"].to_dict()
# )

# # %%
# df_features_and_target.tokenized_text = tokenize(df_features_and_target.text)


# def compute_mean_word_rating(words, word_mean_review):
#     return np.mean(
#         [word_mean_review[w] for w in words if w in word_mean_review] or [0]
#     )


# df_features_and_target.mean_word_rating = (
#     df_features_and_target.tokenized_text.apply(
#         compute_mean_word_rating, args=(word_mean_review,)
#     )
# )


# %% [markdown]
#  ### Positive & negative words counts
#  Instructions:
#  - Compute the "positive words" set containing the words with a high rating
#  - Compute the "negative words" set containing the words with a low rating
#  - Compute the `positive_words_count` & `negative_words_count` columns
#  containing the counts of the words in each set for each text

# %%
# positive_words_set = set(
#     df_words_count.loc[lambda df: df.stars_review["mean"] >= 4]
#     .loc[:, "tokenized_text"]
#     .tolist()
# )
# negative_words_set = set(
#     df_words_count.loc[lambda df: df.stars_review["mean"] <= 3.5]
#     .loc[:, "tokenized_text"]
#     .tolist()
# )



# %%
# def count_words_in_set(words, word_set):
#     return len(set(words) & word_set)


# df_features_and_target.positive_words_count = (
#     df_features_and_target.tokenized_text.apply(
#         count_words_in_set, args=(positive_words_set,)
#     )
# )
# df_features_and_target.negative_words_count = (
#     df_features_and_target.tokenized_text.apply(
#         count_words_in_set, args=(negative_words_set,)
#     )
# )


# %% [markdown]
#  ## Splits: Train/test & features/target

# %% [markdown]
#  ## Features/target selection
#  Select the features & the target

# %%
target = ["positive_review"]
features = [
    "review_appearance",
    "review_aroma",
    "review_palate",
    "review_taste",
    "beer_ABV",
    "number_of_reviews",
    # "average_rating"
]
df_features = df_features_and_target.loc[:, features]
df_target = df_features_and_target.loc[:, target]


# %% [markdown]
#  ### Features/target selection
#  Split the features & target, keeping 10% of the data in the test set

# %%
X_train, X_test, y_train, y_test = model_selection.train_test_split(
    df_features,
    df_target,
    test_size=0.1,
    random_state=42,
)

# %% [markdown]
#  ## Model training
#  Instructions:
#  - use a pipeline to wrap the model with its automatized preprocessing steps
#  - try different models & preprocessing step to improve the performance

# %%
pipe = pipeline.make_pipeline(
    linear_model.LogisticRegression(),
)
pipe.fit(X_train, y_train)

# %% [markdown]
#  ## Model evaluation
#  Instructions: add some comments about the measured performance of the model:
#  - why is the performance high/low ?
#  - what can we deduce from the train & test performance ?

# %% [markdown]
#  ### Accuracy

# %%
score_train = pipe.score(X_train, y_train)
score_test = pipe.score(X_test, y_test)

print(f"Accuracy (train): {score_train}")
print(f"Accuracy (test): {score_test}")

# %% [markdown]
#  ### Confusion matrix
#  Instructions:
#  - plot the confusion matrix
#  - analyze the confusion matrix & add some comments about the measured
#  performance of the model (markdown): what are the strengths & weaknesses of
#  the model?

# %%
metrics.ConfusionMatrixDisplay.from_estimator(pipe, X_test, y_test, cmap="YlOrRd")

# %% [markdown]
#  ### Classification report: precision, recall & $F_1$-score
#  In this case the accuracy may be misleading. Let's use another metric.

# %% [markdown]
#  <p align = "center">
#  <img src=https://upload.wikimedia.org/wikipedia/commons/thumb/2/26/Precisionrecall.svg/700px-Precisionrecall.svg.png width=400>
#  </p >
#
#  Precision = "purity" of the predictions.
#
#  Recall = "volume" of events you catch.
#
#
#  The $F_1$-score is the harmonic mean of precision & recall:
#  $$F_1 score = 2*\frac{precision*recall}{precision+recall}$$
#
#  Depending on context, we might also need to use the $F_\beta$-score which
#  allows to give more weight to precision or recall, thanks to the $\beta$
#  parameter:
#  $$F_\beta score = \frac{(1 +\beta)precision*recall}{\beta^2*precision+recall}$$

# %% [markdown]
#  Instructions:
#  - from the classification report, add some comments to explain the strengths
#  & weaknesses of the model
#  - compare to the performance values of a (very stupid) baseline model (e.g:
#  which predicts always 1)

# %%
y_pred = pipe.predict(X_test)

print(metrics.classification_report(y_test, y_pred))


# %%
print(metrics.classification_report(y_test, np.ones(y_pred.shape)))


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# %% [markdown]
#  # Plan du TD
#  - Accueil: **(10m)**
#  - Courbe precision-recall (est-ce qu'une autre threshold est plus pertinente ?): **(20m)**
#    - Predict_proba + choix de threshold **(10m)**
#    - Travaux individuels **(10m)**
#  - Hyperparameter tuning automatisé: gridsearch **(20m)**
#    - Présentation **(5m)**
#    - Expérimentation individuelle **(15m)**
#  - Feature engineering automatisé: **(30m)**
#    - PolynomialFeatures **(10m)**
#    - TF-IDF **(20m)**
#  - Pause **(15m)**
#  - Modèles: **(45m)**
#    - Présenter [classifiers dans sklearn](https://scikit-learn.org/stable/auto_examples/classification/plot_classifier_comparison.html) **(5m)**
#    - Exemple avec decision tree **(10m)**
#    - Travaux individuels: essayez un modèle qu'on ne vous a pas présenté **(30m)**
#  - Présentation du podium: 1er et 2nd **(30m)**

# %% [markdown]
#  # Preparation
#  ## Install & import modules

# %%
import plotly.express as px
import seaborn as sns
from sklearn import (
    linear_model,
    preprocessing,
    pipeline,
    model_selection,
    metrics,
    decomposition,
)
import numpy as np
from wordcloud import STOPWORDS
import os
import threading
from boto3.s3.transfer import TransferConfig
import boto3
import urllib3
import sys
import pandas as pd
from pathlib import Path



# %% [markdown]
#  ## Load data

# %%
df_master = pd.read_parquet("df_master.parquet")


# %%
df_master


# %% [markdown]
#  # Data exploration
#  Instructions:
#  - create 3 charts and/or indicators which show interesting facts about the
#  dataset
# 
#  Hint:
#  - [pandas plotting](https://pandas.pydata.org/pandas-docs/stable/user_guide/visualization.html)
#  - [seaborn](https://seaborn.pydata.org/examples/index.html)

# %% [markdown]
#  # Data preparation & feature engineering
# 
#  Select only a subset of the data (only 100k lines)

# %%
df_features_and_target = (df_master).sample(100000, random_state=42)


# %% [markdown]
#  ## Target

# %%
df_features_and_target.positive_review.value_counts()


# %% [markdown]
#  ## Features
#  Instructions:
#  - add new features to add them to the training set and try to improve the
#  model performance.
#  - try different hyper-parameters to change the way those features are computed
#  and see if performance improves.

# %%


def tokenize(serie):
    return (
        (serie)
        .str.lower()
        .str.replace(r"[^a-z]", " ")
        .str.replace(r" +", " ")
        .str.split(" ")
    )


df_words_count = (
    (df_master)
    .head(300000)
    .assign(tokenized_text=lambda df: tokenize(df.text))
    .loc[:, ["stars_review", "tokenized_text"]]
    .explode("tokenized_text")
    .groupby("tokenized_text", as_index=False)
    .agg(["mean", "count"])
    .reset_index()
    .sort_values(by=("stars_review", "count"), ascending=False)
    .loc[lambda df: ~df.tokenized_text.isin(list(STOPWORDS))]
    .loc[lambda df: df.tokenized_text.str.len() > 1]
    .head(10000)
)


# %% [markdown]
#  ### Mean word rating
#  Compute the "word ratings" dictionary containing the mean review for each word
#  Compute the "mean word ratings" of each text

# %%
word_mean_review = (
    df_words_count.set_index("tokenized_text").stars_review["mean"].to_dict()
)


# %%
df_features_and_target["tokenized_text"] = tokenize(df_features_and_target.text)


def compute_mean_word_rating(words, word_mean_review):
    return np.mean(
        [word_mean_review[w] for w in words if w in word_mean_review] or [0]
    )


df_features_and_target[
    "mean_word_rating"
] = df_features_and_target.tokenized_text.apply(
    compute_mean_word_rating, args=(word_mean_review,)
)


# %% [markdown]
#  ### Positive & negative words counts
#  Instructions:
#  - Compute the "positive words" set containing the words with a high rating
#  - Compute the "negative words" set containing the words with a low rating
#  - Compute the `positive_words_count` & `negative_words_count` columns
#  containing the counts of the words in each set for each text

# %%
positive_words_set = set(
    df_words_count.loc[lambda df: df.stars_review["mean"] >= 4]
    .loc[:, "tokenized_text"]
    .tolist()
)
negative_words_set = set(
    df_words_count.loc[lambda df: df.stars_review["mean"] <= 3.5]
    .loc[:, "tokenized_text"]
    .tolist()
)



# %%
def count_words_in_set(words, word_set):
    return len(set(words) & word_set)


df_features_and_target[
    "positive_words_count"
] = df_features_and_target.tokenized_text.apply(
    count_words_in_set, args=(positive_words_set,)
)
df_features_and_target[
    "negative_words_count"
] = df_features_and_target.tokenized_text.apply(
    count_words_in_set, args=(negative_words_set,)
)


# %% [markdown]
#  ## Splits: Train/test & features/target

# %% [markdown]
#  ## Features/target selection
#  Select the features & the target

# %%
target = ["positive_review"]
features = [
    "useful",
    "funny",
    "cool",
    "mean_word_rating",
    "positive_words_count",
    "negative_words_count",
]
df_features = df_features_and_target.loc[:, features]
df_target = df_features_and_target.loc[:, target]


# %% [markdown]
#  ### Features/target selection
#  Split the features & target, keeping 10% of the data in the test set

# %%
X_train, X_test, y_train, y_test = model_selection.train_test_split(
    df_features,
    df_target,
    test_size=0.1,
    random_state=42,
)


# %% [markdown]
#  ## Model training
#  Instructions:
#  - use a pipeline to wrap the model with its automatized preprocessing steps
#  - try different models & preprocessing step to improve the performance

# %%
pipe = pipeline.Pipeline(
    [
        ("preprocessing", preprocessing.StandardScaler()),
        ("classifier", linear_model.LogisticRegression()),
    ]
)
pipe.fit(X_train, y_train)



# %% [markdown]
#  ## Model evaluation
#  Instructions: add some comments about the measured performance of the model:
#  - why is the performance high/low ?
#  - what can we deduce from the train & test performance ?

# %% [markdown]
#  ### Accuracy

# %%
score_train = pipe.score(X_train, y_train)
score_test = pipe.score(X_test, y_test)

print(f"Accuracy (train): {score_train}")
print(f"Accuracy (test): {score_test}")


# %% [markdown]
#  ### Confusion matrix
#  Instructions:
#  - plot the confusion matrix
#  - analyze the confusion matrix & add some comments about the measured
#  performance of the model (markdown): what are the strengths & weaknesses of
#  the model?

# %%
metrics.ConfusionMatrixDisplay.from_estimator(pipe, X_test, y_test)
plt.show()


# %% [markdown]
#  ### Classification report: precision, recall & $F_1$-score
#  In this case the accuracy may be misleading. Let's use another metric.

# %% [markdown]
#  <p align = "center">
#  <img src=https://upload.wikimedia.org/wikipedia/commons/thumb/2/26/Precisionrecall.svg/700px-Precisionrecall.svg.png width=400>
#  </p >
# 
#  Precision = "purity" of the predictions.
# 
#  Recall = "volume" of events you catch.
# 
# 
#  The $F_1$-score is the harmonic mean of precision & recall:
#  $$F_1 score = 2*\frac{precision*recall}{precision+recall}$$
# 
#  Depending on context, we might also need to use the $F_\beta$-score which
#  allows to give more weight to precision or recall, thanks to the $\beta$
#  parameter:
#  $$F_\beta score = \frac{(1 +\beta)precision*recall}{\beta^2*precision+recall}$$

# %% [markdown]
#  Instructions:
#  - from the classification report, add some comments to explain the strengths
#  & weaknesses of the model
#  - compare to the performance values of a (very stupid) baseline model (e.g:
#  which predicts always 1)

# %%
y_pred = pipe.predict(X_test)

print(metrics.classification_report(y_test, y_pred))


# %%
print(metrics.classification_report(y_test, np.ones(y_pred.shape)))


# %% [markdown]
#  ### Prediction threshold and Precision/Recall curve

# %% [markdown]
#  By default, the logistic regression predicts 1 if the output probability is
#  greater than 0.5. This threshold can be customised. It has an impact on the precision and the recall
#  Let's play with this threshold and try to find a more pertinent one !

# %%
y_pred_proba = [x[1] for x in pipe.predict_proba(X_test)]


def binary_pred(y_pred, threshold=0.5):
    """
    Returns the binary array of preds from proba array and threshold
    """
    return np.array([1 if x > threshold else 0 for x in y_pred])


print(
    metrics.classification_report(
        y_test, binary_pred(y_pred_proba, threshold=0.5)
    )
)


# %% [markdown]
#  We can plot the Precision/Recall curve, which calculates the precision and
#  recall for a threshold from 0 to 1.

# %% [markdown]
#  Creation of a dataframe with precision and recall for a threshold range

# %%
thresholds = np.arange(0, 1, 0.001)
precisions = []
recalls = []
f1s = []
accuracies = []
for thresh in thresholds:
    preds = binary_pred(y_pred_proba, threshold=thresh)
    precisions.append(metrics.precision_score(y_test, preds))
    recalls.append(metrics.recall_score(y_test, preds))
    f1s.append(metrics.f1_score(y_test, preds))
    accuracies.append(metrics.accuracy_score(y_test, preds))

df = pd.DataFrame(
    {
        "threshold": thresholds,
        "precision": precisions,
        "recall": recalls,
        "f1": f1s,
        "accuracy": accuracies,
    }
)
df


# %% [markdown]
#  Other option to get precision & recall data to plot (but it misses the
#  threshold information). Useful only for model selection but not for threshold
#  tuning.

# %%
# Print precision recall curve
metrics.precision_recall_curve(
    y_test, y_pred_proba
)


# %%
fig = px.area(
    data_frame=df,
    x="recall",
    y="precision",
    title="Precision-Recall Curve",
    labels=dict(x="Recall", y="Precision"),
    width=700,
    height=500,
    hover_data=["threshold"],
)
fig.add_shape(type="line", line=dict(dash="dash"), x0=0, x1=1, y0=1, y1=0)
fig.update_yaxes(scaleanchor="x", scaleratio=1)
fig.update_xaxes(constrain="domain")

fig.show()


# %%
px.line(
    data_frame=df, x="threshold", y=["precision", "recall", "f1", "accuracy"]
)


# %%
import plotly
plotly.__version__

# %% [markdown]
#  ### Grid search

# %%
param_grid = {
    "preprocessing": ["passthrough", preprocessing.StandardScaler(), preprocessing.PowerTransformer()],
    "classifier": [linear_model.LogisticRegression(max_iter=1000)],
    "classifier__class_weight": [None, "balanced"],
    "classifier__C": [0.01, 1, 100],
}

grid = model_selection.GridSearchCV(
    pipe, param_grid=param_grid, cv=3, refit=False, scoring="f1", verbose=3
)

grid.fit(X_train, y_train.values.reshape(-1))


# %%
(
    pd.DataFrame(grid.cv_results_)
    .sort_values(by="rank_test_score")
    .drop("params", axis=1)
    .style.background_gradient()
)


# %%





