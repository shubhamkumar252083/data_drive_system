from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import FolderDetail, FileDetail
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

def home(request):
    if request.user.is_authenticated:
        user = request.user
        print(user)
        root_folders = FolderDetail.objects.filter(folderuser=user, parent_folder=None)
        # print(root_folders)
        return render(request, 'home.html', {'root_folders': root_folders})
    else:
        return redirect('signup')

def SignUp(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            cpassword = request.POST['cpassword']
            firstname = request.POST['fname']
            lname = request.POST['lname']
            if username and password and email and cpassword and firstname and lname:
                if password == cpassword:
                    user = User.objects.create_user(username,email,password)
                    user.first_name = firstname
                    user.last_name = lname
                    user.save()
                    if user:
                        messages.success(request,"User Account Created")
                        return redirect("login")
                    else:
                        messages.error(request,"User Account Not Created")
                else:
                    messages.error(request,"Password Not Matched")
                    redirect("signup")
        return render(request,'signup.html')

def Login(request):
    if request.user.is_authenticated:
        return redirect("login")
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            if username and password:
                user = authenticate(username=username,password=password)
                if user is not None:
                    login(request,user)
                    return redirect('home')
        return render(request,'login.html')
# User logout function

def Logout(request):
    logout(request)
    return redirect("home")

@login_required()
def create_folder(request):
    if request.method == 'POST':
        foldername = request.POST.get('foldername')
        FolderDetail.objects.create(foldername=foldername, folderuser=request.user, parent_folder=None)
    return redirect('home')

@login_required()
def folder_detail(request, folder_id):
    folder = FolderDetail.objects.get(pk=folder_id)
    subfolders = folder.children.all()
    files = FileDetail.objects.filter(folder=folder)
    if request.method == 'POST':
        foldername = request.POST.get('foldername')
        uploaded_file = request.FILES.get('file')

        if foldername:
            # Create a new folder inside the current folder
            new_folder = FolderDetail(foldername=foldername, folderuser=request.user, parent_folder=folder)
            new_folder.save()
            return redirect('folder_detail', folder_id=folder.id)

        elif uploaded_file:
            # Process the uploaded file and save it in the current folder
            file_instance = FileDetail(filetitle=uploaded_file.name, folder=folder, file=uploaded_file)
            file_instance.save()
            return redirect('folder_detail', folder_id=folder.id)

    return render(request, 'folder_detail.html', {'folder': folder, 'subfolders': subfolders, 'files': files})

@login_required()
def file_detail(request, file_id):
    file = get_object_or_404(FileDetail, pk=file_id)
    if request.method == 'POST' and 'delete_file' in request.POST:
        # Delete the file
        file.delete()
        return redirect('folder_detail', folder_id=file.folder.id)
    return render(request, 'file_detail.html', {'file': file})

@login_required()
def folder_delete(request, folder_id):
    folder = get_object_or_404(FolderDetail, pk=folder_id)
    files_to_delete = FileDetail.objects.filter(folder=folder)
    for file in files_to_delete:
        file.delete()
    # Recursively delete all subfolders and the folder itself
    def delete_folder_and_subfolders(folder):
        subfolders_to_delete = FolderDetail.objects.filter(parent_folder=folder)
        for subfolder in subfolders_to_delete:
            delete_folder_and_subfolders(subfolder)
        folder.delete()
    delete_folder_and_subfolders(folder)
    return redirect('home') 
    # return HttpResponse(status=200)

@login_required()
def file_download(request, file_id):
    file = get_object_or_404(FileDetail, pk=file_id)
    response = HttpResponse(file.file, content_type='application/force-download')
    response['Content-Disposition'] = f'attachment; filename="{file.filetitle}"'
    return response













