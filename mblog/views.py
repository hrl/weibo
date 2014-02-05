from django.http import HttpResponse
from django.shortcuts import render_to_response
from mblogdb.models import UserDetail
import datetime
import re
from flask import Markup

from mblogdb.config import *
from mblogdb.models import *

from django import forms
from django.forms.util import ErrorList
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect

from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from math import ceil

def get_time():
    return unicode(datetime.datetime.now())[:19]

def inform(user_id, inform_type, body):
    user_id = int(user_id)
    user = User.objects.filter(id=user_id).get()
    type_dict = {'post': 0,
                 'comment': 1,
                 'message': 2}
    inform_type = type_dict[inform_type]
    new_inform = InformPool(user=user,
                            inform_type=inform_type,
                            body=body,
                            date=get_time())
    new_inform.save()

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            if request.POST.has_key('nickname'):
                nickname = request.POST['nickname']
            else:
                nickname = request.POST['username']
            nickname = unicode(Markup.escape(nickname))
            new_user = User.objects.create_user(username=request.POST['username'],
                                                password=request.POST['password1'])
            new_user.save()

            new_user_detail = UserDetail(user=new_user,
                                         nickname=nickname)
            new_user_detail.save()
            return HttpResponseRedirect("/login")
    else:
        form = UserCreationForm()
    return render_to_response("register.html", {
        'form': form,
    },context_instance=RequestContext(request))

def logout(request):
    auth.logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect("/")

@login_required(login_url="/login")
def profile(request):
    class ProfileForm(forms.Form):
        nickname = forms.CharField(max_length=30)
        self_describe = forms.CharField(max_length=140,required=False)
        mail = forms.EmailField()
        image = forms.URLField(required=False)
        birthday = forms.DateField(required=False)

    user = UserDetail.objects.get(user=request.user.id)

    if request.method == "POST":
        form = ProfileForm(request.POST)
        if form.is_valid():
            cdata = form.cleaned_data

            # sex
            if request.POST['sex'] == 'man':
                sex = True
            elif request.POST['sex'] == 'woman':
                sex = False
            else:
                sex = None

            # sexual orientation
            if request.POST['sexual_orientation'] == 'unknow':
                sexual_orientation = 0
            elif request.POST['sexual_orientation'] == 'heterosexuality':
                sexual_orientation = 1
            elif request.POST['sexual_orientation'] == 'homosexuality':
                sexual_orientation = 2
            elif request.POST['sexual_orientation'] == 'bisexuality':
                sexual_orientation = 3
            elif request.POST['sexual_orientation'] == 'transgender':
                sexual_orientation = 4
            elif request.POST['sexual_orientation'] == 'asexuality':
                sexual_orientation = 5
            else:
                sexual_orientation = 0

            # city

            # update
            cnickname = unicode(Markup.escape(cdata.get('nickname', user.user.username)))
            user.nickname = cnickname
            user.self_describe = cdata.get('self_describe', '')
            user.mail = cdata.get('mail', None)
            user.image = cdata.get('image', '/static/images/avatar.jpg')
            user.birthday = cdata.get('birthday', '2014-01-01')
            user.city = 0
            user.sex = sex
            user.sexual_orientation = sexual_orientation
            user.save()

    else:
        form = ProfileForm()
    return render_to_response("profile.html",
                              {'form':form},
                              context_instance=RequestContext(request))

@login_required(login_url="/login")
def password(request):
    class PasswordForm(forms.Form):
        old_password = forms.CharField()
        new_password = forms.CharField()
        password_confirmation = forms.CharField()

        def clean_password_confirmation(self):
            cnew_password = self.cleaned_data['new_password']
            cpassword_confirmation = self.cleaned_data['password_confirmation']
            if cnew_password != cpassword_confirmation:
                raise forms.ValidationError("The two password fields didn't match")
            return cpassword_confirmation

    user = User.objects.get(id=request.user.id)

    if request.method == "POST":
        form = PasswordForm(request.POST)
        if form.is_valid():
            if user.check_password(form.cleaned_data.get('old_password', '')):
                user.set_password(form.cleaned_data['new_password'])
                user.save()
            else:
                form.errors["old_password"] = ErrorList([u'Invalid Password.'])
    else:
        form = PasswordForm()
    return render_to_response("password.html",
                              {'form':form},
                              context_instance=RequestContext(request))

def home(request, uid):
    pass

def following(request, uid):
    target_user = User.objects.filter(id=uid).get()

    # temp handle
    following_number = target_user.following.count()
    try:
        page = int(request.GET['page'])
    except:
        page = 1
    max_page = int(ceil(float(following_number) / USER_PER_PAGE))
    max_page = max(1, max_page)
    page = min(page, max_page)

    following_list = target_user.following.all()[(page-1)*USER_PER_PAGE:
                                                page*USER_PER_PAGE]

    return render_to_response("following.html", {
        'target_user': target_user,
        'following_list': following_list,
        'page': page,
        'max_page': max_page,
    }, context_instance=RequestContext(request))

def follower(request, uid):
    target_user = User.objects.filter(id=uid).get()

    # temp handle
    follower_number = target_user.follower.count()
    try:
        page = int(request.GET['page'])
    except:
        page = 1
    max_page = int(ceil(float(follower_number) / USER_PER_PAGE))
    max_page = max(1, max_page)
    page = min(page, max_page)

    follower_list = target_user.follower.all()[(page-1)*USER_PER_PAGE:
                                                page*USER_PER_PAGE]

    return render_to_response("follower.html", {
        'target_user': target_user,
        'follower_list': follower_list,
        'page': page,
        'max_page': max_page,
    }, context_instance=RequestContext(request))

def follow(request):
    try:
        target_user = User.objects.filter(id=int(request.GET['uid'])).get()
        user = request.user
        now = get_time()
        assert user != target_user
        assert Follow.objects.filter(user=user, follow=target_user).count() == 0
        following = Follow(user=user, follow=target_user, date=now)
        following.save()
        return HttpResponse('success')
    except:
        raise
        return HttpResponse('fail')

# write microblog
def convert_at_link(nickname):
    if UserDetail.objects.filter(nickname=nickname).count() == 1:
        user_id = int(UserDetail.objects.filter(nickname=nickname).get().user_id)
        link = u"<a class='at_link' href='/u/" + unicode(user_id) + u"'>" \
            + u"@" + unicode(nickname) + u" </a>"
        return link
    else:
        return u"@" + nickname + u' '

def convert_topic_link(topic):
    if Topic.objects.filter(name=topic).count() == 0:
        new_topic = Topic(name=topic)
        new_topic.save()
        topic_id = new_topic.id
    else:
        topic_id = int(Topic.objects.filter(name=topic).get().id)

    link = u"<a class='topic_link' href='/t/" + unicode(topic_id) + u"'>" \
        + u"#" + unicode(topic) + u"#</a>"
    return link

def text_handle(text, text_type):
    text = unicode(Markup.escape(text))

    # @user
    text = re.sub(r'@[^@]+? ',
                  lambda x: convert_at_link(x.group(0)[1:-1]),
                  text)

    if text_type == u'post':
        # #topic#
        text = re.sub(r'#[^#]+?#',
                      lambda x: convert_topic_link(x.group(0)[1:-1]),
                      text)

    return text

def link_topicid_post(topicid, post):
    topicid = int(topicid)
    topic = Topic.objects.filter(id=topicid).get()
    post.topic.add(topic)
    post.save()

class WriteForm(forms.Form):
    repo = forms.IntegerField(required=False)
    body = forms.CharField(max_length=140)
    image = forms.CharField(required=False)
    audio = forms.CharField(required=False)
    video = forms.CharField(required=False)

    def clean_image(self):
        cimage = self.cleaned_data['image']
        if len(cimage.split('/////')) > IMAGE_PER_POST+1:
            raise forms.ValidationError("Invalid input: too many images")
        image_re = re.compile(r'[^?#]+\.jpeg$|[^?#]+\.jpg$|[^?#]+\.png$|[^?#]+\.bmp$')
        for image_url in cimage.split('/////')[1:]:
            try:
                assert image_url == re.search(image_re, image_url).group(0)
            except:
                raise forms.ValidationError("Invalid image.")
        return cimage

    def clean_audio(self):
        caudio = self.cleaned_data['audio']
        if len(caudio.split('/////')) > AUDIO_PER_POST+1:
            raise forms.ValidationError("Invalid input: too many audios")
        audio_re = re.compile(r'[^?#]+\.mp3$|[^?#]+\.wav$|[^?#]+\.ogg$')
        for audio_url in caudio.split('/////')[1:]:
            try:
                assert audio_url == re.search(audio_re, audio_url).group(0)
            except:
                raise forms.ValidationError("Invalid audio.")
        return caudio

    def clean_video(self):
        cvideo = self.cleaned_data['video']
        if len(cvideo.split('/////')) > VIDEO_PER_POST+1:
            raise forms.ValidationError("Invalid input: too many videos")
        video_re = re.compile(r'[^?#]+\.mp4$|[^?#]+\.flv$|[^?#]+\.ogg$')
        for video_url in cvideo.split('/////')[1:]:
            try:
                assert video_url == re.search(video_re, video_url).group(0)
            except:
                raise forms.ValidationError("Invalid video.")
        return cvideo

@login_required(login_url="/login")
def write(request):
    if request.method == "POST":
        form = WriteForm(request.POST)
        if form.is_valid():
            cdata = form.cleaned_data
            try:
                repo = int(cdata['repo'])
            except:
                repo = None
            body = cdata['body']
            image = cdata.get('image', '')
            audio = cdata.get('video', '')
            video = cdata.get('video', '')

            safe_body = text_handle(body, 'post')

            new_post = Post(user=request.user,
                            repo=repo,
                            body=body,
                            encoded_body=safe_body,
                            image=image,
                            audio=audio,
                            video=video,
                            date=get_time(),
                            is_active=True)
            new_post.save()

            # link topic post
            re.sub(r"href='/t/\d+'",
                   lambda x: link_topicid_post(x.group(0)[9:-1], new_post),
                   safe_body)

            # inform @
            re.sub(r"href='/u/\d+'",
                   lambda x: inform(x.group(0)[9:-1], 'post', new_post.id),
                   safe_body)
    else:
        form = WriteForm()
    return render_to_response("write.html",
                              {'form': form},
                              context_instance=RequestContext(request))

def main(request):
    return render_to_response("main.html", context_instance=RequestContext(request))

def hello(request):
    return HttpResponse("Hello world!")

def current_time(request):
    now = datetime.datetime.now()
    return render_to_response('current_time.html', {'current_date': now})

def hours_ahead(request, offset):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()
    dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    html = "<html><body>In %s hour(s), \
        It will be %s.</body></html>" % (offset, dt)
    return HttpResponse(html)

def display_meta(request):
    values = request.META.items()
    #values = request.GET.items()
    #values = request.POST.items()
    values.sort()
    html = []
    for k, v in values:
        html.append('<tr><td>%r</td><td>%r</td></tr>' % (k, v))
    return HttpResponse('<table>%s</table>' % '\n'.join(html))

def search_form(request):
    return render_to_response('search_form.html')

def search(request):
    if 'q' in request.GET:
        q = request.GET['q']
        users = User.objects.filter(username__icontains=q)
        return render_to_response('search_results.html',
                                  {'users': users, 'query': q})
    else:
        return HttpResponse('You submitted an empty form.')
