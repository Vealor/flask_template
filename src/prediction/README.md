# Prediction

This is a brief summary of the prediction pipeline.

## Pipeline

### Training
* Start with *Transaction data*
* Select entries whose schedules do not have "paredown" and that have been "approved". Of these entries, take a subset whose last modification date lies within a certain range. This is the *Training data*.
* Select another, more-recently-modified, disjoint, subset of this data. This is the *Validation data*.
* Take both subsets of data and preprocess them to be ingested into the predictive model for training. This means cleaning data, formatting data, ensuring that all columns are present, etc.
* Train a new predictive model using the *Training data*.
* When training is complete, Test the predictive power of the new model using the *Validation data*.
* If there is an Active model, Test the predictive power of the new model using the *Validation data*. The user makes a choice to set the new model as the active model, based on performance.
* If no active model exists, set the newly trained model as the active model.


## Model Training



#### Metrics
According to Erin Jensen, maximizing recall is the most important thing in the project. However, this does not mean that we should automatically target only recall.

The measure the performance of the algorithm, I have opted to use the $`F_{\beta}`$-score.

The $`F_{\beta}`$ score is a weighted balance between pure recall and pure precision driven utility. The scoring formula is:

```math
F_{\beta} = \frac{(1 + \beta^{2})RP}{R + \beta^{2}P}
```
