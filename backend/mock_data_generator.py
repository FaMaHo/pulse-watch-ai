import requests
import random
import time
from datetime import datetime

API_URL = "http://localhost:8000"

def generate_reading(abnormal=False):
    if abnormal:
        hr = random.choice([random.randint(35, 48), random.randint(130, 180)])
        spo2 = random.uniform(85, 92) if random.random() < 0.3 else random.uniform(95, 100)
    else:
        hr = random.randint(60, 100)
        spo2 = random.uniform(95, 100)
    
    return {
        "heart_rate": hr,
        "spo2": round(spo2, 1),
        "signal_quality": random.choice(["excellent", "good"]),
        "timestamp": datetime.utcnow().isoformat()
    }

def simulate_watch(num_readings=20):
    print("🏥 Starting Pulse Watch simulation...\n")
    
    for i in range(num_readings):
        # 70% normal, 30% abnormal
        reading = generate_reading(abnormal=(random.random() < 0.3))
        
        response = requests.post(f"{API_URL}/api/readings", json=reading)
        
        if response.status_code == 200:
            hr = reading['heart_rate']
            marker = "⚠️" if (hr > 120 or hr < 50) else "✅"
            print(f"{marker} Reading {i+1}: HR={hr}, SpO2={reading['spo2']}")
        else:
            print(f"❌ Error: {response.text}")
        
        time.sleep(1)
    
    # Show stats
    stats = requests.get(f"{API_URL}/api/stats").json()
    print(f"\n📊 Summary:")
    print(f"   Total readings: {stats['total_readings']}")
    print(f"   Anomalies detected: {stats['total_anomalies']}")
    print(f"   Average HR: {stats['avg_heart_rate']} BPM")

if __name__ == "__main__":
    simulate_watch(20)