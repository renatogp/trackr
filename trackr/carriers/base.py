
class TrackingInfo(object):

    def __init__(self, date, location, status, description, extra_info=None):
        self.date = date
        self.location = location
        self.status = status
        self.description = description
        self.extra_info = extra_info or {}

    def __unicode__(self):
        return u'{} - {} - {}'.format(
            self.date,
            self.location,
            self.status,
        )


class Package(object):

    def __init__(self, carrier_class, object_id, service_name, extra_info=None):
        self.carrier_class = carrier_class
        self.object_id = object_id
        self.service_name = service_name
        self.tracking_info = []
        self.extra_info = extra_info or {}

    def __unicode__(self):
        return u'{} - {} - {}'.format(
            self.carrier_class.name,
            self.object_id,
            self.service_name,
        )

    def add_tracking_info(self, **kwargs):
        self.tracking_info.append(
            self.carrier_class.tracking_info_class(**kwargs))


class BaseCarrier(object):
    id = None
    name = None
    package_class = Package
    tracking_info_class = TrackingInfo

    def __unicode__(self):
        return self.name

    def track(self, object_id):
        return NotImplementedError()

    def create_package(self, object_id, service_name, extra_info=None):
        return self.package_class(self.__class__, object_id, service_name, extra_info)
