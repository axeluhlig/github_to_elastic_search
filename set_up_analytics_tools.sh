# This file helps you to set up Elasticsearch, Kibana and Grafana to do you analysis

docker pull elasticsearch:7.9.3
docker pull kibana:7.9.3
docker pull grafana/grafana

# uncomment if you want to stop and delete all other containers first
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
docker network rm somenetwork

docker network create somenetwork
docker run -d --name elasticsearch --net somenetwork -p 9200:9200 -p 9300:9300 -e "xpack.security.enabled=true" -e "discovery.type=single-node" -e "xpack.security.http.ssl.enabled=true" -e "ELASTIC_PASSWORD=asdf" elasticsearch:7.9.3
docker run -d --name kibana --net somenetwork -p 5601:5601 -e "xpack.security.enabled=true" -e "ELASTICSEARCH_PASSWORD=asdf" kibana:7.9.3
docker ps

# Enter docker to set up security: docker exec -it [els-container-id] bash
# Set up passwords: docker exec [els-container-id] /bin/bash -c "bin/elasticsearch-setup-passwords auto --batch --url https://localhost:9200"

echo "IP of Kibana (Port 5601): "
ip route get 1 | sed -n 's/^.*src \([0-9.]*\) .*$/\1/p'
# If you want to protect your services, here is a HowTo: https://www.elastic.co/guide/en/elasticsearch/reference/current/security-getting-started.html
# mounting config file into ELS: -v full_path_to/custom_elasticsearch.yml:/usr/share/elasticsearch/config/elasticsearch.yml

# Alternativly - is better, user comfort will be higher
# - block external traffic to server using a firewall
# - use ssh -L 1337:remotehost:5601 user@myserver (https://serverfault.com/questions/78351/can-i-create-ssh-to-tunnel-http-through-server-like-it-was-proxy)