## Instructions

1. Clone this repository

2. Ensure that you have `docker`, and `docker-compose` available on your computer.

3. Optionally, produce a github Personal access token.

4. Set the environment variable `GITHUB_API_TOKEN` with the Key optionally produced from Step 3.

## Setup

1. Execute `docker compose build` to build and tag the image.

2. Execute `docker compose up -d --remove-orphans` to start up the stack.

3. Verify that the containers for the application stack are up:

```
docker ps
CONTAINER ID   IMAGE                        COMMAND                  CREATED         STATUS                   PORTS                                         NAMES
a352d72e19f1   ghgist-scraper-http-server   "uvicorn app:app --h…"   8 seconds ago   Up 2 seconds             0.0.0.0:8080->8080/tcp, [::]:8080->8080/tcp   equal-experts-fashionable-decisive-dignified-animal-11faa3add24c-http-server-1
ee065e8513a8   redis:7-alpine               "docker-entrypoint.s…"   8 seconds ago   Up 7 seconds (healthy)   0.0.0.0:6379->6379/tcp, [::]:6379->6379/tcp   equal-experts-fashionable-decisive-dignified-animal-11faa3add24c-redis-1
```

4. Make a request, using curl or any other tool like so:
```
curl localhost:8080/torvalds
```

Expect a response like so:
```
[{"url":"https://api.github.com/gists/6faadce34c56d53b2d5352da0c3cd093","forks_url":"https://api.github.com/gists/6faadce34c56d53b2d5352da0c3cd093/forks","commits_url":"https://api.github.com/gists/6faadce34c56d53b2d5352da0c3cd093/commits","id":"6faadce34c56d53b2d5352da0c3cd093","node_id":"G_kwDOAA-gGdoAIDZmYWFkY2UzNGM1NmQ1M2IyZDUzNTJkYTBjM2NkMDkz","git_pull_url":"https://gist.github.com/6faadce34c56d53b2d5352da0c3cd093.git","git_push_url":"https://gist.github.com/6faadce34c56d53b2d5352da0c3cd093.git","html_url":"https://gist.github.com/torvalds/6faadce34c56d53b2d5352da0c3cd093","files":{"gistfile1.txt":{"filename":"gistfile1.txt","type":"text/plain","language":"Text","raw_url":"https://gist.githubusercontent.com/torvalds/6faadce34c56d53b2d5352da0c3cd093/raw/79c51a5c1785993f4583547bb55306f0b2e142cd/gistfile1.txt","size":312}},"public":true,"created_at":"2025-05-22T19:56:29Z","updated_at":"2026-09-18T10:48:13Z","description":"Not involved with any fishy crypto fishy business","comments":94,"user":null,"comments_enabled":true,"comments_url":"https://api.github.com/gists/6faadce34c56d53b2d5352da0c3cd093/comments","owner":{"login":"torvalds","id":1024025,"node_id":"MDQ6VXNlcjEwMjQwMjU=","avatar_url":"https://avatars.githubusercontent.com/u/1024025?v=4","gravatar_id":"","url":"https://api.github.com/users/torvalds","html_url":"https://github.com/torvalds","followers_url":"https://api.github.com/users/torvalds/followers","following_url":"https://api.github.com/users/torvalds/following{/other_user}","gists_url":"https://api.github.com/users/torvalds/gists{/gist_id}","starred_url":"https://api.github.com/users/torvalds/starred{/owner}{/repo}","subscriptions_url":"https://api.github.com/users/torvalds/subscriptions","organizations_url":"https://api.github.com/users/torvalds/orgs","repos_url":"https://api.github.com/users/torvalds/repos","events_url":"https://api.github.com/users/torvalds/events{/privacy}","received_events_url":"https://api.github.com/users/torvalds/received_events","type":"User","user_view_type":"public","site_admin":false},"truncated":false}]% 
```
