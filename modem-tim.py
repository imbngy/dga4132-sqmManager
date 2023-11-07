import paramiko
import time
import os
import sys
import argparse
import speedtest
from colorama import Fore
import getpass
import json

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--stop", help="Stop SQM.", required=False, action="store_true")
    parser.add_argument("-r", "--restart", help="Restart SQM.", required=False, action="store_true")
    parser.add_argument("-i", "--start", help="Start SQM.", required=False, action="store_true")
    parser.add_argument("-t", "--speedtest", help="Run a Speedtest to check changes...", required=False, action="store_true")
    parser.add_argument("-c", "--config", help="Configure the script.", required=False, action="store_true")
    parser.add_argument("-y", "--yes", help="Skip the 'Are you sure?' prompt.", required=False, action="store_true")
    args = parser.parse_args()
    return args

#change these if you cba using args
def set_stock():
    ip = "192.168.1.1"
    username = "root"
    password = "root"
    return ip, username, password

def connect(ip, username, password):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, username=username, password=password)
        return ssh
    except Exception as e:
        print(e)
        return None
    
def send_commands(command, ssh):
    print("Sending command: \n"f"{command} \n")
    match command:
        case "/etc/init.d/sqm stop":
            err = "It is likely that SQM is already stopped."
        case "/etc/init.d/sqm restart":
            pass
        case "/etc/init.d/sqm start":
            err = "It is likely that SQM is already started."
        case _:
            pass
    stdin, stdout, stderr = ssh.exec_command(command)
    output = stdout.read()
    if output:
        print(output.decode("utf-8"))
    stderr = stderr.read()
    if stderr:
        print(stderr.decode("utf-8"))
        if "Not found" in stderr.decode("utf-8"):
            print(Fore.YELLOW, f"NOTE: {err}\n", Fore.RESET)
    time.sleep(2) #wait for command to execute
    print(Fore.GREEN, "Command sent", Fore.RESET)
    return None

def speed_test():
    print("Starting speed test")
    #make a loading animation for the speed test
    s = speedtest.Speedtest()

    print("Finding best server...")
    s.get_best_server()
    print("Server found")

    print("Testing download speed...")
    s.download()
    
    print("Testing upload speed...")
    s.upload()
    
    res = s.results.dict()
    print("Speed test completed. \n")
    print("Speed test results:")
    print("Server: " + res["server"]["sponsor"])
    print("Download: " + str(res["download"]/1000000) + " Mbps")
    print("Upload: " + str(res["upload"]/1000000) + " Mbps")
    print("Ping: " + str(res["ping"]) + " ms")
    return None

def are_you_sure_check(yes):
    if yes:
        return None
    #check if user wants to continue
    user_input = input("Are you sure you want to continue?(Y/n)")
    positive = ["Y", "y", "yes", "Yes", "YES", "si", "Si", "SI", "s", "S"]
    if user_input not in positive:
        print("Exiting...")
        sys.exit(0)
    return None

def config_f(stock):
    print(Fore.YELLOW,"Configuring script...", Fore.RESET)
    if not stock:
        config = {}
        config["ip"] = input("Enter IP (default:192.168.1.1) :")
        config["username"] = input("Enter username (default: root) :")
        config["password"] = getpass.getpass("Enter password (default: root) :")
        config["first_run"] = False
    else:
        ip, username, password = set_stock()
        config = {}
        config["ip"] = ip
        config["username"] = username
        config["password"] = password
        config["first_run"] = False
    with open("config.json", "w") as f:
        json.dump(config, f)
    #wait for config file to be created
    time.sleep(2)
    print("Configured!")

def check_if_stock():
    print(Fore.GREEN, "Do you want to use stock values? \n", Fore.RESET)
    stock = input("Y/n: ")
    if stock not in ["Y", "y", "yes", "Yes", "YES", "si", "Si", "SI", "s", "S"]:
        stock = False
    else:
        stock = True
    return stock
    

def main():

    yes = False
    #check if user wants to skip the 'Are you sure?' prompt
    if "-y" in sys.argv or "--yes" in sys.argv:
        yes = True
    

    print(r"""
         
            ████████╗██╗███╗   ███╗    ███╗   ███╗ ██████╗ ██████╗ ███████╗███╗   ███╗
            ╚══██╔══╝██║████╗ ████║    ████╗ ████║██╔═══██╗██╔══██╗██╔════╝████╗ ████║
               ██║   ██║██╔████╔██║    ██╔████╔██║██║   ██║██║  ██║█████╗  ██╔████╔██║
               ██║   ██║██║╚██╔╝██║    ██║╚██╔╝██║██║   ██║██║  ██║██╔══╝  ██║╚██╔╝██║
               ██║   ██║██║ ╚═╝ ██║    ██║ ╚═╝ ██║╚██████╔╝██████╔╝███████╗██║ ╚═╝ ██║
               ╚═╝   ╚═╝╚═╝     ╚═╝    ╚═╝     ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝╚═╝     ╚═╝
          
                        ░█▀▀░▄▀▄░█▄█░░░█▄█░█▀█░█▀█░█▀█░█▀▀░█▀▀░█▀▄
                        ░▀▀█░█\█░█░█░░░█░█░█▀█░█░█░█▀█░█░█░█▀▀░█▀▄
                        ░▀▀▀░░▀\░▀░▀░░░▀░▀░▀░▀░▀░▀░▀░▀░▀▀▀░▀▀▀░▀░▀
          """)

    #check args
    args = parse_args()
    
    if not args.yes:
        print(Fore.RED, "WARNING: This script is for rooted TIM HUBs (DGA 4132) only. If you have a different modem, this script will not work. \n", Fore.RESET)
        print(Fore.YELLOW, "WARNING: This script will not work if you have not installed SQM, or if you have changed the stock port for SSH. \n", Fore.RESET)
    #Are you sure you want to continue?
    are_you_sure_check(yes)

    #check if user wants to configure the script
    if args.config:
        config_f(stock=False)

    #check if config file exists
    if os.path.isfile("config.json"):
        with open("config.json", "r") as f:
            config = json.load(f)
        #check if first run, if so, ask if user wants to use stock values
        if config["first_run"]:
            stock = check_if_stock()
            config_f(stock)
        #load config
        ip = config["ip"]        
        username = config["username"]
        print(Fore.GREEN, f"Using conf: {username}@{ip}", Fore.RESET)
        password = config["password"]
    else:
        #if config file does not exist, ask if user wants to use stock values
        print(Fore.YELLOW, "Config file not found... ", Fore.RESET)
        stock = check_if_stock()
        config_f(stock)
        with open("config.json", "r") as f:
            config = json.load(f)
        #load config
        ip = config["ip"]
        username = config["username"]
        print(Fore.GREEN, f"Using conf: {username}@{ip}", Fore.RESET)
        password = config["password"]

    #connect to modem
    ssh = connect(ip, username, password)
    if ssh is None:
        print(Fore.RED, "Connection failed", Fore.RESET)
        sys.exit(1)
    print(Fore.GREEN, "Connected! \n", Fore.RESET)
    #check action args
    if args.stop == False and args.restart == False and args.start == False:
        print(Fore.YELLOW,"You must specify an action e.g. -s for stop, -r for restart, -i for start. Use -h for help.", Fore.RESET)
        ssh.close()
        sys.exit(1)

    #send commands
    if args.stop:
        stop_command = "/etc/init.d/sqm stop"
        send_commands(stop_command, ssh)
    if args.restart:
        restart_command = "/etc/init.d/sqm restart"
        send_commands(restart_command, ssh)
    if args.start:
        start_command = "/etc/init.d/sqm start"
        send_commands(start_command, ssh)
    
    ssh.close()
    print("Exiting... \n")

    #speed test
    if args.speedtest == False:
        sys.exit(0)
    
    speed_test()
    return None
    
if __name__ == "__main__":
    main()