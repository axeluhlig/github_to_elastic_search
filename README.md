
Periodically push your git meta data to elasticsearch for further analysis.

## Setup
1. `mv sample_config.ini config.ini`
1. Enter your Github access data, Elasticsearch URl and target repository into the `config.ini`
1. `pip3 install -r requirements.txt`
1. `./main.py`

You can use the `./set_up_analytics_tools.sh` to start up elasticsearch, Kibana and Grafana on your local machine. 