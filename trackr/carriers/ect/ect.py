# coding: utf-8
import os
from datetime import datetime

from zeep import Client as ZeepClient

from ..base import BaseCarrier
from ...exceptions import MissingCarrierConfig, PackageNotFound


ECT_USERNAME_ENV_NAME = 'TRACKR_ECT_USERNAME'
ECT_PASSWORD_ENV_NAME = 'TRACKR_ECT_PASSWORD'


class ECT(BaseCarrier):
    id = 'ect'
    name = 'ECT'

    def __init__(self, ect_username=None, ect_password=None, **kwargs):
        self.ect_username = ect_username or os.environ.get(
            ECT_USERNAME_ENV_NAME)
        self.ect_password = ect_password or os.environ.get(
            ECT_PASSWORD_ENV_NAME)

        if self.ect_username is None or self.ect_password is None:
            raise MissingCarrierConfig(
                'Carrier "ECT" requires {} and {} env vars to be set'.format(
                    ECT_USERNAME_ENV_NAME, ECT_PASSWORD_ENV_NAME)
            )

        super(ECT, self).__init__(**kwargs)

    def _fetch_soap_ws(self, object_id):
        client = ZeepClient(
            '{}/soap/Rastro.wsdl'.format(
                os.path.dirname(os.path.abspath(__file__)))
        )

        data = client.service.buscaEventos(
            usuario=self.ect_username,
            senha=self.ect_password,
            tipo='L',
            resultado='T',
            lingua='101',
            objetos=object_id,
        )

        return data['objeto'][0]

    def track(self, object_id):
        data = self._fetch_soap_ws(object_id)

        if not any([data['nome'], data['categoria'], data['evento']]):
            raise PackageNotFound(
                object_id=object_id,
                carrier_message=data['erro'],
            )

        package = self.create_package(
            object_id=object_id,
            service_name=data['categoria'],
            extra_info={
                'service_detail': data['nome'],
            }
        )

        for event in data['evento']:
            package.add_tracking_info(
                date=datetime(*map(int, event['data'].split('/')
                                   [::-1] + event['hora'].split(':'))),
                location=u'{} - {} - {}'.format(
                    event['local'], event['cidade'], event['uf']),
                status=event['descricao'].strip(),
                description='',
                extra_info={}
            )

        return package
