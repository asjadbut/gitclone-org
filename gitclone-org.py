import os
import requests
import subprocess
import argparse
from urllib.parse import urlparse

def extract_org_name(url):
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

def filter_repos(repos, repo_type):
    if repo_type == "forked":
        return [r for r in repos if r["fork"]]
    elif repo_type == "original":
        return [r for r in repos if not r["fork"]]
    return repos  # "all"

def clone_repo(repo_url, output_dir):
    try:
        subprocess.run(["git", "clone", repo_url], cwd=output_dir, check=True)
    except subprocess.CalledProcessError:
        print(f"[!] Failed to clone {repo_url}")

def main():
    parser = argparse.ArgumentParser(description="Download GitHub org repositories")
    parser.add_argument("org_url", help="GitHub org URL")
    parser.add_argument(
        "--type",
        choices=["all", "forked", "original"],
        default="all",
        help="Filter repositories (default: all)"
    )
    parser.add_argument(
        "--output",
        default="downloaded_repos",
        help="Output directory"
    )

    args = parser.parse_args()

    if not os.path.exists(args.output):
        os.makedirs(args.output)

    org_name = extract_org_name(args.org_url)
    print(f"[+] Org detected: {org_name}")

    repos = get_repos(org_name)
    print(f"[+] Total repos found: {len(repos)}")

    filtered_repos = filter_repos(repos, args.type)
    print(f"[+] Repos after filter ({args.type}): {len(filtered_repos)}")

    for repo in filtered_repos:
        clone_url = repo["clone_url"]
        print(f"[+] Cloning {clone_url}")
        clone_repo(clone_url, args.output)

    print("[✓] Done.")

if __name__ == "__main__":
    main()
