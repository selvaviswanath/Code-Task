from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import generics
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from django.db.models import Q
from .models import GlobalContact, User, Contact
from .serializers import GlobalContactSerializer, UserSerializer, ContactSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets

# Create your views here.

class valid_pass:
    def valid(password):
        SpecialSym =['$', '@', '#', '%']
        val = True
        if len(password) < 8:
            print('length should be at least 8')
            val = False
        if len(password) > 18:
            print('length should be not be greater than 18')
            val = False
            
        if not any(char.isdigit() for char in password):
            print('Password should have at least one numeral')
            val = False
            
        if not any(char.isupper() for char in password):
            print('Password should have at least one uppercase letter')
            val = False
            
        if not any(char.islower() for char in password):
            print('Password should have at least one lowercase letter')
            val = False
            
        if not any(char in SpecialSym for char in password):
            print('Password should have at least one of the symbols $@#')
            val = False
        if val:
            return val


class GlobalContactViewSet(viewsets.ModelViewSet):

    @action(detail=True, methods=['get'])
    def getGCList(self, request, pk=None):
        password = request.data.get('password')
        user = User.objects.get(pk=pk)
        if(password!=user.password):
            return Response({'detail':'You are not authenticated.'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            queryset = GlobalContact.objects.all()
            serializer_class = GlobalContactSerializer(queryset, many=True)
            return JsonResponse(data=serializer_class.data, safe=False)

        
    @action(detail=True, methods=['get'])
    def search_name(self, request, pk=None):
        password = request.data.get('password')
        user = User.objects.get(pk=pk)
        if(password!=user.password):
            return Response({'detail':'You are not authenticated.'}, status=status.HTTP_401_UNAUTHORIZED)
        query = request.query_params.get('name', '')
        results = GlobalContact.search_by_name(query)
        serializer = GlobalContactSerializer(results, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def search_phone_number(self, request, pk=None):
        password = request.data.get('password')
        user = User.objects.get(pk=pk)
        if(password!=user.password):
            return Response({'detail':'You are not authenticated.'}, status=status.HTTP_401_UNAUTHORIZED)
        query = request.query_params.get('phone_number', '')
        results = GlobalContact.search_by_phone_number(query)
        serializer = GlobalContactSerializer(results, many=True)
        return Response(serializer.data)
    
class UserViewSet(viewsets.ModelViewSet):

    @action(detail=True, methods=['post'])
    def addUser(self, request):
        username = request.data.get('username')
        phone = request.data.get('phone_number')
        password = request.data.get('password')
        if(valid_pass.valid(password=password)):
            if (not phone) or (not username):
                return Response({'detail':'phone number and username required'}, status=status.HTTP_400_BAD_REQUEST)
            user = User(username=username, phone_number=phone, password=password)
            try:
                user.save()
                return Response({'detail':'Successful'}, status=status.HTTP_201_CREATED)
            except:
                return Response({'detail':'phone number already exists'}, status=status.HTTP_502_BAD_GATEWAY)

        else:
            return Response({'detail':'password is not valid'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def mark_contact_as_spam(self, request, pk=None):
        user = self.get_object()
        phone = request.data.get('phone_number')

        password = request.data.get('password')
        if(password!=user.password):
            return Response({'detail':'You are not authenticated.'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            if not phone:
                return Response({'detail': 'Phone number is required.'}, status=status.HTTP_400_BAD_REQUEST)
            try:
                contact = user.contacts.get(phone_number=phone, user=user)
            except Contact.DoesNotExist:
                return Response({'detail': 'Contact not found.'}, status=status.HTTP_404_NOT_FOUND)
            
            if contact.is_spam:
                return Response({'detail': 'Contact is already marked as spam.'}, status=status.HTTP_400_BAD_REQUEST)

            user.mark_contact_as_spam(contact)
            return Response({'detail': 'Contact marked as spam successfully.'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def add_contacts(self, request, pk=None):
        password = request.data.get('password')
        if(password!=user.password):
            return Response({'detail':'You are not authenticated.'}, status=status.HTTP_401_UNAUTHORIZED)
        user = self.get_object()
        contacts = request.data.get('contacts')
        user.add_contacts(contacts)
        return Response({'detail': 'Contacts added successfully to user id='+str(user.id)}, status=status.HTTP_200_OK)
        # for contact_data in contacts:
        #     contact = Contact.objects.create(user=self, **contact_data)
        #     GlobalContact.add_phone_number(contact.name, contact.phone_number)

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer(queryset,many=True)
    @action(detail=True, methods=['get'])
    def getContacts(self, request, pk=None):
        password = request.data.get('password')
        user = User.objects.get(pk=pk)
        print(str(password)+'||'+user.password)
        if(password!=user.password):
            return Response({'detail':'You are not authenticated.'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            queryset = Contact.objects.filter(user=user)
            serializer_class = ContactSerializer(queryset,many=True)
            return JsonResponse(data=serializer_class.data, safe=False)



# class GlobalContactList(generics.ListCreateAPIView):
#     @api_view(['GET','POST'])
#     def GC(request):
#         if(request.method=='GET'):
#             GCserializer = GlobalContactSerializer(GlobalContact.objects.all(),many=True)
#             return Response(GCserializer.data)
#         if(request.method=='POST'):
#             GCserializer = GlobalContactSerializer(data=request.data, many=True)
#             if(GCserializer.is_valid()):
#                 GCserializer.save()
#                 return Response(GCserializer.data, status=status.HTTP_201_CREATED)
#             else:
#                 return Response(content_type='text',)
    
#     @api_view(['GET','PUT'])
#     def GC_search(request, phone_number):
#         if(request.method=='GET'):
#             try:
#                 GlobalContact.objects.get(pk=phone_number)
#             except GlobalContact.DoesNotExist:
#                 return Response(status=status.HTTP_404_NOT_FOUND)
    


# class UserList(generics.ListCreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

# class ContactList(generics.ListCreateAPIView):
#     queryset = Contact.objects.all()
#     serializer_class = ContactSerializer

# class ContactDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Contact.objects.all()
#     serializer_class = ContactSerializer

# class SearchByName(generics.ListAPIView):
#     serializer_class = GlobalContactSerializer

#     def get_queryset(self):
#         search_query = self.request.query_params.get('name', '')
#         return GlobalContact.objects.filter(name__istartswith=search_query)

# class SearchByPhoneNumber(generics.ListAPIView):
#     serializer_class = GlobalContactSerializer

#     def get_queryset(self):
#         search_query = self.request.query_params.get('phone_number', '')
#         return GlobalContact.objects.filter(Q(phone_number=search_query) | Q(user__phone_number=search_query))