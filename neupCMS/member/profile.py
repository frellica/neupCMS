﻿#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response,RequestContext,get_object_or_404
from django.contrib import auth
from django.http import HttpResponseRedirect
from neupCMS.custom_proc import custom_proc
from neupCMS.member.group_auth import in_editor_group,in_admin_group
from django.contrib.auth.decorators import login_required,user_passes_test
from articles.models import Type,Article,AddonArticle
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@login_required
#@user_passes_test(in_editor_group)
def profile_page(request,username):
    user=get_object_or_404(auth.models.User,username=username)
    page = request.GET.get('page','')
    profile_dict={
        'username':username,
        'email':user.email,
    }
    article_list=[{'aid':item.aid,'is_deleted':item.is_deleted,'is_verified':item.is_verified,'is_headline':item.is_headline,'title':item.title,'authorname':item.authorname,'typename':Type.objects.get(typeid=item.typeid).typename} for item in Article.objects.filter(authorname=user.username)]
    verify_auth=in_editor_group(request.user)
    resume_auth=in_admin_group(request.user)
    p = Paginator(article_list,10)
    try:
        article_list = p.page(page)
    except PageNotAnInteger:
        # 如果页码不是整数，返回第一页.
        article_list = p.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        article_list = p.page(p.num_pages)
    return render_to_response('member-profile.html',{'profile_dict':profile_dict,
        'article_list':article_list,
        'verify_auth':verify_auth,
        'resume_auth':resume_auth,
        'page_title':username},context_instance=RequestContext(request,processors=[custom_proc]))