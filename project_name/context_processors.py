from {{ project_name }} import __version__


def version_context_processor(_) -> dict:
    return {
        'project_version': __version__,
    }

