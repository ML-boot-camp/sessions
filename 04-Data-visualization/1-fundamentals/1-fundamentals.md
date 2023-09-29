# Fundamentals

Creating powerful data visualitzaion might seem to be a difficult art, learnt through years of practice. But still there is method which can help to do basic.

This course has 2 objectives:

- being able to "explain" the content of a dataset to a functional expert - usually the "customer" of the data scientist. This is the **data story telling**.
- being able to explore a dataset looking for powerful predicting variables to solve a prediction problem. This is the **exploratory data analysis**.

To do so, this course provides basic knowledge about which kind of plot is suitable for each data type. 

## Levels of measurement and data types

To classify data, the most used typology is [Stevens' typology (1946)](https://en.wikipedia.org/wiki/Level_of_measurement#Stevens's_typology):

<figure markdown>
| Measurement | Property       | Math. operations           | Advanced Operations       | Data Type | Key idea                    |
| ----------- | -------------- | -------------------------- | ------------------------- | --------- | --------------------------- |
| Nominal     | Classification | =, ≠ <br> (equality)       | Grouping                  | String    | "I can make groups"         |
| Ordinal     | Comparison     | >, < <br> (inequality)     | Ranking                   | Integer   | "I can order stuff"         |
| Interval    | Difference     | +, − <br> (addition)       | Deviation from a standard | Float     | "I can measure differences" |
| Ratio       | Magnitude      | x, / <br> (multiplication) | Ratio between values      | Float     | "There is an absolute zero" |
</figure>

Measurements types do not contain the same level of information. There is a - kind of - inclusion relationship between them:

<figure markdown>
[Nominal<br>(group)](){.md-button} [<](){.very-very-big}
[Ordinal<br>(order)](){.md-button} [<](){.very-very-big}
[Interval<br>(relative)](){.md-button} [<](){.very-very-big}
[Ratio<br>(absolute)](){.md-button}
</figure>

E.g: You can convert an ordinal measurement to a nominal, but the opposite is often impossible without making an hypothesis.

To be noted that, even if this typology is widely used because it's simple, it is heavily criticized. Stevens was a psychologist and his typology is an oversimplification of the diversity of measurement types we can find in nature. More exhaustive - and complex - typologies have been proposed, see the note below.

??? Note "More information about measurement types"

    [Scribbr - Levels of measurement](https://www.scribbr.com/statistics/levels-of-measurement/)

    [Wikipedia - Level of measurement](https://en.wikipedia.org/wiki/Level_of_measurement)

### Exercises

It's time to consolidate your understanding of the **measurement types** concept with the exercises below.

> Tip: Put your mouse over the question mark to display the answer: [❓]{42|always}

**Exercise 1:** For each measurement type, find if it's a **quantitative** or **qualitative** measurement.

<figure markdown>
| Measurement | Qualitative or Quantitative |
| ----------- | --------------------------- |
| Nominal     | [❓]{Qualitative}            |
| Ordinal     | [❓]{Qualitative}            |
| Interval    | [❓]{Quantitative}           |
| Ratio       | [❓]{Quantitative}           |
</figure>

**Exercise 2:** Find what is the measurement level for each data example

<figure markdown>
| Data                            | Example                            | Measurement              |
| ------------------------------- | ---------------------------------- | ------------------------ |
| **name**                        | Julie, Quentin, Hakim, Marta       | [❓]{Nominal}             |
| **country**                     | France, USA, Marocco, Spain        | [❓]{Nominal}             |
| **age**                         | 27, 35, 12, 3                      | [❓]{Ratio}               |
| **marathon ranking**            | 13th, 1st, 2nd, 2037th             | [❓]{Ordinal}             |
| **date**                        | 2020-01-01, 2022-03-27, 1977-12-04 | [❓]{Interval}            |
| **time duration**               | 27s, 34m 12s, 1h 07m 01s           | [❓]{Ratio}               |
| **temperature °C**              | 41 °C, 12 °C, -21 °C               | [❓]{Interval}            |
| **temperature K**               | 273.15 K, 2500 K, 0.2 K, 500 nK    | [❓]{Ratio}               |
| **app rating**                  | ⭐, ⭐⭐⭐⭐⭐                           | [❓]{Ordinal}             |
| **USA school rating**           | F, A+, B+, C-                      | [❓]{Ordinal}             |
| **french school rating**        | 0, 5, 20, 12                       | [❓]{Interval}            |
| **S&P countries credit rating** | CCC, A+, BBB-, AAA                 | [❓]{Ordinal}             |
| **salary**                      | 25k€, 50k€, 150k€, 400k€, 8M€      | [❓]{Ratio}               |
| **money transfer**              | +40 €, -127 €, +150k€, -20000€     | [❓]{Interval}            |
| **images**                      |                                    | [❓]{Unstructured data !} |
</figure>

## Visual variables

[Jacques Bertin](https://fr.wikipedia.org/wiki/Jacques_Bertin_(cartographe)), a cartographer, introduced a basic set of [visual variables (1967)](https://en.wikipedia.org/wiki/Visual_variable). A visual variable is "the differences in graphical elements as perceived by the human eye". In other words, they are visual properties which we can perceive.

In other words, a visual variable is a way to display your (non-visual) data. Data visualization is the activity of **encoding data on visual variables**.

The most used visual variables in cartography are
**position, shape, size, hue, value, texture** and **orientation** (visually described by the figure below).

<figure markdown>
![](files/Visual_variables_pawandeep_kaur.png){width=80% .center}
<figurecaption>
7 visual variables and their description (from [Towards Visualization Recommendation ... [Kaur]](http://ceur-ws.org/Vol-1366/paper7.pdf))
</figurecaption>
</figure>

In practice, in data science, you'll use only the first 5 visual variables. There is also a - kind of - ordering relationship, in terms of expression power, between them:

<figure markdown>
[Position](){.md-button} [>](){.very-big}
[Size](){.md-button} [>](){.very-big}
[Shape](){.md-button} [>](){.very-big}
[Value](){.md-button} [>](){.very-big}
[Hue](){.md-button}
</figure>

Position is the most easy to use visual property and can be used to display any kind of data. Color value and hue are only slightly useful in a graph.

??? Note "More information on visual variables"

    [Visualization of geographical data [Victor Olaya]](https://volaya.github.io/gis-book/en/Visualization.html)

    [Visual variables [Roth]](https://geography.wisc.edu/cartography/projects/publications/Roth_2015_EG.pdf)

## Visual properties

Visual variables can have four basic properties, which are related to the measurement types:

- **Associative**: Values can be grouped together. Suitable to represent **nominal** variables.
- **Selective**. Values from a group can be isolated from the other groups. Suitable to represent **nominal** variables.
- **Ordered**. Values show a linear order. Suitable to represent **ordinal** variables
- **Quantitative**. Values can be directly measured. Suitable to represent **quantitative (interval & ratio)** variables.

There is one big catch to representing quantitative variables though: you have to represent the zero value for ratio variables, because it has a meaning. This **is** the most common mistake in data visualization.

Bertin has analyzed the properties of the visual variables:

<figure markdown>
![](files/Visual_variables_axis_maps.png){width=80% .center}
<figurecaption>
Visual variables and their properties (from [Visual variables [Axis maps]](https://www.axismaps.com/guide/visual-variables))
</figurecaption>
</figure>

Those properties emerge when our visual cortex in our brain does the visual information processing. It's a perceptual phenomenon and there is a subjective dimension here.

??? Note "More information on visual properties"

    [Visual variables [Axis maps]](https://www.axismaps.com/guide/visual-variables)

## From measurement type to visual variable

A professor recently proposed a refinement & simplification of this analysis, doing a mapping from the visual variable to the variable type directly:

<figure markdown>
![](files/visual-variables-and-their-syntactics.png){width=80% .center}
<figurecaption>
Visual variables and their syntactics (from [Visual variables [Roth]](https://geography.wisc.edu/cartography/projects/publications/Roth_2015_EG.pdf))
</figurecaption>
</figure>

In the context of data science, we can even more simplify this analysis, since we rarely use texture or orientation:

<figure markdown>
|              | Position | Size | Shape | Value | Hue |
| ------------ | -------- | ---- | ----- | ----- | --- |
| **Nominal**  | ✅        | ❔    | ✅     | ❌     | ✅   |
| **Ordinal**  | ✅        | ✅    | ❌     | ✅     | ❔   |
| **Interval** | ✅        | ✅    | ❌     | ❔     | ❔   |
| **Ratio**    | ✅        | ✅    | ❌     | ❔     | ❔   |

<figurecaption>
Legend: ✅=Perfect for it, ❔=Try it but don't expect much, ❌=Don't even try

Measurement types & visual variables,<br>simplified in the context of data visualization for data science.<br>(Maybe the one and only table you need to remember from this course)
</figurecaption>

</figure>

### Exercise

**Exercise**: Pick one bad visualization from [tumblr.com/badvisualisations](https://www.tumblr.com/badvisualisations) and explain what is wrong with the visualization.
