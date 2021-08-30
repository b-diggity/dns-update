# dns-update
Update dynamic DNS entries with the correct IPs

This script updates NO-IP and DNSOMATIC.

The following environment variables must be set:
NOIP_USER => NOIP user name html encoded
NOIP_PASS => NOIP password html encoded
DNSO_USER => DNSOMATIC user name html encoded
DNSO_PASS => DNSOMATIC password html encoded
DNS_UPDATES => JSON of NOIP and DNSOMATIC entries to udpate

EXAMPLE OF HTML ENCODING: @ == %40

A file called `dns.json` will be created two levels up from $GITHUB_WORKSPACE: (GITHUB_WORKSPACE/../../dns.json).  The information from the `DNS_UPDATES` ENV var will be used to populate and maintain this file, which is used for state tracking.  The ip keys will be automatically filled in after the first run. `DNS_UPDATES` tells this script which hostnames to update IPs for. For NOIP, you can update hostnames with public or private addresses.  For DNSOMATIC, you'll need to provde the site name to update your public IP for.  The private IP will be the IP of the device running this script.  If any one of these aren't used, make that list and empty list.


```json
{
  "noip": {
    "public": [
      "site1.ddns.net",
      "site2.ddns.net"
    ],
    "private": [
      "site3.ddns.net"
    ]
  },
  "dnsomatic": [
    "MySite"
  ]
}
```