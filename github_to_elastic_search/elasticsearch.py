class Github():
    def __init__(self, config):
        self.config = config

# es.push_commits()
# -> for every commit
# -> push to es, using sha as _id


# I might need to refactor the config part





# put
# curl - X PUT "localhost:9200/customer/_doc/1?pretty" - H 'Content-Type: application/json' - d'
# {
#    "name": "John Doe"
# }
# '

# get
# curl - X GET "localhost:9200/customer/_doc/1?pretty"


# idea: the _id field, e.g. /1 can be used for the sha values. If it already exists one can just overwrite the data.
