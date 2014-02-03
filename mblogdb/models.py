from django.db import models
from django.contrib.auth.models import User

class UserDetail(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    nickname = models.CharField(max_length=30, unique=True)
    self_describe = models.TextField(blank=True)
    mail = models.EmailField(unique=True)
    image = models.URLField(blank=True)
    birthday = models.DateField(blank=True, null=True)
    city = models.IntegerField(blank=True, null=True)
    sex = models.NullBooleanField(blank=True)
    sexual_orientation = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        return self.nickname

class Follow(models.Model):
    user = models.ForeignKey(User, related_name="following")
    # u = User()
    # u.following.count() -> the number of people that u is following
    # u.following.get().follow -> one user that u is following
    # u.following.get().user -> u

    follow = models.ForeignKey(User, related_name="follower")
    # u = User()
    # u.follower.count() -> the number of people who is following u
    # u.follower.get().user -> one user who is following u
    # u.follower.get().follow -> u

    date = models.DateTimeField()

class Post(models.Model):
    user = models.ForeignKey(User, related_name="post")
    repo = models.ForeignKey('self', related_name="repoed",
                             blank=True, null=True)
    body = models.TextField()
    encoded_body = models.TextField()
    image = models.TextField(blank=True)
    audio = models.TextField(blank=True)
    bideo = models.TextField(blank=True)
    date = models.DateTimeField()
    is_active = models.BooleanField()

class Comment(models.Model):
    post = models.OneToOneField(Post, related_name="comment")
    reco = models.ForeignKey('self', related_name="recoed",
                             blank=True, null=True)
    user = models.ForeignKey(User, related_name="comment")
    body = models.TextField()
    date = models.DateTimeField()
    is_active = models.BooleanField()

class Message(models.Model):
    sender = models.ForeignKey(User, related_name="message_send")
    # u = User()
    # u.message_send.count() -> the number of messages that u has sent
    # u.message_send.get() -> one message that u has sent

    recipient = models.ForeignKey(User, related_name="message_received")
    body = models.TextField()
    date = models.DateTimeField()
    is_active = models.BooleanField()

class InformPool(models.Model):
    "new @/Message : send to InformPool; read information: clean InformPool"
    user = models.ForeignKey(User, related_name="information")

    inform_type = models.IntegerField()
    # 0:post
    # 1:comment
    # 2:Message

    body = models.TextField()
    date = models.DateTimeField()

class Collect(models.Model):
    user = models.ForeignKey(User, related_name="collection")
    # u = User()
    # u.collention.count() -> the number of posts that u is collecting

    post = models.ForeignKey(Post, related_name="collector")
    # p = Post()
    # p.collector.count() -> the number of people that is collecting p

class Topic(models.Model):
    name = models.CharField(max_length=140)
