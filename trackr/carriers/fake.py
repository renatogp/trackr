from datetime import datetime

from .base import BaseCarrier


class FakeCarrier(BaseCarrier):
    id = 'fake'
    name = 'Fake Carrier'

    def _track_single(self, object_id):
        package = self.create_package(
            object_id=object_id,
            service_name='Default',
        )

        for i in range(1, 5):
            package.add_tracking_info(
                date=datetime.now(),
                location='City {}'.format(i),
                status='In transit {}'.format(i),
                description='Wow',
            )

        return package
