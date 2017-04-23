class PackageNotFound(Exception):

    def __init__(self, object_id, carrier_message):
        self.object_id = object_id
        self.carrier_message = carrier_message


class MissingCarrierConfig(Exception):
    pass
