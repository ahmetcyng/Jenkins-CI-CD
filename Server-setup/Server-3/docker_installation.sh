#! /bin/bash

sudo apt update -y

sudo apt install docker.io -y
sudo apt install docker-compose -y

sudo systemctl start docker

mkdir docker-registry/
mkdir certs/
mkdir auth/

mv certs/ docker-registry/certs/

mv docker-compose.yaml ./docker-registry
mv config ./docker-registry/certs
cd docker-registry/certs/

# Create certificate
openssl genrsa -out cert-key.pem 4096
openssl req -new -x509 -sha256 -days 365 -key cert-key.pem -out ca.pem -config config
openssl req -new -sha256 -subj "/CN=192.168.2.176" -key cert-key.pem -out cert.csr
openssl x509 -req -sha256 -days 365 -in cert.csr -CA ca.pem -CAkey cert-key.pem -out cert.pem -CAcreateserial
openssl verify -CAfile ca.pem -verbose cert.pem

# Add certificate
sudo cp ca.pem /usr/local/share/ca-certificates/ca.crt
sudo update-ca-certificates

sudo apt install apache2-utils -y

sudo usermod -aG docker jenkins

sudo systemctl restart docker

cd /home/server3/docker-registry
sudo docker-compose up -d

echo "docker installation done"