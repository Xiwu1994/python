import json


str = '''{"site_id":"d","type":"page_op","element_id":"sign_out","uid":1001712,"ip":"192.168.1.100","extra":"{"access_token":"dfcac52d-4223-42e7-b325-e896fe9c5e0b","channel":"default","devtoken":"","from":"1701","ip":"192.168.1.100","model":"iPhone 5s","osname":"iOS","osversion":"11.2.5","sign":"f0ae909bc37f92648eab297fe2c63d24","time":"2018-02-11 00:03:13","timestamp":"1518278746215","type":"sign_out","udid":"4B14945C-CE93-4DD9-A1A4-A5A6AE693F5A","user_phone_name":"\u201cjiang\u201d\u7684 iPhone","version":"200000000"}","created_at":"2018-02-11 00:05:46"}'''

print json.loads(str)