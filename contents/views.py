from django.views.generic.base import TemplateView # 템플릿이 있으면 해당 템플릿으로 렌더링을 해주는 장고의 기본 View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch

from contents.models import Content, FollowRelation


@method_decorator(login_required, name='dispatch')
class HomeView(TemplateView):

    template_name = 'home.html' # 렌더링 해줄 html파일 이름만 적어주면 알아서 렌더링 해줌

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)

        # 내가 쓴 글이랑 내가 팔로우한 사람들의 글들도 보이도록 설정 
        user = self.request.user
        followees = FollowRelation.objects.filter(follower=user).values_list('followee__id', flat=True)
        lookup_user_ids = [user.id] + list(followees)
        context['contents'] = Content.objects.select_related('user').prefetch_related('image_set').filter( # contents.objects.all은 속도가 느리다.
            user__id__in=lookup_user_ids                                                                   # 그래서 성능 개선을 진행한 select_related()랑 prefetch_related()를 사용하는 데 전자는 포린키나 원투원 그리고 프리패치는 매니투매니에서 사용
        )

        return context


@method_decorator(login_required, name='dispatch')
class RelationView(TemplateView):

    template_name = 'relation.html'

    def get_context_data(self, **kwargs):
        context = super(RelationView, self).get_context_data(**kwargs)

        user = self.request.user

        # 내가 팔로우하는 사람들
        try:
            followers = FollowRelation.objects.get(follower=user).followee.all()
            context['followees'] = followers
            context['followees_ids'] = list(followers.values_list('id', flat=True)) # values는 튜플형태로 가져오고, values_list는 리스트 형태로 가져온다
            
        except FollowRelation.DoesNotExist:
            pass

        context['followers'] = FollowRelation.objects.select_related('follower').filter(followee__in=[user])
        
        return context
