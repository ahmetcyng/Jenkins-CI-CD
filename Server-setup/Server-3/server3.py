import os
import paramiko
import argparse
import time


class app:
    def __init__(self):
        parser = argparse.ArgumentParser()
        
        parser.add_argument("--host", "-H")
        parser.add_argument("--username", "-u")
        parser.add_argument("--password", "-p")
        
        args = parser.parse_args()
           
        self.host = args.host
        self.username = args.username
        self.password = args.password 
        
        self.commands = ["chmod +x ./jenkins_installation.sh", "chmod +x ./docker_installation.sh", \
            "sudo ./jenkins_installation.sh", "sudo ./docker_installation.sh"]
    
    def send_scripts(self, ssh_session):
        sftp = ssh_session.open_sftp()             
            
        sftp.put("jenkins_installation.sh", f"/home/{self.username}/jenkins_installation.sh")
        sftp.put("docker_installation.sh", f"/home/{self.username}/docker_installation.sh")
        sftp.put("docker-compose.yaml", f"/home/{self.username}/docker-compose.yaml")
        sftp.put("config", f"/home/{self.username}/config")
        sftp.close()        
        
    def start_docker_installation(self, ssh_session):
        channel = ssh_session.invoke_shell()
        time.sleep(3)
        channel.send(f"{self.commands[3]}\n")
        time.sleep(3)
        channel.send(f"{self.password}\n")
        time.sleep(1)
        
        while True:
            s = channel.recv(60000)
            s = s.decode()
            print(s)
            
            if "[Y/n]" in s:
                channel.send("y\n")
                time.sleep(3)
                
            elif "docker installation done" in s:
                break
            
            time.sleep(0.5)
            
    def start_jenkins_installation(self, ssh_session):
        stdin, stdout, stderr = ssh_session.exec_command(self.commands[0])
        stdin, stdout, stderr = ssh_session.exec_command(self.commands[1])
        
        channel = ssh_session.invoke_shell()
        time.sleep(3)
        channel.send(f"{self.commands[2]}\n")
        time.sleep(3)
        channel.send(f"{self.password}\n")
        
        while True:
            s = channel.recv(60000)
            s = s.decode()
            print(s)
            
            if "(y|n)" in s :
                channel.send("y\n")
                time.sleep(3)
                break
            
            time.sleep(0.5)
        
        time.sleep(1)
        tmp = channel.recv(1024).decode()
        print(tmp)
        
    def copy_script_to_host(self):
        ssh = paramiko.SSHClient() 
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.host, username=self.username, password=self.password)
    
        self.send_scripts(ssh_session=ssh)
        self.start_jenkins_installation(ssh_session=ssh)
        self.start_docker_installation(ssh_session=ssh)
        
        ssh.close()
        
asd = app()
asd.copy_script_to_host()