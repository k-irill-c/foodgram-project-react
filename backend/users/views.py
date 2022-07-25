from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .pagination import BackendPagination
from .models import Follow, User
from .serializers import CustomUserSerializer, FollowSerializer
# from ..api import permissions (cust)

class CustomUserViewSet(UserViewSet):
    """ViewSet пользовательский."""

    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    # cust



class FollowViewSet(APIView):
    """
    APIView добавления / удаления подписки на автора.
    """

    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = BackendPagination

    def post(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        if user_id == request.user.id:
            return Response(
                {'error': 'Невозможно на себя подписаться!'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if Follow.objects.filter(
                user=request.user,
                following_id=user_id
        ).exists():
            return Response(
                {'error': 'Подписка на автора уже есть'},
                status=status.HTTP_400_BAD_REQUEST
            )
        following = get_object_or_404(User, id=user_id)
        Follow.objects.create(
            user=request.user,
            following_id=user_id
        )
        return Response(
            self.serializer_class(
                following, context={'request': request}
            ).data,
            status=status.HTTP_201_CREATED
        )

    def delete(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        get_object_or_404(User, id=user_id)
        subscription = Follow.objects.filter(
            user=request.user,
            following_id=user_id
        )
        if subscription:
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'error': 'Нет подписки на автора!'},
            status=status.HTTP_400_BAD_REQUEST
        )


class FollowListView(ListAPIView):
    """APIView подписок."""

    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = BackendPagination

    def get_queryset(self):
        return User.objects.filter(following__user=self.request.user)  # __
