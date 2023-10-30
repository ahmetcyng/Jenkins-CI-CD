#! /bin/bash

sudo apt update -y
sudo apt install openjdk-17-jre -y

curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key | sudo tee \
    /usr/share/keyrings/jenkins-keyring.asc > /dev/null

echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] \
    https://pkg.jenkins.io/debian-stable binary/ | sudo tee \
    /etc/apt/sources.list.d/jenkins.list > /dev/null

#java -Djenkins.install.runSetupWizard=false -jar jenkins.war

sudo apt update -y
sudo apt install jenkins -y

systemctl restart jenkins

sudo ufw allow 8080
sudo ufw enable 


