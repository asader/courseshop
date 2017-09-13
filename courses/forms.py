from django import forms

from videos.models import Video
from .models import Lecture


class LectureAdminForm(forms.ModelForm):
    class Meta:
        model = Lecture
        fields = [
            'title',
            'seodesc',
            'free',
            'video',
            'description',
            'slug', 
        ]

    # Для видео доступны только неиспользованные видео или уже выбранное заранее видео 
    def __init__(self, *args, **kwargs):
        super(LectureAdminForm, self).__init__(*args, **kwargs)
        obj = kwargs.get("instance")
        qs = Video.objects.all().unused()
        if obj:
            if obj.video:
                this_ = Video.objects.filter(pk=obj.video.pk)
                qs = (qs | this_)
            self.fields['video'].queryset = qs
        else:
            self.fields['video'].queryset = qs
