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

Can we learn something by adding more information ?

Other visual variables - such as size, shape, color - can be used to visualize other data. In the example below, `size` represents the `number of cylinders` (an ordinal variable) and `color value` represents the `weight in lbs` (a ratio variable) of the engine:


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
        "color": {"field": "Weight_in_lbs", "type": "quantitative"},
        "size": {"field": "Cylinders", "type": "quantitative"}
    }
}
```
</th>
</tr>
<tr><td>Position (x)</td><td>Horsepower (Ratio)</td></tr>
<tr><td>Position (y)</td><td>Miles per gallon (Ratio)</td></tr>
<tr><td>Color value</td><td>Weight in lbs (Ratio)</td></tr>
<tr><td>Size</td><td>Cylinders (Ratio)</td></tr>
</table>
</figure>

As our perception of `color value` is not very precise, we notice that there *may* be a relationship between `weight in lbs` and the first 2 data represented - `miles per gallon` & `horsepower` - but it's unclear which one.

Also as this plot is saturated due to **overplotting**, we are not able to perceive the `number of cylinders`.

We can try to improve this chart by **reducing** the number of information plotted - let's remove the weight - and use **redundancy**, i.e. several variables such as `color hue` and `shape` represent only one data the `number of cylinders`:


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
        "color": {"field": "Cylinders", "type": "nominal"},
        "shape": {"field": "Cylinders", "type": "nominal"}
    }
}
```
</th>
</tr>
<tr><td>Position (x)</td><td>Horsepower (Ratio)</td></tr>
<tr><td>Position (y)</td><td>Miles per gallon (Ratio)</td></tr>
<tr><td>Color hue</td><td rowspan=2>Cylinders (Nominal)</td></tr>
<tr><td>Shape</td></tr>
</table>
</figure>


The relationship between `number of cylinders` and the first 2 data represented - `miles per gallon` & `horsepower` - is much clearer: there are thresholds for which all.

There is still an issue with overplotting. One solution is to use a bit of transparency.

<figure markdown>
<table>
<tr>
<th>Visual variable</th>
<th>Data</th>
<th rowspan=6>
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
        "color": {"field": "Cylinders", "type": "nominal"},
        "shape": {"field": "Cylinders", "type": "nominal"}
    }
}
```
</th>
</tr>
<tr><td>Position (x)</td><td>Horsepower (Ratio)</td></tr>
<tr><td>Position (y)</td><td>Miles per gallon (Ratio)</td></tr>
<tr><td>Color hue</td><td rowspan=2>Cylinders (Nominal)</td></tr>
<tr><td>Shape</td></tr>
<tr><td>Opacity</td><td>25%</td></tr>
</table>
</figure>

### Strip

<figure markdown>
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
</figure>

### Bar

<figure markdown>
```vegalite
{
    "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
    "description": "A simple bar chart with embedded data.",
    "width": 200,
    "data": {
        "values": [
        {"a": "A", "b": 28}, {"a": "B", "b": 55}, {"a": "C", "b": 43},
        {"a": "D", "b": 91}, {"a": "E", "b": 81}, {"a": "F", "b": 53},
        {"a": "G", "b": 19}, {"a": "H", "b": 87}, {"a": "I", "b": 52}
        ]
    },
    "mark": "bar",
    "encoding": {
        "x": {"field": "a", "type": "nominal", "axis": {"labelAngle": 0}},
        "y": {"field": "b", "type": "quantitative"}
    }
}
```
</figure>

### Line

In certain cases, the scatter plot is not really relevant, as for the plot below, which shows Google's stock price as a function of time. Can you guess what's wrong with this chart?

<figure markdown>
<table>
<tr>
<th>Visual variable</th>
<th>Data</th>
<th rowspan=6>
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
```vegalite
{
    "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
    "description": "Google's stock price over time.",
    "width": 200,
    "data": {"url": "https://vega.github.io/vega-lite/data/stocks.csv"},
    "transform": [{"filter": "datum.symbol==='GOOG'"}],
    "mark": "line",
    "encoding": {
        "x": {"field": "date", "type": "temporal"},
        "y": {"field": "price", "type": "quantitative"}
    }
}
```
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
