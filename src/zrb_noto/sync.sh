set -e

if [ "${IGNORE_ERROR}" = "1" ]
then
    # Define cleanup operations or override commands here
    cleanup() {
        exit 0 # Override the exit code
    }
    # Trap the EXIT signal
    trap cleanup EXIT
fi

if [ ! -d "${LOCAL_REPO_DIR}" ]
then
    echo "Local repository not found, cloning..."
    mkdir -p "${LOCAL_REPO_DIR}"
    cd ..
    git clone "${REMOTE_GIT_URL}" "${LOCAL_REPO_DIR}"
fi

cd "${LOCAL_REPO_DIR}"
git add . -A
if git diff --quiet && git diff --cached --quiet
then
    echo "Nothing to commit"
else
    echo "Commiting changes"
    if [ -z "${COMMIT_MESSAGE}" ]
    then
        COMMIT_MESSAGE="Modified on $(date)"
    fi
    git commit -m "${COMMIT_MESSAGE}"
fi
GIT_BRANCH="$(git symbolic-ref --short HEAD)"
echo "Current branch: ${GIT_BRANCH}"

echo "Fetching origin ${GIT_BRANCH}"
git fetch origin

LOCAL=$(git rev-parse $GIT_BRANCH)
REMOTE=$(git rev-parse origin/$GIT_BRANCH)
BASE=$(git merge-base $GIT_BRANCH origin/$GIT_BRANCH)

echo "Comparing local branch $GIT_BRANCH with origin/$GIT_BRANCH"

if [ "$LOCAL" = "$REMOTE" ]
then
    echo "Up to date with origin/$GIT_BRANCH."
elif [ "$LOCAL" = "$BASE" ]
then
    echo "Need to pull. Local branch $GIT_BRANCH is behind origin/$GIT_BRANCH."
    echo "Pulling from Server"
    git pull origin ${GIT_BRANCH:-main}
elif [ "$REMOTE" = "$BASE" ]
then
    echo "Need to push. Local branch $GIT_BRANCH is ahead of origin/$GIT_BRANCH."
    echo "Pushing to Server"
    git push -u origin ${GIT_BRANCH:-main}
else
    echo "Branch $GIT_BRANCH has diverged from origin/$GIT_BRANCH."
fi
