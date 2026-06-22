# Bash Scripts
Bash scripting projects

---

## Scripts

### `dir_check.sh`

Checks if a target directory exists/creates it if not. Then checks for a specific file inside that directory/creates it if missing. Prints a status message at each decision point and confirms any creation. Ends with a recursive `ls` of the directory to list contents and show creation.

**Output:**

![dir_check output](../../../assets/images/scripting/bash_dir_test.png)

### `umask_calc.sh`

Calculates and displays umask configuration based on either argument or system config, for both directory and file. Also displays associated symbolic permissions.

**Output:**

![umask_calc output](../../../assets/images/scripting/bash_umask_calc.png)

### `lab-setup.sh`

Checks if root; flushes/configures interfaces; updates/upgrades; launches firefox (as user) and launches terminator (as user) with preset layout; kills oldest terminator process to clean up

**Output:**

![setupscript output](../../../assets/images/scripting/setupscript.png)
