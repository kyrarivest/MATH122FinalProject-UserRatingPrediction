import numpy as np
import pandas as pd
import pickle as pkl

import build_WEIGHT_matrix
import build_RATINGS_matrix
import predict
import analyze_results



#Load Data
user_history = pd.read_csv("user_history.csv")
user_ratings = pd.read_csv("user_ratings.csv")
RATINGS_matrix = build_RATINGS_dfs.build(user_history, user_ratings)




#__________________MAIN METHOD__________________#

powers = [0.5,1, 2,4,8,16,32]


#For each power, run the model
#So that means generate a weight matrix for that power, and predict ratings using the weight matrix values
for power in powers:
    print("Computing for power: " + str(power))
    WEIGHT_matrix = build_WEIGHT_matrix.build(user_history, power)
    predicted_ratings = predict.run(user_history, WEIGHT_matrix, RATINGS_matrix, power)


#Run analysis on the resulting raw prediction files
analyze_results.run(RATINGS_matrix)
