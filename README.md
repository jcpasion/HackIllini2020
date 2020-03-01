# HackIllini2020
Working on the Caterpillar IoT Challenge.

Our idea for filtering the data:
  For each channel, place data point values into bins and treat data points in underrepresented bins as outliers, then remove them.
  Compute a global confidence interval for variance using range parameters min and max, and omit channels that had a large deviance from the global confidence interval
  
After data filtering, we planned to use a linear regression model to look at all data points of a channel, and predict similar channels using a training dataset. We would utilize the technique '5-fold cross validation' from our cleaned dataset.


We implemented our ideas using python dictionaries, but ran into run-time issues. We discovered the world of Pandas dataframe, but too late to implement them into our workflow. 


 
