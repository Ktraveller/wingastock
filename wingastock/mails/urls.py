from django.urls import path
from mails.views_m.index import mail_index
from mails.views_m.read_m import mail_read, readed, unreaded, compose_m, sent_mails, delete_mail, clear_mails
from mails.views_m.settings_m import mail_settings

urlpatterns = [
    path('', mail_index, name='mail_home'),
    path('read/<str:m_receiver>/', mail_read, name='mail_read'),
    path('unreaded/', unreaded, name='unreaded'),
    path('readed/', readed, name='readed'),
    path('sent_mails', sent_mails, name='sent_mails'),
    path('compose/<str:m_receiver>/', compose_m, name='compose_m'),
    path('settings/', mail_settings, name='mail_settings'),
    path('delete_mail/<int:id>/', delete_mail, name='delete_mail'),
    path('clear_mails/<str:m_receiver>/', clear_mails, name='clear_mails')
]