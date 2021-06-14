from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response


class TokenAPI(ObtainAuthToken):

    def delete(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        return Response({'deleted': 'Ok'})
