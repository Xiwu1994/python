#!/usr/bin/env python
#encoding:utf-8
import sys
import time
import random
import threading
reload(sys)
from kafka import SimpleClient, SimpleProducer

sleep_time = 1

def send_beeper2_location():
    kafka = SimpleClient("master:9092")
    producer = SimpleProducer(kafka)
    topic = "mysql__beeper2_location"
    with open("./test_data_beeper2_location") as fp:
        for line in fp:
            producer.send_messages(topic, line.strip())  # kafka传消息
            print line.strip()
            time.sleep(random.random() % sleep_time)


def send_beeper2_drivers():
    kafka = SimpleClient("master:9092")
    producer = SimpleProducer(kafka)
    topic = "mongo__beeper2__drivers"

    with open("./test_data_beeper2__drivers") as fp:
        for line in fp:
            producer.send_messages(topic, line.strip())  # kafka传消息
            print line.strip()
            time.sleep(random.random() % sleep_time)

def send_beeper2_trans_event():
    kafka = SimpleClient("master:9092")
    producer = SimpleProducer(kafka)
    topic = "mysql__beeper_trans_event"

    with open("./test_data_beeper2_trans_event") as fp:
        for line in fp:
            producer.send_messages(topic, line.strip())  # kafka传消息
            print line.strip()
            time.sleep(random.random() % sleep_time)


if __name__ == "__main__":
    t1 = threading.Thread(target=send_beeper2_location)
    t2 = threading.Thread(target=send_beeper2_drivers)
    t3 = threading.Thread(target=send_beeper2_trans_event)

    t1.start()
    t2.start()
    t3.start()
    t1.join()
    t2.join()
    t3.join()
