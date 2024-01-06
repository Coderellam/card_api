from django.urls import path
from .views import hello_view, HolderRUDView, HolderListAPIView, HolderCreateAPIView, \
    CardCreateAPIView, CardListAPIView, TransferMoneyView, CheckCardholderBalanceView

urlpatterns = [
    path('', hello_view),

    path('holder/<int:pk>/', HolderRUDView.as_view()),
    # holder, phone, type -> card create (number, expire, token) -> token
    path('holder/', HolderListAPIView.as_view()),
    path('holdercreate/', HolderCreateAPIView.as_view()),

    path('cardcreate/', CardCreateAPIView.as_view()),
    path('cardlist/', CardListAPIView.as_view()),
    path('transfer/', TransferMoneyView.as_view()),

    path('balance/<int:holder_id>/', CheckCardholderBalanceView.as_view())
    # <str:card_token>/ balance u.n shu yoziladi, view yoziladi alohida ,
    # modeldagi cardnni faqat balance fieldi olib yoziladi
    # balance holder info emas, aynan katadagi balance ni olishi kk!card token blishi kk

    # token, card_number_to, amount -> balance check, check card_number_to, balance -+ -> OK

    # path("card/<token:str>/balance/", ),
    # path("card/<token:str>/history/", ),
    #
    # path("card/<token:str>/", ),  # token -> card info
]
