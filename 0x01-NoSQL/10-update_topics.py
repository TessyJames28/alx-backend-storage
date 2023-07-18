#!/usr/bin/env python3
"""changes all topics of a school document based on the name"""


def update_topics(mongo_collection, name, topics):
    """changes topic based on name"""
    mongo_collection.update_many({"name": name}, {"$set": {"topics": topics}} )
