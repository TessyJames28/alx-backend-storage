#!/usr/bin/env python3
"""provides some stats about Nginx logs stored in MongoDB"""
from pymongo import MongoClient

if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    log = client.logs.nginx
    print("{} logs".format(log.count_documents({})))
    print("Methods:")
    print("\tmethod GET: {}".format(log.count_documents({"method" : "GET"})))
    print("\tmethod POST: {}".format(log.count_documents({"method" : "POST"})))
    print("\tmethod PUT: {}".format(log.count_documents({"method" : "PUT"})))
    print("\tmethod PATCH: {}".format(log.count_documents({"method" : "PATCH"})))
    print("\tmethod DELETE: {}".format(log.count_documents({"method" : "DELETE"})))
    print("{} status check".format(log.count_documents({"path" : "/status"})))
    print("IPs:")
    
    doc = client.logs.nginx.find()
    doc_list = [val['ip'] for val in doc]
    dict_list = {val: doc_list.count(val) for val in set(doc_list)}
    sort_dict = dict(sorted(dict_list.items(), key=lambda item: item[1], reverse=True)[:10])
    for key, val in sort_dict.items():
        print("\t{}: {}".format(key, val))
