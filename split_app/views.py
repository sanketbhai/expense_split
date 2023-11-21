from rest_framework.authtoken.views import obtain_auth_token

from rest_framework.response import Response

from rest_framework.views import APIView

from rest_framework import status


from django.contrib.auth import authenticate

from rest_framework.authtoken.models import Token

from rest_framework.authentication import TokenAuthentication

from rest_framework.permissions import IsAuthenticated
from .models import *

from .serializer import *



class LoginView(APIView):

    def post(self, request, *args, **kwargs):

        username = request.data.get('username')

        password = request.data.get('password')

        user = None
        if username and password:

            user = authenticate(username=username, password=password)
        

        # Check if the token is present in the response data

        if user:

            # Create or retrieve the token associated with the user

            token, created = Token.objects.get_or_create(user=user)


            return Response({'token': token.key})

        else:

            return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)



class Simplify(APIView):

    authentication_classes = [TokenAuthentication]

    permission_classes = [IsAuthenticated]

    def post(self,request):

        user = request.user
        if user.simplify:
            user.simplify = False
        else:
            user.simplify = True

        user.save()

        return Response({'message': 'Success'})

def split_equal(split,total_amount):
    no_of_people = len(split)

    share = round(total_amount/no_of_people)

    share_list = [share]*no_of_people

    if not share * no_of_people == total_amount:

        share_list[0] =  share_list[0] + (total_amount-share * no_of_people) 
    return share_list


def split_percent(split,total_amount):
    no_of_people = len(split)
    

    share_list = [1]*no_of_people
     

    for ind,i in enumerate(split):

        share_list[ind] = total_amount/100 *i['amt']
    return share_list

    



 

class Expense(APIView):

    authentication_classes = [TokenAuthentication]

    permission_classes = [IsAuthenticated]

    def post(self,request):

        split_type = request.data.get('split_type')
        print(split_type,'split type')

        total_amount = request.data.get('total_amount')

        split = request.data.get('split')
        note = request.data.get('note')
         

        user = request.user


        if split_type == "EQUAL":

            share_list = split_equal(split,total_amount)


        elif split_type == "PERCENT":

            total_per = sum(entry['amt'] for entry in split)

            if not total_per == 100:

                return Response({"status":False,'message':"percentage not equating to 100"})
            
            share_list = split_percent(split,total_amount)


        elif split_type=="EXACT":

            share_list = [i["amt"] for i in split]

        else:

            return Response({'status':'error','message':"split_type is invalid"})


        for ind,x in enumerate(split):
            debtor = CustomUser.objects.get(username= x["user"])
            own = Own.objects.filter(Creditor=user,Debtor=debtor).first()
            if not own:
                Own.objects.create(Creditor=user,Debtor=debtor,amount=share_list[ind])
            else:
                own.amount += x['amt']
                own.save() 
        Ledger.objects.create(total_amount=total_amount,note=note,split_with=split,split_type=split_type)
        return Response({'status':'success','message':"success"}) 

        



            


        
            
            
            




class OwnsApi(APIView):

    authentication_classes = [TokenAuthentication]

    permission_classes = [IsAuthenticated]
    

    def post(self,request):

        user = request.user
        owns =Own.objects.filter(Creditor = user)
        owns = OwnSerializer(owns,many=True)

        return Response({'data': owns.data})



        

