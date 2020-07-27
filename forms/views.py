from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Blog
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.db.models import Q
#listview :리스트 형태의 데이터를 보여주기 위한 것
#index 부분 

class index(ListView):
    template_name = 'index.html'
    context_object_name = 'blog_list'
    def get_queryset(self):
        return Blog.objects.all

#하고 indext.html에 정보 추가 해주기 
#detail view만들기
class detail(DetailView):
    model = Blog
    template_name ='detail.html'
    context_object_name ='blog'
#detail html 작성하기 
#삭제 구현하기
class delete(DeleteView):
    model = Blog
    template_name = 'delete.html'
    context_object_name = 'blog'
    success_url = reverse_lazy('index')

class update(UpdateView):
    model =Blog
    template_name ='update.html'
    fields = ['title','text']
    success_url = reverse_lazy('index')

#create 구현
class create(CreateView):
    model = Blog
    template_name = 'create.html'
    fields = ['title','text']

    def form_valid(self,form):
        Blog = form.save(commit=False)
        Blog.author = self.request.user
        Blog.save()

        return HttpResponseRedirect(self.request.POST.get('next','/'))

#검색하는 법
def result(request):
   BlogPosts = Blog.objects.all()
   query = request.GET.get('query', '')
   selected = request.GET.get('selected', '')
    
   if selected=="no":
       BlogPosts = BlogPosts.filter(Q(title__icontains=query)| Q(text__icontains=query)).order_by('-time')
       count = len(BlogPosts)
        
   elif selected=="title":
        BlogPosts = BlogPosts.filter(Q(title__icontains=query)).order_by('-time')
        count = len(BlogPosts)
        
   elif selected=="text":
        BlogPosts = BlogPosts.filter(Q(text__icontains=query)).order_by('-time')
        count = len(BlogPosts)
        
   elif selected=="author":
        BlogPosts = BlogPosts.filter(Q(author__icontains=query)).order_by('-time')
        count = len(BlogPosts)

   return render(request, 'result.html', {'BlogPosts':BlogPosts, 'query':query, 'count':count, 'selected':selected})