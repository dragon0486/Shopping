import redis
import json

conn = redis.Redis(host='192.168.80.128',port=6379)

# for key in conn.scan_iter("luffy_payment_1_*"):
#     conn.delete(key)

key_list = conn.keys("luffy_payment_1_*")
conn.delete(*key_list)

print(conn.keys())