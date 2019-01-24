__version__ = "1.2"


def get_model():
    from threadedcomments.models import ThreadedComment
    return ThreadedComment

def get_form():
    from .forms import CustomCommentForm
    return CustomCommentForm