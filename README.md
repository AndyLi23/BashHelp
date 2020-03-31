# BashHelp


-Adding alias

Go to home in terminal ```cd ~``` <br />
Do ```vi .zprofile``` for zsh and ```vi .bash_profile``` for bash <br />
Add ```alias help = "python3 /path/to/help.py"``` <br />
Restart terminal <br />


-How to use

Use ```help [command]``` to list short info about the command <br />
```help -a [command]``` prints the man page for the command (will change later) <br />
```help [question]``` lists the 3 commands closest to the question <br />
```help -[N] [question]``` lists the N commands closest to the question, where N is a whole number <br />
