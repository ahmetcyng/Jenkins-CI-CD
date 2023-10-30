# Jenkins-CI-CD

How to build docker image, push local docker registry and deploy kubernetes cluster using jenkins pipeline

## Environment:

    Virtulation Software: VirtualBox
        
    Servers: Ubuntu Server 22.04 LTS
    
    Server Properties:
      cpu: 2 core
      ram 2 GB
      network: bridge
      storage 25 GB
      
# Steps

## 1-) Create 3 vm with ubuntu server

Before starting server3.py, configue IP.1 section in the config file under the server-3 directory with your own server3 IP address.

## 2-) Start server3.py with args:

      --host: 
      --username:
      --password:

      e.g. "python3 server3.py --host 192.168.2.176 --username server3 --password Password1"

      Some operation must be done manualy in server3
      
      2.a) go auth directory under docker-registry folder and delete registry.password
      
      2.b) create registry.password file with "sudo htpswd -Bc registry.password <registryuser>" command (registryuser going to be using in pipeline and also must be created in jenkins credential)
      
      2.c) access jenkins web ui with browser via "https://<server3ipaddress>:8080/" url
      
      2.d) print jenkins installation password command="cat /var/lib/jenkins/secretes/initialAdminPassword" copy password and complete jenkins installation
      
      2.e) install docker pipeline and ssh pipeline plugins on jenkins also create credential for registery secret 

      2.f) ca.pem certificate file that under /home/server3/certs/ path, must copy to server1 and server2 before k8s cluster initilation 
            e.g. "scp command: sudo scp ca.pem server1@<server1_ip_address>:/home/server1/"
            then reboot both servers.
      
## 3-) Start master.py with args:

        --host: 
        --username:
        --password:

        e.g. "python3 master.py --host 192.168.2.220 --username server1 --password Password1"

    3.a) copy join command. it should be printed on terminal. if join command wasnt print, perform bellow steps:
        connect server1 via ssh
        exec "kubeadm token create --prin-join-command" then copy output

## 4-) Start node.py with args:

      --host: 
      --username:
      --password:
      --token: 
      e.g. "python3 node.py --host 192.168.2.109 --username server2 --password Password1 --token <token that you copy from server1>"

## 5-) Create pipeline job on jenkins:

            Create pipeline job on jenkins.
            Edit server ip addresses from Jenkinsfile that under Jenkinsfile directory

        
    
