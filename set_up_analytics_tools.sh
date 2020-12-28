# This file helps you to set up Elasticsearch, Kibana and Grafana to do you analysis
docker pull elasticsearch:7.9.3
docker pull kibana:7.9.3
docker pull grafana/grafana

# uncomment if you want to stop and delete all other containers first
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
docker network rm somenetwork

docker network create somenetwork
docker run -d --name elasticsearch --net somenetwork -p 9200:9200 -p 9300:9300 elasticsearch:7.9.3
docker run -d --name kibana --net somenetwork -p 5601:5601 kibana:7.9.3

echo "IP of Kibana (Port 5601): "
ip route get 1 | sed -n 's/^.*src \([0-9.]*\) .*$/\1/p'

# Security
# - block external traffic to server using a firewall: ufw allow from YOUR.PUBLIC.IP && ufw enable
# - use ssh -L 1337:remotehost:5601 user@myserver (https://serverfault.com/questions/78351/can-i-create-ssh-to-tunnel-http-through-server-like-it-was-proxy)