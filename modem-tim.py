import paramiko
import time
import os
import sys
import argparse
import speedtest
from colorama import Fore

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--stop", help="Stop SQM.", required=False, action="store_true")
    parser.add_argument("-r", "--restart", help="Restart SQM.", required=False, action="store_true")
    parser.add_argument("-i", "--start", help="Start SQM.", required=False, action="store_true")
    parser.add_argument("-t", "--speedtest", help="Run a Speedtest to check changes...", required=False, action="store_true")
    parser.add_argument("-a", "--address", help="Change IP address. (default: 192.168.1.1)", required=False, action="store_true")
    parser.add_argument("-u", "--username", help="Change Username. (default: root)", required=False, action="store_true")
    parser.add_argument("-p", "--password", help="Change Password. (default: root)", required=False, action="store_true")
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

def are_you_sure_check():
    user_input = input("Are you sure you want to continue?(Y/n)")
    positive = ["Y", "y", "yes", "Yes", "YES", "si", "Si", "SI", "s", "S"]
    if user_input not in positive:
        print("Exiting...")
        sys.exit(0)
    return None

def main():
    #print warning
    print(Fore.RED, "WARNING: This script is for rooted TIM HUBs (DGA 4132) only. If you have a different modem, this script will not work. \n", Fore.RESET)
    print(Fore.YELLOW, "WARNING: This script will not work if you have not installed SQM, or if you have changed the stock port for SSH. \n", Fore.RESET)
    #Are you sure you want to continue?
    are_you_sure_check()

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

    #set stock values if args not specified
    if args.address:
        ip = input("Enter IP: ")
    if args.username:
        username = input("Enter username: ")
    if args.password:
        password = getpass.getpass("Enter password: ")
    if args.address == False and args.username == False and args.password == False:
        ip, username, password = set_stock()

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