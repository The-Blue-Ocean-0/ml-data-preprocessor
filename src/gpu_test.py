# gpu_test.py

import lightgbm as lgb
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# ✅ データ生成（3クラス × 2クラスタ分 → n_informative>=3にする）
X, y = make_classification(
    n_samples=1000,
    n_features=20,
    n_informative=5,
    n_redundant=0,
    n_classes=3,
    random_state=42
)

# データ分割
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# LightGBM Dataset
train_data = lgb.Dataset(X_train, label=y_train)
test_data = lgb.Dataset(X_test, label=y_test)

# GPU使用のためのパラメータ
params = {
    'device': 'gpu',
    'gpu_platform_id': 0,
    'gpu_device_id': 0,
    'boosting_type': 'gbdt',
    'objective': 'multiclass',
    'metric': 'multi_logloss',
    'num_class': 3,
    'verbosity': -1
}

# モデル学習
print("🚀 Training with GPU...")
model = lgb.train(
    params,
    train_data,
    valid_sets=[test_data],
    num_boost_round=100,
    callbacks=[
        lgb.early_stopping(stopping_rounds=10),
        lgb.log_evaluation(period=10)
    ]
)

# 推論と評価
y_pred = model.predict(X_test)
y_pred_labels = y_pred.argmax(axis=1)
acc = accuracy_score(y_test, y_pred_labels)

print(f"✅ GPU Test Successful! Accuracy: {acc:.4f}")
