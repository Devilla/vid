__version__ = "1.2"


def get_model():
    from .models import CustomThreadedComment
    return CustomThreadedComment

def get_form():
    from .forms import CustomCommentForm
    return CustomCommentForm