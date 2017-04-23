from .ect import ECT
from .fake import FakeCarrier

# for now, this is acceptable
registry = {
    ECT.id: ECT,
    FakeCarrier.id: FakeCarrier,
}
