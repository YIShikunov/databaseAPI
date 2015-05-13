from django.conf.urls import patterns,  url

urlpatterns = patterns('',
    url(r"^db/api/user/create/$", 'forumDB.views.user.create', name='user_create'),
    url(r"^db/api/user/follow/$", 'forumDB.views.user.follow', name='follow'),
    url(r"^db/api/user/unfollow/$", 'forumDB.views.user.unfollow', name='unfollow'),
    url(r"^db/api/user/details/$", 'forumDB.views.user.details', name='user_details'),
    url(r"^db/api/user/updateProfile/$", 'forumDB.views.user.update', name='user_update'),
    url(r"^db/api/user/listFollowers/$", 'forumDB.views.user.list_followers', name='list_followers'),
    url(r"^db/api/user/listFollowing/$", 'forumDB.views.user.list_following', name='list_following'),
    url(r"^db/api/user/listPosts/$", 'forumDB.views.user.list_posts', name='list_posts'),

    url(r"^db/api/forum/create/$", 'forumDB.views.forum.create', name='forum_create'),
    url(r"^db/api/forum/details/$", 'forumDB.views.forum.details', name='forum_details'),
    url(r"^db/api/forum/listThreads/$", 'forumDB.views.forum.list_threads', name='forum_list_threads'),
    url(r"^db/api/forum/listPosts/$", 'forumDB.views.forum.list_posts', name='forum_list_posts'),
    url(r"^db/api/forum/listUsers/$", 'forumDB.views.forum.list_users', name='forum_list_users'),

    url(r"^db/api/thread/create/$", 'forumDB.views.thread.create', name='thread_create'),
    url(r"^db/api/thread/subscribe/$", 'forumDB.views.thread.subscribe', name='subscribe'),
    url(r"^db/api/thread/unsubscribe/$", 'forumDB.views.thread.unsubscribe', name='unsubscribe'),
    url(r"^db/api/thread/details/$", 'forumDB.views.thread.details', name='thread_details'),
    url(r"^db/api/thread/vote/$", 'forumDB.views.thread.vote', name='thread_vote'),
    url(r"^db/api/thread/open/$", 'forumDB.views.thread.open', name='thread_open'),
    url(r"^db/api/thread/close/$", 'forumDB.views.thread.close', name='thread_close'),
    url(r"^db/api/thread/list/$", 'forumDB.views.thread.list', name='thread_list'),
    url(r"^db/api/thread/update/$", 'forumDB.views.thread.update', name='thread_update'),
    url(r"^db/api/thread/listPosts/$", 'forumDB.views.thread.list_posts', name='thread_list_post'),
    url(r"^db/api/thread/remove/$", 'forumDB.views.thread.remove', name='thread_remove'),
    url(r"^db/api/thread/restore/$", 'forumDB.views.thread.restore', name='thread_restore'),

    url(r"^db/api/post/create/$", 'forumDB.views.post.create', name='post_create'),
    url(r"^db/api/post/details/$", 'forumDB.views.post.details', name='post_details'),
    url(r"^db/api/post/update/$", 'forumDB.views.post.update', name='post_update'),
    url(r"^db/api/post/remove/$", 'forumDB.views.post.remove', name='post_remove'),
    url(r"^db/api/post/restore/$", 'forumDB.views.post.restore', name='post_restore'),
    url(r"^db/api/post/vote/$", 'forumDB.views.post.vote', name='post_vote'),
    url(r"^db/api/post/list/$", 'forumDB.views.post.list', name='post_list'),

    url(r"^db/api/clear/$", 'forumDB.views.user.clear', name='clear'),

)
