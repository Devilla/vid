from threadedcomments.forms import ThreadedCommentForm

class CustomCommentForm(ThreadedCommentForm):
    pass
    #add username here
    # name = None
    # email = None
    # url = None
    # email = None
    # title = None

    def __init__(self, *args, **kwargs):
        super(CustomCommentForm, self).__init__(*args, **kwargs)
        self.fields.pop('name')
        self.fields.pop('email')
        self.fields.pop('url')
        self.fields.pop('title')


    def clean(self):
        self.cleaned_data['name'] = "a"
        self.cleaned_data['email'] = "a@a.com"
        self.cleaned_data['url'] = "https://a.com"
        self.cleaned_data['title'] = "a" #username here
        
        return self.cleaned_data