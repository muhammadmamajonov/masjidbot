from django.urls import path
from .views import GetList, DarslarApiView, MavzularApiView, MaruzalarApiView, MalumotYozish, ymq, namoz_vaqti_qoshish, nvo, darslar_ochirish, maruzalar, maruza_ochirish, darslar
# import bot
urlpatterns = [
    # path('masjidbot/', bot.MasjidBot.as_view()),
    #darslar
    path('ymq/', ymq, name = 'ymq'),
    path('darslar_ochirish/', darslar_ochirish, name = 'dars-ochirish'),
    path('darslar/', darslar, name = 'darslar'),
    # Maruzalar
    path('maruza-ochirish/', maruza_ochirish, name = 'maruza_ochirish'),
    path('maruzalar/', maruzalar, name = 'maruzalar'),
    # Namoz vaqti
    path('nvo/', nvo, name = 'nvo'),
    path('namoz_vaqti_qoshish/', namoz_vaqti_qoshish, name = 'nvq'),
    path('malumotlar-qoshish/', MalumotYozish, name = 'malumot-yozish'),
    # API
    path('namozvaqti', GetList.as_view(), name = 'namoz-vaqti'),
    path('audio-maruzalar', MaruzalarApiView.as_view(), name = 'audio-maruzalari'),
    path('mavzular', MavzularApiView.as_view(), name = 'mavzular'),
    path('darslarapi', DarslarApiView.as_view(), name = 'darslar-api'),
]