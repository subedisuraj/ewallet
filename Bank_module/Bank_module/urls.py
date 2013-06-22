from django.conf.urls import patterns, include, url
from Bank_module import settings

import ewallet
# Enabling the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
                         url(r'^admin/', include(admin.site.urls)),
                        (r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT}),
#    (r'^sitemedia/(?P<path>.*)$', 'django.views.static.serve', {
#        'document_root': settings.MEDIA_ROOT
#    }),
                       )


urlpatterns += patterns('ewallet.views',
    (r'^project/ewallet/pwreset/$','info_page',{"page":"pwreset"}),
    (r'^project/ewallet/about/$', 'info_page',{"page":"about"}),
    (r'^project/ewallet/faq/$', 'info_page',{"page":"faq"}),
    (r'^project/ewallet/contact/$', 'info_page',{"page":"contact"}),
    (r'^project/ewallet/security/$', 'info_page',{"page":"security"}),
#    (r'^project/ewallet/merchants/$','info_page',{"page":"merchants"}),
#    (r'^project/ewallet/partnerbanks/$','info_page',{"page":"partnerbanks"}),

)


urlpatterns += patterns ('ewallet.views',
    (r'^project/ewallet/(?P<username>[a-z_]+)/profile$','profile'),
    (r'^project/ewallet/(?P<username>[a-z_]+)/transfer$','transfer'),
#    (r'^project/ewallet/(?P<username>[a-z]+)/$','profile'),

            )

urlpatterns += patterns('ewallet.views',
    (r'^project/ewallet/register/$', 'register'),
    (r'^project/ewallet/home/$', 'sign_in'),
    (r'^project/ewallet/verification/','pwreset'),
    (r'^project/ewallet/pwr/(?P<username>[a-zA-Z0-9_.-]+)/(?P<id>[a-z0-9]+)/$', 'pwreset'),
    (r'^project/ewallet/(?P<username>[a-zA-Z0-9_.-]+)/account/$','account'),
    (r'^project/ewallet/(?P<username>[a-zA-Z0-9_.-]+)/payment/$','payment'),
    (r'^project/ewallet/(?P<username>[a-zA-Z0-9_.-]+)/transfer/$','transfer'),
    (r'^project/ewallet/(?P<username>[a-zA-Z0-9_.-]+)/profile/$','profile'),
    (r'^project/ewallet/(?P<username>[a-zA-Z0-9_.-]+)/statements/$','statement'),
    (r'^project/ewallet/(?P<username>[a-zA-Z0-9_.-]+)/changepass/$','changepass'),
    (r'^project/ewallet/(?P<username>[a-zA-Z0-9_.-]+)/top/$','topup'),
    (r'^project/ewallet/(?P<username>[a-zA-Z0-9_.-]+)/tof/$','tof'),
    (r'^project/ewallet/(?P<username>[a-zA-Z0-9_.-]+)/mpayment/$','mpayment'),
    (r'^project/ewallet/(?P<username>[a-zA-Z0-9_.-]+)/payonline/$','payonline'),
    (r'^project/ewallet/(?P<username>[a-zA-Z0-9_.-]+)/buycards/$','buycards'),

#    (r'^project/ewallet/admin/$', 'admin_page'),
    (r'^project/ewallet/(?P<username>[a-zA-Z0-9_.-]+)/$','home'),



#    (r'^project/ewallet/help/$','help'),
)
#
#
urlpatterns += patterns('bank_1.views',
                       (r'^project/banks/bank_1/register/$', 'register'),
                       (r'^project/banks/bank_1/signin/$', 'sign_in'),
                       (r'^project/banks/bank_1/admin/$', 'admin_page'),
    (r'^project/banks/bank_1/admin/incoming$','incoming'),
    (r'^project/banks/bank_1/admin/outgoing$','outgoing'),
                       (r'^project/banks/bank_1/(?P<username>[a-zA-Z0-9_.-]+)/$','home')
                        )

urlpatterns += patterns('bank_2.views',
                        (r'^project/banks/bank_2/register/$', 'register'),
                        (r'^project/banks/bank_2/signin/$', 'sign_in'),
                        (r'^project/banks/bank_2/admin/$', 'admin_page'),
                        (r'^project/banks/bank_2/admin/incoming$','incoming'),
                        (r'^project/banks/bank_2/admin/outgoing$','outgoing'),
                         (r'^project/banks/bank_2/(?P<username>[a-zA-Z0-9_.-]+)/$','home')
                       )








