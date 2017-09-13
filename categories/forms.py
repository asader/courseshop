from django import forms
from videos.models import Video
from .models import Category


class CategoryAdminForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = [
            'title',
            'slug',
            'seodesc',
            'seokw',
            'video',
            'description',
            'active',
        ]

    # Для видео доступны только неиспользованные видео или уже выбранное заранее видео 
    def __init__(self, *args, **kwargs):
        super(CategoryAdminForm, self).__init__(*args, **kwargs)
        obj = kwargs.get("instance")
        qs = Video.objects.all().unused()
        if obj:
            if obj.video:
                this_ = Video.objects.filter(pk=obj.video.pk)
                qs = (qs | this_)
            self.fields['video'].queryset = qs
        else:
            self.fields['video'].queryset = qs
