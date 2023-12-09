# Noto

A personal todo list based on [Zrb](https://github.com/state-alchemists/zrb) and [todo.txt](https://github.com/todotxt/todo.txt)

# Features

- Auto sync using git (on progress)
- Using todo.txt format (planned)
- Reminder (planned)
- CLI commands to manage todo.txt (planned)


# Prerequisites

To start working with Noto, you need to have:

- Python 3.10 or higher
- Pip
- Venv

You can also use [Zrb Docker container](https://github.com/state-alchemists/zrb#-with-docker) if you prefer to work with Docker.

# Getting started

To start working with Noto, you should activate the virtual environment and install a few packages (including Zrb). You can do this by invoking the following command in your terminal:

```bash
source ./project.sh
```

Once the virtual environment is activated, you can start the Noto monitoring system by invoking:

```bash
zrb noto start
```

# Writing custom flow

To write custom flows, you can overwrite `_automate/main.py`.
