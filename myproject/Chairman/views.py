from myproject.settings import EMAIL_HOST_PASSWORD
from django.db.models.fields import CharField
from django.db.models.deletion import PROTECT
from django.shortcuts import render,redirect
from django.urls.conf import path
from .models import *
from django.core.mail import send_mail
from random import randint, choice
from MemberApp.models import *
from Watchman.models import *
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

# Create your views here.

count=0

@csrf_exempt
def login(request):
    global count
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        if uid.role == 'chairman':
            cid = Chairman.objects.get(user_id = uid)
            mcount = Member.objects.all().count()
            ncount = Notice.objects.all().count()
            ecount = Event.objects.all().count()
             
            context={
                'uid':uid,
                'cid':cid,
                'mcount':mcount,
                'ncount':ncount,
                'ecount':ecount,
                
            }
            return render(request, 'chairman/index.html',{'context':context})

        elif uid.role == "member":
            mid = Member.objects.get(user_id = uid)
            mcount = Member.objects.all().count()
            ncount = Notice.objects.all().count()
            ecount = Event.objects.all().count()
            context = {
                'uid':uid,
                'mid':mid,
                'mcount':mcount,
                'ncount':ncount,
                'ecount':ecount,
            }
            return render(request,"MemberApp/m_index.html",{'context':context})
        else:
            wid = Watchman.objects.get(user_id = uid)
            mcount = Member.objects.all().count()
            ncount = Notice.objects.all().count()
            ecount = Event.objects.all().count()
            context = {
                'uid':uid,
                'wid':wid,
                'mcount':mcount,
                'ncount':ncount,
                'ecount':ecount,
            }
            return render(request,"watchman/w_index.html",{'context':context})

    if request.POST:
        try:
            print('---> inside the request post')

            p_email = request.POST['email'] # email (html name = 'email')
            p_password = request.POST['password']

        # here, eamil is fieldname and p_name is python variable which contain html output    
            uid = User.objects.get(email = p_email)       

            print('--->uid',uid)
            print('--->password',uid.password)
            

            if uid:
                if uid.password == p_password:
                    if uid.role == "chairman":
                        count=0
                        print('welcome')
                        cid = Chairman.objects.get(user_id = uid)
                        print('--->',cid.firstname)
                        if cid.gender == "male":
                            cid.profile_pic = "media/default.png"
                            cid.save()
                        elif cid.gender == "female":
                            cid.profile_pic = "media/female.png"
                            cid.save()
                        mcount = Member.objects.all().count()
                        ncount = Notice.objects.all().count()
                        ecount = Event.objects.all().count()
                          
                        context={
                            'uid':uid,
                            'cid':cid,
                            'mcount':mcount,
                            'ncount':ncount,
                            'ecount':ecount,
                            
                        }

                        request.session['email'] = uid.email #storing session in variable
                        # send_mail("DIGITAL SOCIETY","WELCOME TO DIGITAL SOCIETY","anjali.20.learn@gmail.com",[uid.email])
                        return render(request, 'chairman/index.html',{'context':context})

                    elif uid.role == "member":
                        mid = Member.objects.get(user_id = uid)
                        
                        if uid.is_verified == False:
                            email = uid.email
                            otp = randint(1111,9999)      
                            uid.otp = otp
                            uid.save()
                            msg = "your otp is"+str(otp)
                            send_mail("Reset-Password",msg,"anjali.20.learn@gmail.com",[email])
                            return render(request,"MemberApp/m_reset-password.html",{'email':email})
                        else:
                            if mid.gender == "male":
                                mid.profile_pic = "media/default.png"
                                mid.save()
                            elif mid.gender == "female":
                                mid.profile_pic = "media/female.png"
                                mid.save()
                            
                            mcount = Member.objects.all().count()
                            ncount = Notice.objects.all().count()
                            ecount = Event.objects.all().count()
                            
                            context={
                                'uid':uid,
                                'mid':mid,
                                'mcount':mcount,
                                'ncount':ncount,
                                'ecount':ecount,
                            }
                            
                            request.session['email'] = uid.email
                            return render(request,"MemberApp/m_index.html",{'context':context})
                    else:
                        wid = Watchman.objects.get(user_id = uid)

                        if uid.is_verified == False:
                            email = uid.email
                            otp = randint(1111,9999)
                            uid.otp = otp
                            uid.save()
                            msg = "Your OTP is"+str(otp)
                            send_mail("Reset-Password",msg,"anjali.20.learn@gmail.com",[email])
                            return render(request,"Watchman/w_reset-password.html",{'email':email})
                        else:
                            request.session['email'] = uid.email
                            context={
                                'uid':uid,
                                'wid':wid
                            }
                            return render(request,"Watchman/w_index.html",{'context':context})

                else:
                    count+=1
                    e_msg = 'invalid password'
                    if count>2:
                        e_msg = "You Entered Multiple Time Wrong Password. Crate Your New Password"
                        return render(request,"Chairman/forgotpassword.html",{'e_msg':e_msg})
                    else:
                        print('c',count)
                        return render(request, 'chairman/login.html',{'e_msg':e_msg})        
            else:
                print(p_email)               
                return render(request, 'chairman/login.html')
        
        except:
                e_msg='invalid email or password'
                return render(request,'chairman/login.html',{'e_msg':e_msg})

    else:    
        print('---> outside the request post')
        return render(request,  'chairman/login.html')

def logout(request):
    if 'email' in request.session:
        del request.session['email']
        s_msg= 'successfully logout'
        return redirect('login')
    else:
        return redirect('login')

def c_profile(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        
        if request.POST:
            currentpassword = request.POST['currentpassword']
            newpassword = request.POST['newpassword']

            if uid.password == currentpassword:
                uid.password = newpassword
                uid.save() # update
                return redirect('c-profile')
        else:
            if uid.role == 'chairman':
                cid = Chairman.objects.get(user_id = uid)
                
                context={
                    'uid':uid,
                    'cid':cid,
                }
                return render(request, 'chairman/c_profile.html',{'context':context})
            else:
                pass
    else:
        return redirect('login')

def c_dashboard(request):
    return redirect('login')

def upload_pic(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        cid = Chairman.objects.get(user_id = uid)
        pic = request.FILES['pic']

        cid.profile_pic = pic
        cid.save()

        return redirect('c-dashboard')
    else:
        return redirect('login')

    

def forgot_password(request):
    if request.POST:
        email = request.POST['email']
        otp = randint(1111,9999)
        # print('1')
        # uid = User.objects.get(email = email)
        try:
            # print('2')
            uid = User.objects.get(email = email)
            # print('3')        
            if uid:
                uid.otp = otp # store
                uid.save() # update
                msg = "your otp is "+str(otp)
                send_mail("OTP",msg,"anjali.20.learn@gmail.com",[email])
                return render(request,'chairman/reset-password.html',{'email':email})
                
        except:
            # print('except')
            e_msg = "Email does not exist"
            return render(request,'chairman/forgotpassword.html',{'e_msg':e_msg})
    else:        
        return render(request,'chairman/forgotpassword.html')

def reset_password(request):
    if request.POST:
        email= request.POST['email']
        otp = request.POST['otp']
        newpassword = request.POST['newpassword']
        confirmpassword = request.POST['confirmpassword']

        uid = User.objects.get(email = email)

        if newpassword == confirmpassword:
            if str(uid.otp) == otp and uid.email == email:
                uid.password = newpassword
                uid.is_verified = True
                uid.save()
                return redirect('login')
            else:
                e_msg = "Invalid OTP"
                return render(request,"chairman/reset-password.html",{'e_msg':e_msg,'email':email})
        else:
            e_msg = "newpassword and confirmpassword does not match!!!"
            return render(request,"chairman/reset-password.html",{'e_msg':e_msg,'email':email})

    else:
        return redirect('forgot-password') 


def add_member(request):
   if "email" in request.session:
       uid = User.objects.get(email = request.session['email'])
       cid = Chairman.objects.get(user_id = uid)
       l1 = ["aasa34","45asd546","456dsv","8098sd","dsf35f"]
       if request.POST:
           email = request.POST['email']
           password = email[:4]+choice(l1)

           house_no = request.POST['house_no']
           role = "member"

           uid = User.objects.create(email = email,password = password,role = role)
           hid = House.objects.get(house_no = house_no)
           
           hid.status = "Active"
           hid.save()

           mid = Member.objects.create(
                           user_id = uid,
                           house_id = hid,
                           firstname = request.POST['fname'],
                           lastname = request.POST['lname'],
                           mobileno = request.POST['mobileno'],
                           job_specification = request.POST['job_specification'],
                           job_address = request.POST['job_address'],
                           birthdate = request.POST['birthdate'],
                           no_of_members = request.POST['no_of_members'],
                           marrital_status = request.POST['m_status'],
                           locality = request.POST['locality'],
                           nationality = request.POST['nationality'],
                           gender = request.POST['gender'],
                           no_of_vehicles = request.POST['no_of_vehicles'],
                           vehicle_type= request.POST['vehicle_type'],
                           id_proof= request.FILES['id_proof'],
                       )
           if mid:
               msg = "Your Password is :"+password
               send_mail("Welcome to Super City",msg,"anjali.20.learn@gmail.com",[email])
               m_all = Member.objects.all()
               context = {
                   'uid':uid,
                   'cid':cid,
                   'm_all':m_all
               }
               return render(request,"chairman/all-members.html",{'context':context})
               
       else:
           gender = cid.gender
           house_all = House.objects.filter(status = "pending")
           context = {
                       'uid':uid,
                       'cid':cid,
                       'gender':gender,
                       'house_all':house_all,
                   }
           return render(request,"chairman/add-member.html",{'context':context})
   else:
       return redirect('login')

def all_members(request):
    uid = User.objects.get(email = request.session['email'])
    cid = Chairman.objects.get(user_id = uid)
    m_all = Member.objects.all()
    context = {
                'uid':uid,
                'cid':cid,
                'm_all':m_all,
            }
    
    return render(request,"chairman/all-members.html",{'context':context})
            
def add_notice(request):
    if request.POST:
        if "pic" in request.FILES and "video" not in request.FILES:
            nid = Notice.objects.create(
                title = request.POST['title'],
                description = request.POST['description'],
                pic = request.FILES['pic'],
            )
        
        elif "video" in request.FILES and "pic" not in request.FILES:
            nid = Notice.objects.create(
                title = request.POST['title'],
                description = request.POST['description'],
                videofile = request.FILES['video'], 
            )
        
        elif "pic" in request.FILES and "video" in request.FILES:
            nid = Notice.objects.create(
                title = request.POST['title'],
                description = request.POST['description'],
                pic = request.FILES['pic'],
                videofile = request.FILES['video'],
            )
        
        else:
            nid = Notice.objects.create(
                title = request.POST['title'],
                description = request.POST['description'],
            )
        return redirect('add-notice')

    else:
        uid = User.objects.get(email = request.session['email'])
        cid = Chairman.objects.get(user_id = uid)
        context={
            'uid':uid,
            'cid':cid,
        }
        return render(request, "chairman/add-notice.html",{'context':context})

def all_notice(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        cid = Chairman.objects.get(user_id = uid)
        n_all = Notice.objects.all().order_by('created_at').reverse()
        context={
            'uid':uid,
            'cid':cid,
            'n_all':n_all,
        }
        return render(request,"chairman/all-notice.html",{'context':context})
    else:
        return redirect('login')

# def edit_notice(request,pk):
#     if "email" in request.session:
#         uid = User.objects.get(email = request.session['email'])
#         cid = Chairman.objects.get(user_id = uid)
#         nid = Notice.objects.get(id = pk)
#         context = {
#             'uid':uid,
#             'cid':cid,
#             'nid':nid,
#         }
#         return render(request,"Chairman/edit-notice.html",{'context':context})
#     else:
#         return redirect('login')


def add_event(request):
    if request.POST:
        if "pic" in request.FILES and "video" not in request.FILES:
            eid = Event.objects.create(
                title = request.POST['title'],
                description = request.POST['description'],
                pic = request.FILES['pic']
            )

        elif "video" in request.FILES and "pic" not in request.FILES:
            eid = Event.objects.create(
                title = request.POST['title'],
                description = request.POST['description'],
                videofile = request.FILES['video']
            ) 
        elif "video" in request.FILES and "pic" in request.FILES:
            eid = Event.objects.create(
                title = request.POST['title'],
                description = request.POST['description'],
                pic = request.FILES['pic'],
                videofile = request.FILES['video']
            )
        else:
            eid = Event.objects.create(
                title = request.POST['title'],
                description = request.POST['description'],
            )
        return redirect('add-event')
    else:
        uid = User.objects.get(email = request.session['email'])
        cid = Chairman.objects.get(user_id = uid)
        
        context = {
            'uid':uid,
            'cid':cid,
            
        }
        return render(request,"chairman/add-event.html",{'context':context})

def all_event(request):
    uid = User.objects.get(email = request.session['email'])
    cid = Chairman.objects.get(user_id = uid)
    e_all = Event.objects.all().order_by('created_at').reverse()
     
    context={
        'uid':uid,
        'cid':cid,
        'e_all':e_all,
       
    }
    return render(request,"chairman/all-event.html",{'context':context})

def all_complain(request):
    uid = User.objects.get(email = request.session['email'])    
    cid = Chairman.objects.get(user_id = uid)
    com_all = Compain.objects.all()
    context = {
        'cid':cid,
        'com_all':com_all
    }
    return render(request,"chairman/all-complain.html",{'context':context})

def all_watchman(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        cid = Chairman.objects.get(user_id = uid)
        wall = Watchman.objects.all()
        context = {
                'uid':uid,
                'cid':cid,
                'wall':wall,
        }
        for i in wall:
            print('=====<>>>>>',i.id)
        return render(request,"Chairman/all-watchman.html",{'context':context})

def approved(request,pk):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        cid = Chairman.objects.get(user_id = uid)
        
        wid = Watchman.objects.get(user_id = pk)
        wemail = wid.user_id.email        
        wid.status = "approved"
        wid.save()

        l1 = ["aasa34","45asd546","456dsv","8098sd","dsf35f"]
        password = wemail[:4]+choice(l1)

        w_uid = User.objects.get(email = wemail)
        w_uid.password = password
        w_uid.save()

        msg = "You are approved by Chairman... Your password is"+password
        send_mail("DIGITAL SOCIETY",msg,"anjali.20.learn@gmail.com",[wemail])
        return redirect('all-watchman')
    else:
        return redirect('login')

def rejected(request,pk):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        cid = Chairman.objects.get(user_id = uid)

        wid = Watchman.objects.get(user_id = pk)
        wid.status = "rejected"
        wid.save()
        return redirect('all-watchman')

def del_notice(request,pk):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        cid = Chairman.objects.get(user_id = uid)
        
        nid = Notice.objects.get(id = pk)
        nid.delete()

        return redirect('all-notice')
    else:
        return redirect('login')

def del_event(request,pk):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        cid = Chairman.objects.get(user_id = uid)

        eid = Event.objects.get(id = pk)
        eid.delete()

        return redirect('add-event')
    else:
        return redirect('login')

def del_complain(request,pk):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        cid = Chairman.objects.get(user_id = uid)

        com_id = Compain.objects.get(id=pk)
        com_id.delete()

        return redirect('all-complain')
        
    else:
        return redirect('login')


def m_noticeview_details(request,pk):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        cid = Chairman.objects.get(user_id = uid)

        nid = Notice.objects.get(id = pk)
        nvid = NoticeView.objects.filter(notice_id = nid)

        context = {
            'uid':uid,
            'cid':cid,
            'nid':nid,
            'nvid':nvid
        }

        return render(request,"chairman/m-noticeview-details.html",{'context':context})
    
    else:
        return redirect('login')

@csrf_exempt
def check_email(request):
    email = request.POST['email']
    print("-----------> email ajax",email)
    # uid = User.objects.all()
    try:
        uid = User.objects.get(email = email)
        print('--------->>>',uid)
        context = {
        'msg': "success"
    }
    except:
        context = {
            'msg' : "Fail"
        }

    return JsonResponse({'context':context})

@csrf_exempt
def app(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        cid = Chairman.objects.get(user_id = uid)

        myid = request.POST['myid']
        wid = Watchman.objects.get(id = request.POST['id'])
        wemail = wid.user_id.email
        wid.status = "approved"
        x= wid.status
        wid.save()
        l1 = ["aasa34","45asd546","456dsv","8098sd","dsf35f"]
        password = wemail[:4]+choice(l1)

        w_uid = User.objects.get(email = wemail)
        w_uid.password = password
        w_uid.save()

        print('====',x)
        print('------------',myid)
        context = {
            'x' : x,
            'myid' : myid,
        }
        return JsonResponse({'context':context})

    else:
        return redirect('login')

@csrf_exempt
def rejct(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        cid = Chairman.objects.get(user_id = uid)

        myid = request.POST['myid']
        wid = Watchman.objects.get(id = request.POST['id'])
        wemail = wid.user_id.email
        wid.status = "rejected"
        x= wid.status
        wid.save()
        context = {
            'x' : x,
            'myid' : myid,
        }
        return JsonResponse({'context':context})
        # uid = User.objects.get(email = request.session['email'])
        # cid = Chairman.objects.get(user_id = uid)

        # wid = Watchman.objects.get(user_id = pk)
        # wid.status = "rejected"
        # wid.save()
        # return redirect('all-watchman')
        
def add_maintenance(request):
    if "email" in request.session:
        if request.POST:
            amount = request.POST['amount']
            penalty = request.POST['penalty']
            total = amount
            status = "Pending"
            m_all = Member.objects.all()
            for i in m_all:
                email = i.user_id.email
                uid = User.objects.get(email=email)
                mtid = Maintenance.objects.create(
                    user_id = uid,
                    date = request.POST['date'],
                    duedate = request.POST['duedate'],
                    amount = amount,
                    penalty = penalty,
                    total = total,
                    status = status,
            )                                                               
            return redirect('add-maintenance')
        else:
            uid = User.objects.get(email = request.session['email'])
            cid = Chairman.objects.get(user_id = uid)
            context = {
                        'uid':uid,
                        'cid':cid,
            }
            return render(request,"Chairman/add-maintenance.html",{'context':context})
    else:
        return redirect('login')


def view_maintenanace(reqeust):
    if "email" in reqeust.session:
        uid = User.objects.get(email = reqeust.session['email'])
        cid = Chairman.objects.get(user_id = uid)

        t_all = Transaction.objects.all()
         
        context={
            'uid':uid,
            'cid':cid,
            't_all':t_all,
            }
        return render(reqeust,"chairman/view-maintenance.html",{'context':context})
    
    else:
        return redirect('login')