from subprocess import check_output
from sys import argv
# Class for comparing question with descriptions

class sentenceComparator:

    # Return value depending on degree of matching fo two strings
    def compareWords(self, a, b):
        temp = 0
        if a == b or a in b:
            # Exact match: return 10 * length
            return len(a) * 10
        for i in range(len(a)):
            if i < len(b):
                if a[i] == b[i]:
                    # Letter & position match: +10
                    temp += 10
            elif a[i] in b:
                # Letter match: + more depending on position difference
                temp += 10 / (abs(b.index(a[i]) - i) + 1)
        return temp

    def compare(self, a, b):
        # Compare keyword
        keyword = b.strip().lower().split(" ")[0]
        keywordMatch = 0
        a_split = [i.lower() for i in a.strip().split(" ") if i]
        for a1 in a_split:
            keywordMatch = max(keywordMatch, self.compareWords(a1, keyword))

        for i in a_split:
            # Keyword in description: +200
            if i == keyword:
                keywordMatch += 200

        # More than 90% match: +100
        if keywordMatch > 9 * len(keyword):
            keywordMatch += 100

        # Compare two sentences
        sentenceMatch = 0
        a_split = [i.lower() for i in a.strip().split(" ") if i]
        b_split = [i.lower() for i in b.strip().split(" ") if i]
        for a1 in a_split:
            temp = 0
            for b1 in b_split:
                # Compare each word in sentence, take max match
                temp += self.compareWords(a1, b1)
            sentenceMatch += temp / ((len(a_split) + len(b_split))/2)

        # Exact description match: +200
        if set(a_split).intersection(set(b_split)) == set(a_split):
            sentenceMatch += 200

        return sentenceMatch + keywordMatch

    def returnInOrder(self, a, ls, n=3):
        l = []
        for i in ls:
            l.append([i, self.compare(a, i)])
        #Sort based on match value
        l.sort(key=lambda x: x[1], reverse=True)
        #Return top N matches
        return [i for i in l[:n]]


class Help():
    def __init__(self, ):

        # parse commands.txt to update commands
        self.commands_to_descr = {}

        with open('/Users/andyli/Documents/Github/Personal/BashHelp/commands.txt', 'r') as f:
           utilities = f.read()

        for j in utilities.split("\n"):
            if len(j.strip().split(" ")) > 1:
                self.commands_to_descr[j.strip().split(" ")[0][:-1]] = j
            else:
                self.commands_to_descr[j.strip()] = j.strip()
        # print(commands_to_descr)

    def takeInput(self, q, c):
        print("\n")
        # takes raw input (q) and parses it
        q = q.strip()

        i = 0
        n = ""
        a = ""
        last = 0
        new = ""

        while i < len(q):
            if q[i] == "-" and q[i-1] != "-":
                # man page section arguments
                if q[i + 1].isalpha():
                    i += 1
                    while i < len(q) and q[i].isalpha():
                        a += q[i]
                        i += 1

                # Top N arguments
                elif q[i+1].isdigit():
                    i += 1
                    while i < len(q) and q[i].isdigit():
                        n += q[i]
                        i += 1
                else:
                    new += q[i]
            else:
                new += q[i]
            i += 1
        if n:
            n = int(n)

        # q is all letters that are not arguments
        q = new.strip()

        try:
            # parse man page
            if a and q != "helper" and q != "--help":
                # most common sections
                sections = ["SEE ALSO", "EXAMPLES", "DESCRIPTION", "SYNOPSIS", "NAME", "OPTIONS", "EXIT STATUS",
                            "RETURN VALUE", "ENVIRONMENT", "BUGS", "FILES", "AUTHORS", "BUG REPORTS", "HISTORY",
                            "COPYRIGHT"]

                # get man page
                manpage = check_output(['man', q]).decode('utf-8').split("\n")

                # store sections
                manpage_split = {}

                # previous section start index, previous section name
                prev, cur = 0, "INTRO"

                for i in range(len(manpage)):
                    # get printable characters
                    temp = ""
                    for j in manpage[i]:
                        if j.isprintable():
                            temp += j

                    for section in sections:
                        # if line is a section header, save section
                        if temp == "".join([i * 2 if i != " " else " " for i in section]):
                            manpage_split[cur] = manpage[prev:i]
                            cur = section
                            prev = i

                # update section storage
                manpage_split[cur] = manpage[prev:len(manpage)]

                # print sections based on keywords
                if "n" in a:
                    if "NAME" in manpage_split.keys():
                        print("\n".join(manpage_split["NAME"]))
                if "s" in a:
                    if "SYNOPSIS" in manpage_split.keys():
                        print("\n".join(manpage_split["SYNOPSIS"]))
                if "d" in a:
                    if "DESCRIPTION" in manpage_split.keys():
                        print("\n".join(manpage_split["DESCRIPTION"]))
                if "x" in a:
                    if "EXAMPLES" in manpage_split.keys():
                        print("\n".join(manpage_split["EXAMPLES"]))
                if "v" in a:
                    if "ENVIRONMENT" in manpage_split.keys():
                        print("\n".join(manpage_split["ENVIRONMENT"]))
                if "e" in a:
                    if "SEE ALSO" in manpage_split.keys():
                        print("\n".join(manpage_split["SEE ALSO"]))
                if "o" in a:
                    if "OPTIONS" in manpage_split.keys():
                        print("\n".join(manpage_split["OPTIONS"]))
                if "t" in a:
                    if "EXIT STATUS" in manpage_split.keys():
                        print("\n".join(manpage_split["EXIT STATUS"]))
                if "r" in a:
                    if "RETURN VALUE" in manpage_split.keys():
                        print("\n".join(manpage_split["RETURN VALUE"]))
                if "f" in a:
                    if "FILES" in manpage_split.keys():
                        print("\n".join(manpage_split["FILES"]))
                if "u" in a:
                    if "AUTHORS" in manpage_split.keys():
                        print("\n".join(manpage_split["AUTHORS"]))
                if "p" in a:
                    if "BUG REPORTS" in manpage_split.keys():
                        print("\n".join(manpage_split["BUG REPORTS"]))
                if "h" in a:
                    if "HISTORY" in manpage_split.keys():
                        print("\n".join(manpage_split["HISTORY"]))
                if "b" in a:
                    if "BUGS" in manpage_split.keys():
                        print("\n".join(manpage_split["BUGS"]))
                if "c" in a:
                    if "COPYRIGHT" in manpage_split.keys():
                        print("\n".join(manpage_split["COPYRIGHT"]))
                if "a" in a:
                    print("\n".join(manpage))

            else:
                # print short description
                print("        " + self.commands_to_descr[q])
        except:
            # print all commands
            if q == "all":
                for val in self.commands_to_descr.values():
                    print("        " + val)
            # print help
            elif q == "helper" or q == "--help" or not q:
                if a:
                    print("Man page parsing options:\n    -a: ALL\n    -b: BUGS\n    -c: COPYRIGHT\n    -d: DESCRIPTION\n    -e: SEE ALSO\n    -f: FILES\n    -h: HISTORY\n    -n: NAME\n    -o: OPTIONS\n    -r: RETURN VALUE\n    -s: SYNOPSIS\n    -u: AUTHOR\n    -v: ENVIRONMENT\n    -x: EXAMPLES")
                else:
                    print(
                    "         Type a command name or question after a space: hi [-abcdefhnorsuvx (for man page)] [-# (# closest matches)] [command/question]. Type 'hi all' to list all commands. Type 'hi -a helper' or 'hi -a --help' for more information on man page arguments.")
            # print version
            elif q == "--version" or q == "-v":
                print("         BashHelp v.0.5.1  –––  Made by Andy Li")
            else:
                # get n closest matches (default is 3), print them
                if n:
                    m = c.returnInOrder(q, self.commands_to_descr.values(), n=n)
                else:
                    m = c.returnInOrder(q, self.commands_to_descr.values(), n=3)

                for i in m:
                    print("        " + i[0])
        print("\n")

# get input


c = sentenceComparator()
h = Help()

if __name__ == "__main__":
    q = ""

    for i, arg in enumerate(argv):
        if i > 0:
            q += arg + " "
    h.takeInput(q, c)

