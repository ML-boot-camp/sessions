# Plots

## Points based plots

### Scatter

Scatter plot is the most basic plot to encode any data using **points** and their properties. Location (X, Y) are 2 properties which are able to represent any measurement type.

Below, two ratio variables are represented (notice how the scale shows the level zero) thanks to position:

<figure markdown>
<table>
<tr>
<th>Visual variable</th>
<th>Data</th>
<th rowspan=10>
```vegalite
{
    "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
    "width": 200,
    "data": {"url": "https://vega.github.io/vega-lite/data/cars.json"},
    "mark": {"type": "point", "filled": true},
    "encoding": {
        "x": {"field": "Horsepower", "type": "quantitative"},
        "y": {"field": "Miles_per_Gallon", "type": "quantitative"}
    }
}
```
</th>
</tr>
<tr><td>Position (x)</td><td>Horsepower (Ratio)</td></tr>
<tr><td>Position (y)</td><td>Miles per gallon (Ratio)</td></tr>
</table>
</figure>

What we learn from this plot is that there might be a quadratic relationship between $X$ and $Y$ like: $Y = a X^{2} + b X + c$.

Let's try to learn something by adding more information on this chart, mapping another data column on visual properties:

<figure markdown>
<table>
<tr>
<th>Visual variable</th>
<th>Data</th>
<th rowspan=5>
```vegalite
{
    "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
    "width": 200,
    "data": {"url": "https://vega.github.io/vega-lite/data/cars.json"},
    "mark": {"type": "point", "filled": true},
    "encoding": {
        "x": {"field": "Horsepower", "type": "quantitative"},
        "y": {"field": "Miles_per_Gallon", "type": "quantitative"},
        "color": {"field": "Cylinders", "type": "ordinal", "scale": {"scheme": "turbo"}}
    }
}
```
</th>
</tr>
<tr><td>Position (x)</td><td>Horsepower (Ratio)</td></tr>
<tr><td>Position (y)</td><td>Miles per gallon (Ratio)</td></tr>
<tr><td>Color hue</td><td>Cylinders (Ordinal)</td></tr>
</table>
</figure>

We can improve this chart by using **redundancy**, i.e. several visual variables used to represent only a single column of data:

<figure markdown>
<table>
<tr>
<th>Visual variable</th>
<th>Data</th>
<th rowspan=5>
```vegalite
{
    "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
    "width": 200,
    "data": {"url": "https://vega.github.io/vega-lite/data/cars.json"},
    "mark": {"type": "point", "filled": true},
    "encoding": {
        "x": {"field": "Horsepower", "type": "quantitative"},
        "y": {"field": "Miles_per_Gallon", "type": "quantitative"},
        "color": {"field": "Cylinders", "type": "ordinal", "scale": {"scheme": "turbo"}},
        "shape": {"field": "Cylinders", "type": "ordinal"}
    }
}
```
</th>
</tr>
<tr><td>Position (x)</td><td>Horsepower (Ratio)</td></tr>
<tr><td>Position (y)</td><td>Miles per gallon (Ratio)</td></tr>
<tr><td>Color hue</td><td rowspan=2>Cylinders (Ordinal)</td></tr>
<tr><td>Shape</td></tr>
</table>
</figure>

We understand that there are several categories of cars, defined by their number of cylinders and that they differ wildly in their use cases: some cars ave a low consumption but a low power - maybe to drive long distances - while others have a high power but a high consumption - maybe to do sports racing. 

There is a slight issue of **overplotting**: the information is saturated due to elements being on top of each other. One solution is to use a bit of transparency.

<figure markdown>
<table>
<tr>
<th>Visual variable</th>
<th>Data</th>
<th rowspan=10>
```vegalite
{
    "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
    "width": 200,
    "data": {"url": "https://vega.github.io/vega-lite/data/cars.json"},
    "mark": {"type": "point", "filled": true, "opacity": 0.25},
    "encoding": {
        "x": {"field": "Horsepower", "type": "quantitative"},
        "y": {"field": "Miles_per_Gallon", "type": "quantitative"},
        "color": {"field": "Cylinders", "type": "ordinal", "scale": {"scheme": "turbo"}},
        "shape": {"field": "Cylinders", "type": "ordinal"}
    }
}
```
</th>
</tr>
<tr><td>Position (x)</td><td>Horsepower (Ratio)</td></tr>
<tr><td>Position (y)</td><td>Miles per gallon (Ratio)</td></tr>
<tr><td>Color hue</td><td rowspan=2>Cylinders (Ordinal)</td></tr>
<tr><td>Shape</td></tr>
<tr><td>Opacity</td><td>25%</td></tr>
</table>
</figure>

We now see that most cars are in the *long-distance driving* region, with low consumption & low power.

Can we learn something by adding even more information ?

Below we try to map another data column on a supplementary visual variable:

<figure markdown>
<table>
<tr>
<th>Visual variable</th>
<th>Data</th>
<th rowspan=10>
```vegalite
{
    "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
    "width": 200,
    "data": {"url": "https://vega.github.io/vega-lite/data/cars.json"},
    "mark": {"type": "point", "filled": true, "opacity": 0.25},
    "encoding": {
        "x": {"field": "Horsepower", "type": "quantitative"},
        "y": {"field": "Miles_per_Gallon", "type": "quantitative"},
        "color": {"field": "Cylinders", "type": "ordinal", "scale": {"scheme": "turbo"}},
        "shape": {"field": "Cylinders", "type": "ordinal"},
        "size": {"field": "Weight_in_lbs", "type": "quantitative"}
    }
}
```
</th>
</tr>
<tr><td>Position (x)</td><td>Horsepower (Ratio)</td></tr>
<tr><td>Position (y)</td><td>Miles per gallon (Ratio)</td></tr>
<tr><td>Color hue</td><td rowspan=2>Cylinders (Ordinal)</td></tr>
<tr><td>Shape</td></tr>
<tr><td>Opacity</td><td>25%</td></tr>
<tr><td>Size</td><td>Weights in lbs (Ratio)</td></tr>
</table>
</figure>

The plot is barely readable. 😕

It is saturated due to **overplotting**, so we are not able to perceive the relationship between the new columns and the other. Also it's **too complex**: we are trying to show 4 data columns at once, it's often difficult to represent more than 3 information at once in an understandable way.

### Strip

If you'd like to visualize the relationship between a **discrete** variable (nominal or ordinal) and a quantitative variable (interval or ratio), you can try to use a **scatter** plot:

<figure markdown>
<table>
<tr>
<th>Visual variable</th>
<th>Data</th>
<th rowspan=10>
```vegalite
{
    "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
    "width": 200,
    "data": {"url": "https://vega.github.io/vega-lite/data/cars.json"},
    "mark": {"type": "point", "filled": true, "opacity": 0.25},
    "encoding": {
        "x": {"field": "Horsepower", "type": "quantitative"},
        "y": {"field": "Cylinders", "type": "ordinal"}
    }
}
```
</th>
</tr>
<tr><td>Position (x)</td><td>Horsepower (Ratio)</td></tr>
<tr><td>Position (y)</td><td>Cylinders (Ordinal)</td></tr>
<tr><td>Opacity</td><td>25%</td></tr>
</table>
</figure>

But the result is often barely readable due to **overplotting**, even if we use transparency, due to points being drawn on a few lines (1 for each discrete value of the data).

The **strip** plot is a simple chart composed of **vertical lines instead of points** to display information:

<figure markdown>
<table>
<tr>
<th>Visual variable</th>
<th>Data</th>
<th rowspan=10>
```vegalite
{
    "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
    "width": 200,
    "data": {"url": "https://vega.github.io/vega-lite/data/cars.json"},
    "mark": {"type": "tick", "opacity": 0.25},
    "encoding": {
        "x": {"field": "Horsepower", "type": "quantitative"},
        "y": {"field": "Cylinders", "type": "ordinal"}
    }
}
```
</th>
</tr>
<tr><td>Position (x)</td><td>Horsepower (Ratio)</td></tr>
<tr><td>Position (y)</td><td>Cylinders (Ordinal)</td></tr>
<tr><td>Opacity</td><td>25%</td></tr>
</table>
</figure>

It's a bit more readable than the scatter plot and very compact, but It is rarely used. For teaching purposes, it allows to understand what how you can encode a mix of discrete and quantitative data on position as a visual parameter: the trick is to draw lines instead of points.  

Note that we can also use redundancy to improve the readability of the chart:

<figure markdown>
<table>
<tr>
<th>Visual variable</th>
<th>Data</th>
<th rowspan=10>
```vegalite
{
    "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
    "description": "Shows the relationship between horsepower and the number of cylinders using tick marks.",
    "width": 200,
    "data": {"url": "https://vega.github.io/vega-lite/data/cars.json"},
    "mark": {"type": "tick", "opacity": 0.25},
    "encoding": {
        "x": {"field": "Horsepower", "type": "quantitative"},
        "y": {"field": "Cylinders", "type": "ordinal"},
        "color": {"field": "Cylinders", "type": "ordinal", "scale": {"scheme": "turbo"}}
    }
}
```
</th>
</tr>
<tr><td>Position (x)</td><td>Horsepower (Ratio)</td></tr>
<tr><td>Position (y)</td><td rowspan=2>Cylinders (Ordinal)</td></tr>
<tr><td>Color</td></tr>
<tr><td>Opacity</td><td>25%</td></tr>
</table>
</figure>

## Rectangle based plots

### Bar & histogram

**Bar** plots use the bar **size** a visual variable to encode data. It is good to represent a **quantity**, so it is used by default in **histograms**:

<figure markdown>
<table>
<tr>
<th>Visual variable</th>
<th>Data</th>
<th rowspan=10>
```vegalite
{
    "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
    "width": 200,
    "data": {"url": "https://vega.github.io/vega-lite/data/cars.json"},
    "mark": "bar",
    "encoding": {
        "x": {"field": "Horsepower", "type": "quantitative", "bin": true},
        "y": {"field": "Cylinders", "aggregate": "count"}
    }
}
```
</th>
</tr>
<tr><td>Position (x)</td><td>Horsepower (Ratio) binned</td></tr>
<tr><td>Size</td><td>Count (aggregate for each bin)</td></tr>
</table>
</figure>

You can try also to encode a discrete variable on color as a secondary visual variable, which is called a **stacked bar** chart:

<figure markdown>
<table>
<tr>
<th>Visual variable</th>
<th>Data</th>
<th rowspan=10>
```vegalite
{
    "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
    "description": "Shows the relationship between horsepower and the number of cylinders using tick marks.",
    "width": 200,
    "data": {"url": "https://vega.github.io/vega-lite/data/cars.json"},
    "mark": "bar",
    "encoding": {
        "x": {"field": "Horsepower", "type": "quantitative", "bin": true},
        "y": {"field": "Cylinders", "aggregate": "count", "title": "Count"},
        "color": {"field": "Cylinders", "type": "ordinal", "scale": {"scheme": "turbo"}}
    }
}
```
</th>
</tr>
<tr><td>Position (x)</td><td>Horsepower binned (Ordinal)</td></tr>
<tr><td>Size</td><td>Count (for each bin)</td></tr>
<tr><td>Color</td><td>Cylinders (Ordinal)</td></tr>
</table>
</figure>

It gives an idea of the distribution of values in each class of the discrete data, but it's difficult to do a precise assessment: you can't compare the distributions in a stacked bar chart. The overall distribution is still understandable, though.

To get a precise view of each distribution and to compare them, it's better to separate them using the position as a visual variable: 

<figure markdown>
<table>
<tr>
<th>Visual variable</th>
<th>Data</th>
<th rowspan=10>
```vegalite
{
    "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
    "description": "Shows the relationship between horsepower and the number of cylinders using tick marks.",
    "width": 200,
    "height": 50,
    "data": {"url": "https://vega.github.io/vega-lite/data/cars.json"},
    "mark": "bar",
    "encoding": {
        "x": {"field": "Horsepower", "type": "quantitative", "bin": true},
        "y": {"field": "Cylinders", "aggregate": "count", "title": "Count"},
        "color": {"field": "Cylinders", "type": "ordinal", "scale": {"scheme": "turbo"}},
    "row": {"field": "Cylinders"}
    }
}
```
</th>
</tr>
<tr><td>Position (x)</td><td>Horsepower binned (Ordinal)</td></tr>
<tr><td>Size</td><td>Count (for each bin)</td></tr>
<tr><td>Color</td><td rowspan=2>Cylinders (Ordinal)</td></tr>
<tr><td>Position (y)</td></tr>
</table>
</figure>

But you lose the representation of the overall distribution.

### Line

In certain cases, the scatter plot is not really relevant, as for the plot below, which shows the mean consumption for all car released a given year time, and breakdown by number of cylinders. Can you guess what's wrong with this chart?

<figure markdown>
<table>
<tr>
<th>Visual variable</th>
<th>Data</th>
<th rowspan=5>
```vegalite
{
    "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
    "description": "A scatterplot showing horsepower and miles per gallons for various cars.",
    "width": 200,
    "data": {"url": "https://vega.github.io/vega-lite/data/cars.json"},
    "mark": {"type": "point", "filled": true},
    "encoding": {
        "x": {"field": "Year", "type": "temporal"},
        "y": {"aggregate": "mean", "field": "Horsepower", "type": "quantitative"},
        "color": {"field": "Cylinders", "type": "ordinal", "scale": {"scheme": "turbo"}},
        "shape": {"field": "Cylinders", "type": "nominal"}
    }
}
```
</th>
</tr>
<tr><td>Position (x)</td><td>Horsepower (Ratio)</td></tr>
<tr><td>Position (y)</td><td>Year (Ordinal)</td></tr>
<tr><td>Color hue</td><td rowspan=2>Cylinders (Ordinal)</td></tr>
<tr><td>Shape</td></tr>
</table>
</figure>

The data encoded in position X is a date, which is an **ordinal** variable, so there is an order relationship (a.k.a temporal relationship) between the points which isn't shown using only points. As a result, the chart is messy and we can't understand easily what are the trends of the variations.

This **temporal relationship** between data points can be represented using a **line** chart. A line chart uses small segments which have 2 additional visual variables - **size & slope** - which are powerful to perceive a **variation rate**.

<figure markdown>
<table>
<tr>
<th>Visual variable</th>
<th>Data</th>
<th rowspan=5>
```vegalite
{
    "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
    "description": "A scatterplot showing horsepower and miles per gallons for various cars.",
    "width": 200,
    "data": {"url": "https://vega.github.io/vega-lite/data/cars.json"},
    "mark": {"type": "line", "point": true},
    "encoding": {
        "x": {"field": "Year", "type": "temporal"},
        "y": {"aggregate": "mean", "field": "Horsepower", "type": "quantitative"},
        "color": {"field": "Cylinders", "type": "ordinal", "scale": {"scheme": "turbo"}}
    }
}
```
</th>
</tr>
<tr><td>Position (x)</td><td>Horsepower (Ratio)</td></tr>
<tr><td>Position (y)</td><td>Year (Ordinal)</td></tr>
<tr><td>Color hue</td><td>Cylinders (Ordinal)</td></tr>
<tr><td>Size (of segments)</td><td rowspan=2>Horsepower variation (Interval)</td></tr>
<tr><td>Slope (of segments)</td></tr>
</table>
</figure>

This line plot allows to analyze the trends: along the years the very powerful cars have been less popular due to their fuel consumption and the mean power of new models declined. This has been especially true for 8-cylinders cars.

We can refine this chart by encoding the count of cars for each year and cylinder class, as we made a mean aggregate. This is a ratio data which can be shown using the size:

<figure markdown>
<table>
<tr>
<th>Visual variable</th>
<th>Data</th>
<th rowspan=5>
```vegalite
{
    "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
    "description": "A scatterplot showing horsepower and miles per gallons for various cars.",
    "width": 200,
    "data": {"url": "https://vega.github.io/vega-lite/data/cars.json"},
    "mark": {"type": "line", "point": true},
    "encoding": {
        "x": {"field": "Year", "type": "temporal"},
        "y": {"aggregate": "mean", "field": "Horsepower", "type": "quantitative"},
        "size": {"aggregate": "count", "field": "Miles_per_Gallon", "type": "quantitative"},
        "color": {"field": "Cylinders", "type": "ordinal", "scale": {"scheme": "turbo"}}
    }
}
```
</th>
</tr>
<tr><td>Position (x)</td><td>Horsepower (Ratio)</td></tr>
<tr><td>Position (y)</td><td>Year (Ordinal)</td></tr>
<tr><td>Color hue</td><td>Cylinders (Ordinal)</td></tr>
<tr><td>Size (of points)</td><td>Count</td></tr>
<tr><td>Size (of segments)</td><td rowspan=2>Horsepower variation (Interval)</td></tr>
<tr><td>Slope (of segments)</td></tr>
</table>
</figure>

This chart allows to tell the whole story of the car industry in the 70s and the 80s: at first, *muscle cars* were very popular due to their huge power and their 8 cylinders, but the oil shocks in the 70s led people to prefer more fuel-savvy models with 4 cylinders.

![](files/deathproof.jpg){width=46.5%}
<span style="font-size: 100pt">➜</span>
![](files/ford_escort.jpg){width=33%}

At the end, the industry tried to design less powerful cars but with still with 8 cylinders, in an attempt to lure the consumers into thinking that they were still buying *muscle cars* (but more fuel-savvy).

### Area & distribution

Area charts are line charts, but filled with color. As bar charts, they are powerful to represent quantities.

It can also replace an histogram made on a binned quantitative variable, by using kernel smoothing (which is a type of weighted moving average).

<figure markdown>
<table>
<tr>
<th>Visual variable</th>
<th>Data</th>
<th rowspan=10>
```vegalite
{
    "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
    "description": "Shows the relationship between horsepower and the number of cylinders using tick marks.",
    "width": 200,
    "data": {"url": "https://vega.github.io/vega-lite/data/cars.json"},
    "transform":[{
        "density": "Horsepower",
        "counts": true,
        "bandwidth": 5
    }],
    "mark": "area",
    "encoding": {
        "x": {"field": "value", "type": "quantitative"},
        "y": {"field": "density", "type": "quantitative", "title": "Count (smoothed)"}
    }
}
```
</th>
</tr>
<tr><td>Position (x)</td><td>Horsepower (Ratio)</td></tr>
<tr><td>Position (y)</td><td>Density (Ratio)</td></tr>
</table>
</figure>

Like with histograms, we can also encode an ordinal data on the color as a visual variable:

<figure markdown>
<table>
<tr>
<th>Visual variable</th>
<th>Data</th>
<th rowspan=10>
```vegalite
{
    "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
    "description": "Shows the relationship between horsepower and the number of cylinders using tick marks.",
    "width": 200,
    "data": {"url": "https://vega.github.io/vega-lite/data/cars.json"},
    "transform":[{
        "density": "Horsepower",
        "groupby": ["Cylinders"],
        "counts": true,
        "steps": 100,
        "extent": [40, 240],
        "bandwidth": 5
    }],
    "mark": "area",
    "encoding": {
        "x": {"field": "value", "type": "quantitative"},
        "y": {"field": "density", "type": "quantitative", "title": "Count (smoothed)", "stack": "zero"},
        "color": {"field": "Cylinders", "type": "ordinal", "scale": {"scheme": "turbo"}}
    }
}
```
</th>
</tr>
<tr><td>Position (x)</td><td>Horsepower (Ratio)</td></tr>
<tr><td>Position (y)</td><td>Density (Ratio)</td></tr>
<tr><td>Color</td><td>Cylinders (Ordinal)</td></tr>
</table>
</figure>

### 2D-histogram

Finally, if have too much overplotting with scatter plots, it's possible to make 2D-histograms. The data is binned across 2 quantitative dimensions, which are transformed intro ordinal data. The count aggregate can then be encoded into visual variables, such as the size or the color.

When the count is encoded on the **size** of the points, it's a **bubble** plot:

<figure markdown>
<table>
<tr>
<th>Visual variable</th>
<th>Data</th>
<th rowspan=10>
```vegalite
{
    "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
    "width": 200,
    "data": {"url": "https://vega.github.io/vega-lite/data/cars.json"},
    "transform": [{
        "filter": {"and": [
        {"field": "Horsepower", "valid": true},
        {"field": "Miles_per_Gallon", "valid": true}
        ]}
    }],
    "mark": "circle",
    "encoding": {
        "x": {
        "bin": {"maxbins": 32},
        "field": "Horsepower",
        "scale": {"zero": true},
        "type": "quantitative"
        },
        "y": {
        "bin": {"maxbins": 32},
        "field": "Miles_per_Gallon",
        "scale": {"zero": true},
        "type": "quantitative"
        },
        "size": {
        "aggregate": "count",
        "type": "quantitative"
        }
    },
    "config": {
        "view": {
        "stroke": "transparent"
        }
    }
}
```
</th>
</tr>
<tr><td>Position (x)</td><td>Horsepower binned (Ordinal)</td></tr>
<tr><td>Position (y)</td><td>Miles per gallon binned (Ordinal)</td></tr>
<tr><td>Size</td><td>Count (Ratio)</td></tr>
</table>
</figure>

Which you can also improve using **redundancy**:

<figure markdown>
<table>
<tr>
<th>Visual variable</th>
<th>Data</th>
<th rowspan=10>
```vegalite
{
    "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
    "width": 200,
    "data": {"url": "https://vega.github.io/vega-lite/data/cars.json"},
    "transform": [{
        "filter": {"and": [
        {"field": "Horsepower", "valid": true},
        {"field": "Miles_per_Gallon", "valid": true}
        ]}
    }],
    "mark": "circle",
    "encoding": {
        "x": {
        "bin": {"maxbins": 32},
        "field": "Horsepower",
        "scale": {"zero": true},
        "type": "quantitative"
        },
        "y": {
        "bin": {"maxbins": 32},
        "field": "Miles_per_Gallon",
        "scale": {"zero": true},
        "type": "quantitative"
        },
        "size": {
        "aggregate": "count",
        "type": "quantitative"
        },
        "color": {
        "aggregate": "count",
        "type": "quantitative",
        "scale": {"scheme": "yellowgreenblue"}
        }
    },
    "config": {
        "view": {
        "stroke": "transparent"
        }
    }
}
```
</th>
</tr>
<tr><td>Position (x)</td><td>Horsepower binned (Ordinal)</td></tr>
<tr><td>Position (y)</td><td>Miles per gallon binned (Ordinal)</td></tr>
<tr><td>Size</td><td rowspan=2>Count (Ratio)</td></tr>
<tr><td>Color</td></tr>
</table>
</figure>

When the count is encoded on the **color** of the points, it's a **heatmap** plot

<figure markdown>
<table>
<tr>
<th>Visual variable</th>
<th>Data</th>
<th rowspan=10>
```vegalite
{
    "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
    "width": 200,
    "data": {"url": "https://vega.github.io/vega-lite/data/cars.json"},
    "transform": [{
        "filter": {"and": [
        {"field": "Horsepower", "valid": true},
        {"field": "Miles_per_Gallon", "valid": true}
        ]}
    }],
    "mark": "rect",
    "encoding": {
        "x": {
        "bin": {"maxbins": 32},
        "field": "Horsepower",
        "scale": {"zero": true},
        "type": "quantitative"
        },
        "y": {
        "bin": {"maxbins": 32},
        "field": "Miles_per_Gallon",
        "scale": {"zero": true},
        "type": "quantitative"
        },
        "color": {
        "aggregate": "count",
        "type": "quantitative"
        }
    },
    "config": {
        "view": {
        "stroke": "transparent"
        }
    }
}
```
</th>
</tr>
<tr><td>Position (x)</td><td>Horsepower binned (Ordinal)</td></tr>
<tr><td>Position (y)</td><td>Miles per gallon binned (Ordinal)</td></tr>
<tr><td>Color</td><td>Count (Ratio)</td></tr>
</table>
</figure>

## Complex plots: parallel coordinate

Many complex plots exists out there and we can't show everything.

For this beginner course, the only one worth showing is the parallell coordinate plot, which allows to show all the dimensions of the data at the same time:


```vegalite
{
    "$schema": "https://vega.github.io/schema/vega/v5.json",
    "description": "Parallel coordinates plot showing 7 dimensions of automobile statistics.",
    "width": 700,
    "height": 400,
    "padding": 5,
    "config": {
        "axisY": {
            "titleX": -2,
            "titleY": 410,
            "titleAngle": 0,
            "titleAlign": "right",
            "titleBaseline": "top"
        }
    },
    "data": [
        {
            "name": "cars",
            "url": "https://vega.github.io/vega-lite/data/cars.json",
            "format": {
                "type": "json",
                "parse": {"Year": "date:%Y-%m-%d"}
            },
            "transform": [
                { "type": "filter", "expr": "datum.Horsepower && datum.Miles_per_Gallon" },
                { "type": "formula", "as": "Year",
                "expr": "isNumber(datum.year) ? datum.year : year(datum.Year)" }
            ]
        },
        {
            "name": "fields",
            "values": [
                "Cylinders",
                "Displacement",
                "Weight_in_lbs",
                "Horsepower",
                "Acceleration",
                "Miles_per_Gallon",
                "Year"
            ]
        }
    ],
    "scales": [
        {
            "name": "ord", "type": "point",
            "range": "width", "round": true,
            "domain": {"data": "fields", "field": "data"}
        },
        {
            "name": "Cylinders", "type": "linear",
            "range": "height", "zero": false, "nice": true,
            "domain": {"data": "cars", "field": "Cylinders"}
        },
        {
            "name": "Displacement", "type": "linear",
            "range": "height", "zero": false, "nice": true,
            "domain": {"data": "cars", "field": "Displacement"}
        },
        {
            "name": "Weight_in_lbs", "type": "linear",
            "range": "height", "zero": false, "nice": true,
            "domain": {"data": "cars", "field": "Weight_in_lbs"}
        },
        {
            "name": "Horsepower", "type": "linear",
            "range": "height", "zero": false, "nice": true,
            "domain": {"data": "cars", "field": "Horsepower"}
        },
        {
            "name": "Acceleration", "type": "linear",
            "range": "height", "zero": false, "nice": true,
            "domain": {"data": "cars", "field": "Acceleration"}
        },
        {
            "name": "Miles_per_Gallon", "type": "linear",
            "range": "height", "zero": false, "nice": true,
            "domain": {"data": "cars", "field": "Miles_per_Gallon"}
        },
        {
            "name": "Year", "type": "linear",
            "range": "height", "zero": false, "nice": true,
            "domain": {"data": "cars", "field": "Year"}
        }
    ],
    "axes": [
        {
            "orient": "left", "zindex": 1,
            "scale": "Cylinders", "title": "Cylinders",
            "offset": {"scale": "ord", "value": "Cylinders", "mult": -1}
        },
        {
            "orient": "left", "zindex": 1,
            "scale": "Displacement", "title": "Displacement",
            "offset": {"scale": "ord", "value": "Displacement", "mult": -1}
        },
        {
            "orient": "left", "zindex": 1,
            "scale": "Weight_in_lbs", "title": "Weight_in_lbs",
            "offset": {"scale": "ord", "value": "Weight_in_lbs", "mult": -1}
        },
        {
            "orient": "left", "zindex": 1,
            "scale": "Horsepower", "title": "Horsepower",
            "offset": {"scale": "ord", "value": "Horsepower", "mult": -1}
        },
        {
            "orient": "left", "zindex": 1,
            "scale": "Acceleration", "title": "Acceleration",
            "offset": {"scale": "ord", "value": "Acceleration", "mult": -1}
        },
        {
            "orient": "left", "zindex": 1,
            "scale": "Miles_per_Gallon", "title": "Miles_per_Gallon",
            "offset": {"scale": "ord", "value": "Miles_per_Gallon", "mult": -1}
        },
        {
            "orient": "left", "zindex": 1,
            "scale": "Year", "title": "Year", "format": "d",
            "offset": {"scale": "ord", "value": "Year", "mult": -1}
        }
    ],
    "marks": [
        {
            "type": "group",
            "from": {"data": "cars"},
            "marks": [
                {
                    "type": "line",
                    "from": {"data": "fields"},
                    "encode": {
                        "enter": {
                            "x": {"scale": "ord", "field": "data"},
                            "y": {
                                "scale": {"datum": "data"},
                                "field": {"parent": {"datum": "data"}}
                            },
                            "stroke": {"value": "steelblue"},
                            "strokeWidth": {"value": 1.01},
                            "strokeOpacity": {"value": 0.3}
                        }
                    }
                }
            ]
        }
    ]
}
```

