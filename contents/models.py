import os
import uuid

from django.db import models
from django.contrib.auth.models import User

# 특정 폴더에만 마이그레이션을 진행하고 싶으면 python manage.py makemigrations contents / python manage.py migrate contents
# 그리고 마이그레이션이 적용된 걸 보고 싶다면 python manage.py showmigrations contents

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta: 
        abstract = True # 클래스 메타에서 abstract를 true로 주면 이 모델클래스는 추상클래스이다. 무조건 자동으로 들어가게 되는 값들 


class Content(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(default='')

    class Meta:
        ordering = ['-created_at'] # 나중에 포스트한 사진들이 먼저 나오게 하는 코드
        verbose_name_plural = "컨텐츠"


def image_upload_to(instance, filename):
    ext = filename.split('.')[-1]
    return os.path.join(instance.UPLOAD_PATH, "%s.%s" % (uuid.uuid4(), ext))
    # uuid는 16자리 고유한 아이디 생성


class Image(BaseModel):
    UPLOAD_PATH = 'user-upload'

    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=image_upload_to)
    order = models.SmallIntegerField() # image numbering # 인스타그램에서 여러장의 사진을 업로드할 때 1,2,3...같은 순서를 정할 때 사용할 필드
                                       # 파이썬에서 이미지를 불러올 때 사용할 라이브러리 다운로드 필요 pip install pillow
    class Meta:
        unique_together = ['content', 'order'] # 유니크를 두개로 줄 수 있는 기능
        ordering = ['order']# image numbering # 인스타그램에서 여러장의 사진을 업로드할 때 1,2,3...같은 순서를 정할 때 사용할 필드
                            # -는 내림차순 아무것도 안붙이면 오름차순 / 리스트 안에서 ,를 넣고 또 다른 정렬 순서를 넣을 수도 있음


class FollowRelation(BaseModel): # 팔로우 기능
    follower = models.OneToOneField(User, on_delete=models.CASCADE, related_name = 'follower') # 내가 ~를 팔로우한다에서 팔로워는 '나'임
    followee = models.ManyToManyField(User, related_name='followee') # 내가 ~를 팔로우한다에서 팔로위는 '~'임

