import json 
import random
import time
from datetime import datetime , timezone
from kafka import KafkaProducer

#1. 初始化 kafka producer ， 連線到 redpanda (localhost:9092)
producer  = KafkaProducer(
    bootstrap_servers = ['localhost:19092'],
    value_serializer = lambda v: json.dumps(v).encode('utf-8')
)

# 模擬用的資料
SITES = [1,2,3,4,5]
PAGES = ["/home","/product/detail","/cart","/checkout","/search"]
REFERRERS = [
    "https://www.google.com",
    "https://www.facebook.com",
    "https://www.twitter.com",
    "https://direct",
    "https://line.me"
]
DEVICES = ["Mobile","Desktop","Tablet"]

print("開始向 redpanda topic 發送資料...(Ctrl+C 結束)")

try:
    while True:
        #2. 隨機生成一筆點擊事件
        event = {
            "event_time": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
            "site_id": random.choice(SITES),
            "user_id": random.randint( 1000,9999),
            "page_url": random.choice(PAGES),
            "referrer": random.choice(REFERRERS),
            "ip_address" : f"192.168.1.{random.randint(1,254)}",
            "device_type": random.choice(DEVICES),
            "click_count": 1,
        }
        #3. 發資料到clickstream topic
        producer.send("clickstream_events", value=event)
        producer.flush()
        print(f"sent : site = {event['site_id']}, user = {event['user_id']}, page = {event['page_url']} ")
        
        time.sleep(0.2)  # 每0.2秒發送一筆資料
except KeyboardInterrupt:
    print("停止發送資料")
finally:
    producer.flush()
    producer.close()