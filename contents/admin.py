from django.contrib import admin

from contents.models import Content, Image, FollowRelation


class ImageInline(admin.TabularInline):
    model = Image


class ContentAdmin(admin.ModelAdmin): 
    inlines = [ImageInline] # 인라인 변수 안에 이미지 인라인 클래스를 리스트 안에 넣으면 동일한 페이지 안에서 작업을 한다는 뜻
    list_display = ('user', 'created_at',)


admin.site.register(Content, ContentAdmin)


class ImageAdmin(admin.ModelAdmin):
    pass


admin.site.register(Image, ImageAdmin)


class FollowRelationAdmin(admin.ModelAdmin): # 팔로우 관계가 관리자 페이지에서 보이도록
    pass

admin.site.register(FollowRelation, FollowRelationAdmin)