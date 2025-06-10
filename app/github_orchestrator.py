from github import Github
import os

def get_github_client():
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise Exception("GITHUB_TOKEN not set")
    return Github(token)

def list_repo_issues(owner, repo):
    g = get_github_client()
    repository = g.get_repo(f"{owner}/{repo}")
    return [{"title": issue.title, "number": issue.number} for issue in repository.get_issues()]