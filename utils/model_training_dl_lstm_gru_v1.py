import os
import json
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, f1_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import random
from sklearn.ensemble import RandomForestClassifier
import pandas as pd

# Reproducibility
SEED = 42
random.seed(SEED)
np.random.seed(SEED)
tf.random.set_seed(SEED)

# Load JSON sequence data
SEQUENCE_LENGTH = 150
NUM_FEATURES = 6  # x, y, velocity, acceleration, jerk, curvature

def load_sequences_from_folder(folder_path, label):
    sequences = []
    labels = []
    for fname in os.listdir(folder_path):
        if fname.endswith(".json"):
            with open(os.path.join(folder_path, fname), 'r') as f:
                data = json.load(f)

            try:
                xys = np.array(data['mouseMovements'])
                ts = np.array(data['timestamps'])
                acc = np.array(data['accelerations'])
                jerk = np.array(data['jerks'])
                curvature = np.array(data['curvatures'])
            except KeyError as e:
                print(f"Missing key {e} in {fname}, skipping.")
                continue

            if len(xys) < 2 or len(ts) < 2:
                continue

            xys = np.array(xys)
            ts = np.array(ts)
            dt = np.diff(ts)
            dt[dt == 0] = 1e-6
            velocity = np.linalg.norm(np.diff(xys, axis=0), axis=1) / dt
            velocity = np.concatenate(([0], velocity))

            seq = np.stack([
                xys[:, 0],  # x
                xys[:, 1],  # y
                velocity,
                acc,
                jerk,
                curvature
            ], axis=1)

            if seq.shape[0] >= SEQUENCE_LENGTH:
                seq = seq[:SEQUENCE_LENGTH]
            else:
                pad = np.zeros((SEQUENCE_LENGTH - seq.shape[0], seq.shape[1]))
                seq = np.vstack((seq, pad))

            sequences.append(seq)
            labels.append(label)
    return np.array(sequences), np.array(labels)

# Load both truthful and deceptive
truthful_seq, truthful_labels = load_sequences_from_folder("data/truthful_responses", 0)
deceptive_seq, deceptive_labels = load_sequences_from_folder("data/deceptive_responses", 1)

X = np.concatenate([truthful_seq, deceptive_seq], axis=0)
y = np.concatenate([truthful_labels, deceptive_labels], axis=0)

# 70/20/10 split
X_temp, X_test, y_temp, y_test = train_test_split(X, y, test_size=0.1, stratify=y, random_state=SEED)
X_train, X_val, y_train, y_val = train_test_split(X_temp, y_temp, test_size=2/9, stratify=y_temp, random_state=SEED)

# Model definition
inputs = tf.keras.Input(shape=(SEQUENCE_LENGTH, NUM_FEATURES))
x = tf.keras.layers.LSTM(64, return_sequences=True)(inputs)
x = tf.keras.layers.GRU(64)(x)
x = tf.keras.layers.Dense(64, activation='relu')(x)
x = tf.keras.layers.Dropout(0.3)(x)
outputs = tf.keras.layers.Dense(1, activation='sigmoid')(x)

model = tf.keras.Model(inputs, outputs)
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Training
history = model.fit(
    X_train, y_train,
    validation_data=(X_val, y_val),
    epochs=50,
    batch_size=32,
    callbacks=[tf.keras.callbacks.EarlyStopping(patience=5, restore_best_weights=True)]
)

# Save the best model
model.save("best_lstm_gru_model.h5")
print("✅ Model saved as best_lstm_gru_model.h5")

# Evaluation
y_pred = (model.predict(X_test) > 0.5).astype(int)
print("\n✅ Final Evaluation on Test Set")
print("Macro F1:", f1_score(y_test, y_pred, average='macro'))
print(classification_report(y_test, y_pred))

# Confusion matrix
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Truthful', 'Deceptive'], yticklabels=['Truthful', 'Deceptive'])
plt.title("Confusion Matrix")
plt.xlabel("Predicted Label")
plt.ylabel("True Label")
plt.tight_layout()
plt.savefig("confusion_matrix.png")
plt.show()

# Training & Validation Loss Plot
plt.figure(figsize=(8, 5))
plt.plot(history.history['loss'], label='Train Loss')
plt.plot(history.history['val_loss'], label='Val Loss')
plt.title("Training and Validation Loss")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("training_validation_loss.png")
plt.show()

# Feature importance from summary statistics using RandomForest
X_flat = X_train.reshape((X_train.shape[0], -1))

# Create meaningful feature names
feature_types = ['x', 'y', 'velocity', 'acceleration', 'jerk', 'curvature']
feature_names = []
for time_step in range(SEQUENCE_LENGTH):
    for feat_type in feature_types:
        feature_names.append(f"{feat_type}_t{time_step}")

rf = RandomForestClassifier(n_estimators=100, random_state=SEED)
rf.fit(X_flat, y_train)
importances = rf.feature_importances_

importance_df = pd.DataFrame({"Feature": feature_names, "Importance": importances})
importance_df = importance_df.sort_values("Importance", ascending=False)

# Get top 10 features
top_10_features = importance_df.head(10)['Feature'].values
top_10_indices = [feature_names.index(f) for f in top_10_features]

# Plot feature importance for top 20
plt.figure(figsize=(12, 6))
sns.barplot(data=importance_df.head(20), x="Importance", y="Feature")
plt.title("Top 20 Features by Importance")
plt.tight_layout()
plt.savefig("feature_importance.png")
plt.show()

# Feature Correlation Matrix for top 10 features (triangular version)
X_top10 = X_flat[:, top_10_indices]
corr_matrix = np.corrcoef(X_top10, rowvar=False)

# Create mask for upper triangle
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))

plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, 
            mask=mask,
            annot=True, 
            fmt=".2f", 
            cmap="coolwarm", 
            center=0,
            vmin=-1,
            vmax=1,
            xticklabels=top_10_features,
            yticklabels=top_10_features,
            square=True)
plt.title("Feature Correlation Matrix")
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)
plt.tight_layout()
plt.savefig("feature_correlation_matrix.png")
plt.show()