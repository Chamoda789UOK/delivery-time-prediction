import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from tensorflow import keras

data = np.load("data.npz")
x_train, y_train = data["x_train"], data["y_train"]
x_test, y_test = data["x_test"], data["y_test"]

model = keras.models.load_model("best_model.keras")
dnn_pred = model.predict(x_test).flatten()

linear = LinearRegression().fit(x_train, y_train)
forest = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1).fit(x_train, y_train)

results = {
    "DNN": dnn_pred,
    "Linear Regression": linear.predict(x_test),
    "Random Forest": forest.predict(x_test),
}

for name, pred in results.items():
    mae = mean_absolute_error(y_test, pred)
    mse = mean_squared_error(y_test, pred)
    print(name)
    print("  MAE :", round(mae, 2))
    print("  MSE :", round(mse, 2))
    print("  RMSE:", round(np.sqrt(mse), 2))
    print("  R2  :", round(r2_score(y_test, pred), 3))

print("negative predictions:", (dnn_pred < 0).sum())

plt.scatter(y_test, dnn_pred, alpha=0.3)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], color="red")
plt.xlabel("Actual (minutes)")
plt.ylabel("Predicted (minutes)")
plt.savefig("actual_vs_predicted.png")
plt.clf()

plt.hist(y_test - dnn_pred, bins=50)
plt.xlabel("Error (minutes)")
plt.ylabel("Count")
plt.savefig("residuals.png")