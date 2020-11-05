import numpy as np
import pytest

import event_library.generator.representations as representation


class TestConstantCount:
    @pytest.mark.parametrize("num_events", [(100, 200)])
    def test_init(self, num_events):
        r = representation.ConstantRepresentation(num_events)
        assert r is not None

    @pytest.mark.parametrize(
        "num_events,H,W", [(100, 200, 300), (10, 100, 200), (100, 10, 200)]
    )
    def test_generatrion(self, num_events, H, W):
        rep = representation.ConstantRepresentation(num_events)
        events = np.random.randint(0, 100, (4, 1000))
        rep.frame_generator(events, H, W)
