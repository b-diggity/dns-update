# dns-update
Update dynamic DNS entries with the correct IPs

This script updates NO-IP and DNSOMATIC.

The following environment variables must be set:
NOIP_USER => NOIP user name html encoded
NOIP_PASS => NOIP password html encoded
DNSO_USER => DNSOMATIC user name html encoded
DNSO_PASS => DNSOMATIC password html encoded

EXAMPLE OF HTML ENCODING: @ == %40

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