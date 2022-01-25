from Watchman.models import Visitor, Watchman
from Chairman.models import User
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from MemberApp.models import *

# Create your views here.

def sign_up(request):
    
    if request.POST:
        email = request.POST['email']
        password = ""
        role = "watchman"

        uid = User.objects.create(email = email, password = password, role =role)
        wid = Watchman.objects.create(
                user_id = uid,
                firstname = request.POST['firstname'],
                lastname = request.POST['lastname'],
                contact = request.POST['contact'],
                id_pic = request.FILES['id_proof']
            )
        
        if wid:
                msg = "You have been Successfully registered, Your password will ge generated and sent to you when your Status will be Approved"
                send_mail("Welcome to Super City",msg,"anjali.20.learn@gmail.com",[email])
                s_msg = "You have been Successfully registered"

                context = {
                            'uid':uid,
                            'wid':wid,
                        }
                
                return  render(request,"Chairman/login.html",{'context':context,'s_msg':s_msg})

    else:

        return render(request,"watchman/sign-up.html")

def w_dashboard(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
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


def w_profile(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])

        if request.POST:
            cpassword = request.POST['cpassword']
            npassword = request.POST['npassword']
            if uid.password == cpassword:
                uid.password = npassword
                uid.save()
                return redirect('w-profile')
        else:
            if uid.role == "watchman":
                wid = Watchman.objects.get(user_id = uid)
                context = {
                            'uid':uid,
                            'wid':wid,
                        }
                return render(request,"watchman/w_profile.html",{'context':context})
            else:
                pass
    else:
        return redirect('login')

def w_all_member(request):
    if "email" in request.session:
        print('---->>>>>>>>')
        uid = User.objects.get(email = request.session['email'])
        wid = Watchman.objects.get(user_id = uid)
        m_all = Member.objects.all()
        context = {
                    'uid':uid,
                    'wid':wid,
                    'm_all':m_all,
                }
        return render(request,"watchman/w-all-members.html",{'context':context})
    
def w_all_notice(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        wid = Watchman.objects.get(user_id = uid)
        n_all = Notice.objects.all()
        context = {
            'uid':uid,
            'wid':wid,
            'n_all':n_all
        }

        return render(request,"watchman/w-all-notice.html",{'context':context})
    else:
        return redirect('login')

def w_all_event(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        wid = Watchman.objects.get(user_id = uid)
        e_all = Event.objects.all()
        context = {
            'uid':uid,
            'wid':wid,
            'e_all':e_all
        }

        return render(request,"watchman/w-all-event.html",{'context':context})
    else:
        return redirect('login')

def w_add_visitor(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        wid = Watchman.objects.get(user_id = uid)
        house_all = House.objects.all()

        if request.POST:
            vid = Visitor.objects.create(
                house_no = request.POST['house_no'],
                firstname = request.POST['fname'],
                lastname = request.POST['lname'],
                phone = request.POST['phone'],
                v_detail = request.POST['vehicle_type']
            )

            context={   
            'uid':uid,
            'wid':wid,
            'house_all':house_all,
            }

            return render(request,"watchman/w-add-visitors.html",{'context':context})
            

        context={   
            'uid':uid,
            'wid':wid,
            'house_all':house_all,
        }

        return render(request,"watchman/w-add-visitors.html",{'context':context})   

    else:
        return redirect('login')


def w_all_visitor(request):
    if "email" in request.session:
        uid = User.objects.get(email=request.session['email'])
        wid = Watchman.objects.get(user_id=uid)

        v_all = Visitor.objects.all()
        context={   
            'uid':uid,
            'wid':wid,
            'v_all':v_all,
        }

        return render(request,"watchman/w-all-visitors.html",{'context':context})
    else:
        return redirect('login')