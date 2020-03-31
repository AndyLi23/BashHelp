# BashHelp


##Adding alias

Go to home in terminal ```cd ~```
Do ```vi .zprofile``` for zsh and ```vi .bash_profile``` for bash
Add ```alias help = "python3 /path/to/help.py"```
Restart terminal


##How to use

Use ```help [command]``` to list short info about the command
```help -a [command]``` prints the man page for the command (will change later)
```help [question]``` lists the 3 commands closest to the question
```help -[N] [question]``` lists the N commands closest to the question, where N is a whole number
