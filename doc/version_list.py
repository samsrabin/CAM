"""
Define the versions we want to build
"""
import sys
import os
# The doc_builder package may live in a "doc-builder" subdir (as in repos where doc-builder is a
# submodule) or directly alongside this file (as in the doc-builder repo itself). Add whichever
# exists to sys.path so "doc_builder" is importable either way.
dir2add = os.path.join(os.path.dirname(__file__), "doc-builder")
if not os.path.exists(dir2add):
    dir2add = os.path.dirname(__file__)
sys.path.insert(0, dir2add)
# pylint: disable=wrong-import-position,import-error
from doc_builder.docs_version import DocsVersion
from doc_builder.sys_utils import get_git_head_or_branch

# Branch name, tag, or commit SHA whose version of certain files we want to preserve
LATEST_REF = get_git_head_or_branch()

# List of version definitions
VERSION_LIST = [
    # Always keep this one! You can change short_name and display_name if you want.
    DocsVersion(
        short_name="latest",
        display_name="Latest development code",
        landing_version=True,
        ref=LATEST_REF,
    ),
    DocsVersion(
        short_name="cam6-users-guide",  # shows up in URL
        display_name="CAM6 User’s Guide",  # shows up in menu
        ref="cam6-users-guide",  # branch name
    ),
    DocsVersion(
        short_name="cam6.3-users-guide",  # shows up in URL
        display_name="CAM6.3 User’s Guide",  # shows up in menu
        ref="cam6.3-users-guide",  # branch name
    ),
]
# End version definitions (keep this comment; Sphinx is looking for it)
