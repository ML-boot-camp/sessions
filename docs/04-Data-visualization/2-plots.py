# %% [markdown]
# # Plots
#
# ## Point based plots
#
# ### Scatter
#
# Scatter plot is the most basic plot to encode any data using **points** and their
# properties. Location (X, Y) are 2 properties which are able to represent any
# measurement type.
#
# Below, two ratio variables are represented (notice how the scale shows the level zero)
# thanks to position:
#
# | Visual variable | Data               |
# |-----------------|--------------------|
# | Position (x)    | Horsepower (Ratio) |
# | Position (y)    | Miles per gallon (Ratio) |

# %% tags=["hide_code"]
import altair as alt
import pandas as pd
import plotly.express as px

alt.renderers.set_embed_options(actions=False)

# Load the dataset
url = "https://vega.github.io/vega-lite/data/cars.json"
data = pd.read_json(url)

# Create the plot
alt.Chart(data).mark_point(filled=True).encode(x="Horsepower:Q", y="Miles_per_Gallon:Q")

# %% [markdown]
# What we learn from this plot is that there might be a quadratic relationship between
# $ X $ and $ Y $ like: $ Y = a X^{2} + b X + c $.
#
# Let's try to learn something by adding more information on this chart, mapping another
# data column on visual properties:
#
# | Visual variable | Data               |
# |-----------------|--------------------|
# | Position (x)    | Horsepower (Ratio) |
# | Position (y)    | Miles per gallon (Ratio) |
# | Color hue       | Cylinders (Ordinal) |

# %% tags=["hide_code"]
alt.Chart(data).mark_point(filled=True).encode(
    x="Horsepower:Q",
    y="Miles_per_Gallon:Q",
    color=alt.Color("Cylinders:O").scale(scheme="turbo"),
)

# %% [markdown]
# We can improve this chart by using **redundancy**, i.e. several visual variables used
# to represent only a single column of data:
#
# | Visual variable | Data               |
# |-----------------|--------------------|
# | Position (x)    | Horsepower (Ratio) |
# | Position (y)    | Miles per gallon (Ratio) |
# | Color hue       | Cylinders (Ordinal) |
# | Shape           | Cylinders (Ordinal) |

# %% tags=["hide_code"]
alt.Chart(data).mark_point(filled=True).encode(
    x="Horsepower:Q",
    y="Miles_per_Gallon:Q",
    color=alt.Color("Cylinders:O").scale(scheme="turbo"),
    shape="Cylinders:O",
)

# %% [markdown]
# There is a slight issue of **overplotting**: the information is saturated due to
# elements being on top of each other. One solution is to use a bit of transparency.
#
# | Visual variable | Data               |
# |-----------------|--------------------|
# | Position (x)    | Horsepower (Ratio) |
# | Position (y)    | Miles per gallon (Ratio) |
# | Color hue       | Cylinders (Ordinal) |
# | Shape           | Cylinders (Ordinal) |
# | Opacity         | 25% |

# %% tags=["hide_code"]
alt.Chart(data).mark_point(filled=True, opacity=0.25).encode(
    x="Horsepower:Q",
    y="Miles_per_Gallon:Q",
    color=alt.Color("Cylinders:O").scale(scheme="turbo"),
    shape="Cylinders:O",
)

# %% [markdown]
# We now see that most cars are in the *long-distance driving* region, with low
# consumption & low power.
#
# Can we learn something by adding even more information ?
#
# Below we try to map another data column on a supplementary visual variable:
#
# | Visual variable | Data                   |
# |-----------------|------------------------|
# | Position (x)    | Horsepower (Ratio)     |
# | Position (y)    | Miles per gallon (Ratio) |
# | Color hue       | Cylinders (Ordinal) |
# | Shape           | Cylinders (Ordinal) |
# | Opacity         | 25% |
# | Size            | Weights in lbs (Ratio) |

# %% tags=["hide_code"]
alt.Chart(data).mark_point(filled=True, opacity=0.25).encode(
    x="Horsepower:Q",
    y="Miles_per_Gallon:Q",
    color=alt.Color("Cylinders:O").scale(scheme="turbo"),
    shape="Cylinders:O",
    size="Weight_in_lbs:Q",
)

# %% [markdown]
#
# The plot is barely readable. 😕
#
# It is saturated due to **overplotting**, so we are not able to perceive the
# relationship between the new columns and the other. Also it's **too complex**: we are
# trying to show 4 data columns at once, it's often difficult to represent more than 3
# information at once in an understandable way.
#
# ### Strip
#
# If you'd like to visualize the relationship between a **discrete** variable (nominal
# or ordinal) and a quantitative variable (interval or ratio), you can try to use a
# **scatter** plot:
#
# | Visual variable | Data               |
# |-----------------|--------------------|
# | Position (x)    | Horsepower (Ratio) |
# | Position (y)    | Cylinders (Ordinal) |
# | Opacity         | 25% |

# %% tags=["hide_code"]
alt.Chart(data).mark_point(filled=True, opacity=0.25).encode(
    x="Horsepower:Q", y="Cylinders:O"
)

# %% [markdown]
# But the result is often barely readable due to **overplotting**, even if we use
# transparency, due to points being drawn on a few lines (1 for each discrete value of
# the data).
#
# The **strip** plot is a simple chart composed of **vertical lines instead of points**
# to display information:
#
# | Visual variable | Data               |
# |-----------------|--------------------|
# | Position (x)    | Horsepower (Ratio) |
# | Position (y)    | Cylinders (Ordinal) |
# | Opacity         | 25% |

# %% tags=["hide_code"]
alt.Chart(data).mark_tick(opacity=0.25).encode(x="Horsepower:Q", y="Cylinders:O")

# %% [markdown]
# It's a bit more readable than the scatter plot and very compact, but It is rarely
# used. For teaching purposes, it allows to understand what how you can encode a mix of
# discrete and quantitative data on position as a visual parameter: the trick is to draw
# lines instead of points.
#
# Note that we can also use redundancy to improve the readability of the chart:
#
# | Visual variable | Data               |
# |-----------------|--------------------|
# | Position (x)    | Horsepower (Ratio) |
# | Position (y)    | Cylinders (Ordinal) |
# | Color           | Cylinders (Ordinal) |
# | Opacity         | 25% |

# %% tags=["hide_code"]
alt.Chart(data).mark_tick(opacity=0.25).encode(
    x="Horsepower:Q",
    y="Cylinders:O",
    color=alt.Color("Cylinders:O").scale(scheme="turbo"),
)

# %% [markdown]
# ## Rectangle based plots
#
# ### Bar & histogram
#
# **Bar** plots use the bar **size** a visual variable to encode data. It is good to
# represent a **quantity**, so it is used by default in **histograms**:

# %% [markdown]
# | Visual variable | Data                          |
# |-----------------|-------------------------------|
# | Position (x)    | Horsepower (Ratio) binned     |
# | Size            | Count (aggregate for each bin)|

# %% tags=["hide_code"]
alt.Chart(data).mark_bar().encode(
    x=alt.X("Horsepower:Q", bin=True), y="count(Cylinders):Q"
)

# %% [markdown]
# You can try also to encode a discrete variable on color as a secondary visual
# variable, which is called a **stacked bar** chart:

# %% [markdown]
# | Visual variable | Data                    |
# |-----------------|-------------------------|
# | Position (x)    | Horsepower binned (Ordinal)  |
# | Size            | Count (for each bin)    |
# | Color           | Cylinders (Ordinal)     |

# %% tags=["hide_code"]
alt.Chart(data).mark_bar().encode(
    x=alt.X("Horsepower:Q", bin=True),
    y=alt.Y("count(Cylinders):Q", title="Count"),
    color=alt.Color("Cylinders:O").scale(scheme="turbo"),
)

# %% [markdown]
# It gives an idea of the distribution of values in each class of the discrete data, but
# it's difficult to do a precise assessment: you can't compare the distributions in a
# stacked bar chart. The overall distribution is still understandable, though.
#
# To get a precise view of each distribution and to compare them, it's better to
# separate them using the position as a visual variable:

# %% [markdown]
# | Visual variable | Data                    |
# |-----------------|-------------------------|
# | Position (x)    | Horsepower binned (Ordinal)  |
# | Size            | Count (for each bin)    |
# | Color           | Cylinders (Ordinal)     |
# | Position (y)    | -                       |

# %% tags=["hide_code"]
alt.Chart(data).mark_bar().encode(
    x=alt.X("Horsepower:Q", bin=True),
    y=alt.Y("count(Cylinders):Q", title="Count"),
    color=alt.Color("Cylinders:O").scale(scheme="turbo"),
    row="Cylinders:O",
)

# %% [markdown]
# But you lose the representation of the overall distribution.

# %% [markdown]
# ### 2D-histogram
#
# Finally, if have too much overplotting with scatter plots, it's possible to make
# 2D-histograms. The data is binned across 2 quantitative dimensions, which are
# transformed intro ordinal data. The count aggregate can then be encoded into visual
# variables, such as the size or the color.
#
# When the count is encoded on the **size** of the points, it's a **bubble** plot:

# %% [markdown]
# | Visual variable | Data                          |
# |-----------------|-------------------------------|
# | Position (x)    | Horsepower binned (Ordinal)   |
# | Position (y)    | Miles per gallon binned (Ordinal) |
# | Size            | Count (Ratio)                 |

# %% tags=["hide_code"]
alt.Chart(data).mark_circle().encode(
    x=alt.X("Horsepower:Q").bin(maxbins=32).scale(zero=True),
    y=alt.Y("Miles_per_Gallon:Q").bin(maxbins=32).scale(zero=True),
    size="count()",
).configure_view(stroke="transparent")

# %% [markdown]
# Which you can also improve using **redundancy**:

# %% [markdown]
# | Visual variable | Data                          |
# |-----------------|-------------------------------|
# | Position (x)    | Horsepower binned (Ordinal)   |
# | Position (y)    | Miles per gallon binned (Ordinal) |
# | Size            | Count (Ratio)                 |
# | Color           | Count (Ratio)                 |

# %% tags=["hide_code"]
alt.Chart(data).mark_circle().encode(
    x=alt.X("Horsepower:Q").bin(maxbins=32).scale(zero=True),
    y=alt.Y("Miles_per_Gallon:Q").bin(maxbins=32).scale(zero=True),
    size="count()",
    color=alt.Color("count()").scale(scheme="yellowgreenblue"),
).configure_view(stroke="transparent")

# %% [markdown]
# When the count is encoded on the **color** of the points, it's a **heatmap** plot

# %% [markdown]
# | Visual variable | Data                          |
# |-----------------|-------------------------------|
# | Position (x)    | Horsepower binned (Ordinal)   |
# | Position (y)    | Miles per gallon binned (Ordinal) |
# | Color           | Count (Ratio)                 |

# %% tags=["hide_code"]
alt.Chart(data).mark_rect().encode(
    x=alt.X("Horsepower:Q").bin(maxbins=32).scale(zero=True),
    y=alt.Y("Miles_per_Gallon:Q").bin(maxbins=32).scale(zero=True),
    color="count()",
).configure_view(stroke="transparent")

# %% [markdown]
## Line based plots

# %% [markdown]
### Line

# %% [markdown]
# In certain cases, the scatter plot is not really relevant, as for the plot below,
# which shows the mean consumption for all car released a given year time, and breakdown
# by number of cylinders. Can you guess what's wrong with this chart?

# %% [markdown]
# | Visual variable | Data                 |
# |-----------------|----------------------|
# | Position (x)    | Year (Ordinal)       |
# | Position (y)    | Horsepower mean (Ratio) |
# | Color hue       | Cylinders (Ordinal)  |
# | Shape           | Cylinders (Ordinal)  |

# %% tags=["hide_code"]
alt.Chart(data).mark_point(filled=True).encode(
    alt.X("Year:T"),
    alt.Y("Horsepower:Q").aggregate("mean"),
    alt.Color("Cylinders:O").scale(scheme="turbo"),
    alt.Shape("Cylinders:N"),
)

# %% [markdown]
# This **temporal relationship** between data points can be represented using a **line**
# chart. A line chart uses small segments which have 2 additional visual variables -
# **size & slope** - which are powerful to perceive a **variation rate**.
#
# | Visual variable     | Data                           |
# |---------------------|--------------------------------|
# | Position (x)        | Year (Ordinal)                 |
# | Position (y)        | Horsepower mean (Ratio)        |
# | Size (of segments)  | Horsepower mean variation (Interval) |
# | Slope (of segments) |                                |
# | Color hue           | Cylinders (Ordinal)            |

# %% tags=["hide_code"]
alt.Chart(data).mark_line(point=True).encode(
    alt.X("Year:T"),
    alt.Y("Horsepower:Q", aggregate="mean"),
    alt.Color("Cylinders:O").scale(scheme="turbo"),
)

# %% [markdown]
# We can refine this chart by encoding the count of cars for each year and cylinder
# class, as we made a mean aggregate. This is a ratio data which can be shown using the
# size:

# %% [markdown]
# | Visual variable     | Data                   |
# |---------------------|------------------------|
# | Position (x)        | Year (Ordinal)         |
# | Position (y)        | Horsepower mean (Ratio)|
# | Size (of segments)  | Horsepower mean variation (Interval) |
# | Slope (of segments) |                        |
# | Color hue           | Cylinders (Ordinal)    |
# | Size (of points)    | Count                  |

# %% tags=["hide_code"]
alt.Chart(data).mark_line(point=True).encode(
    alt.X("Year:T"),
    alt.Y("Horsepower:Q").aggregate("mean"),
    alt.Size("Miles_per_Gallon:Q").aggregate("count"),
    alt.Color("Cylinders:O").scale(scheme="turbo"),
)

# %% [markdown]
# This chart allows to tell the whole story of the car industry in the 70s and the 80s:
# at first, *muscle cars* were very popular due to their huge power and their 8
# cylinders, but the oil shocks in the 70s led people to prefer more fuel-savvy models
# with 4 cylinders.

# %% [markdown]
# <img src="https://medias.spotern.com/spots/w1280/51/51099-1669106381.webp"
#   width=300>
# <span style="font-size: 100pt">➜</span>
# <img src="https://i1.wp.com/www.aronline.co.uk/wp-content/uploads/2011/12/xr3i.jpg"
#   width=300>

# %% [markdown]
# At the end, the industry tried to design less powerful cars but with still with 8
# cylinders, in an attempt to lure the consumers into thinking that they were still
# buying *muscle cars* (but more fuel-savvy).

# %% [markdown]
### Area & distribution

# Area charts are line charts, but filled with color. As bar charts, they are powerful
# to represent quantities.
#
# It can also replace an histogram made on a binned quantitative variable, by using
# kernel smoothing (which is a type of weighted moving average).

# %% [markdown]
# | Visual variable | Data |
# | --- | --- |
# | Position (x) | Horsepower (Ratio) |
# | Position (y) | Density (Ratio) |

# %% tags=["hide_code"]
alt.Chart(data).transform_density(
    density="Horsepower",
    counts=True,
    bandwidth=5,
).mark_area().encode(alt.X("value:Q"), alt.Y("density:Q").title("Count (smoothed)"))

# %% [markdown]
# Like with histograms, we can also encode an ordinal data on the color as a visual
# variable:

# | Visual variable | Data |
# | --- | --- |
# | Position (x) | Horsepower (Ratio) |
# | Position (y) | Density (Ratio) |
# | Color | Cylinders (Ordinal) |

# %% tags=["hide_code"]
alt.Chart(data).transform_density(
    density="Horsepower",
    groupby=["Cylinders"],
    counts=True,
    steps=100,
    extent=[40, 240],
    bandwidth=5,
).mark_area().encode(
    alt.X("value:Q"),
    alt.Y("density:Q").title("Count (smoothed)").stack("zero"),
    alt.Color("Cylinders:N").scale(scheme="turbo"),
)

# %% [markdown]
# ## Complex plots

# Many complex plots exists out there and we can't show everything.
# For this beginner course, the only one worth showing is the **parallel coordinate**
# plot, which allows to show all the dimensions of the data at the same time:

# %% tags=["hide_code"]
px.parallel_coordinates(
    data, color="Cylinders", color_continuous_scale="turbo"
).update_coloraxes(showscale=False)

# %% [markdown]
## Exercises

# **Exercise 1**: Pick one bad visualization from [tumblr.com/badvisualisations](https://www.tumblr.com/badvisualisations)
# and explain how you would do the visualization better.
#
# **Exercise 2**: Explain why the data visualization below made by Minart in 1869 is
# known as "*the best statistical graphic ever drawn*":
# ![Minard's Map](files/Minard.png)
