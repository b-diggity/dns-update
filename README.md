# dns-update
Update dynamic DNS entries with the correct IPs

This script updates NO-IP and DNSOMATIC.

You must create a dns.json file: /opt/scripts/data/dns.json
The ip keys will be automatically filled in after the first run.
If a DNS entry should be udpated with the private IP, set the private key to true.

`{
  "noip": [
    {
      "dns": "mydomain1.ddns.net",
      "ip": ""
    },
    {
      "dns": "mydomain2.ddns.net",
      "ip": "",
      "private": "true"
    }
  ],
  "dnsomatic": "true",
  "dnsomatic_ip": "",
  "dnsomatic_name": "MyName"
}`