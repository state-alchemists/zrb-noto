# Noto

Noto is a personal management tool based on [Zrb](https://pypi.org/project/zrb) and [todo.txt](https://github.com/todotxt/todo.txt).

# Installing Noto

```bash
pip install zrb
pip install zrb-noto
```

# Setting up Repository

## Making Noto accessible

First of all, you will need a file named `~/zrb_init.py`.

```python
import noto
```

Then, you need to set the value of `ZRB_INIT_SCRIPTS` variable as follows:

```bash
export ZRB_INIT_SCRIPTS=${ZRB_INIT_SCRIPTS}:~/zrb_init.py
```

To automatically `ZRB_INIT_SCRIPTS`, you can add the script to your `~/.bashrc` or `~/.zshrc`.

## Setting up a daily repository

- Create an empty repository on Github/Gitlab
- Clone the repository to your local computer
- Configure Noto by setting up the following variables

  ```bash
  export NOTO_LOCAL_REPO=${HOME}/daily
  export NOTO_REMOTE_GIT=git@github.com:yourUserName/daily.git
  ```

# Start working

```bash
zrb noto list
zrb todo add -t "Learn noto"
zrb todo start -t "Learn noto"
zrb todo stop -t "Learn noto"
zrb todo complete -t "Learn noto"
zrb noto list
```



# Trivia

```python
noto = {
    "japanese": "note",
    "javanese": "to arrange"
}
```
