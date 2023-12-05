#!/bin/bash

NOTO_DIR=$(pwd)
echo "🤖 Set project directory to ${NOTO_DIR}"


if [ -z "$NOTO_USE_VENV" ] || [ "$NOTO_USE_VENV" = 1 ]
then
    if [ ! -d .venv ]
    then
        echo '🤖 Create virtual environment'
        python -m venv "${NOTO_DIR}/.venv"
        echo '🤖 Activate virtual environment'
        source "${NOTO_DIR}/.venv/bin/activate"
    fi

    echo '🤖 Activate virtual environment'
    source "${NOTO_DIR}/.venv/bin/activate"
fi

reload() {

    if [ ! -f "${NOTO_DIR}/.env" ]
    then
        echo '🤖 Create project configuration (.env)'
        cp "${NOTO_DIR}/template.env" "${NOTO_DIR}/.env"
    fi

    echo '🤖 Load project configuration (.env)'
    source "${NOTO_DIR}/.env"

    if [ -z "$NOTO_AUTO_INSTALL_PIP" ] || [ "$NOTO_AUTO_INSTALL_PIP" = 1 ]
    then
        echo '🤖 Install requirements'
        pip install --upgrade pip
        pip install -r "${NOTO_DIR}/requirements.txt"
    fi

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
        echo "🤖 Set up shell completion for $_CURRENT_SHELL"
        eval "$(_ZRB_COMPLETE=${_CURRENT_SHELL}_source zrb)"
    else
        echo "🤖 Cannot set up shell completion for $_CURRENT_SHELL"
    fi
}

reload
echo '🤖 Happy Coding :)'
