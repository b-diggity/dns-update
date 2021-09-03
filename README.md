# dns-update
Update dynamic DNS entries with the current IPs.  Supported platforms are DNSOMATIC and NO-IP. A self-hosted runner in required for this setup. 

DNSOMATIC - This tool provides an interface to udpating your IP for [OpenDNS](https://signup.opendns.com/homefree/), which can be used for DNS security to block known bad DNS requested.  This is a great basic tool for providing some level of security on your home network.  OpenDNS uses your public IP to provide the customized filtering repsonses requested for your network.  DNSOMATIC can also update NOIP.  If you want to use this option, just add another site to the DNSOMATIC list.

[NOIP](https://www.noip.com/) - This site allows you to manage dynamic DNS entries.  This can be for internal or external DNS entries.  For internal addresses, this script will the the leading internal IP for where the runner is installed.

Email alerts will be sent when there are issues.  @outlook.com is the default email platform included in the script for source emails. The outlook email function must be pip installed.

The following environment variables must be set:
- NOIP_USER => NOIP user name html encoded
- NOIP_PASS => NOIP password html encoded
- DNSO_USER => DNSOMATIC user name html encoded
- DNSO_PASS => DNSOMATIC password html encoded
- MAIL_USER_OUTLOOK => Outlook email account to send emails from and to
- MAIL_PASS_OUTLOOK => Password of said email account
- DNS_UPDATES => JSON of NOIP and DNSOMATIC entries to udpate

EXAMPLE OF HTML ENCODING: @ == %40

A file called `dns.json` will be created two levels up from $GITHUB_WORKSPACE by default: ($GITHUB_WORKSPACE/../../dns.json).  The information from the `DNS_UPDATES` ENV var will be used to populate and maintain this file, which is used for state tracking. `DNS_UPDATES` tells this script which hostnames to update IPs for. For NOIP, you can update hostnames with public or private addresses.  For DNSOMATIC, you'll need to provde the site name to update your public IP for.  The private IP will be the IP of the device running this script.  If any one of these aren't used, make that list and empty list.


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
    "Site4"
  ]
}
```