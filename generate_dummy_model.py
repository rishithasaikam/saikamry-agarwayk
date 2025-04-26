import pickle
from sklearn.ensemble import RandomForestRegressor

# Step 1: Create some dummy training data
X_train = [[i] for i in range(100)]  # Features: numbers 0 to 99
y_train = [2 * i + 5 for i in range(100)]  # Target: some simple function (2x + 5)

# Step 2: Create and train a simple Random Forest model
model = RandomForestRegressor()
model.fit(X_train, y_train)

# Step 3: Save the model into the models/ directory
pickle.dump(model, open('models/clv_model.pkl', 'wb'))

print("✅ Dummy CLV model created and saved successfully!")
