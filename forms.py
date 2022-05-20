from django.contrib.auth.forms import SetPasswordForm


class BootstrapStylesMixin:
    """
    this class BootstrapStyles
    """

    field_names = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.field_names:
            for fieldname in self.field_names:
                field = self.fields.get(fieldname)
                field.widget.attrs = {'class': 'form-control'}
                field.widget.attrs.update(
                    {'placeholder': field.label, 'width': '10px'})
        else:
            raise ValueError('Complete el campo')


class EstablecerContrasena(BootstrapStylesMixin, SetPasswordForm):
    field_names = ['new_password1', 'new_password2']
