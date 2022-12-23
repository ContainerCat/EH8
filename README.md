# Welcome to the najort program
This small project is made for the python part of ethical hacking.

## Getting started
1. Clone the repository.
```bash
git clone git@github.com:vanHooijdonkC/EH8.git
```

2. Make a fine-grained access token to this repository on your github. \
go to settings > Developer settings > personal access tokens > fine-grained tokens > generate new token > choose the right repository and read/write rights

3. Copy the token, paste in the root directory in "mytoken.txt".

4. Be sure to change the repository name and user.
* in github-client.py => line 18 and 20
* in whoisd.py => line 14 and 16

5. Run the client
```bash
sudo python github-client.py
```
This needs to be run as "sudo" as we're running a module with Scapy. 

6. Run the logger
After running the client, you can decide to show all data collected of the system. In order to do this:

```bash
python whoisd.py
```

## Module
The module I chose to work out, is made with Scapy. We previously had an excercise with this particular library. Turned out I quite liked it, so I decided to work with this module.
It will scan your internal(!) network, return the active hosts, their open ports and operating system.  

## logging
The logging module, whoisd (who is data), is made to read all files in your repo under /data. It will then be displayed in your console.