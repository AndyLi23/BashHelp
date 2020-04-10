from subprocess import check_output
from time import time

# Start timer
start = time()

# Get all installed commands with compgen
output = check_output('compgen -c', shell=True, executable='/bin/bash')
commands = [i.decode('utf-8') for i in output.splitlines()]
commands.sort()

# Get description from an info page
def getDesc(i):
    # Get info page
    info = " ".join(check_output(['info', i]).decode('utf-8').split("\n"))
    info = [i for i in info.split(" ") if i]
    for i in range(len(info)):
        # Parse for "DESCRIPTION"
        if info[i] == "DESCRIPTION":
            desc = ""
            # Save sentence after "DESCRIPTION"
            for j in range(i+1, len(info)):
                if "." not in info[j] :
                    desc += info[j] + " "
                else:
                    desc += info[j][:-1]
                    break
            return desc

# Write descriptions to file
with open("/Users/andyli/Documents/Github/Personal/BashHelp/commands.txt", "w+") as fout:
    for command in commands:
        try:
            fout.write(command + ": " + getDesc(command) + "\n")
        except:
            fout.write(command + "\n")
    fout.close()

# Print time
print("Parsing finished in %.2f" % (time()-start) + " seconds")
