from django import forms
from django.forms import formset_factory
from .models import Type,Category
class Catform(forms.ModelForm):
    # category_name=forms.CharField(label='نام دسته ',max_length=255)
    # types=forms.ModelMultipleChoiceField(label='نوع اصلی دسته',widget=forms.Select(),queryset=Type.objects.all())

    class Meta:
        model=Category
        fields=['type','category_name']




class AttribiutForm(forms.Form):
    type_choices=(
        ('string','متنی'),
        ('number','عدد'),
        ('boolean','صفر و یک '),

    )



    name=forms.CharField(
        label='نام ویژگی',
        widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'نام ویژگی را  اضافه کنید'
        })
    )
    att_type=forms.MultipleChoiceField(choices=type_choices)


AttribiutFormSet=formset_factory(AttribiutForm)
