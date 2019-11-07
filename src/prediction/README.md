# Prediction methodology

### Metrics
According to Erin Jensen, maximizing recall is the most important thing in the project. However, this does not mean that we should automatically target only recall.

The measure the performance of the algorithm, I have opted to use the $`F_{\beta}`$-score.

The $`F_{\beta}`$ score is a weighted balance between pure recall and pure precision driven utility. The scoring formula is:

```math
F_{\beta} = \frac{(1 + \beta^{2})RP}{R + \beta^{2}P}
```
