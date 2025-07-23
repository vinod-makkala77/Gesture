import pickle
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Load data
data_dict = pickle.load(open('./data1.pickle', 'rb'))

# Verify and standardize data length
processed_data = []
for sample in data_dict['data']:
    if len(sample) == 42:  # 21 landmarks × 2 coordinates
        processed_data.append(sample)
    elif len(sample) > 42:
        processed_data.append(sample[:42])  # Truncate if longer
    else:
        processed_data.append(np.pad(sample, (0, 42-len(sample))))  # Pad if shorter

data = np.array(processed_data)
labels = np.array(data_dict['labels'])[:len(processed_data)]  # Match labels to processed data

print("Final data shape:", data.shape)
print("Labels shape:", labels.shape)

# Split data
x_train, x_test, y_train, y_test = train_test_split(
    data, labels, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(x_train, y_train)

# Evaluate
y_pred = model.predict(x_test)
print(f"Accuracy: {accuracy_score(y_test, y_pred):.2f}")

# Save model
with open('model.p', 'wb') as f:
    pickle.dump({'model': model}, f)