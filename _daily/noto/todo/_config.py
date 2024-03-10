from _daily.noto.todo._helper import get_existing_contexts, get_existing_projects

EXISTING_CONTEXTS = get_existing_contexts()
EXISTING_CONTEXT_STR = ",".join(EXISTING_CONTEXTS)
EXISTING_PROJECTS = get_existing_projects()
EXISTING_PROJECT_STR = ",".join(EXISTING_PROJECTS)
