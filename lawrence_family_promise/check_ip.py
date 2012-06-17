import smtplib
import socket
import os

"""
Jason Novinger
6/17/2012
A quick one-off to email an alert when a router's public IP address changes. Saves a whopping $5/mo!
"""

# where to store previous results
file = '/tmp/router_ip_address'

# ensure file exists
if not os.path.isfile(file):
   open(file, 'w').close()

# setup email info
to = ''
user = ''
pw = ''

# hacky way to get public interfaces ip address
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('gmail.com', 80))
current_ip = s.getsockname()[0]

# check against previous, send email and record if different
with open(file, 'r+') as f:
    old_ip = f.read().strip()
    if old_ip != current_ip:
        # send an email
        serv = smtplib.SMTP('smtp.gmail.com', 587)
        serv.ehlo(); serv.starttls(); serv.ehlo()
        serv.login(user, pw)
        msg = "To: %s\nFrom: %s\nSubject: new ip address\nOh dear, I seem to have been given a new IP address -- %s" % (to, user, current_ip)
        serv.sendmail(user, to, msg)
        serv.close()
	f.truncate(0)
	f.seek(0, 0)
        f.writelines(current_ip)
