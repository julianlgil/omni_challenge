from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response


class TokenAPI(ObtainAuthToken):

    def delete(self, request, *args, **kwargs):
        return Response({'deleted': 'Ok'})
