# Exploratory data analysis

> This section is still a Work In Progress.

## Data visualization method

1. Analyze data type: analyze the "measurement type" of the data you want to plot
2. Encode data on visuals: choose a set of visual variables adapted to each data, according to their measurement type
3. Confront your subjectivity: make several versions of the plot and choose the best one by discussing it with other people.

## Golden rules

- **Avoid information overload**: don't try to plot more that 3 informations on one plot.
- **Use visual redundancy**: use more than one visual variable per measurement.
- **Never forget zero**: always plot the zero if its meaningful
- **Avoid overplotting**: don't try to plot too much data points on the same plot, at the risk of saturating the visual space. If needed, reduce the number of data points (take a sample) or use transparency.
- **Don't use pie charts**: period.

## Descriptive statistics

| Measurement | Central stat.   | Variability stat                                 |
| ----------- | --------------- | ------------------------------------------------ |
| Nominal     | Mode            | Unique count, <br>Information entropy            |
| Ordinal     | Median          | Unique count, <br>Interquartile range            |
| Interval    | Arithmetic mean | Standard deviation                               |
| Ratio       | Geometric mean  | Standard deviation, <br>Coefficient of variation |

## Exploratory data analysis in short

At each step, use **plots & descriptive statistics** to:

1. Describe each variable individually
1. Describe the target
1. Describe relationships between variables
1. Describe variables' relationships with the target

The goal is to give a subjective answer to those questions:

- Are the data clean ?
- What kind of information do we have in the data ?
- What are the variables which will help us the most to solve the prediction problem ?
- Is the prediction problem difficult ? Do we have the right data to do a prediction ? What kind of prediction performance can we expect ?

A nice example can be found [here](https://www.shriramjaju.page/2017-03-26-DAND-titanic/).
