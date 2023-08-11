# Data format

You should be able to reshape your data according to your need. Should you use
wide format or long format or none of them ?

<figure markdown>
![](https://www.statology.org/wp-content/uploads/2021/12/wideLong1-1.png)
<figcaption>Wide & long format</figcaption>
</figure>

Let's find out.

## Raw format

In its raw form, data is usually made of payloads containing keys and values
(i.e. dictionaries).

Example when receiving payload of meteorological data with temperature and
humidity (integrated sensor):

```json
[
  {
    "Date": "2023-01-01",
    "City": "CityA",
    "Temperature": 20,
    "Humidity": "30%"
  },
  {
    "Date": "2023-01-01",
    "City": "CityB",
    "Temperature": 15,
    "Humidity": "25%"
  },
  {
    "Date": "2023-01-01",
    "City": "CityC",
    "Temperature": 18,
    "Humidity": "28%"
  },
  {
    "Date": "2023-01-02",
    "City": "CityA",
    "Temperature": 21,
    "Humidity": "31%"
  },
  {
    "Date": "2023-01-02",
    "City": "CityB",
    "Temperature": 16,
    "Humidity": "26%"
  },
  {
    "Date": "2023-01-02",
    "City": "CityC",
    "Temperature": 19,
    "Humidity": "29%"
  }
]
```

Or alternatively when receiving payloads of meteorological data with either
temperature or humidity (different sensors):

```json
[
  {"Date": "2023-01-01", "City": "CityA", "Temperature": 20},
  {"Date": "2023-01-01", "City": "CityA", "Humidity": "30%"},
  {"Date": "2023-01-01", "City": "CityB", "Temperature": 15},
  {"Date": "2023-01-01", "City": "CityB", "Humidity": "25%"},
  {"Date": "2023-01-01", "City": "CityC", "Temperature": 18},
  {"Date": "2023-01-01", "City": "CityC", "Humidity": "28%"},
  {"Date": "2023-01-02", "City": "CityA", "Temperature": 21},
  {"Date": "2023-01-02", "City": "CityA", "Humidity": "31%"},
  {"Date": "2023-01-02", "City": "CityB", "Temperature": 16},
  {"Date": "2023-01-02", "City": "CityB", "Humidity": "26%"},
  {"Date": "2023-01-02", "City": "CityC", "Temperature": 19}
  {"Date": "2023-01-02", "City": "CityC", "Humidity": "29%"}
]
```

Each record is dictionary made of variables which can be:

- **categories**: used to select and filter data or link to other table. Usually
  a string or an integer.
- **values**: an actual measurement of a sensor. Usually a float.

## Long Format

The easiest way to store the data in the _long format_ using only 3 columns:

- an ID of the measurement
- the variable name
- the variable value

The long format would look like this:

| ID  | Variable    | Value      |
| --- | ----------- | ---------- |
| 1   | Date        | 2023-01-01 |
| 1   | City        | CityA      |
| 1   | Temperature | 20         |
| 1   | Humidity    | 30%        |
| 2   | Date        | 2023-01-01 |
| 2   | City        | CityB      |
| 2   | Temperature | 15         |
| 2   | Humidity    | 25%        |
| 3   | Date        | 2023-01-01 |
| 3   | City        | CityC      |
| 3   | Temperature | 18         |
| 3   | Humidity    | 28%        |
| 4   | Date        | 2023-01-02 |
| 4   | City        | CityA      |
| 4   | Temperature | 21         |
| 4   | Humidity    | 31%        |
| 5   | Date        | 2023-01-02 |
| 5   | City        | CityB      |
| 5   | Temperature | 16         |
| 5   | Humidity    | 26%        |

In this representation, the integer ID serves to group the related values for
each observation, while the variable column specifies the type of information,
and the value column contains the actual data.

This format is best suited for **storage**:

- it is extremely flexible, as we can add more variables for each measurement
  **without changing the table schema**
- it has a better storage efficiency when working with sparse data.

But it can become more complex to work with, particularly for data analysis
tasks.

## Compact format

!!! note

    The term "Compact" format has been defined only in the context of this course.
    It is not a standard concept and is not commonly used across the industry. Don't
    use it as if it's something widely known in the data engineering community.

Usually the best format for your data is neither fully wide nor fully long. The
purpose of those "extreme" format examples is to show that data can (and should)
be reshaped depending on the use case.

The best practice for data engineering is to format your data to **have 1 column
per variable**. This implies:

- not wide format: don't use variables in column names
- not long format: don't mix different variables in the same column

The compact format applied to our meteorological data example looks like this:

| Date       | City  | Temperature | Humidity |
| ---------- | ----- | ----------- | -------- |
| 2023-01-01 | CityA | 20          | 30%      |
| 2023-01-01 | CityB | 15          | 25%      |
| 2023-01-01 | CityC | 18          | 28%      |
| 2023-01-02 | CityA | 21          | 31%      |
| 2023-01-02 | CityB | 16          | 26%      |
| 2023-01-02 | CityC | 19          | 29%      |

It naturally aligns with the structure of the data: each row represents a single
observation (in a city on a particular date), and each variable (temperature and
humidity) has its column.

The compact format is best suited for **data engineering**:

- to filter and select the data for various criteria
- to transform variables (scaling, outliers management)
- to compute new variables (e.g: wet bulb temperature from temperature &
  humidity)

It's not very readable but is very convenient to work with.

## Wide format

The wide format uses the categories to create the columns, it displays only
values for a given index (on the left).

Here is how the meteorological would look in the wide format:

| Date       | Temperature_CityA | Humidity_CityA | Temperature_CityB | Humidity_CityB | Temperature_CityC | Humidity_CityC |
| ---------- | ----------------- | -------------- | ----------------- | -------------- | ----------------- | -------------- |
| 2023-01-01 | 20                | 30%            | 15                | 25%            | 18                | 28%            |
| 2023-01-02 | 21                | 31%            | 16                | 26%            | 19                | 29%            |

This is not very readable and usually the only reasonable use of wide format is
to display data for a particular use-case:

- select a **single category** for the **index** (e.g: year)
- select a **single category** for the **columns** (e.g: city)
- select a **single value** to fill the **cells** (e.g: temperature)

So, if we'd like to compare temperatures in various cities:

| Date       | Temperature_CityA | Temperature_CityB | Temperature_CityC |
| ---------- | ----------------- | ----------------- | ----------------- |
| 2023-01-01 | 20                | 15                | 18                |
| 2023-01-02 | 21                | 16                | 19                |

The wide format is best suited for **visualization**.

## Conclusion

Here is a table summarizing the various formats:

| Format  | Description                                                   | Best Suited For                         | Example Characteristics                              |
| ------- | ------------------------------------------------------------- | --------------------------------------- | ---------------------------------------------------- |
| Raw     | Dictionaries containing keys and values (e.g., JSON).         | Initial data storage                    | Separate dictionaries for each record                |
| Long    | 3 columns: ID, variable name, variable value.                 | Storage (sparse data & flexible schema) | Each variable is a separate row                      |
| Compact | 1 column per variable, not mixed in wide or long format.      | Data engineering                        | Each row represents a single observation             |
| Wide    | Categories create columns; values are displayed for an index. | Visualization                           | Columns include categories, like `Temperature_CityA` |

A good data scientist / analyst / engineer should be able to easily reshape and
reformat data from one format to another, depending on the need.
