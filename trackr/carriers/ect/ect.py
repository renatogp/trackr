# coding: utf-8
import json
import os
from datetime import datetime

from ..base import BaseCarrier
from ...exceptions import MissingCarrierConfig, PackageNotFound


import requests
from requests.auth import HTTPBasicAuth

ECT_USERNAME_ENV_NAME = 'TRACKR_ECT_USERNAME'
ECT_API_KEY_ENV_NAME = 'TRACKR_ECT_API_KEY'
ECT_CARD_NUMBER = 'TRACKR_ECT_CARD_NUMBER'


class ECT(BaseCarrier):
    id = 'ect'
    name = 'ECT'

    def __init__(self, ect_username=None, ect_password=None, ect_card_number=None, **kwargs):
        self.ect_username = ect_username or os.environ.get(
            ECT_USERNAME_ENV_NAME)
        self.ect_api_key = ect_password or os.environ.get(
            ECT_API_KEY_ENV_NAME)

        self.ect_card_number = ect_card_number or os.environ.get(
            ECT_CARD_NUMBER)

        if self.ect_username is None or self.ect_api_key is None:
            raise MissingCarrierConfig(
                'Carrier "ECT" requires {} and {} env vars to be set'.format(
                    ECT_USERNAME_ENV_NAME, ECT_API_KEY_ENV_NAME)
            )

        super(ECT, self).__init__(**kwargs)

    def _generate_token(self):
        """
        Generate token for Correios webservice
        """
        response = requests.post(
            'https://api.correios.com.br/token/v1/autentica/cartaopostagem',
            auth=HTTPBasicAuth(self.ect_username, self.ect_api_key),
            data=json.dumps({"numero": self.ect_card_number}),
            headers={"content-type": "application/json", }
        )

        response.raise_for_status()

        return response.json()['token']

    def _track_bulk(self, object_ids, ignore_missing=True):
        response = requests.get('https://api.correios.com.br/srorastro/v1/objetos?codigosObjetos={}&resultado=T&'.format(
            ','.join(object_ids),
        ), headers={
            "authorization": "Bearer {}".format(self._generate_token()),
            "content-type": "application/json",
        })

        print(response.content)

        objects = []
        for o in response.json()['objetos']:
            try:
                objects.append(self._handle_package(o))
            except PackageNotFound as e:
                if not ignore_missing:
                    raise e

        return objects

    def _track_single(self, object_id):
        return self._track_bulk([object_id], ignore_missing=False)[0]

    def _handle_package(self, data):
        if not data.get('eventos'):
            raise PackageNotFound(
                object_id=data['codObjeto'],
                carrier_message=data['mensagem'],
            )

        package = self.create_package(
            object_id=data['codObjeto'],
            service_name=data['tipoPostal']['categoria'],
            extra_info={
                'service_detail': data['tipoPostal']['descricao'],
            }
        )

        for event in data['eventos']:
            date, time = event['dtHrCriado'].split('T')
            package.add_tracking_info(
                date=datetime(*map(int, date.split('-') + time.split(':'))),
                location=u'{} - {} - {}'.format(
                    event['unidade']['tipo'],
                    event['unidade']['endereco'].get('cidade', '-'),
                    event['unidade']['endereco']['uf'],
                ),
                status=event['descricao'].strip(),
                description='',
                extra_info={}
            )

        return package
