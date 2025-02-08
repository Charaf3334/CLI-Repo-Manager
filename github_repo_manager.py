import requests
import time
import os
from colorama import init as colorama_init
from colorama import Fore as color
from colorama import Style
from git import Repo
import socket

def triggerErrorAuth(username, token=None):
    
    url = f"https://api.github.com/users/{username}"

    headers = {}
    if token:
        headers['Authorization'] = f"token {token}"
    response = requests.get(url, headers=headers)
    if response.status_code == 401:
        return True
    return False

def triggerNoUsername(username, token=None):
    
    url = f"https://api.github.com/users/{username}"

    headers = {}
    if token:
        headers['Authorization'] = f"token {token}"
    response = requests.get(url, headers=headers)
    if response.status_code == 404:
        return True
    return False

def getGithubRepos(username, token=None):

    url = f"https://api.github.com/users/{username}/repos"
    
    headers = {}
    if token:
        headers['Authorization'] = f"token {token}"
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        repos = response.json()
        return [repo['name'] for repo in repos]
    else:
        print(f"{color.RED}Failed to retrieve repositories: {Style.RESET_ALL}{response.status_code}")
        return []


def getGithubFollowers(username, token=None):
    
    url = f"https://api.github.com/users/{username}/followers"

    headers = {}
    if token:
        headers['Authorization'] = f"token {token}"

    followers = []
    page = 1
    per_page = 100

    while len(followers) < 200:
        response = requests.get(url, headers=headers, params={'page': page, 'per_page': per_page})
        
        if response.status_code == 200:
            page_followers = response.json()
            if not page_followers:
                break  
            followers.extend(page_followers)
            if len(page_followers) < per_page:
                break  
            page += 1
        else:
            print(f"{color.RED}Failed to retrieve followers: {Style.RESET_ALL}{response.status_code}")
            break
    
    return [follower['login'] for follower in followers[:200]]


def getGithubFollowings(username, token=None):

    url = f"https://api.github.com/users/{username}/following"

    headers = {}
    if token:
        headers['Authorization'] = f"token {token}"

    followings = []
    page = 1
    per_page = 100

    while len(followings) < 200:
        response = requests.get(url, headers=headers, params={'page': page, 'per_page': per_page})
        
        if response.status_code == 200:
            page_followings = response.json()
            if not page_followings:
                break  
            followings.extend(page_followings)
            if len(page_followings) < per_page:
                break  
            page += 1
        else:
            print(f"{color.RED}Failed to retrieve followings: {Style.RESET_ALL}{response.status_code}")
            break
    
    return [following['login'] for following in followings[:200]]

def getGithubProfileLink(username, token=None):
    
    url = f"https://api.github.com/users/{username}"

    headers = {}
    if token:
        headers['Authorization'] = f"token {token}"
    
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        profileLink = response.json()
        return profileLink['html_url']
    else:
        print(f"{color.RED}Failed to retrieve Github profile link: {Style.RESET_ALL}{response.status_code}")
        return []

def getGithubJoinedDate(username, token=None):

    url = f"https://api.github.com/users/{username}"

    headers = {}
    if token:
        headers['Authorization'] = f"token {token}"
    
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        dateJoined = response.json()
        return dateJoined['created_at']
    else:
        print(f"{color.RED}Failed to retrieve the joined date: {Style.RESET_ALL}{response.status_code}")
        return []
    
def getGithubFullName(username, token=None):

    url = f"https://api.github.com/users/{username}"

    headers = {}
    if token:
        headers['Authorization'] = f"token {token}"
    
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        fullName = response.json()
        return fullName['name']
    else:
        print(f"{color.RED}Failed to retrieve the fullname: {Style.RESET_ALL}{response.status_code}")
        return []

def isDirectoryEmpty(path):
    
    if not os.path.exists(path):
        parent_dir = os.path.dirname(path)
        if os.path.exists(parent_dir) and os.path.isdir(parent_dir):
            return True
        else:
            print(f"{color.RED}{parent_dir} doesn't exist.{Style.RESET_ALL}")
            return False
    elif os.path.isdir(path):
        return len(os.listdir(path)) == 0
    return False

def cloneRepository(username, repos, path):
    repo_url = f"https://github.com/{username}/{repos}.git"
    path = os.path.normpath(path)
    if path == '/':
        print(f"{color.RED}Not a valid path{Style.RESET_ALL}")
        return
    if not isDirectoryEmpty(path):
        if os.path.exists(path) and len(os.listdir(path)) > 0:
            print(f"{color.RED}You must have an empty directory to clone the repo.{Style.RESET_ALL}")
            print(f"{color.RED}{os.path.split(path)[1]}: Is not an empty directory.{Style.RESET_ALL}")
            return
        else:
            print(f"{color.RED}{os.path.split(path)[1]}Not a valid path{Style.RESET_ALL}")
            return
    print("Wait please ...")
    time.sleep(3)
    Repo.clone_from(repo_url, path)
    print(f"{color.GREEN}Repository cloned successfully!{Style.RESET_ALL}")

def checkInputs(_input):
    if not _input:
        return True
    return False

def isInternetAvailable():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        return False

# main
def main():

    colorama_init()

    if not isInternetAvailable():
        print(f"{color.GREEN}Connecting to server ...{Style.RESET_ALL}")
        time.sleep(3)
        print(f"{color.RED}Cannot establish connection ... please check your internet and try again.{Style.RESET_ALL}")
        return
    else:
        print(f"{color.GREEN}Connecting to server ...{Style.RESET_ALL}")
        time.sleep(3)
    
    print(f"{color.GREEN}Enter Github Username:{Style.RESET_ALL}")
    username = input()
    if checkInputs(username):
        print(f"{color.RED}You have to enter a username.{Style.RESET_ALL}")
        return 
    print()
    print(f"{color.GREEN}Enter your token here:{Style.RESET_ALL}")
    token = input()
    if checkInputs(token):
        print(f"{color.RED}You have to enter your token.{Style.RESET_ALL}")
        return

    if triggerErrorAuth(username, token):
        print(f"{color.RED}Authentification failed.{Style.RESET_ALL}")
        return
    
    if triggerNoUsername(username, token):
        print(f"{color.RED}'{username}': Username doesn't exist{Style.RESET_ALL}")
        return

    repos = getGithubRepos(username, token)
    followers = getGithubFollowers(username, token)
    followings = getGithubFollowings(username, token)
    urlProfile = getGithubProfileLink(username, token)
    joinedDate = getGithubJoinedDate(username, token)
    fullName = getGithubFullName(username, token)

    if not repos:
        print(f"{color.RED}No repositories are available!{Style.RESET_ALL}")
    else:
        print()
        print(f"{color.GREEN}Repositories:{Style.RESET_ALL}")
        n = 1
        for repo in repos:
            print(f"{n} -> {repo}")
            n += 1
    if not followers:
        print(f"{color.RED}No followers are available!{Style.RESET_ALL}")
    else:
        print()
        print(f"{color.GREEN}Followers:{Style.RESET_ALL} {color.BLUE}{len(followers)} / 200 (max to show is 200){Style.RESET_ALL}")
        for follower in followers:
            print(follower)
    if not followings:
        print(f"{color.RED}No followings are available!{Style.RESET_ALL}")
    else:
        print()
        print(f"{color.GREEN}Followings:{Style.RESET_ALL} {color.BLUE}{len(followings)} / 200 (max to show is 200){Style.RESET_ALL}")
        for following in followings:
            print(following)
    if not urlProfile:
        print('')
    else:
        print()
        x = username.capitalize()
        print(f"{color.GREEN}{x}'s user data:{Style.RESET_ALL}")
        print(f"{color.GREEN}Profile link:{Style.RESET_ALL} '{urlProfile}'")
        if not joinedDate:
            print('')
        else:
            print(f"{color.GREEN}Joined Github:{Style.RESET_ALL} '{joinedDate[0:10]}'")
            if not fullName:
                print('')
            else:
                print(f"{color.GREEN}Fullname:{Style.RESET_ALL} '{fullName}'")
        print()
    if not repos:
        return
    else:
        print(f"{color.GREEN}Do you want to clone a repository from {username}'s repos? (Y/n){Style.RESET_ALL}")
        response = input()

        if response not in ('Y', 'y', 'N', 'n'):
            print(f"{color.RED}Invalid option{Style.RESET_ALL}")
            return

        if response in ('Y', 'y'):
            print(f"{color.GREEN}Enter the number of repository to clone:{Style.RESET_ALL}")
            numOfRepo = input()
            if not numOfRepo.isdigit():
                print(f"{color.RED}Invalid option{Style.RESET_ALL}")
                return
            if int(numOfRepo) <= 0 or int(numOfRepo) > len(repos):
                print(f"{color.RED}This repository doesn't exist{Style.RESET_ALL}")
            else:
                print(f"{color.GREEN}Enter the full valid path where you want to clone the repo:{Style.RESET_ALL}")
                path = input()

                if not os.path.exists(os.path.split(path)[0]):
                    print(f"{color.RED}The path you entered doesn't exist{Style.RESET_ALL}")
                    return
                cloneRepository(username, repos[int(numOfRepo) - 1], path)
        else:
            print(f"{color.RED}Exiting program ...{Style.RESET_ALL}")
            time.sleep(2)
            print(f"{color.RED}Bye{Style.RESET_ALL}")


if __name__ == "__main__":
    main()
