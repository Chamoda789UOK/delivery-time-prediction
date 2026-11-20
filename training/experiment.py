import numpy as np
from tensorflow import keras
from tensorflow.keras import layers

data = np.load("data.npz")
x_train, y_train = data["x_train"], data["y_train"]
x_val, y_val = data["x_val"], data["y_val"]

configs = [
    {"units": [128, 64, 32], "dropout": 0.0, "lr": 0.001},
    {"units": [128, 64, 32], "dropout": 0.2, "lr": 0.001},
    {"units": [256, 128, 64, 32], "dropout": 0.2, "lr": 0.001},
    {"units": [64, 32], "dropout": 0.1, "lr": 0.0005},
]

for config in configs:
    layer_list = [keras.Input(shape=(x_train.shape[1],))]
    for size in config["units"]:
        layer_list.append(layers.Dense(size, activation="relu"))
        if config["dropout"] > 0:
            layer_list.append(layers.Dropout(config["dropout"]))
    layer_list.append(layers.Dense(1))

    model = keras.Sequential(layer_list)
    model.compile(optimizer=keras.optimizers.Adam(config["lr"]), loss="mse", metrics=["mae"])

    stop = keras.callbacks.EarlyStopping(monitor="val_loss", patience=10, restore_best_weights=True)
    model.fit(x_train, y_train, validation_data=(x_val, y_val),
              epochs=100, batch_size=64, callbacks=[stop], verbose=0)

    loss, mae = model.evaluate(x_val, y_val, verbose=0)
    print(config, "-> validation MAE:", round(mae, 2))