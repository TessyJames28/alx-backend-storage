#!/usr/bin/env python3
"""returns the list of school having a specific topic"""


def schools_by_topic(mongo_collection, topic):
    """returns list of school"""
    return mongo_collection.find({"topics": {"$in": [topic]}})
