set -e
cd "${PROJECT_DIR}"
if git diff --quiet && git diff --cached --quiet
then
    echo "Nothing to commit"
else
    echo "Commiting changes"
    git add . -A
    git commit -m "Save changes on $(date)"
fi
GIT_BRANCH="$(git symbolic-ref --short HEAD)"
echo "Current branch: ${GIT_BRANCH}"
echo "Pulling from Server"
git pull origin ${GIT_BRANCH:-main}
echo "Pushing to Server"
git push -u origin ${GIT_BRANCH:-main}