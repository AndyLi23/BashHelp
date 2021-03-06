# BashHelp

A Python3 script to help with finding commands for Bash and Zsh<br />Optimized for MacOS (<0.1 seconds)

## Adding alias

Go to home in terminal `cd ~` <br />
Do `vi .zprofile` for zsh and `vi .bash_profile` for bash <br />
Add `alias help = "python3 /path/to/help.py"` for help with common commands <br />
Add `alias hi = "python3 /path/to/helpInstalled.py` for help with all installed commands <br />
Restart terminal <br />


## Usage

`help` to help with common and builtin commands. `hi` to help with all installed commands.<br />
`help/hi [command]` to list short info about the command <br />
`help/hi -abcdefhnorsuvx [command]` prints the parts of the man page for the command depending on the arguments. Use `help/hi -a helper` or `help/hi -a --help` to list valid arguments<br />
`help/hi [question]` lists the 3 commands closest to the question <br />
`help/hi -[N] [question]` lists the N commands closest to the question, where N is a whole number <br />

## Requirements

* subprocess
* sys
