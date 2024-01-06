from .models import Holder, Card, Transaction_history
from rest_framework import generics, status

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import HolderSerializer, CardSerializer
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView


class HolderRUDView(RetrieveUpdateDestroyAPIView):
    serializer_class = HolderSerializer
    queryset = Holder.objects.all()


class HolderCreateAPIView(CreateAPIView):
    serializer_class = HolderSerializer
    queryset = Holder.objects.all()


class HolderListAPIView(ListAPIView):
    serializer_class = HolderSerializer
    queryset = Holder.objects.all()


class CardCreateAPIView(CreateAPIView):
    serializer_class = CardSerializer
    queryset = Card.objects.all()


# def save(
#     self, force_insert=False, force_update=False, using=None, update_fields=None
# ):
""" 
shu yerga saqlashdan oldingi logikani yozsa boladi, masalan, 
masalan karta randomly  raqam generstsiya qilish logikasi yoziladi. 
yoki modelga yoki viewga yozsa boladi, sal farq qiladi.
"""


class CardListAPIView(ListAPIView):
    serializer_class = CardSerializer
    queryset = Card.objects.all()


""" kartani ochirish mmkinmas, exp date da o'zi o'chadi """


class TransferMoneyView(generics.CreateAPIView):  # from gpt
    serializer_class = CardSerializer

    def create(self, request, *args, **kwargs):
        from_card_token = request.data.get('from_card_token')
        to_card_token = request.data.get('to_card_token')
        amount = request.data.get('amount')

        try:
            from_card = Card.objects.get(token=from_card_token)
            to_card = Card.objects.get(token=to_card_token)
        except Card.DoesNotExist:
            return Response({"error": "Card not found"}, status=status.HTTP_404_NOT_FOUND)

        if from_card.balance >= amount:
            from_card.balance -= amount
            to_card.balance += amount

            from_card.save()
            to_card.save()
            Transaction_history.objects.create(from_card=from_card, to_card=to_card, status=status, amount=amount) # model fieldlari yoziladi

            return Response({"message": "Transfered successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Insufficient balance"}, status=status.HTTP_400_BAD_REQUEST)


class CheckCardholderBalanceView(generics.RetrieveAPIView):
    queryset = Holder.objects.all()
    serializer_class = HolderSerializer

    def get(self, request, *args, **kwargs):
        holder_id = self.kwargs.get('holder_id')
        try:
            holder = self.queryset.get(pk=holder_id)
            cards = Card.objects.filter(holder=holder)
        except Holder.DoesNotExist:
            return Response({"error": "Holder not found"}, status=status.HTTP_404_NOT_FOUND)

        card_data = []
        for card in cards:
            card_data.append({
                "card_number": card.card_number,
                "token": card.token,
                "balance": card.balance
            })

        response_data = {
            "holder": HolderSerializer(holder).data,
            "cards": card_data
        }

        return Response(response_data, status=status.HTTP_200_OK)


@api_view(http_method_names=["GET"])
def hello_view(request):
    value = 'SUCCESS'
    p = {
        "status": value
    }
    return Response(data=p)
