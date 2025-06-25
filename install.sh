#!/bin/bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
echo "✅ Setup complete!"
echo "Next, set env variables:"
echo "  export TELEGRAM_TOKEN=..."
echo "  export TELEGRAM_CHAT_ID=..."
echo "  export DATA_URL=https://..."
echo "Then run: python main.py"
