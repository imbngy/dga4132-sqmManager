# TIM HUB (DGA4132) SQM Manager
 A simple tool made to manage TIMHUB(DGA4132)'s SQM state in Python, using Paramiko for SSH communication. 

## Requirements

1. You need to [root](https://www.ilpuntotecnico.com/forum/index.php/topic,78162.0.html) your TIMHUB;
> [!WARNING]
> The root process may be a bit janky, and it could result in bricking your TIMHUB, do it at your own risk.
2. Then you need to [install SQM](https://www.ilpuntotecnico.com/forum/index.php?topic=85190.0).


## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/imbngy/dga4132-sqmManager.git
   ```
2. Navigate to the project directory:
   
   ```bash
   cd dga4132-sqmManager
   ```
3. Install dependencies using `pip`:

   ```bash
   pip install -r requirements.txt
   ```
   
## Usage

Run the script using one of the following methods:

- Option 1: Execute the provided .bat files,
- Option 2: Run the script directly using Python:

  ```bash
  py modem-tim.py
  ```

## Command-line Options

- `-s` or `--stop`: Stop SQM.
- `-r` or `--restart`: Restart SQM.
- `-i` or `--start`: Start SQM.
- `-t` or `--speedtest`: Run a Speedtest to check changes.
- `-a` or `--address`: Change IP address (default: 192.168.1.1).
- `-u` or `--username`: Change Username (default: root).
- `-p` or `--password`: Change Password (default: root).

### Example

```bash
py modem-tim.py -s
```
This command stops SQM on the default IP address (192.168.1.1) with the default username and password.

## Contributing

Feel free to contribute to this project by opening issues or submitting pull requests. Your feedback and improvements are highly appreciated!

## Disclaimer

This project is not affiliated with or endorsed by TIM or any related entities. The TIM logo is a registered trademark of Telecom Italia S.p.A. All product names, logos, and brands are property of their respective owners. The use of these names, logos, and brands does not imply endorsement or affiliation.
