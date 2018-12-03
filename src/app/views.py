from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django_filters.views import FilterView

from pure_pagination.mixins import PaginationMixin
from .models import Item
from .filters import ItemFilter
from .forms import ItemForm
from users.models import User
from django.http import HttpResponse

# Create your views here.



# 検索一覧画面

class ItemListView(LoginRequiredMixin, ListView):
    model = Item
    paginate_by = 3
    def get_queryset(self):
        #uid = self.request.session.get_decoded().get('_auth_user_id')
        uid = self.request.session.get('_auth_user_id')
        user_id = uid.translate(str.maketrans({'-': ''}))
        dept_ids = User.objects.get(pk=user_id).departments.all()
        dept_id = []
        for d in dept_ids:
            dept_id.append(d.id)
        query_set = Item.objects.filter(department__in=dept_id)
        return query_set




# 詳細画面
class ItemDetailView(LoginRequiredMixin, DetailView):
    model = Item
    def get_queryset(self):


        uid = self.request.session.get('_auth_user_id')
        user_id = uid.translate(str.maketrans({'-': ''}))
        dept_ids = User.objects.get(pk=user_id).departments.all()
        item = Item.objects.filter(id=self.kwargs['pk']).filter(department__in=dept_ids)
        return item


# 登録画面
class ItemCreateView(LoginRequiredMixin, CreateView):
    model = Item
    form_class = ItemForm
    success_url = reverse_lazy('index')


# 更新画面
class ItemUpdateView(LoginRequiredMixin, UpdateView):
    model = Item
    form_class = ItemForm
    success_url = reverse_lazy('index')


# 削除画面
class ItemDeleteView(LoginRequiredMixin, DeleteView):
    model = Item
    success_url = reverse_lazy('index')


# session情報
#def sesinfo(request):
#    ses = request.session['_auth_user_id']
#    uuid = ses.translate(ses.maketrans({'-': '', }))
#    return HttpResponse(uuid)




# from django.contrib.sessions.models import Session
# from django.contrib.auth.models import User

# session_key = '8cae76c505f15432b48c8292a7dd0e54'

# session = Session.objects.get(session_key=session_key)
# uid = session.get_decoded().get('_auth_user_id')
# user = User.objects.get(pk=uid)

# print user.username, user.get_full_name(), user.email

class ItemFilterView(LoginRequiredMixin, PaginationMixin, FilterView):

    filterset_class = ItemFilter
    # デフォルトの並び順を新しい順とする
    # クエリ未指定の時に全件検索を行うために以下のオプションを指定（django-filter2.0以降）
    strict = False
    # pure_pagination用設定
    paginate_by = 3
    object = Item

    # 検索条件をセッションに保存する or 呼び出す
    def get(self, request, **kwargs):

        if request.GET:
            request.session['query'] = request.GET
        else:
            request.GET = request.GET.copy()
            if 'query' in request.session.keys():
                for key in request.session['query'].keys():
                    request.GET[key] = request.session['query'][key]
        return super().get(request, **kwargs)

    def get_queryset(self):
        #uid = self.request.session.get_decoded().get('_auth_user_id')
        uid = self.request.session.get('_auth_user_id')
        user_id = uid.translate(str.maketrans({'-': ''}))
        dept_ids = User.objects.get(pk=user_id).departments.all()
        dept_id = []
        for d in dept_ids:
            dept_id = d.id
        query_set = Item.objects.filter(department__in=dept_id)
        return query_set

