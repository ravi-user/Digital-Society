from django.http.response import JsonResponse
from django.urls.conf import path
from .models import *
from Chairman.models import User
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.conf import  settings
from .paytm import generate_checksum, verify_checksum
import datetime
from django.core.mail import send_mail
from .utils import *


# Create your views here.

def m_dashboard(request):
    if "email" in request.session:
        uid = User.objects.get(email=request.session['email'])
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
        return redirect('login')

def m_all_members(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        if uid.role == "member":
            mid = Member.objects.get(user_id = uid)
            m_all = Member.objects.exclude(user_id =uid)
            context = {
                'uid':uid,
                'mid':mid,
                'm_all':m_all
            }
            return render(request,"MemberApp/m-all-mem.html",{'context':context})

def m_profile(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])

        if request.POST:
            currentpassword = request.POST['currentpassword']
            newpassword = request.POST['newpassword']

            if uid.password == currentpassword:
                uid.password = newpassword
                uid.save()
                return redirect('m-profile')
        else:
            if uid.role == "member":
                mid = Member.objects.get(user_id = uid)
                context = {
                    'uid':uid,
                    'mid':mid,
                }
                return render(request,"MemberApp/m_profile.html",{'context':context})
            else:
                pass
    else:
        return redirect('login')

def m_upload_pic(request):
    if "email" in request.session:
        uid = User.objects.get(email=request.session['email'])
        mid = Member.objects.get(user_id=uid)
        pic = request.FILES['pic']

        mid.profile_pic = pic
        mid.save()

        return redirect('m-profile')
    
    else:
        return redirect('login')

def m_add_member(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        if uid.role == "member":
            mid = Member.objects.get(user_id = uid)
            m_all = Member.objects.exclude(user_id =uid)
            context = {
                'uid':uid,
                'mid':mid,
                'm_all':m_all
            }
            return render(request,"MemberApp/m_add_member.html",{'context':context})


def m_add_complain(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        mid = Member.objects.get(user_id = uid)

        if request.POST:
            if "pic" in request.FILES and "video" not in request.FILES:
                cid = Compain.objects.create(
                    title = request.POST['title'],
                    description = request.POST['description'],
                    pic = request.FILES['pic']
                )
            
            elif "video" in request.FILES and "pic" not in request.FILES:
                cid = Compain.objects.create(
                    title = request.POST['title'],
                    description = request.POST['description'],
                    videofile = request.FILES['video']
                )
            
            elif "video" in request.FILES and "pic" in request.FILES:
                cid = Compain.objects.create(
                    title = request.POST['title'],
                    description = request.title['description'],
                    pic = request.FILES['pic'],
                    videofile = request.FILES['video']
                )
            
            else:
                cid = Compain.objects.create(
                    title = request.POST['title'],
                    description = request.POST['description'],
                )
            return redirect('m-add-complain')
    
        else:
            context = {
                'uid':uid,
                'mid':mid
            }
            return render(request,"MemberApp/m-add-complain.html",{'context':context})
    
    else:
        return redirect('login')

def m_all_notice(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        mid = Member.objects.get(user_id = uid)
        n_all = Notice.objects.all().order_by('created_at').reverse()
        context = {
            'uid':uid,
            'mid':mid,
            'n_all':n_all
        }

        return render(request,"MemberApp/m-all-notice.html",{'context':context})
    else:
        return redirect('login')

def m_all_notice_details(request,pk):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        mid = Member.objects.get(user_id = uid)
        nid = Notice.objects.get(id = pk)

        nall = NoticeView.objects.filter(member_id = mid, notice_id = nid)

        if nall:
            print('Alraeady notice read')
        else:
            nvid = NoticeView.objects.create(notice_id = nid, member_id = mid)

        context = {
            'uid':uid,
            'mid':mid,
            'nid':nid
        }

        return render(request,"MemberApp/m-all-notice-details.html",{'context':context})
    else:
        return redirect('login')

def m_all_event(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        mid = Member.objects.get(user_id = uid)

        e_all = Event.objects.all().order_by('created_at').reverse()
        context = {
            'uid':uid,
            'mid':mid,
            'e_all':e_all
        }

        return render(request,"MemberApp/m-all-event.html",{'context':context})
    else:
        return redirect('login')

def m_all_event_details(request,pk):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        mid = Member.objects.get(user_id = uid)
        eid = Event.objects.get(id = pk)

        eall = EventView.objects.filter(member_id = mid, event_id = eid)

        if eall:
            print("Already Read")
        else:
            evid = EventView.objects.create(event_id = eid, member_id = mid)

        context={
            'uid':uid,
            'mid':mid,
            'eid':eid
        }
        return render(request,"MemberApp/m-all-event-details.html",{'context':context})
    else:
        return redirect('login')

@csrf_exempt
def like_notice(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        mid = Member.objects.get(user_id = uid)
        nid = request.POST['id']
        mydata = request.POST['mydata']
        mdata = request.POST['mdata']

        nid = Notice.objects.get(id = nid)
        n_like = LikeNotice.objects.filter(notice_id = nid, member_id = mid)
        
        
        if n_like:
            if n_like[0].status == 'Dislike':
                print('------->>>',n_like)
                print('=======>><<<',n_like[0].status)
                n_like.delete()
                status = "Like"
                n_like = LikeNotice.objects.create(notice_id = nid, member_id = mid, status = status)

            elif n_like[0].status == 'Like':
                n_like.delete()

        else:
            status = "Like"
            n_like = LikeNotice.objects.create(notice_id = nid, member_id = mid, status = status)
            # print('---------->>>>',n_like.status)

        count_like = LikeNotice.objects.filter(notice_id=nid,status='Like').count()
        count_dislike = LikeNotice.objects.filter(notice_id=nid,status='Dislike').count()

        a=''
        if count_like>1:
            a=str(count_like)+"Likes"
        else:
            a=str(count_like)+"Like"

        b=''
        if count_dislike>1:
            b=str(count_dislike)+"Dislikes"
        else:
            b=str(count_dislike)+"Dislike"
        print('====================',mydata)
        context = {
            'msg':'like',
            'mydata':mydata,
            'mdata':mdata,
            'c_like': a,
            'c_dislike': b,
        }

        return JsonResponse({'context':context})

    else:
        return redirect('login')    

@csrf_exempt
def dislike_notice(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        mid = Member.objects.get(user_id = uid)
        nid = request.POST['id']
        mydata = request.POST['mydata']
        mdata = request.POST['mdata']
        nid = Notice.objects.get(id = nid)
        n_dis = LikeNotice.objects.filter(notice_id = nid, member_id = mid)

        if n_dis:
            if n_dis[0].status == 'Like':
                n_dis.delete()
                status = "Dislike"
                n_dislike = LikeNotice.objects.create(notice_id = nid, member_id = mid, status = status)

            elif n_dis[0].status == 'Dislike':
                n_dis.delete()

        else:
            status = "Dislike"
            n_dis = LikeNotice.objects.create(notice_id = nid, member_id = mid, status = status)

        count_like = LikeNotice.objects.filter(notice_id = nid,status='Like').count()
        count_dislike = LikeNotice.objects.filter(notice_id = nid,status='Dislike').count()

        a=''
        if count_like>1:
            a=str(count_like)+" Likes"
        else:
            a=str(count_like)+" Like"

        b=''
        if count_dislike>1:
            b=str(count_dislike)+" Dislikes"
        else:
            b=str(count_dislike)+" Dislike"

        context = {
            'msg':'like',
            'c_like': a,
            'c_dislike': b,
            'mydata':mydata,
            'mdata':mdata,
        }

        return JsonResponse({'context':context})
    
    else:
        return redirect('login')

@csrf_exempt
def like_event(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        mid = Member.objects.get(user_id = uid)
        e_id = request.POST['id']
        eid = Event.objects.get(id = e_id)
        e_like = LikeEvent.objects.filter(event_id = eid, member_id = mid)
        
        
        if e_like:
            if e_like[0].status == 'Dislike':
                # print('------->>>',n_like)
                # print('=======>><<<',n_like[0].status)
                e_like.delete()
                status = "Like"
                n_like = LikeEvent.objects.create(event_id = eid, member_id = mid, status = status)

            elif e_like[0].status == 'Like':
                e_like.delete()

        else:
            status = "Like"
            e_like = LikeEvent.objects.create(event_id = eid, member_id = mid, status = status)
            # print('---------->>>>',n_like.status)

        count_like = LikeEvent.objects.filter(status='Like').count()
        count_dislike = LikeEvent.objects.filter(status='Dislike').count()

        a=''
        if count_like>1:
            a=str(count_like)+" Likes"
        else:
            a=str(count_like)+" Like"

        b=''
        if count_dislike>1:
            b=str(count_dislike)+" Dislikes"
        else:
            b=str(count_dislike)+" Dislike"

        context = {
            'msg':'like',
            'c_like': a,
            'c_dislike': b,
        }

        return JsonResponse({'context':context})

    else:
        return redirect('login')

@csrf_exempt
def dislike_event(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        mid = Member.objects.get(user_id = uid)
        e_id = request.POST['id']
        eid = Event.objects.get(id = e_id)
        e_dis = LikeEvent.objects.filter(event_id = eid, member_id = mid)

        if e_dis:
            if e_dis[0].status == 'Like':
                e_dis.delete()
                status = "Dislike"
                e_dislike = LikeEvent.objects.create(event_id = eid, member_id = mid, status = status)

            elif e_dis[0].status == 'Dislike':
                e_dis.delete()

        else:
            status = "Dislike"
            e_dis = LikeEvent.objects.create(event_id = eid, member_id = mid, status = status)

        count_like = LikeEvent.objects.filter(status='Like').count()
        count_dislike = LikeEvent.objects.filter(status='Dislike').count()

        a=''
        if count_like>1:
            a=str(count_like)+" Likes"
        else:
            a=str(count_like)+" Like"

        b=''
        if count_dislike>1:
            b=str(count_dislike)+" Dislikes"
        else:
            b=str(count_dislike)+" Dislike"

        context = {
            'msg':'like',
            'c_like': a,
            'c_dislike': b,
        }

        return JsonResponse({'context':context})
    
    else:
        return redirect('login')

def maintenance(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        mid = Member.objects.get(user_id = uid)

        currentdate = datetime.date.today()
        print('================',currentdate)
        pid = Maintenance.objects.filter(user_id = uid)
        print('==========pd',pid)
        
        x = currentdate
        # print('yyyyyyyyyyyyyyyy',y)
        # print('zzzzzzzzzzzzzzzzzzzzzzzzz',z)
        
        for m in pid:

            y = m.duedate
            z = datetime.date.fromisoformat(y)

            if m.status == "Pending":
                print('penddddddddddddddddddddiiiiiiiiiin')
                if  x > z: 
                    print('===============dueeeeeeeeeee')
                    m.status = "Due"

            if m.status == "Due":
                total = int(m.amount) + int(m.penalty)
                m.total = total
                m.save()
            elif m.status == "Paid":
                total = int(m.amount)
                m.total = total
                m.save()
         
        context = {
            'uid':uid,
            'mid':mid,
            'pid':pid,
        }

        return render(request,"MemberApp/maintenance.html",{'context':context})

    else:
        return redirect('login')

@csrf_exempt
def initiate_payment(request,pk):
    if "email" in request.session:
        global paymentid
        userid = User.objects.get(email = request.session['email'])
        mid = Member.objects.get(user_id = userid)
        maintenance = Maintenance.objects.get(id=pk)
        paymentid = pk
        amount = maintenance.total

        transaction = Transaction.objects.create(made_by=userid, member_id=mid ,amount=amount,maintenance_id=maintenance)  ##
        transaction.save()
   
        merchant_key = settings.PAYTM_SECRET_KEY

        params = (
            ('MID', settings.PAYTM_MERCHANT_ID),
            ('ORDER_ID', str(transaction.order_id)),
            ('CUST_ID', str(transaction.made_by.email)),
            ('TXN_AMOUNT', str(transaction.amount)),
            ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
            ('WEBSITE', settings.PAYTM_WEBSITE),
            # ('EMAIL', request.user.email),
            # ('MOBILE_N0', '9911223388'),
            ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
            ('CALLBACK_URL', 'http://127.0.0.1:8000/member/callback/'),
            # ('PAYMENT_MODE_ONLY', 'NO'),
        )

        paytm_params = dict(params)
        checksum = generate_checksum(paytm_params, merchant_key)

        transaction.checksum = checksum
        transaction.save()

        paytm_params['CHECKSUMHASH'] = checksum
        print('SENT: ', checksum)
        return render(request, 'MemberApp/redirect.html', context=paytm_params)
    else:
        return redirect('login')
        
@csrf_exempt
def callback(request):
    if request.method == 'POST':
        received_data = dict(request.POST)
        paytm_params = {}
        paytm_checksum = received_data['CHECKSUMHASH'][0]
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
        # Verify checksum
        is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))        
        if is_valid_checksum:
            received_data['message'] = "Checksum Matched"
            if received_data['STATUS'] ==  ['TXN_SUCCESS']:
                maintenance=Maintenance.objects.get(id=paymentid)
                maintenance.status='Paid'
                maintenance.save()
                t_id=Transaction.objects.get(maintenance_id=maintenance)
                #uid=User.objects.get(email=request.session['m_email'])
                print('-----------------',t_id.made_by)
                context={'received_data':received_data}
                print('-----------------------',received_data)
                
                sendPaymentMail('Paytm Payment','email_callback',t_id.made_by,{'maintenance':maintenance,'txnid':received_data['TXNID'],'orderid':received_data['ORDERID'],'txnamount':received_data['TXNAMOUNT']})
        else:
            received_data['message'] = "Checksum Mismatched"
            return render(request, 'MemberApp/callback.html', context=received_data)
        return render(request, 'MemberApp/callback.html', context=received_data)

