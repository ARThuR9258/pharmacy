from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from ACL.rest_mixin import RestPermissionMixin
from Sms.api.serializers import SmsGroupSerializer


class SmsViewSet(viewsets.GenericViewSet):
    permission_classes = [RestPermissionMixin]
    permissions = ['sms_list', 'sms_send']
    serializer_class = SmsGroupSerializer

    @action(
        detail=False,
        methods=['post'],
        url_path='group/send',
    )
    def send_group_sms(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(True)
        serializer.save()

        return Response({'status': 'ok'})
