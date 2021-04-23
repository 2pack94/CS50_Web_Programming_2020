import re
from django import forms
from django.core.exceptions import ValidationError
from . import util

class NewPageForm(forms.Form):
    # title will be the name of the Markdown file.
    # content will be the content of the Markdown file (including the heading of the article).
    # Widgets: https://docs.djangoproject.com/en/3.1/ref/forms/widgets/
    title = forms.CharField(label='Title', max_length=100)
    content = forms.CharField(label='Content', widget=forms.Textarea)

    # clean method that operates on the title field
    # https://docs.djangoproject.com/en/3.1/ref/forms/validation/#cleaning-a-specific-field-attribute
    # This function will be called when the method is_valid() is called.
    # When raising a ValidationError, the member "errors" of the Form class will be set and
    # by default will be printed as HTML when rendering the bound form.
    def clean_title(self):
        title = self.cleaned_data.get("title")

        # This regex matches any character not present in the list (^ is used as negation of the expression)
        allowed_chars_re = re.compile(r'[^a-zA-Z0-9 \-\_]')
        match_obj = allowed_chars_re.search(title)
        if bool(match_obj):
            raise ValidationError(
                f"Error: Only alphanumeric and the special characters - _ are allowed!"
            )

        if util.get_entry_name(title):
            raise ValidationError(
                f"Error: The entry '{title}' does already exist."
            )

        return title
