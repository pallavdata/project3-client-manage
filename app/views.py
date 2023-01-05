from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from .models import Client,project,LoginModel
# from django.contrib.auth.decorators import login
from .forms import RegForm, LoginForm,ProjectForm,ClientForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def custom(request):
    data = LoginModel.objects.get(email= request.user)
    clientdata = Client.objects.filter(userid = data)
    return clientdata

def customProject(request):
    data = LoginModel.objects.get(email= request.user)
    projectdata = project.objects.filter(userid = data)
    return projectdata
@login_required(login_url='/login/')
def home(request):
    return render(request,"page/home.html")
@login_required(login_url='/login/')
def project_main(request):
    data = custom(request)
    if request.POST:
        form = ProjectForm(request.POST)
        if form.is_valid():
            client = request.POST['client']
            see = Client.objects.get(pk=client)
            postdata = form.save(commit=False)
            postdata.ClientId = see
            postdata.userid = LoginModel.objects.get(email= request.user)
            postdata.save()
            return render(request,"page/project.html",{"success": "success - your project is saved"})
        else:
            return render(request,"page/project.html",{"dataCompleted":dataCompleted,"dataPending":dataPending,"dataProgress":dataProgress,"dataTotal":dataTotal,"client": data,"form":form})
    # if request.POST:
    #     return render(request,"page/project.html")
    dataCompleted = customProject(request).filter(Status = "Completed").count()
    dataPending = customProject(request).filter(Status = "Pending").count()
    dataProgress = customProject(request).filter(Status = "On Progress").count()
    dataTotal = dataCompleted + dataPending + dataProgress
    return render(request,"page/project.html",{"dataCompleted":dataCompleted,"dataPending":dataPending,"dataProgress":dataProgress,"dataTotal":dataTotal,"client": data})
@login_required(login_url='/login/')
def new_project(request):
    data = custom(request)
    if request.POST:
        form = ProjectForm(request.POST)
        if form.is_valid():
            client = request.POST['client']
            see = Client.objects.get(pk=client)
            postdata = form.save(commit=False)
            postdata.ClientId = see
            postdata.userid = LoginModel.objects.get(email= request.user)
            postdata.save()
            return redirect(project_main)
        else:
            return render(request,"page/new-project.html",{"client": data,"form":form})
    return render(request,"page/new-project.html",{"client": data})
@login_required(login_url='/login/')
def project_details(request):
    data = customProject(request)
    return render(request,"page/project-details.html",{"data": data})
@login_required(login_url='/login/')
def client(request):
    data = Client.objects.all().count()
    if request.POST:
        form = ClientForm(request.POST)
        if form.is_valid():
            see = form.save(commit=False)
            see.userid = LoginModel.objects.get(email= request.user)
            see.save()
            return render(request,"page/client.html",{"success": "success - your project is saved","client":data})
        else:
            return render(request,"page/client.html",{"fail": "Failed - Something is missing","form":form,"client":data})
    return render(request,"page/client.html",{"client":data})
@login_required(login_url='/login/')
def client_details(request):
    data = custom(request)
    m=0
    data2 = []
    for i in data:
        if data2 == []:
            data2 = [{1: data[m], 2: [project.objects.filter(ClientId = i)], 3: project.objects.filter(ClientId = i).count()}]
        else:
            data2 = data2 + [{1 : data[m], 2: [project.objects.filter(ClientId = i)],  3: project.objects.filter(ClientId = i).count()}]
        m=m+1
    return render(request,"page/client-details.html",{"client":data2})
@login_required(login_url='/login/')
def manage_client(request):
    data = custom(request)
    return render(request,"page/manage-client.html",{"client":data})

def signup(request,*args,**kwargs):
    user = request.user
    if user.is_authenticated:
        return redirect("home")
        return HttpResponse(f"You are already authenticated as {user}")
    if request.POST:
        form = RegForm(request.POST)
            
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email,password=raw_password)
            login(request,account)
            # destination = kwargs.get("next")
            # if destination:
            #     return redirect(destination)
            return redirect("home")
        else:
            return render(request,"page/signup.html",{"form":RegForm(request.POST)})
    
    login_data={
        "form": RegForm(),
    }
    return render(request,"page/signup.html",login_data)
def logout_view(request):
    logout(request)
    return redirect("home")

    
def login_view(request,*args,**kwaegs):
    user = request.user
    if user.is_authenticated:
        return redirect("home")
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST['email'].lower()
            raw_password = request.POST['password']
            account = authenticate(email=email,password=raw_password)
            if account:
                login(request,account)
                return redirect("home")
            else:
                data = f"Email id \"{email}\" or Password is incorrect. Please try again with correct email id and password"
                return render(request,"page/login.html",{"form":LoginForm(request.POST),"nologin":data})
        else:
            return render(request,"page/login.html",{"form":LoginForm(request.POST)})
    return render(request,"page/login.html",{"form":LoginForm()})
