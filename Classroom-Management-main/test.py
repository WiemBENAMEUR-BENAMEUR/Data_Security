import requests

url = 'http://localhost:8090/JSON/core/view/alerts/'

response = requests.get(url)
data = response.json()

with open('zap_alerts_report.txt', 'w', encoding='utf-8') as f:
    for alert in data.get("alerts", []):
        f.write(f"Alert ID: {alert.get('id')}\n")
        f.write(f"Alert Name: {alert.get('alert')}\n")
        f.write(f"Risk Level: {alert.get('risk')}\n")
        f.write(f"Confidence: {alert.get('confidence')}\n")
        f.write(f"URL: {alert.get('url')}\n")
        f.write(f"Method: {alert.get('method')}\n")
        f.write(f"Parameter: {alert.get('param')}\n")
        f.write(f"Evidence: {alert.get('evidence')}\n")
        f.write(f"Description: {alert.get('description')}\n")
        f.write(f"Solution: {alert.get('solution')}\n")
        f.write("-" * 50 + "\n")

print("Report saved to zap_alerts_report.txt")
