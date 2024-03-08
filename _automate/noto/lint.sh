set -e
cd "${PROJECT_DIR}"
isort .
black .