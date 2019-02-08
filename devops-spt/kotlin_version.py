"""Automate management of Kotlin versions"""

def existing():
    """Determine existing Kotlin version"""
    from subprocess import check_output
    # shell=True okay in this case, b/c not building the command from user input
    output = check_output("cat build.gradle.kts | grep '^  kotlin(\"jvm\")'" + \
                          " | sed 's/^  kotlin(\"jvm\") version //'", \
                          shell=True, text=True)
    import re
    # eliminate quotes & trailing newline from output, only match the version
    pattern = re.match(r'"(.+)"', output)
    return pattern.group(1)


def latest():
    """Find latest available Kotlin version"""
    # Use Requests library to track the redirect, guidance here:
    #    https://bit.ly/2JRvapH
    import requests
    req = requests.get('https://github.com/JetBrains/kotlin/releases/latest')
    from urllib.parse import urlparse
    url = urlparse(req.url)
    from os.path import basename
    base = basename(url.path)
    # strip off the leading "v"
    _, rhs = base.split("v", 1)
    return rhs


def update(verbose=False):
    """Update existing to latest Kotlin version"""
    old = existing()
    new = latest()
    if verbose:
        print("existing Kotlin ==> " + old)
        print("latest Kotlin   ==> " + new)
    if old == new:
        if verbose:
            print("Kotlin update not necessary")
    else:
        # Guidance: https://stackoverflow.com/a/17141572
        with open('build.gradle.kts', 'r') as infile:
            filedata = infile.read()
        filedata = filedata.replace(old, new)
        # write the same filename out again
        with open('build.gradle.kts', 'w') as outfile:
            outfile.write(filedata)
        from subprocess import call
        call("dos2unix build.gradle.kts", shell=True)