import paramiko
import argparse
import time

class CreateWorkerNode:
    def __init__(self) -> None:
        parser = argparse.ArgumentParser()
        
        parser.add_argument("--host", "-H")
        parser.add_argument("--username", "-u")
        parser.add_argument("--password", "-p")
        parser.add_argument("--token", "-t")
        
        args = parser.parse_args()
           
        self.host = args.host
        self.username = args.username
        self.password = args.password 
        self.token = args.token
    
    def copy_script(self, ssh_session):
        sftp = ssh_session.open_sftp()             
        sftp.put("node.sh", f"/home/{self.username}/node.sh")
        sftp.close()        
        
    def install(self, ssh_session):
        channel = ssh_session.invoke_shell()
        time.sleep(3)
        channel.send("chmod +x node.sh\n")
        
        time.sleep(3)
        channel.send("./node.sh\n")
        time.sleep(3)
        
        while True:
            s = channel.recv(60000)
            s = s.decode()
            print(s)
            
            if "[sudo]" in s:
                channel.send(f"{self.password}\n")
                
            elif "(y/N)" in s:
                channel.send("y\n")
                
            elif "node created" in s:
                break
            
            time.sleep(0.5)
        
        channel.send(f"sudo {self.token}\n")
        time.sleep(3)
        channel.send(f"{self.password}\n")
            
    def main(self):
        ssh = paramiko.SSHClient() 
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.host, username=self.username, password=self.password)
        
        self.copy_script(ssh_session=ssh)
        self.install(ssh_session=ssh)
        
        ssh.close()
        
        
if __name__ == "__main__":
    crmaster = CreateWorkerNode()
    crmaster.main()
            