import tensorflow as tf
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
# import seaborn as sns
# import matplotlib.pyplot as plt

df = pd.read_csv('ufc_data.csv')

def create_input_data(fighter1, fighter2, df, numerical_features, categorical_features, encoded_data):
    # 1. Gather historical data
    fighter1_data = df[df['R_fighter'] == fighter1] 
    fighter2_data = df[df['B_fighter'] == fighter2] 

    # 2. Select numerical features (directly)
    fighter1_features = fighter1_data[numerical_features].copy()
    fighter2_features = fighter2_data[numerical_features].copy()

    # 3. Encode categorical features
    encoded_features = encode_data(fighter1_data, fighter2_data, categorical_features)

    # 4. Combine features (Assuming correct order)
    combined_features = pd.concat([fighter1_features, fighter2_features, encoded_features], axis=1) 

    return combined_features  

def calculate_numerical_features(fighter_data, numerical_features):
    features = fighter_data[numerical_features].copy()  
    return features 

def encode_data(fighter1_data, fighter2_data, categorical_features):
    encoded_features = pd.DataFrame() 

    encoder = OneHotEncoder(handle_unknown='ignore') 

    for col in categorical_features:
        combined_data = pd.concat([fighter1_data[col], fighter2_data[col]]) 
        encoded_col = encoder.fit_transform(combined_data.to_numpy().reshape(-1, 1)).toarray() 
        encoded_features = pd.concat([encoded_features, pd.DataFrame(encoded_col)], axis=1) 

    return encoded_features 

def process_prediction(prediction):
    """Converts raw model output (probability) into a predicted winner"""
    if prediction >= 0.5:
        return 'Fighter 1'
    else:
        return 'Fighter 2'


# def calculate_features(fighter_data, numerical_features):
#     """Calculates relevant features from a fighter's historical data"""

#     features = {}

#     # Example numerical features:
#     for feature_name in numerical_features:
#         if feature_name == 'average_elo':
#             features['average_elo'] = fighter_data['Elo'].mean()
#         elif feature_name == 'recent_win_streak':
#             recent_fights = fighter_data.tail(5)  # Assuming last 5 fights are recent
#             features['recent_win_streak'] = (recent_fights['Winner'] == fighter_data['Fighter'].iloc[0]).sum()
#         # ... add more feature calculations based on your model

#     return features

# def combine_features(fighter1_features, fighter2_features):
#     """Combines features for both fighters, ensuring the correct order for your model"""  

#     combined_features = pd.DataFrame([fighter1_features, fighter2_features])

#      # If necessary, rearrange columns to match the order your model expects
#      # combined_features = combined_features[[col1, col2, ...]]   

#     return combined_features  

# def create_input_data(fighter1, fighter2, df, numerical_features, categorical_features, encoded_data):
#     # 1. Gather historical data for fighter1 and fighter2 from 'df' 
#     fighter1_data = ... # Filter df for fighter1's data
#     fighter2_data = ... # Filter df for fighter2's data

#     # 2. Calculate features
#     fighter1_features = calculate_features(fighter1_data, numerical_features) 
#     fighter2_features = calculate_features(fighter2_data, numerical_features)

#     # 3. Combine features (consider the order your model expects)
#     combined_features = combine_features(fighter1_features, fighter2_features)

#     # 4. Apply encoding (if needed)
#     encoded_features = encoded_data.transform(combined_features) 

#     return encoded_features  # This should be in the format your model expects


# mango advice
# RELU and softmax activtion methods
# funcntional api is for more complex things. multiple inputs mapped to multiple outputs
# sequential api is less complex, one input to one output
'''
gemini note:
Your sequential model is appropriate for this scenario. Functional API is better for more complex networks with multiple inputs or outputs.
'''

'''
gemini note:
Convolutional Neural Networks (CNNs) can be useful for image or time-series data but might be less relevant here.
Batch normalization and max-pooling could be considered for larger, deeper networks, potentially improving performance.
'''

'''
gemini note softmax activation: oftmax activation is used for multi-class classification (more than two outcome categories). 
Since we're predicting Winner (two classes), stick with sigmoid activation in the output layer.
Unless we do more than two classes later, then give softmax activation a try!
'''

# ade advice on what to add
# you could add batch normalization, max pulling, convoloution neural networks use many layers to predict output


#prints all the columns in df
# columns = df.columns
# print(columns)

#defines a logistical regression model
model = tf.keras.Sequential([
    # in input_shape, we have the number of our features
    tf.keras.layers.Dense(units=1, input_shape=(3099,), activation='sigmoid')
])

#compiles the model and specifies our metrics for the optimizer, loss, and accuracy metrics
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# add finish, finish_details, finish round, etc. later.  columns DE in the csv file 
#X_train = df[['R_fighter', 'B_fighter', 'R_odds', 'B_odds', 'weight_class','gender','no_of_rounds', 'B_current_lose_streak','B_current_win_streak','B_avg_SIG_STR_landed','B_avg_SIG_STR_pct','B_avg_SUB_ATT','B_avg_TD_landed','B_avg_TD_pct','B_longest_win_streak', 'B_losses','B_total_rounds_fought','B_total_title_bouts','B_win_by_Decision_Majority','B_win_by_Decision_Split','B_win_by_Decision_Unanimous','B_win_by_KO/TKO','B_win_by_Submission','B_win_by_TKO_Doctor_Stoppage','B_wins','B_Stance','B_Height_cms','B_Reach_cms', 'R_current_lose_streak','R_current_win_streak','R_avg_SIG_STR_landed','R_avg_SIG_STR_pct','R_avg_SUB_ATT','R_avg_TD_landed','R_avg_TD_pct','R_longest_win_streak', 'R_losses','R_total_rounds_fought','R_total_title_bouts','R_win_by_Decision_Majority','R_win_by_Decision_Split','R_win_by_Decision_Unanimous','R_win_by_KO/TKO','R_win_by_Submission','R_win_by_TKO_Doctor_Stoppage','R_wins','R_Stance','R_Height_cms','R_Reach_cms', 'B_match_weightclass_rank','R_match_weightclass_rank']]
#y_train =df[['Winner']]

'''
Numerical Features: These are already in a numerical format suitable for direct use in machine learning models: 
'''
numerical_features = df[['R_odds', 'B_odds', 'no_of_rounds', 
                         'B_current_lose_streak', 'B_current_win_streak', 'B_avg_SIG_STR_landed', 'B_avg_SIG_STR_pct', 'B_avg_SUB_ATT', 'B_avg_TD_landed', 'B_avg_TD_pct', 'B_longest_win_streak', 'B_losses', 'B_total_rounds_fought', 'B_total_title_bouts', 'B_Height_cms', 'B_Reach_cms',
                         'R_current_lose_streak', 'R_current_win_streak', 'R_avg_SIG_STR_landed', 'R_avg_SIG_STR_pct', 'R_avg_SUB_ATT', 'R_avg_TD_landed', 'R_avg_TD_pct', 'R_longest_win_streak', 'R_losses', 'R_total_rounds_fought', 'R_total_title_bouts',  'R_Height_cms', 'R_Reach_cms',
                         'B_Weight_lbs', 'R_Weight_lbs']]

'''
Categorical Features: These features contain categories (text or labels)
and need to be converted to a numerical representation before being used by the model
'''
categorical_features = ['R_fighter', 'B_fighter', 'weight_class', 'gender', 
                        'B_Stance', 'R_Stance',
                        'B_win_by_Decision_Majority', 'B_win_by_Decision_Split', 'B_win_by_Decision_Unanimous', 'B_win_by_KO/TKO', 'B_win_by_Submission', 'B_win_by_TKO_Doctor_Stoppage',
                        'R_win_by_Decision_Majority', 'R_win_by_Decision_Split', 'R_win_by_Decision_Unanimous', 'R_win_by_KO/TKO', 'R_win_by_Submission', 'R_win_by_TKO_Doctor_Stoppage']

encoded_data = pd.DataFrame() # A placeholder for encoded data
'''
This code performs one-hot encoding on categorical features. TensorFlow doesn't take in strings 
(i.e. "orthoddox" for a fighters stance), so we one-hot encodeeach string to a unique
'''

for col in categorical_features:  
    # Create an encoder to handle unknown categories:
    encoder = OneHotEncoder(handle_unknown='ignore')
    # Fit the encoder to the current column and transform it into numerical representations:
    encoded_col = encoder.fit_transform(df[[col]]).toarray()
    # Convert the encoded column into a DataFrame and append it to the encoded features:
    encoded_data = pd.concat([encoded_data, pd.DataFrame(encoded_col)], axis=1) 


# Combine encoded and numerical features 
X = pd.concat([encoded_data, numerical_features], axis=1) 

y = df['Winner'].replace({'Red': 0, 'Blue': 1})

#
# Train-Test Split
# this splits the data into training and testing sets. test_size = 0.2 would be an 80/20 split of training to testing data. random_state makes the split reproducible.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# this splits the data into training and testing sets. test_size = 0.2 would be an 80/20 split of training to testing data. random_state makes the split reproducible.
#X_train, X_test, y_train, y_test = train_test_split(df[['R_fighter', 'B_fighter', 'R_odds', 'B_odds', 'weight_class','gender','no_of_rounds', 'B_current_lose_streak','B_current_win_streak','B_avg_SIG_STR_landed','B_avg_SIG_STR_pct','B_avg_SUB_ATT','B_avg_TD_landed','B_avg_TD_pct','B_longest_win_streak', 'B_losses','B_total_rounds_fought','B_total_title_bouts','B_win_by_Decision_Majority','B_win_by_Decision_Split','B_win_by_Decision_Unanimous','B_win_by_KO/TKO','B_win_by_Submission','B_win_by_TKO_Doctor_Stoppage','B_wins','B_Stance','B_Height_cms','B_Reach_cms', 'R_current_lose_streak','R_current_win_streak','R_avg_SIG_STR_landed','R_avg_SIG_STR_pct','R_avg_SUB_ATT','R_avg_TD_landed','R_avg_TD_pct','R_longest_win_streak', 'R_losses','R_total_rounds_fought','R_total_title_bouts','R_win_by_Decision_Majority','R_win_by_Decision_Split','R_win_by_Decision_Unanimous','R_win_by_KO/TKO','R_win_by_Submission','R_win_by_TKO_Doctor_Stoppage','R_wins','R_Stance','R_Height_cms','R_Reach_cms', 'B_match_weightclass_rank','R_match_weightclass_rank']], df[['Winner']], test_size=0.2, random_state=42)

#'fit' method trains the model data. 
#first param is , second param is, 3rd , 4th, 
#An epoch is one complete pass through the entire dataset during the training process.

'''
Batch size == to the number of training examples utilized in one iteration. Instead of updating the model's parameters 
after every single example (which would be extremely slow), we update them after a batch of examples. The batch size determines how many examples are processed simultaneously before the model's parameters are updated.
'''

#train_test_split outputs both X and y features as dataFrames, but the model is expecting NumPy arrays
# So, we convert DataFrames to NumPy arrays
X_train = X_train.values
X_test = X_test.values
y_train = y_train.values
y_test = y_test.values

print(X_train.shape)  # Should output something like (Num_Samples, 51 + Num_Encoded_Features)
print(y_train.shape)  # Should output something like (Num_Samples,)
print("\n\nnumerical features print: \n")
print(numerical_features)

print("\n\n df.head()print: \n")
print(df.head())


model.fit(X_train, y_train, epochs=20, batch_size=128)


loss, accuracy = model.evaluate(X_test, y_test)
#print('Test Loss:', loss)
print('Test Accuracy:', accuracy)

model.save('my_ufc_model.keras')  


