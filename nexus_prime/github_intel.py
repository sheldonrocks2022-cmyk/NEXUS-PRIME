"""Read-only GitHub metadata inspection for public repositories."""
import json
import re
from urllib.request import Request, urlopen
from urllib.parse import quote

def inspect(owner, repo):
    pattern = r"[A-Za-z0-9_.-]{1,100}"
    if not re.fullmatch(pattern, owner) or not re.fullmatch(pattern, repo):
        raise ValueError("Invalid repository identifier")
    url = f"https://api.github.com/repos/{quote(owner)}/{quote(repo)}"
    req = Request(url,headers={"Accept":"application/vnd.github+json","User-Agent":"NexusPrime/0.2"})
    with urlopen(req,timeout=12) as response:
        data = json.loads(response.read(100000))
    return {key:data.get(key) for key in ("full_name","description","default_branch","open_issues_count","stargazers_count","updated_at")}
