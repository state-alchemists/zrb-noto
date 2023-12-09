import subprocess


def get_current_branch() -> str:
    # Run the git command to get the current branch name
    branch_name = subprocess.check_output(
        ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
        stderr=subprocess.STDOUT
    ).strip().decode('utf-8')
    return branch_name
