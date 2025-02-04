from django.db import models

# 회원정보
class Member(models.Model):
    userid = models.CharField(max_length=50, null=False, primary_key=True)
    passwd = models.CharField(max_length=500, null=False)
    name = models.CharField(max_length=20, null=False)
    address = models.CharField(max_length=20, null=False)
    tel = models.CharField(max_length=20, null=True)

# 대화내용
class Chat(models.Model):
    idx = models.AutoField(primary_key=True)
    userid = models.CharField(max_length=50, null=False)
    query = models.CharField(max_length=500, null=False)
    answer = models.CharField(max_length=1000, null=False)
    intent = models.CharField(max_length=50, null=False)
