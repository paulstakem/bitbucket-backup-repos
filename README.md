
Setup Netrc
```
cp netrc ~/.netrc && chmod 0700
```

Install the dependencies
```
brew install jq pipenv
brew install parallel
```

Accept the license agreement for parallel
```
parallel --citation
```

Test the python script
```
pipenv install requests
pipenv run python list_repos.py
```

Full run including cloning
```
pipenv run python list_repos.py | jq -r '.links.clone[] | select(.name=="ssh") | .href' | parallel --jobs 5 git clone
```
