# Fax Meets Internet

This is a small project where I try my hand at Flask (python backend for web apps.) It serves a webpage that allows a user to submit a message, which gets printed out of the attached thermal printer. I have implemented this with a Raspberry Pi 3, however I'm sure it is easily adaptable to other machines.

# Usage

*Not actually too sure what I did, take all this with a grain of salt.*  
**Update the Pi as usual**

    sudo apt-get update
    sudo apt-get upgrade  
**Install pip and nginx**

    sudo apt-get install python3-pip nginx  
    
**Clone the repo**  
    git clone https://github.com/CWright2022/iot_thermal_printer  

**Configure Nginx**  
My nginx config file `/etc/nginx/sites-enabled/default` looks like this:
Obviously, replace `your.domain.or.ip.here` with your actual domain or IP.

    server {
	    listen 80;
	    server_name your.domain.or.ip.here;
	    access_log  /var/log/nginx/example.log;

	    location / {
	        proxy_pass http://127.0.0.1:8000;
	        proxy_set_header Host $host;
	        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
		}
	}


**I then followed [this](https://howtoraspberrypi.com/enable-port-serial-raspberry-pi/) guide to get my serial port working.**

**Install Flask and Gunicorn**

    pip3 install flask gunicorn
**Optional (but highly recommended) - create a systemd service for gunicorn**  
Copy the following (that I took from somewhere online) to a file (named something like gunicorn.service) in `/lib/systemd/system`.  
Obviously, replace `/wherever/you/cloned/the/repo` with the path to `app.py`.  

    [Service]
    Type=notify
    # the specific user that our service will run as
    User=pi
    Group=pi
    RuntimeDirectory=gunicorn
    WorkingDirectory=/wherever/you/cloned/the/repo
    ExecStart=/usr/local/bin/gunicorn app:app
    ExecReload=/bin/kill -s HUP $MAINPID
    KillMode=mixed
    TimeoutStopSec=5
    PrivateTmp=true
    
    [Install]
    WantedBy=multi-user.target
**Enable and start the above created service**  
*(replace "gunicorn.service" with whatever you named your service file)*  

    sudo systemctl daemon-reload
    sudo systemctl enable gunicorn.service
    sudo systemctl start gunicorn.service  
    
**Add the following to your crontab (use crontab -e to edit your crontab)**  
0 * * * * echo "0" > /wherever/you/cloned/this/hourly_count.txt  
This allows the hourly count to reset once per hour, on the hour.  

# Security
**PLEASE CHANGE THE DEFAULT PASSWORD FOR THE PI USER!!!**  
Run `passwd` on the Pi and follow the prompts.  

**DO NOT EXPOSE PORT 22 TO THE INTERNET!!!**  
The web server is plain HTTP (not HTTPS by default - no encryption!) and runs on port 80. It is OK to expose port 80 to the internet to let your friends send you messages, but DO NOT FORWARD PORT 22! For those unaware, this is the port that SSH runs on - by exposing this you are going to get a lot of chinese bots trying to log in with credentials like `admin:password` or `pi:raspberry`.  

**THIS SERVER IS HTTP BY DEFAULT!**  
By default, this server uses regular ol' HTTP over port 80. While this isn't inherently insecure, especially not for a hobby project, keep in mind that there is no encryption going on between client and server. Anyone with Wireshark and a box in between you and the server can sniff your traffic. I'm not overly concerned with this because it's just silly messages, just something to keep in mind.  

**I MAKE NO GUARANTEES TO THE SECURITY OF THIS WEB APP**  
Being a Computing Security major, I have tried my best to make this web app secure. However, I am just a first year. There very well may be an XSS exploit or other vulnerability that I have not caught yet. As is such, I make no guarantees to the security of this application and assume no responsibility if your Pi is hacked as a result of running my app.
