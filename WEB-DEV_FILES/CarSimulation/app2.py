from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
import joblib

app = Flask(__name__)

# Define symbolic representation for output classes
# output_classes = {
#     0: '🛑 Emergency Brake',
#     1: '⚡ Speed Up',
#     2: '🐢 Speed Down',
#     3: '↔️ Lane Change',
#     4: '⏸️ No Action',
#     7: '❌ No Input Received'
# }

# Route: Home Page
@app.route('/')
def index2():
    return render_template('index2.html')

# Route: Train Model
@app.route('/train', methods=['POST'])
def train_model():
    # Load the Excel file
    train_file_path = 'Final_Dataset.xlsx'
    df = pd.read_excel(train_file_path)

    # Feature and target separation
    X = df.drop(columns=['Output'])  
    y = df['Output']

    # Preprocess categorical features
    categorical_features = X.select_dtypes(include=['object']).columns.tolist()
    preprocessor = ColumnTransformer(
        transformers=[('cat', OneHotEncoder(), categorical_features)],
        remainder='passthrough'
    )
    X = preprocessor.fit_transform(X)

    # Train-test split
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
    num_samples = 50
    X_test_samples = X_val[:num_samples] # First 50 samples from test features
    y_test_samples = y_val[:num_samples]  # First 50 samples from test labels
   
    # Convert to numpy arrays if necessary
    X_test_samples = np.array(X_test_samples)
    y_test_samples = np.array(y_test_samples)
   
    # Save the test samples to a CSV file
    np.savetxt('X_test_samples.csv', X_test_samples, delimiter=',')
    np.savetxt('y_test_samples.csv', y_test_samples, delimiter=',', fmt='%d')  # Save labels as integers

    print("Test samples saved!")
    
    # Train Decision Tree model
    decision_tree = DecisionTreeClassifier(min_samples_split=10, min_samples_leaf=5, max_depth=8, random_state=42)
    decision_tree.fit(X_train, y_train)

    # Save the model
    joblib.dump(decision_tree, 'decision_tree_model.pkl')
    # Get predictions from the Python model
    python_predictions = decision_tree.predict(X_test_samples)


    # Save predictions for comparison
    np.savetxt('python_predictions_compare_with_y_test_samples.csv', python_predictions, fmt='%d', delimiter=',')

    # Evaluate the model on validation data
    y_pred = decision_tree.predict(X_val)
    accuracy = np.mean(y_pred == y_val)
    print(f"Validation Accuracy: {accuracy:.2f}")

    # Generate a classification report
    print("\nClassification Report:")
    print(classification_report(y_val, y_pred))

    print("\nConfusion Matrix:")
    print(confusion_matrix(y_val, y_pred))

    return redirect(url_for('index2'))

# Route: Predict Outputs
@app.route('/predict', methods=['POST'])
def predict():
    # Load the Data_Conversion file for prediction
    prediction_file_path = 'Data_Conversion.xlsx'  # Ensure this file exists in the project directory
    df_predict = pd.read_excel(prediction_file_path)
    print("Loaded Data for Prediction:")
    print(df_predict.head())

    # Example of how the input data should be structured (make sure this matches the file's content)
    input_data = []

    # Preprocess the data to match the model's expected input format
    for index2, row in df_predict.iterrows():
        # Assuming 'df_predict' has columns similar to your example input format (one-hot encoding + numerical values)
        row_data = [
            row['brake_next_brake_self'],  # One-hot encoding or categorical values
            row['brake_next_turn_self'],
            row['none_next_brake_self'],
            row['none_next_turn_self'],
            row['none_none'],
            row['Speed_km_h'],  # Numeric value
            row['Relative_Distance_m'],  # Numeric value
            row['Direction_deg'],  # Numeric value
        ]
        input_data.append(row_data)

    # Convert the input data into the same format as the model expects
    X_predict = np.array(input_data)
    print("Input Data for Prediction:", X_predict) 
    
    # Load the trained model
    model = joblib.load('decision_tree_model.pkl')

    # Predict outputs
    predictions = model.predict(X_predict)

    # Print the raw prediction output for debugging
    print("Raw Prediction Output:", predictions)

    # Map predictions to symbolic representations
    symbol_mapping = {
        1: '1 🛑 Emergency Brake',
        2: '2 🐢 Speed Down',
        3: '3 ⚡ Speed Up',
        4: '4 ➡️ Lane Change',
        5: '5 ⏸️ No Action'
    }

    # Convert numerical predictions to symbolic representations
    results = [symbol_mapping.get(pred, 'Unknown') for pred in predictions]

    # Send results to the front-end, including raw prediction for debugging
    return render_template('result.html', results=results, raw_predictions=predictions)


if __name__ == '__main__':
    app.run(debug=True)
