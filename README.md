# Noto

Noto is a personal management tool based on [Zrb](https://pypi.org/project/zrb) and [todo.txt](https://github.com/todotxt/todo.txt).

# How to use

- Ensure zrb is installed
- Fork this repository
- Clone this repository to your local computer
- Start working

    ```bash
    zrb todo list
    ```

- Add zrb auto completion on your `~/.bashrc` or `~/.zshrc`

    ```bash
    # Enable auto completion
    _CURRENT_SHELL=$(ps -p $$ | awk 'NR==2 {print $4}')
    case "$_CURRENT_SHELL" in
    *zsh)
        _CURRENT_SHELL="zsh"
        ;;
    *bash)
        _CURRENT_SHELL="bash"
        ;;
    esac
    if [ "$_CURRENT_SHELL" = "zsh" ] || [ "$_CURRENT_SHELL" = "bash" ]
    then
        log_info "Setting up shell completion for $_CURRENT_SHELL"
        eval "$(_ZRB_COMPLETE=${_CURRENT_SHELL}_source zrb)"
    else
        log_info "Cannot set up shell completion for $_CURRENT_SHELL"
    fi
    ```

- Load noto automatically on your `~/.bashrc` or `~/.zshrc`

    ```bash
    # Load daily if exists
    if [ -f "${HOME}/daily/zrb_init.py" ]
    then
        export ZRB_INIT_SCRIPTS="${HOME}/daily/zrb_init.py"
        # Load .env if exists
        if [ -f "${HOME}/daily/.env" ]
        then
            source "${HOME}/daily/.env"
        fi
    fi
    ```


# Trivia

```python
noto = {
    "japanese": "note",
    "javanese": "to arrange"
}
```
