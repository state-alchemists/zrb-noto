set -e
cd "${LOCAL_REPO_DIR}"
isort .
black .