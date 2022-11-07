# Plots

## Plots per type

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
    "description": "A scatterplot showing horsepower and miles per gallons for various cars.",
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
    "description": "A scatterplot showing horsepower and miles per gallons for various cars.",
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
    "description": "A scatterplot showing horsepower and miles per gallons for various cars.",
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
    "description": "A scatterplot showing horsepower and miles per gallons for various cars.",
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
    "description": "A scatterplot showing horsepower and miles per gallons for various cars.",
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

This plot is saturated due to **overplotting**, so we are not able to perceive the relationship between the new columns and the other. Also it's **too complex**: we are trying to show 4 data columns at once, it's often difficult to represent more than 3 information at once in an understandable way.

### Strip

Simple chart, not often used, the strip plot uses vertical lines instead of points to display information.

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
    "mark": "tick",
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
</table>
</figure>

We can also use reundancy to improve the readability of the chart:

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
    "mark": "tick",
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
</table>
</figure>

### Bar

Bar plots allow to use the size as a visual variable to encode data.

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
        "y": {"field": "Cylinders", "aggregate": "count"}
    }
}
```
</th>
</tr>
<tr><td>Position (x)</td><td>Horsepower (Ratio) binned</td></tr>
<tr><td>Position (y)</td><td>Count (aggregate for each bin)</td></tr>
</table>
</figure>

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
        "y": {"field": "Cylinders", "aggregate": "count"},
        "color": {"field": "Cylinders", "type": "ordinal", "scale": {"scheme": "turbo"}}
    }
}
```
</th>
</tr>
<tr><td>Position (x)</td><td>Horsepower (Ratio) binned</td></tr>
<tr><td>Position (y)</td><td>Count (aggregate for each bin)</td></tr>
</table>
</figure>

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
    "height": 90,
    "data": {"url": "https://vega.github.io/vega-lite/data/cars.json"},
    "mark": "bar",
    "encoding": {
        "x": {"field": "Horsepower", "type": "quantitative", "bin": true},
        "y": {"field": "Cylinders", "aggregate": "count"},
        "color": {"field": "Cylinders", "type": "ordinal", "scale": {"scheme": "turbo"}},
    "row": {"field": "Cylinders"}
    }
}
```
</th>
</tr>
<tr><td>Position (x)</td><td>Horsepower (Ratio) binned</td></tr>
<tr><td>Position (y)</td><td>Count (aggregate for each bin)</td></tr>
</table>
</figure>

### Line

In certain cases, the scatter plot is not really relevant, as for the plot below, which shows Google's stock price as a function of time. Can you guess what's wrong with this chart?

<figure markdown>
<table>
<tr>
<th>Visual variable</th>
<th>Data</th>
<th rowspan=10>
```vegalite
{
    "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
    "description": "Google's stock price over time.",
    "width": 200,
    "data": {"url": "https://vega.github.io/vega-lite/data/stocks.csv"},
    "transform": [{"filter": "datum.symbol==='GOOG'"}],
    "mark": {"type": "point", "filled": true},
    "encoding": {
        "x": {"field": "date", "type": "temporal"},
        "y": {"field": "price", "type": "quantitative"}
    }
}
```
</th>
</tr>
<tr><td>Position (x)</td><td>Date (Ratio)</td></tr>
<tr><td>Position (y)</td><td>Stock price (Ratio)</td></tr>
</table>
</figure>

The data encoded in position X is a date, so there is an order relationship between the points which aren't able to visualize with only points. This data needs to be plotted using a [line](#line).

<figure markdown>
<table>
<tr>
<th>Visual variable</th>
<th>Data</th>
<th rowspan=10>
```vegalite
{
    "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
    "description": "Google's stock price over time.",
    "width": 200,
    "data": {"url": "https://vega.github.io/vega-lite/data/stocks.csv"},
    "transform": [{"filter": "datum.symbol==='GOOG'"}],
    "mark": {"type": "line", "point": true},
    "encoding": {
        "x": {"field": "date", "type": "temporal"},
        "y": {"field": "price", "type": "quantitative"}
    }
}
```
</th>
</tr>
<tr><td>Position (x)</td><td>Date (Ratio)</td></tr>
<tr><td>Position (y)</td><td>Stock price (Ratio)</td></tr>
<tr><td>Size (of each line segment)</td><td rowspan=2>Stock price variation (Interval)</td></tr>
<tr><td>Orientation (of each line segment)</td></tr>
</table>
</figure>

...

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
    "mark": {"type": "line"},
    "encoding": {
        "x": {"field": "Year", "type": "temporal"},
        "y": {"aggregate": "mean", "field": "Miles_per_Gallon", "type": "quantitative"},
        "color": {"field": "Cylinders", "type": "nominal"},
        "shape": {"field": "Cylinders", "type": "nominal"}
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

### Area

<figure markdown>
```vegalite
{
  "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
  "width": 300,
  "height": 200,
  "data": {"url": "https://vega.github.io/vega-lite/data/unemployment-across-industries.json"},
  "mark": "area",
  "encoding": {
    "x": {
      "timeUnit": "yearmonth", "field": "date",
      "axis": {"format": "%Y"}
    },
    "y": {
      "aggregate": "sum", "field": "count",
      "title": "count"
    }
  }
}
```
</figure>

### Histogram

<figure markdown>
```vegalite
{
    "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
    "width": 200,
    "data": {"url": "https://vega.github.io/vega-lite/data/movies.json"},
    "mark": "bar",
    "encoding": {
        "x": {
        "bin": true,
        "field": "IMDB Rating"
        },
        "y": {"aggregate": "count"}
    }
}
```
</figure>

### Distribution

<figure markdown>
```vegalite
{
    "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
    "data": {
        "url": "https://vega.github.io/vega-lite/data/movies.json"
    },
    "width": 200,
    "transform":[{
        "density": "IMDB Rating",
        "bandwidth": 0.3
    }],
    "mark": "area",
    "encoding": {
        "x": {
        "field": "value",
        "title": "IMDB Rating",
        "type": "quantitative"
        },
        "y": {
        "field": "density",
        "type": "quantitative"
        }
    }
}
```
</figure>

### 2D-histogram: scatter

<figure markdown>
```vegalite
{
    "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
    "width": 200,
    "data": {"url": "https://vega.github.io/vega-lite/data/movies.json"},
    "mark": "circle",
    "encoding": {
        "x": {
        "bin": {"maxbins": 10},
        "field": "IMDB Rating"
        },
        "y": {
        "bin": {"maxbins": 10},
        "field": "Rotten Tomatoes Rating"
        },
        "size": {"aggregate": "count"}
    }
}

```
</figure>

### 2D-histogram: heatmap

<figure markdown>
```vegalite
{
    "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
    "width": 200,
    "data": {"url": "https://vega.github.io/vega-lite/data/movies.json"},
    "transform": [{
        "filter": {"and": [
        {"field": "IMDB Rating", "valid": true},
        {"field": "Rotten Tomatoes Rating", "valid": true}
        ]}
    }],
    "mark": "rect",
    "width": 300,
    "height": 200,
    "encoding": {
        "x": {
        "bin": {"maxbins":60},
        "field": "IMDB Rating",
        "type": "quantitative"
        },
        "y": {
        "bin": {"maxbins": 40},
        "field": "Rotten Tomatoes Rating",
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
</figure>

## Plots per use case

Mapping variables to visual encoding according to their type (ex: of Altair) 

## Complex plots for 

### Parallel coordinate

### Pair plot / scatter matrix

## Plots for specific data

maps, pictures, volumetry, trees, sankey-diagram, ...

### 3D plot

### Tree

### Maps

### Sankey diagram
