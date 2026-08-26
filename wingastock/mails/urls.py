from django.urls import path
from mails.views_m.index import mail_index, mail_index_c
from mails.views_m.read_m import mail_read, readed, unreaded, compose_m, sent_mails, delete_mail, clear_mails
from mails.views_m.read_m_c import mail_read_c, readed_c, unreaded_c, compose_m_c, sent_mails_c, clear_mails_c, delete_mail_c
from mails.views_m.settings_m import mail_settings, mail_settings_c

urlpatterns = [
    # For seller
    path('', mail_index, name='mail_home'),
    path('read/<str:m_receiver>/', mail_read, name='mail_read'),
    path('unreaded/', unreaded, name='unreaded'),
    path('readed/', readed, name='readed'),
    path('sent_mails', sent_mails, name='sent_mails'),
    path('compose/<str:m_receiver>/', compose_m, name='compose_m'),
    path('settings/', mail_settings, name='mail_settings'),
    path('delete_mail/<int:id>/', delete_mail, name='delete_mail'),
    path('clear_mails/<str:m_receiver>/', clear_mails, name='clear_mails'),


    # For customer
    path('mail_c', mail_index_c, name='mail_home_c'),
    path('read_c/<str:m_receiver>/', mail_read_c, name='mail_read_c'),
    path('unreaded_c/', unreaded_c, name='unreaded_c'),
    path('readed_c/', readed_c, name='readed_c'),
    path('sent_mails_c', sent_mails_c, name='sent_mails_c'),
    path('compose_c/<str:m_receiver>/', compose_m_c, name='compose_m_c'),
    path('settings_c/', mail_settings_c, name='mail_settings_c'),
    path('delete_mail_c/<int:id>/', delete_mail_c, name='delete_mail_c'),
    path('clear_mails_c/<str:m_receiver>/', clear_mails_c, name='clear_mails_c')
]