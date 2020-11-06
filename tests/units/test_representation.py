import numpy as np
import pytest

from event_library.representations import constant_count


def mock_events(n_events, H, W) -> np.array:
    widths = np.random.randint(0, W, (n_events, 1))
    heights = np.random.randint(0, H, (n_events, 1))
    polarities = np.random.randint(0, 1, (n_events, 1))
    times = np.sort(np.random.rand(n_events, 1))
    return np.stack([heights, widths, times, polarities], axis=1)


class TestConstantCount:
    @pytest.mark.parametrize(
        "num_events,H,W", [(100, 200, 300), (10, 100, 200), (100, 10, 200)]
    )
    def test_generator(self, num_events, H, W):
        rep = constant_count
        events = mock_events(1000, H, W)
        generator = rep.get_generator(events, num_events, H, W)

        for event_frame in generator:
            assert event_frame.shape == (H, W, 1)
