# Data format

## Wide & long format

<figure markdown>
![](https://www.statology.org/wp-content/uploads/2021/12/wideLong1-1.png)
<figcaption>Wide & long format</figcaption>
</figure>

| Property                    | Long Format                                                                     | Wide Format                                                                            |
| --------------------------- | ------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| **Description & Structure** | Puts data of the same type in one column, adds columns for categories/tags.     | Duplicates columns for different categories/tags, each variable has its own column.    |
| **Use Case**                | Preferred for complex analyses.                                                 | Common in spreadsheets, easier for simpler analyses with few variables.                |
| **Advantages**              | Flexible for handling related variables, more efficient with sparse data.       | Compact, easier visually with small, dense datasets.                                   |
| **Disadvantages**           | Harder to read with many variables, less efficient with dense data.             | Cumbersome with many variables, less flexible for complex analyses.                    |
| **Flexibility**             | Highly adaptable, simplifies handling multiple related variables or categories. | More rigid, may limit analyses when duplicating columns for different categories/tags. |
| **Storage Efficiency**      | More efficient with sparse data by avoiding unnecessary empty cells.            | More efficient with dense data where most cells contain information.                   |

## Meteorological data example

### Wide format

Let's say you have this meteorological data in wide format:

| Date       | Temp_CityA | Humidity_CityA | Temp_CityB | Humidity_CityB | Temp_CityC | Humidity_CityC |
| ---------- | ---------- | -------------- | ---------- | -------------- | ---------- | -------------- |
| 2023-01-01 | 20         | 30%            | 15         | 25%            | 18         | 28%            |
| 2023-01-02 | 21         | 31%            | 16         | 26%            | 19         | 29%            |

This format quickly becomes cumbersome with many cities and variables, making it hard to perform analyses that require handling multiple related variables (temperature and humidity) for the same observation (city).

### Long Format

In contrast, the long format would look like this:

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

In this representation, the integer ID serves to group the related values for each observation, while the variable column specifies the type of information, and the value column contains the actual data. This format is extremely flexible, as we can add more properties for each measurement without changing the table schema, but can become more complex to work with, particularly for data analysis tasks.

### Hybrid format

The best format to represent those data is a hybrid format: neither fully wide nor fully long:

| Date       | City  | Temperature | Humidity |
| ---------- | ----- | ----------- | -------- |
| 2023-01-01 | CityA | 20          | 30%      |
| 2023-01-01 | CityB | 15          | 25%      |
| 2023-01-01 | CityC | 18          | 28%      |
| 2023-01-02 | CityA | 21          | 31%      |
| 2023-01-02 | CityB | 16          | 26%      |
| 2023-01-02 | CityC | 19          | 29%      |

It naturally aligns with the structure of the data: each row represents a single observation (a city on a particular date), and each variable (temperature and humidity) has its column

With this hybrid format, you can easily filter, analyze, and visualize the data for individual cities or across all cities. It becomes much more straightforward to apply statistical models that require handling related variables as part of the same observation, such as comparing temperature and humidity trends across different cities over time.

## Hybrid format: key & value properties

The above example of a hybrid format is built by keeping some properties of the data as key columns (in long format) and some other are used as value columns (in wide format).

The matrix below summarizes the key considerations for choosing between key and value columns in a hybrid format:

| Criteria                           | Key Columns                                                   | Value Columns                                                          |
| ---------------------------------- | ------------------------------------------------------------- | ---------------------------------------------------------------------- |
| **Uniqueness & Identity**          | Unique identifiers or essential for linking data.             | Actual data measurements or attributes.                                |
| **Relationship & Structure**       | Represents hierarchical or categorical relationships.         | Variables for analysis, comparison, or visualization.                  |
| **Analysis Purpose**               | Used to filter, group, or subset data in analyses.            | Subject of the analysis, such as measurable characteristics.           |
| **Data Sparsity & Density**        | Suitable for sparse data to reduce redundancy.                | Suitable for dense data where a variable applies broadly.              |
| **Flexibility & Interpretability** | Increases flexibility but might hinder visual interpretation. | Simplifies view but might reduce flexibility in complex relationships. |

### Robot logs data example

Let's say we are collecting logs from robots, but actually each payload contains different kinds of values:

1. **Timestamp**: The exact time the log was recorded. Always sent.
2. **RobotID**: Unique identifier for the robot. Always sent.
3. **TaskID**: Identifier for the task being performed. Always sent.
4. **Status**: Current status of the task (e.g., In Progress, Completed, Failed). Always sent.
5. **BatteryLevel**: Remaining battery percentage. Not always sent.
6. **ErrorCodes**: Any error codes recorded, if applicable. Not always sent.
6. **PositionLat**: Position of the robot (Latitude). Not always sent.
6. **PositionLon**: Position of the robot (Longitude). Not always sent.

The data are received payload by payload and the **long format** is the easiest way to store it:

| PayloadID | Variable     | Value               |
| --------- | ------------ | ------------------- |
| 1         | Timestamp    | 2023-08-09 10:00:00 |
| 1         | RobotID      | R101                |
| 1         | TaskID       | T5678               |
| 1         | Status       | In Progress         |
| 1         | BatteryLevel | 78%                 |
| 2         | Timestamp    | 2023-08-09 10:00:01 |
| 2         | RobotID      | R101                |
| 2         | TaskID       | T5678               |
| 2         | Status       | In Progress         |
| 2         | PositionLat  | 42.331              |
| 2         | PositionLon  | -83.045             |
| 3         | Timestamp    | 2023-08-09 10:05:00 |
| 3         | RobotID      | R101                |
| 3         | TaskID       | T5678               |
| 3         | Status       | In Progress         |
| 3         | BatteryLevel | 75%                 |
| ...       | ...          | ...                 |

Since it's very hard to understand and visualize this data, let's reformat it in a hybrid format
which is more convenient.

In a hybrid format, we might choose the following structure:

- **Key Columns**: Timestamp, RobotID, TaskID
- **Value Columns**: Status, BatteryLevel, ErrorCodes, PositionLat, PositionLon

These choices reflect the uniqueness and identity of the logs (Timestamp, RobotID), the hierarchical structure (TaskID), and the variables for analysis or monitoring (Status, BatteryLevel, ErrorCodes, PositionLat, PositionLon).

Here's a preview of the resulting dataset (missing data are shown as empty):

| Timestamp           | RobotID | TaskID | Status      | BatteryLevel | ErrorCodes | PositionLat | PositionLon |
| ------------------- | ------- | ------ | ----------- | ------------ | ---------- | ----------- | ----------- |
| 2023-08-09 10:00:00 | R101    | T5678  | In Progress | 78%          |            |             |             |
| 2023-08-09 10:00:01 | R101    | T5678  | In Progress |              |            | 42.331      | -83.045     |
| 2023-08-09 10:05:00 | R101    | T5678  | In Progress | 75%          |            |             |             |
| 2023-08-09 10:05:01 | R101    | T5678  | In Progress |              | E23        |             |             |
| 2023-08-09 10:05:02 | R101    | T5678  | In Progress |              |            | 42.332      | -83.046     |
| 2023-08-09 10:10:00 | R102    | T5679  | Completed   |              |            | 42.330      | -83.044     |
| 2023-08-09 10:10:01 | R102    | T5679  | Completed   | 50%          |            |             |             |
| 2023-08-09 10:15:00 | R101    | T5678  | Failed      |              | E45, E23   |             |             |
| 2023-08-09 10:15:00 | R101    | T5678  | Failed      | 70%          |            |             |             |
| 2023-08-09 10:15:01 | R101    | T5678  | Failed      |              |            | 42.331      | -83.047     |
| 2023-08-09 10:20:00 | R102    | T5680  | In Progress |              |            | 42.329      | -83.043     |
| 2023-08-09 10:20:01 | R102    | T5680  | In Progress | 46%          |            |             |             |

In practice, we would rework the timestamp in order to merge together rows (payloads) which regard similar robot state and try to have a more complete robot state for each row:

| Timestamp           | RobotID | TaskID | Status      | BatteryLevel | ErrorCodes | PositionLat | PositionLon |
| ------------------- | ------- | ------ | ----------- | ------------ | ---------- | ----------- | ----------- |
| 2023-08-09 10:00:00 | R101    | T5678  | In Progress | 78%          |            | 42.331      | -83.045     |
| 2023-08-09 10:05:00 | R101    | T5678  | In Progress | 75%          | E23        | 42.332      | -83.046     |
| 2023-08-09 10:10:00 | R102    | T5679  | Completed   | 50%          |            | 42.330      | -83.044     |
| 2023-08-09 10:15:00 | R101    | T5678  | Failed      | 70%          | E45, E23   | 42.331      | -83.047     |
| 2023-08-09 10:20:00 | R102    | T5680  | In Progress | 46%          |            | 42.329      | -83.043     |

This structure allows for tracking each robot's activity over time, monitoring their position, status and battery level, and recording any errors, making it suitable for both real-time monitoring and historical analysis.
