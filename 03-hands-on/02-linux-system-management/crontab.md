# Crontab Scheduling

## Cron Overview

```bash
NAME
       cron - daemon to execute scheduled commands (Vixie Cron)
DESCRIPTION
       cron is directly invoked by systemd(1) on entering multi-user runlevels. 
```

---

## Crontab Overview

```bash
NAME
       crontab - maintain crontab files for individual users (Vixie Cron)
DESCRIPTION
       crontab is the program used to install, deinstall or list the tables used to drive the cron(8) daemon in Vixie
       Cron. Each user can have their own crontab, and though these are files in /var/spool/cron/crontabs, they are not
       intended to be edited directly.
```

Essentially, crontab is used for scheduling specific tasks/commands to run at scheduled times

---

## Commands / Steps

```bash
# List the crontab for the current user
crontab -l

# Edit the crontab for the current user
crontab -e

# Edit the crontab for the root user
sudo crontab -e

# List the crontab for a specific user
sudo crontab -l -u USER

# Edit the crontab for a specific user
sudo crontab -e -u USER

# Make sure cron service is enabled at boot
sudo systemctl enable cron.service
```

---

## Examples

| Sequence                   | Schedule                      |
|----------------------------|----------------------------------|
| @reboot date >> ~/date.txt | Logs date/time to a file at boot |
| \* \* \* \* \* date >> ~/date.txt | Logs date/time every minute of every hour |
| \*/1 \* \* \* \* date >> ~/date.txt| Also logs date/time every minute of every hour |
| 1 \* \* \* \* date >> ~/date.txt | Logs date/time at every first minute of every hour |
| \* 2 \* \* \* date >> ~/date.txt | Logs date/time at every minute in the second hour |
| \* \* 3 \* \* date >> ~/date.txt | Logs date/time at every minute on the third day of the month |
| \* \* \* 4 \* date >> ~/date.txt | Logs date/time at every minute in April |
| \* \* \* \* 5 date >> ~/date.txt | Logs date/time at every minute on Fridays |
| \* \* \* \* 0 date >> ~/date.txt | Logs date/time at every minute on Sundays (or set to 7) |
| 23 0-20/2 \* \* \* date >> ~/date.txt | Logs date/time at minute 23 past every second hour from 0 through 20 |
| 5 4 \* \* sun date >> ~/date.txt | Logs date/time at 04:05 on every Sunday |
| 6 3,12 1 \*/2 \* date >> ~/date.txt | Logs date/time at minute 6 past hours 3 and 12 on the first day in every second month |

---

| Symbol   | Value       |
|----------|-------------|
| `*`     | any value      |
| `,`     | list seperator      |
| `-`     | ranges      |
| `/`     | step values |

---

| Place             | Allowed values                   |
|-------------------|----------------------------------|
| minute            | 0 - 59                           |
| hour              | 0 - 23                           |
| day               | 1 - 31                           |
| month             | 1 - 12 (or JAN - DEC)            |
| day of the week   | 0 - 6 (or SUN - SAT)             |

---

## Visual

```bash
* * * * *  command
│ │ │ │ └─ day of week
│ │ │ └─── month
│ │ └───── day of month
│ └─────── hour
└───────── minute
```

---

## Notes / Gotchas

- Cool crontab calculator: https://crontab.guru/