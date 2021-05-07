import numpy as np
import pytest

from event_library import representations
from event_library.representations import (
    ConstantCount,
    ConstantTime,
    PosNeg,
    Raw,
    VoxelGrid,
)


def mock_events(n_events, H, W) -> np.ndarray:
    widths = np.random.randint(0, W, (n_events, 1))
    heights = np.random.randint(0, H, (n_events, 1))
    polarities = np.random.choice([-1, 1], (n_events, 1))
    times = abs(np.sort(np.random.rand(n_events, 1), axis=0)) * 10

    return np.stack([widths, heights, times, polarities], axis=1)


class TestSwitches:
    def test_constant_count(self):
        assert representations.get_representation("constant-count") == ConstantCount

    def test_pos_neg(self):
        assert representations.get_representation("pos-neg") == PosNeg

    def test_raw(self):
        assert representations.get_representation("raw") == Raw

    def test_constant_time(self):
        assert representations.get_representation("constant-time") == ConstantTime

    def test_voxel(self):
        assert representations.get_representation("voxel") == VoxelGrid


class TestConstantCount:
    @pytest.mark.parametrize(
        "n_generated,num_events,H,W",
        [(1000, 100, 200, 300), (2000, 10, 100, 200), (5000, 100, 10, 200)],
    )
    def test_generator(self, n_generated, num_events, H, W):
        events = mock_events(n_generated, H, W)
        generator = ConstantCount(num_events, (H, W)).get_generator(events)

        for event_frame in generator:
            assert event_frame.shape == (H, W, 1)


class TestConstantTime:
    @pytest.mark.parametrize(
        "n_generated,num_events,H,W",
        [(1000, 100, 200, 300), (2000, 10, 100, 200), (5000, 100, 10, 200)],
    )
    def test_generator(self, n_generated, num_events, H, W):
        events = mock_events(n_generated, H, W)
        time_batch = 1  # Hz
        generator = ConstantTime(num_events, (H, W), time_batch).get_generator(events)
        expected_frames_count = self._count_frames_in_times(events[:, 2], time_batch)

        count_generated_frames = 0
        for event_frame in generator:
            count_generated_frames += 1
            assert event_frame.shape == (H, W, 1)
        assert expected_frames_count == count_generated_frames

    def _count_frames_in_times(self, times: np.array, frequence: float):
        time_start = times[0]
        time_batch_ns = 1 / frequence
        result = 0
        for t in times:
            if t > time_start + time_batch_ns:
                result += 1
                time_start = t
        return result + 1


class TestRaw:
    @pytest.mark.parametrize(
        "n_generated,num_events,H,W",
        [(1000, 100, 200, 300), (2000, 10, 100, 200), (5000, 100, 10, 200)],
    )
    def test_generator(self, n_generated, num_events, H, W):
        events = mock_events(n_generated, H, W)
        generator = Raw().get_generator(events)
        events = next(generator)
        assert events.shape == (n_generated, 4, 1)


class TestVoxel:
    @pytest.mark.parametrize(
        "n_generated,num_events,H,W,bins",
        [(1000, 100, 200, 300, 4), (2000, 10, 100, 200, 5), (5000, 100, 10, 200, 1)],
    )
    def test_generator(self, n_generated, num_events, H, W, bins):
        events = mock_events(n_generated, H, W)
        generator = VoxelGrid(num_events, (H, W), bins).get_generator(events)

        for event_frame in generator:
            assert event_frame.shape == (H, W, bins)
