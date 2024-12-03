from django.shortcuts import render,HttpResponse,get_object_or_404
from django.core.files.storage import FileSystemStorage
from .models import *
import datetime

def index(request):
    request.session['log']="out"
    return render(request,'public/index.html')

def register(request):
    if 'submit' in request.POST:
        username=request.POST['username']
        password=request.POST['password']
        firstname=request.POST['firstname']
        place=request.POST['place']
        gender=request.POST['gender']
        dob=request.POST['dob']
        address=request.POST['address']
        photo=request.FILES['photo']
        date=datetime.datetime.now().strftime("%Y%m%d-%H%M%S")+".jpg"
        fs = FileSystemStorage() 
        fp = fs.save(date, photo)
        q=Login(username=username,password=password,user_type='student')
        q.save()
        q1=Register(LOGIN=q,firstname=firstname,place=place,gender=gender,dob=dob,address=address,photo=fs.url(fp))
        q1.save()
        return HttpResponse(f"<script>alert('Registered');window.location='/login'</script>")
    return render(request,'public/register.html')

def login(request):
    if "submit" in request.POST:
        username=request.POST['username']
        password=request.POST['password']
        if Login.objects.filter(username=username,password=password).exists():
            q=Login.objects.get(username=username,password=password)
            request.session['login_id']=q.pk
            login_id=request.session['login_id']
            if q.user_type=='admin':
                return HttpResponse(f"<script>alert('admin login success');window.location='/admin_home'</script>")
            if q.user_type=='student': 
                q1 = Register.objects.get(LOGIN_id=login_id)
                if q1:
                    request.session['student_id']=q1.pk
                    return HttpResponse(f"<script>alert('Student login success');window.location='/student_home'</script>")
                else:
                    return HttpResponse(f"<script>alert('invalid Student login');window.location='/login'</script>")                
        else:
             return HttpResponse(f"<script>alert('invalid..');window.location='/login'</script>")
    return render(request,'public/login.html')

def admin_home(request):
    event_notification = Notifications.objects.all()
    if request.session['login_id']=="out":
        return HttpResponse(f"<script>alert('You havent logged in yet...!');window.location='/login'</script>")
    return render(request,'admin/admin_home.html',{'event_notification':event_notification}) 

def student_home(request):
    if request.session['login_id']=='out':
        return HttpResponse(f"<script>alert('You havent logged in yet...!');window.location='/login'</script>")
    return render(request,'student/student_home.html')


def event_notification(request):
    if "submit" in request.POST:
        event=request.POST['event']
        posted_date=request.POST['posted_date']
        venue=request.POST['venue']
        date=request.POST['date']
        time=request.POST['time']
        fees=request.POST['fees']
        available_ticket=request.POST['available_ticket']
        event_notification=Notifications(event=event,posted_date=posted_date,venue=venue,date=date,time=time,fees=fees,available_ticket=available_ticket)
        event_notification.save()
        return HttpResponse("<script>alert('Event rule added successfully!');window.location='/admin_home'</script>")
    return render(request, 'admin/add_event_notification.html')

def edit_event_notification(request,id):
    event_notification = Notifications.objects.get(id=id)
    if 'submit' in request.POST:
        event_notification.event = request.POST['event']
        event_notification.venue = request.POST['venue']
        event_notification.posted_date = request.POST['posted_date']
        event_notification.date = request.POST['date']
        event_notification.time = request.POST['time']
        event_notification.fees = request.POST['fees']        
        event_notification.save()
        return HttpResponse(f"<script>alert('Event updated successfully!');window.location='/admin_home'</script>")
    return render(request, 'admin/edit_event_notification.html', {'event_notification': event_notification})

def delete_event_notification(request, id):
    delete_event_notification = Notifications.objects.get(id=id)
    delete_event_notification.delete()
    return HttpResponse("<script>alert('Notification Deleted :( '); window.location='/admin_home';</script>")

def student_event(request):
    event_notification = Notifications.objects.all()
    return render(request,'student/student_event.html',{'event_notification':event_notification})

def sent_notes(request):
    students=Register.objects.all()
    sent_notes=Notes.objects.all()
    if 'submit' in request.POST:
        notes = request.POST['notes']
        student_id = request.POST['student_id']
        student_notes=Notes(notes=notes , Register_id=student_id ,reply='pending' )
        student_notes.save()
        return HttpResponse(f"<script>alert('Notes Added !');window.location='/sent_notes'</script>")
    context={'students':students,'sent_notes':sent_notes}
    return render(request,'admin/sent_notes.html',context)

def edit_notes(request,id):
    sent_notes=Notes.objects.get(id=id)
    if 'submit' in request.POST:
       sent_notes.notes = request.POST['notes']
       sent_notes.save()
       return HttpResponse(f"<script>alert('Notes updated successfully!');window.location='/sent_notes'</script>")
    return render(request, 'admin/edit_notes.html', {'sent_notes': sent_notes})

def delete_notes(request,id):
   delete_notes=Notes.objects.get(id=id)
   delete_notes.delete()
   return HttpResponse("<script>alert('Notes Deleted :( '); window.location='/sent_notes';</script>")

def students_view(request):
    student_id=request.session['student_id']
    sent_notes=Notes.objects.filter(Register_id=student_id)
    return render(request,'student/student_view.html',{'sent_notes':sent_notes})

def students_reply(request,id):
    sent_notes=Notes.objects.get(id=id)
    if 'submit' in request.POST:
        sent_notes.reply=request.POST['reply']
        sent_notes.save()
        return HttpResponse(f"<script>alert('Reply submitted successfully!');window.location='/student_profile'</script>")
    return render(request, 'student/student_reply.html', {'sent_notes': sent_notes})

def student_profile(request):
    student_id=request.session['student_id']
    student_profile= Register.objects.get(id=student_id)
    return render(request,'student/student_profile.html',{'student_profile':student_profile})

def student_edit_profile(request):
    student_id=request.session['student_id']
    student_profile= Register.objects.get(id=student_id)
    if 'submit' in request.POST:
        student_profile.firstname=request.POST['firstname']
        student_profile.place=request.POST['place']
        student_profile.gender=request.POST['gender']
        student_profile.dob=request.POST['dob']
        student_profile.address=request.POST['address']
        if 'photo' in request.FILES:
            photo=request.FILES['photo']
            import datetime
            date = datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + ".jpg"
            fs = FileSystemStorage()
            fp = fs.save(date, photo)
            student_profile.photo = fs.url(fp)
        student_profile.save()
        return HttpResponse(f"<script>alert('Profile Edit Successfully!');window.location='/student_profile'</script>")
    return render(request, 'student/student_edit_profile.html', {'student_profile': student_profile})

        