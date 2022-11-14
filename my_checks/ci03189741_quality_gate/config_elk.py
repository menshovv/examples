
sleep_time = 1
num_retries = 3

ELASTIC_PASSWORD = ""
ELASTIC_USER = ""

def get_json_traceid(application_name,gte,lte):
    return {
                "version": "true",
                "size": 500,
                "sort": [
                    {
                    "@timestamp": {
                        "order": "desc",
                        "unmapped_type": "boolean"
                    }
                    }
                ],
                "aggs": {
                    "2": {
                    "date_histogram": {
                        "field": "@timestamp",
                        "fixed_interval": "30s",
                        "time_zone": "Europe/Moscow",
                        "min_doc_count": 1
                    }
                    }
                },
                "stored_fields": [
                    "*"
                ],
                "script_fields": {},
                "docvalue_fields": [
                    {
                    "field": "@timestamp",
                    "format": "date_time"
                    },
                    {
                    "field": "doc.date",
                    "format": "date_time"
                    },
                    {
                    "field": "doc.log_timestamp",
                    "format": "date_time"
                    },
                    {
                    "field": "doc.time2",
                    "format": "date_time"
                    }
                ],
                "_source": {
                    "excludes": []
                },
                "query": {
                    "bool": {
                    "must": [],
                    "filter": [
                        {
                        "match_all": {}
                        },
                        {
                        "match_phrase": {
                            "doc.service.keyword": application_name
                        }
                        },
                        {
                        "exists": {
                            "field": "doc.traceid.keyword"
                        }
                        },
                        {
                        "range": {
                            "@timestamp": {
                            "gte": gte,
                                    
                            "lte": lte,
                            "format": "epoch_second"
                            }
                        }
                        }
                    ],
                    "should": [],
                    "must_not": []
                    }
                },
                "highlight": {
                    "pre_tags": [
                    "@kibana-highlighted-field@"
                    ],
                    "post_tags": [
                    "@/kibana-highlighted-field@"
                    ],
                    "fields": {
                    "*": {}
                    },
                    "fragment_size": 2147483647
            }
}

def get_json_span(application_name,gte,lte):
    return {
                "version": "true",
                "size": 500,
                "sort": [
                    {
                    "@timestamp": {
                        "order": "desc",
                        "unmapped_type": "boolean"
                    }
                    }
                ],
                "aggs": {
                    "2": {
                    "date_histogram": {
                        "field": "@timestamp",
                        "fixed_interval": "30s",
                        "time_zone": "Europe/Moscow",
                        "min_doc_count": 1
                    }
                    }
                },
                "stored_fields": [
                    "*"
                ],
                "script_fields": {},
                "docvalue_fields": [
                    {
                    "field": "@timestamp",
                    "format": "date_time"
                    },
                    {
                    "field": "doc.date",
                    "format": "date_time"
                    },
                    {
                    "field": "doc.log_timestamp",
                    "format": "date_time"
                    },
                    {
                    "field": "doc.time2",
                    "format": "date_time"
                    }
                ],
                "_source": {
                    "excludes": []
                },
                "query": {
                    "bool": {
                    "must": [],
                    "filter": [
                        {
                        "match_all": {}
                        },
                        {
                        "match_phrase": {
                            "doc.service.keyword": application_name
                        }
                        },
                        {
                        "exists": {
                            "field": "doc.span.keyword"
                        }
                        },
                        {
                        "range": {
                            "@timestamp": {
                            "gte": gte,
                                    
                            "lte": lte,
                            "format": "epoch_second"
                            }
                        }
                        }
                    ],
                    "should": [],
                    "must_not": []
                    }
                },
                "highlight": {
                    "pre_tags": [
                    "@kibana-highlighted-field@"
                    ],
                    "post_tags": [
                    "@/kibana-highlighted-field@"
                    ],
                    "fields": {
                    "*": {}
                    },
                    "fragment_size": 2147483647
            }
}