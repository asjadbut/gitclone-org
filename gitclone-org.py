import os
import requests
import subprocess
from urllib.parse import urlparse

def extract_org_name(url):
    # Example: https://github.com/orgs/teslamotors/repositories
    path_parts = urlparse(url).path.strip("/").split("/")
    if "orgs" in path_parts:
        return path_parts[path_parts.index("orgs") + 1]
    return path_parts[0]

def get_repos(org):
    repos = []
    page = 1

    while True:
        api_url = f"https://api.github.com/orgs/{org}/repos?per_page=100&page={page}"
        response = requests.get(api_url)

        if response.status_code != 200:
            print(f"[!] Failed to fetch repos: {response.status_code}")
            break

        data = response.json()
        if not data:
            break

        repos.extend(data)
        page += 1

    return repos

def clone_repo(repo_url, output_dir):
    try:
        subprocess.run(["git", "clone", repo_url], cwd=output_dir, check=True)
    except subprocess.CalledProcessError:
        print(f"[!] Failed to clone {repo_url}")

def main():
    org_url = input("Enter GitHub org URL: ").strip()
    output_dir = "downloaded_repos"

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    org_name = extract_org_name(org_url)
    print(f"[+] Org detected: {org_name}")

    repos = get_repos(org_name)
    print(f"[+] Found {len(repos)} repositories")

    for repo in repos:
        clone_url = repo["clone_url"]
        print(f"[+] Cloning {clone_url}")
        clone_repo(clone_url, output_dir)

    print("[✓] Done.")

if __name__ == "__main__":
    main()
