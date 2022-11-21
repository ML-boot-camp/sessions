# Models properties

## Bias & variance

Course:

- [Principles and Methodology of Machine Learning - David Gianazza (slides 233-236)](https://drive.google.com/file/d/18Ul_jnqLz3I__ycIjFDu0HIH0X_q0kuw/view)

Some sources:

- [Bias–variance tradeoff - Wikipedia](https://en.wikipedia.org/wiki/Bias%E2%80%93variance_tradeoff)
- [Bias vs Variance - Gunjan Agicha (Medium)](https://gunjanagicha.medium.com/bias-vs-var-91846964d40f)

High bias / low variance models generalize better on new tasks.

Low bias / high variance models perform better on the task they have been trained on.

## Parametric & non-parametric

- [What exactly is the difference between a parametric and non-parametric model? - stats.stackexchange](https://stats.stackexchange.com/questions/268638/what-exactly-is-the-difference-between-a-parametric-and-non-parametric-model)
- [Parametric and nonparametric ML algorithms - Machine learning mastery](https://machinelearningmastery.com/parametric-and-nonparametric-machine-learning-algorithms/)

In very brief:

- **Parametric** models have fixed set of parameters. Their complexity is determined by the number of parameters. The parameters are **fitted** to the data. Popular parametric models:
    - Linear regression, Logistic regression
    - Neural networks
- **Non-parametric** models don't have a fixed parameters, but rather are **built from the data**. Their complexity depends on the data on which they are built on.
    - Tree-based models: CART, random forests, gradient boosting regressor or classifier
    - K nearest neighbors
    - Support Vector Machines

## Computational complexity

- [Computational Complexity of ML Models - Paritosh Kumar (Medium)](https://medium.com/analytics-vidhya/time-complexity-of-ml-models-4ec39fad2770)
