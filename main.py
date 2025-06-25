import os, traceback
import pandas as pd, joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from telegram import Bot
import requests

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
bot = Bot(token=BOT_TOKEN)

def send(msg):
    bot.send_message(chat_id=CHAT_ID, text=msg)

def fetch_data():
    url = os.getenv("DATA_URL")
    return pd.read_csv(url)

def preprocess(df):
    df.fillna(method='ffill', inplace=True)
    df['result'] = df.apply(
        lambda r: 1 if r.home_goals > r.away_goals else (0 if r.home_goals == r.away_goals else -1),
        axis=1
    )
    return pd.get_dummies(df)

def train_and_predict(df):
    X = df.drop(columns=['home_goals','away_goals','result'])
    y = df['result']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    acc = accuracy_score(y_test, model.predict(X_test))
    joblib.dump(model, "model.pkl")
    return model, acc

def predict(model, df):
    return model.predict(df.drop(columns=['home_goals','away_goals','result']))[:5]

def main():
    try:
        df = fetch_data()
        df = preprocess(df)
        model, acc = train_and_predict(df)
        preds = predict(model, df)
        send(f"✅ Trained. Acc: {acc:.2f} | Sample preds: {preds.tolist()}")
    except Exception:
        err = traceback.format_exc()
        send(f"❌ Error:\n{err}")
        raise

if _name_ == "_main_":
    main()
