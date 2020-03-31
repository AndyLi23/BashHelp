import sys, subprocess, time
import nltk.corpus
import nltk.tokenize.punkt
from nltk.corpus import wordnet
from string import punctuation


class sentenceComparator:

    def __init__(self):
        self.stopwords = nltk.corpus.stopwords.words('english')
        self.stopwords.extend(punctuation)
        self.stopwords.append('')

    # Get default English stopwords and extend with punctuation

    def get_wordnet_pos(self, pos_tag):
        if pos_tag[1].startswith('J'):
            return pos_tag[0], wordnet.ADJ
        elif pos_tag[1].startswith('V'):
            return pos_tag[0], wordnet.VERB
        elif pos_tag[1].startswith('N'):
            return pos_tag[0], wordnet.NOUN
        elif pos_tag[1].startswith('R'):
            return pos_tag[0], wordnet.ADV
        else:
            return pos_tag[0], wordnet.NOUN

    # Create tokenizer and stemmer

    def is_ci_lemma_stopword_set_match(self, a, b, threshold=0.5):
        """Check if a and b are matches."""
        tokens_a = [token.lower().strip(punctuation) for token in nltk.tokenize.word_tokenize(a) \
                    if token.lower().strip(punctuation) not in self.stopwords]
        tokens_b = [token.lower().strip(punctuation) for token in nltk.tokenize.word_tokenize(b) \
                    if token.lower().strip(punctuation) not in self.stopwords]

        # Calculate Jaccard similarity
        ratio = len(set(tokens_a).intersection(tokens_b)) / float(len(set(tokens_a).union(tokens_b)))
        return ratio

    def returnInOrder(self, a, ls, n=3):
        l = []
        for i in ls:
            l.append([i, self.is_ci_lemma_stopword_set_match(a, i)])
        l.sort(key=lambda x: x[1], reverse=True)
        return [i[0] for i in l[:n]]



class Help():
    def __init__(self, ):
        # default commands
        self.commands_to_descr = {'apropos': '        apropos  Search Help manual pages (man -k)',
                                  'apt-get': '        apt-get  Search for and install software packages (Debian/Ubuntu)',
                                  'aptitude': '        aptitude Search for and install software packages (Debian/Ubuntu)',
                                  'aspell': '        aspell   Spell Checker',
                                  'awk': '        awk      Find and Replace text, database sort/validate/index',
                                  'basename': '        basename Strip directory and suffix from filenames',
                                  'base32': '        base32   Base32 encode/decode data and print to standard output',
                                  'base64': '        base64   Base64 encode/decode data and print to standard output',
                                  'bash': '        bash     GNU Bourne-Again SHell',
                                  'bc': '        bc       Arbitrary precision calculator language',
                                  'bg': '        bg       Send to background',
                                  'bind': '        bind     Set or display readline key and function bindings',
                                  'break': '        break    Exit from a loop',
                                  'builtin': '        builtin  Run a shell builtin',
                                  'bzip2': '        bzip2    Compress or decompress named file(s)',
                                  'cal': '        cal      Display a calendar',
                                  'case': '        case     Conditionally perform a command',
                                  'cat': '        cat      Concatenate and print (display) the content of files',
                                  'cd': '        cd       Change Directory',
                                  'cfdisk': '        cfdisk   Partition table manipulator for Linux',
                                  'chattr': '        chattr   Change file attributes on a Linux file system',
                                  'chgrp': '        chgrp    Change group ownership',
                                  'chmod': '        chmod    Change access permissions',
                                  'chown': '        chown    Change file owner and group',
                                  'chpasswd': '        chpasswd Update passwords in batch mode',
                                  'chroot': '        chroot   Run a command with a different root directory',
                                  'chkconfig': '        chkconfig System services (runlevel)',
                                  'cksum': '        cksum    Print CRC checksum and byte counts',
                                  'clear': '        clear    Clear terminal screen',
                                  'cmp': '        cmp      Compare two files',
                                  'comm': '        comm     Compare two sorted files line by line',
                                  'command': '        command  Run a command - ignoring shell functions',
                                  'continue': '        continue Resume the next iteration of a loop',
                                  'cp': '        cp       Copy one or more files to another location',
                                  'cpio': '        cpio     Copy files to and from archives',
                                  'cron': '        cron     Daemon to execute scheduled commands',
                                  'crontab': '        crontab  Schedule a command to run at a later time',
                                  'csplit': '        csplit   Split a file into context-determined pieces',
                                  'curl': '        curl     Transfer data  from or to a server',
                                  'cut': '        cut      Divide a file into several parts',
                                  'date': '        date     Display or change the date & time',
                                  'dc': '        dc       Desk Calculator',
                                  'dd': '        dd       Data Duplicator - convert and copy a file, write disk headers, boot records',
                                  'ddrescue': '        ddrescue Data recovery tool',
                                  'declare': '        declare  Declare variables and give them attributes',
                                  'df': '        df       Display free disk space',
                                  'diff': '        diff     Display the differences between two files',
                                  'diff3': '        diff3    Show differences among three files',
                                  'dig': '        dig      DNS lookup',
                                  'dir': '        dir      Briefly list directory contents',
                                  'dircolors': "        dircolors Colour setup for 'ls'",
                                  'dirname': '        dirname  Convert a full pathname to just a path',
                                  'dirs': '        dirs     Display list of remembered directories',
                                  'dmesg': '        dmesg    Print kernel & driver messages',
                                  'du': '        du       Estimate file space usage',
                                  'echo': '        echo     Print message',
                                  'egrep': '        egrep    Search file(s) for lines that match an extended expression',
                                  'eject': '        eject    Eject removable media',
                                  'enable': '        enable   Enable and disable builtin shell commands',
                                  'env': '        env      Environment variables',
                                  'ethtool': '        ethtool  Ethernet card settings',
                                  'eval': '        eval     Evaluate several commands/arguments',
                                  'exec': '        exec     Execute a command',
                                  'exit': '        exit     Exit the shell',
                                  'expect': '        expect   Automate arbitrary applications accessed over a terminal',
                                  'expand': '        expand   Convert tabs to spaces',
                                  'export': '        export   Set an environment variable',
                                  'expr': '        expr     Evaluate expressions',
                                  'false': '        false    Do nothing, unsuccessfully',
                                  'fdformat': '        fdformat Low-level format a floppy disk',
                                  'fdisk': '        fdisk    Partition table manipulator for Linux',
                                  'fg': '        fg       Send job to foreground',
                                  'fgrep': '        fgrep    Search file(s) for lines that match a fixed string',
                                  'file': '        file     Determine file type',
                                  'find': '        find     Search for files that meet a desired criteria',
                                  'fmt': '        fmt      Reformat paragraph text',
                                  'fold': '        fold     Wrap text to fit a specified width.',
                                  'for': '        for      Expand words, and execute commands',
                                  'format': '        format   Format disks or tapes',
                                  'free': '        free     Display memory usage',
                                  'fsck': '        fsck     File system consistency check and repair',
                                  'ftp': '        ftp      File Transfer Protocol',
                                  'function': '        function Define Function Macros',
                                  'fuser': '        fuser    Identify/kill the process that is accessing a file',
                                  'gawk': '        gawk     Find and Replace text within file(s)',
                                  'getopts': '        getopts  Parse positional parameters',
                                  'grep': '        grep     Search file(s) for lines that match a given pattern',
                                  'groupadd': '        groupadd Add a user security group',
                                  'groupdel': '        groupdel Delete a group',
                                  'groupmod': '        groupmod Modify a group',
                                  'groups': '        groups   Print group names a user is in',
                                  'gzip': '        gzip     Compress or decompress named file(s)',
                                  'hash': '        hash     Remember the full pathname of a name argument',
                                  'head': '        head     Output the first part of file(s)',
                                  'help': '        help     Display help for a built-in command',
                                  'history': '        history  Command History',
                                  'hostname': '        hostname Print or set system name',
                                  'htop': '        htop     Interactive process viewer',
                                  'iconv': '        iconv    Convert the character set of a file',
                                  'id': "        id       Print user and group id's",
                                  'if': '        if       Conditionally perform a command',
                                  'ifconfig': '        ifconfig Configure a network interface',
                                  'ifdown': '        ifdown   Stop a network interface',
                                  'ifup': '        ifup     Start a network interface up',
                                  'import': '        import   Capture an X server screen and save the image to file',
                                  'install': '        install  Copy files and set attributes',
                                  'iostat': '        iostat   Report CPU and i/o statistics',
                                  'ip': '        ip       Routing, devices and tunnels',
                                  'jobs': '        jobs     List active jobs',
                                  'join': '        join     Join lines on a common field',
                                  'kill': '        kill     Kill a process by specifying its PID',
                                  'killall': '        killall  Kill processes by name',
                                  'less': '        less     Display output one screen at a time',
                                  'let': '        let      Perform arithmetic on shell variables',
                                  'link': '        link     Create a link to a file',
                                  'ln': '        ln       Create a symbolic link to a file',
                                  'local': '        local    Create a function variable',
                                  'locate': '        locate   Find files',
                                  'logname': '        logname  Print current login name',
                                  'logout': '        logout   Exit a login shell',
                                  'look': '        look     Display lines beginning with a given string',
                                  'lpc': '        lpc      Line printer control program',
                                  'lpr': '        lpr      Off line print', 'lprint': '        lprint   Print a file',
                                  'lprintd': '        lprintd  Delete a print job',
                                  'lprintq': '        lprintq  List the print queue',
                                  'lprm': '        lprm     Remove jobs from the print queue',
                                  'lsattr': '        lsattr   List file attributes on a Linux second extended file system',
                                  'lsblk': '        lsblk    List block devices',
                                  'ls': '        ls       List information about file(s)',
                                  'lsof': '        lsof     List open files',
                                  'lspci': '        lspci    List all PCI devices',
                                  'make': '        make     Recompile a group of programs',
                                  'man': '        man      Help manual',
                                  'mapfile': '        mapfile  Read lines from standard input into an indexed array variable',
                                  'mkdir': '        mkdir    Create new folder(s)',
                                  'mkfifo': '        mkfifo   Make FIFOs (named pipes)',
                                  'mkfile': '        mkfile   Make a file',
                                  'mkisofs': '        mkisofs  Create an hybrid ISO9660/JOLIET/HFS filesystem',
                                  'mknod': '        mknod    Make block or character special files',
                                  'mktemp': '        mktemp   Make a temporary file',
                                  'more': '        more     Display output one screen at a time',
                                  'most': '        most     Browse or page through a text file',
                                  'mount': '        mount    Mount a file system',
                                  'mtools': '        mtools   Manipulate MS-DOS files',
                                  'mtr': '        mtr      Network diagnostics (traceroute/ping)',
                                  'mv': '        mv       Move or rename files or directories',
                                  'mmv': '        mmv      Mass Move and rename (files)',
                                  'nc': '        nc       Netcat, read and write data across networks',
                                  'netstat': '        netstat  Networking connections/stats',
                                  'nft': '        nft      nftables for packet filtering and classification',
                                  'nice': '        nice     Set the priority of a command or job',
                                  'nl': '        nl       Number lines and write files',
                                  'nohup': '        nohup    Run a command immune to hangups',
                                  'notify-send': '        notify-send  Send desktop notifications',
                                  'nslookup': '        nslookup Query Internet name servers interactively',
                                  'open': '        open     Open a file in its default application',
                                  'op': '        op       Operator access',
                                  'passwd': '        passwd   Modify a user password',
                                  'paste': '        paste    Merge lines of files',
                                  'pathchk': '        pathchk  Check file name portability',
                                  'Perf': '        Perf     Performance analysis tools for Linux',
                                  'ping': '        ping     Test a network connection',
                                  'pgrep': '        pgrep    List processes by name',
                                  'pkill': '        pkill    Kill processes by name',
                                  'popd': '        popd     Restore the previous value of the current directory',
                                  'pr': '        pr       Prepare files for printing',
                                  'printcap': '        printcap Printer capability database',
                                  'printenv': '        printenv Print environment variables',
                                  'printf': '        printf   Format and print data',
                                  'ps': '        ps       Process status',
                                  'pushd': '        pushd    Save and then change the current directory',
                                  'pv': '        pv       Monitor the progress of data through a pipe',
                                  'pwd': '        pwd      Print Working Directory',
                                  'quota': '        quota    Display disk usage and limits',
                                  'quotacheck': '        quotacheck Scan a file system for disk usage',
                                  'ram': '        ram      ram disk device',
                                  'rar': '        rar      Archive files with compression',
                                  'rcp': '        rcp      Copy files between two machines',
                                  'read': '        read     Read a line from standard input',
                                  'readarray': '        readarray Read from stdin into an array variable',
                                  'readonly': '        readonly Mark variables/functions as readonly',
                                  'reboot': '        reboot   Reboot the system',
                                  'rename': '        rename   Rename files',
                                  'renice': '        renice   Alter priority of running processes',
                                  'remsync': '        remsync  Synchronize remote files via email',
                                  'return': '        return   Exit a shell function',
                                  'rev': '        rev      Reverse lines of a file',
                                  'rm': '        rm       Remove files',
                                  'rmdir': '        rmdir    Remove folder(s)',
                                  'rsync': '        rsync    Remote file copy (Synchronize file trees)',
                                  'screen': '        screen   Multiplex terminal, run remote shells via ssh',
                                  'scp': '        scp      Secure copy (remote file copy)',
                                  'sdiff': '        sdiff    Merge two files interactively',
                                  'sed': '        sed      Stream Editor',
                                  'select': '        select   Accept keyboard input',
                                  'seq': '        seq      Print numeric sequences',
                                  'set': '        set      Manipulate shell variables and functions',
                                  'sftp': '        sftp     Secure File Transfer Program',
                                  'shift': '        shift    Shift positional parameters',
                                  'shopt': '        shopt    Shell Options',
                                  'shutdown': '        shutdown Shutdown or restart linux',
                                  'sleep': '        sleep    Delay for a specified time',
                                  'slocate': '        slocate  Find files', 'sort': '        sort     Sort text files',
                                  'source': "        source   Run commands from a file '.'",
                                  'split': '        split    Split a file into fixed-size pieces',
                                  'ss': '        ss       Socket Statistics',
                                  'ssh': '        ssh      Secure Shell client (remote login program)',
                                  'stat': '        stat     Display file or file system status',
                                  'strace': '        strace   Trace system calls and signals',
                                  'su': '        su       Substitute user identity',
                                  'sudo': '        sudo     Execute a command as another user',
                                  'sum': '        sum      Print a checksum for a file',
                                  'suspend': '        suspend  Suspend execution of this shell',
                                  'sync': '        sync     Synchronize data on disk with memory',
                                  'tail': '        tail     Output the last part of file',
                                  'tar': '        tar      Store, list or extract files in an archive',
                                  'tee': '        tee      Redirect output to multiple files',
                                  'test': '        test     Evaluate a conditional expression',
                                  'time': '        time     Measure Program running time',
                                  'timeout': '        timeout  Run a command with a time limit',
                                  'times': '        times    User and system times',
                                  'touch': '        touch    Change file timestamps',
                                  'top': '        top      List processes running on the system',
                                  'tput': '        tput     Set terminal-dependent capabilities, color, position',
                                  'traceroute': '        traceroute Trace Route to Host',
                                  'trap': '        trap      Execute a command when the shell receives a signal',
                                  'tr': '        tr       Translate, squeeze, and/or delete characters',
                                  'true': '        true     Do nothing, successfully',
                                  'tsort': '        tsort    Topological sort',
                                  'tty': '        tty      Print filename of terminal on stdin',
                                  'type': '        type     Describe a command',
                                  'ulimit': '        ulimit   Limit user resources',
                                  'umask': '        umask    Users file creation mask',
                                  'umount': '        umount   Unmount a device',
                                  'unalias': '        unalias  Remove an alias',
                                  'uname': '        uname    Print system information',
                                  'unexpand': '        unexpand Convert spaces to tabs',
                                  'uniq': '        uniq     Uniquify files',
                                  'units': '        units    Convert units from one scale to another',
                                  'unrar': '        unrar    Extract files from a rar archive',
                                  'unset': '        unset    Remove variable or function names',
                                  'unshar': '        unshar   Unpack shell archive scripts',
                                  'until': '        until    Execute commands (until error)',
                                  'uptime': '        uptime   Show uptime',
                                  'useradd': '        useradd  Create new user account',
                                  'userdel': '        userdel  Delete a user account',
                                  'usermod': '        usermod  Modify user account',
                                  'users': '        users    List users currently logged in',
                                  'uuencode': '        uuencode Encode a binary file',
                                  'uudecode': '        uudecode Decode a file created by uuencode',
                                  'v': "        v        Verbosely list directory contents ('ls -l -b')",
                                  'vdir': "        vdir     Verbosely list directory contents ('ls -l -b')",
                                  'vi': '        vi       Text Editor',
                                  'vmstat': '        vmstat   Report virtual memory statistics',
                                  'w': '        w        Show who is logged on and what they are doing',
                                  'wait': '        wait     Wait for a process to complete',
                                  'watch': '        watch    Execute/display a program periodically',
                                  'wc': '        wc       Print byte, word, and line counts',
                                  'whereis': "        whereis  Search the user's $path, man pages and source files for a program",
                                  'which': "        which    Search the user's $path for a program file",
                                  'while': '        while    Execute commands',
                                  'who': '        who      Print all usernames currently logged in',
                                  'whoami': "        whoami   Print the current user id and name ('id -un')",
                                  'wget': '        wget     Retrieve web pages or files via HTTP, HTTPS or FTP',
                                  'write': '        write    Send a message to another user',
                                  'xargs': '        xargs    Execute utility, passing constructed argument list(s)',
                                  'xdg-open': "        xdg-open Open a file or URL in the user's preferred application.",
                                  'xz': '        xz       Compress or decompress .xz and .lzma files',
                                  'yes': '        yes      Print a string until interrupted',
                                  'zip': '        zip      Package and compress (archive) files.',
                                  '.': '        . (./)   Run a command script',
                                  '|': '        |        Takes standard output of one command and passes it as the input to another',
                                  '!!': '        !!       Run the last command again',
                                  '###': '        ###      Comment / Remark'}

        # parse commands.txt to update commands
        # with open('/Users/andyli/Documents/Github/Personal/Learn-CS/commands.txt', 'r') as f:
        #    utilities = f.read()
        #
        # for j in utilities.split("\n"):
        #    commands_to_descr[j.strip().split(" ")[0]] = j
        #
        # print(commands_to_descr)

    def takeInput(self, q, c):
        q = q.strip()

        # parse input
        i = 0
        n = ""
        a = False
        last = 0
        new = ""

        while i < len(q):
            if q[i] == "-":
                if q[i + 1] == "a":
                    i += 1
                    a = True
                    last = i + 1
                else:
                    i += 1
                    while i < len(q) and q[i].isdigit():
                        n += q[i]
                        i += 1
                        last = i
            else:
                new += q[i]
            i += 1
        if n:
            n = int(n)

        q = new.strip()

        try:
            # print man page (TODO: format based on more args)
            if a:
                manpage = subprocess.check_output(['man', q])
                manpage = manpage.decode('utf-8')
                print(manpage)
            # print short description
            else:
                print(self.commands_to_descr[q])
        except:
            # print all commands
            if q == "all":
                for val in self.commands_to_descr.values():
                    print(val)
            # print help
            elif q == "helper" or q == "--help" or not q:
                print(
                    "         Type a command name or question after a space: help [-a (for more detail)] [-# (# closest)] [command/question]. Type 'help all' to list all commands.")
            # print version
            elif q == "--version" or q == "-v":
                print("         BashHelp v.0.5.1  –––  Made by Andy Li")
            else:
                t = time.time()
                # get n closest matches (default is 3), print them
                if n:
                    m = c.returnInOrder(q, self.commands_to_descr.values(), n=n)
                else:
                    m = c.returnInOrder(q, self.commands_to_descr.values(), n=3)
                for i in m:
                    print(i)

# get input

c = sentenceComparator()
h = Help()

q = ""

if __name__ == "__main__":
    for i, arg in enumerate(sys.argv):
        if i > 0:
            q += arg + " "

h.takeInput(q, c)
