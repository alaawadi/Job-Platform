from django.shortcuts import redirect, render, reverse

from .models import Job
from django.core.paginator import Paginator
from .form import ApplyForm , JobForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .filters import JobFilter
# Create your views here.


def job_list(request):
    job_list = Job.objects.all()
    job_counter=Job.objects.count()
    ## filters
    myfilter = JobFilter(request.GET,queryset=job_list)
    job_list = myfilter.qs


    paginator = Paginator(job_list, 4) # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    context = {'jobs' :page_obj , 'myfilter' : myfilter , 'count':job_counter} # template name
    return render(request,'job/job_list.html',context)


def job_detail(request , slug):
    job_detail = Job.objects.get(slug=slug)
    form = ApplyForm()
    if request.method=='POST':
        form = ApplyForm(request.POST , request.FILES)
        if form.is_valid():
            myform = form.save(commit=False)
            myform.job = job_detail
            myform.owner = request.user
            myform.save()

    else:
        form = ApplyForm()


    context = {'job' : job_detail , 'form1':form}
    return render(request,'job/job_detail.html',context)


def add_job(request):
    if request.method=='POST':
        form = JobForm(request.POST , request.FILES)
        if form.is_valid():
            myform = form.save(commit=False)
            myform.owner = request.user
            myform.save()
            return redirect(reverse('job_list'))

    else:
        form = JobForm()

    return render(request,'job/add_job.html',{'form':form})










# def like_or_unlike(request,id):
#     job = Job.objects.get(id=id)

#     if request.user in Job.like.all():
#         Job.like.remove(request.user)
    
#     else:
#         Job.like.add(request.user)
    
#     return redirect(reverse('job_detail',kwargs={'id':job.id}))



# def user_favourites(request):
#     user_favourites = Job.objects.filter(like=request.user)
#     return render(request,'job_list.html',{'user_favourites':user_favourites})


