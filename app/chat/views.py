from django.shortcuts import get_object_or_404, redirect, render
from .models import MessageModel
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from .serializers import MessageSerializer
from django.utils.decorators import method_decorator
from django.views import View
from django.db.models import Q
from django.contrib.auth.models import User



class ChatView():
    def chat(request, pk):
        customer = request.user
        owner_shop = get_object_or_404(User, pk=pk)

        messages = MessageModel.objects.filter(
            Q(sender=customer, receiver=owner_shop) |
            Q(sender=owner_shop, receiver=customer)
        ).order_by('time')

        return render(
            request,
            "app/chat.html",
            {
                "messages": messages,
                "owner_shop": owner_shop, 
                "customer": customer,
            },
        )



@method_decorator(csrf_exempt, name='dispatch')
class MessageListView(View):

    def get(self, request, sender=None, receiver=None):
        if sender != request.user.pk and receiver != request.user.pk:
            return JsonResponse({'error': 'Unauthorized'}, status=401)

        messages = MessageModel.objects.filter(
            Q(sender=sender, receiver=receiver, seen=False) |
            Q(sender=receiver, receiver=sender, seen=False)
        ).order_by('time')

        serializer = MessageSerializer(messages, many=True)
        for message in messages:
            message.seen = True
            message.save()
        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Unauthorized'}, status=401)

        data = JSONParser().parse(request)
        data["sender"] = request.user.pk  

        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


class ConversationsView():
    def conversations(request):
        user = request.user
        messages = MessageModel.objects.filter(
            (Q(sender=user) | Q(receiver=user)) & ~Q(sender=user, receiver=user)
        ).order_by('sender', 'receiver', 'time')

        
        conversation_set = set()
        conversations = []
        for message in messages:
            pair = (min(message.sender.pk, message.receiver.pk), max(message.sender.pk, message.receiver.pk))
            if pair not in conversation_set:
                conversation_set.add(pair)
                conversations.append(message)

        return render(
            request,
            "app/conversations.html",
            {
                "conversations": conversations,
            },
        )


class DeleteConversationView():
    def delete_conversation(request, pk):
        user = request.user
        other_user = get_object_or_404(User, pk=pk)
        MessageModel.objects.filter(
            (Q(sender=user) & Q(receiver=other_user)) |
            (Q(sender=other_user) & Q(receiver=user))
        ).delete()
        return redirect('conversations')












