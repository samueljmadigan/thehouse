# alerts.py
import requests

# PASTE YOUR LONG LINK INSIDE THE QUOTES BELOW
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1470960955583365151/ppNDapgk5YEf7-BFT8ZLDU_P3KLH8NeCPL5OuZKohRA_vvnL4EYDngdugOjbRArx8Uev"

def send_discord_alert(bet):
    if "YOUR_ACTUAL_LINK" in DISCORD_WEBHOOK_URL:
        print("❌ Error: You forgot to paste the Webhook URL in alerts.py!")
        return

    # Logic: Green for high value (>5%), Blue for normal
    color = 5763719 if bet.ev > 0.05 else 3447003

    payload = {
        "embeds": [
            {
                "title": "🚨 VALUE BET FOUND",
                "color": color,
                "fields": [
                    {"name": "Match", "value": bet.game, "inline": False},
                    {"name": "Bet", "value": f"{bet.team} @ {bet.bookmaker.upper()}", "inline": True},
                    {"name": "Odds", "value": str(bet.odds), "inline": True},
                    {"name": "Edge", "value": f"**{bet.ev:.2%}**", "inline": True},
                    {"name": "Kelly Stake", "value": f"${bet.kel_stake:.2f}", "inline": False},
                    {"name": "True Prob", "value": f"{bet.true_prob:.1%}", "inline": True}
                ],
                "footer": {"text": "MarketIntelPro Quant Engine"}
            }
        ]
    }

    try:
        requests.post(DISCORD_WEBHOOK_URL, json=payload)
        print(f"✅ Alert sent to Discord for {bet.team}")
    except Exception as e:
        print(f"Failed to send alert: {e}")