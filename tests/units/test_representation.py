import numpy as np
import pytest

from event_library import representations
from event_library.representations import (
    constant_count,
    constant_count_fixed_batch,
    raw,
    spatiotemporal_voxel_grid,
)


def mock_events(n_events, H, W) -> np.array:
    widths = np.random.randint(0, W, (n_events, 1))
    heights = np.random.randint(0, H, (n_events, 1))
    polarities = np.random.randint(0, 1, (n_events, 1))
    times = np.sort(np.random.rand(n_events, 1), axis=0) * 1e10

    return np.stack([widths, heights, times, polarities], axis=1)


class TestSwitches:
    def test_constant_count(self):
        assert representations.get_representation("constant-count") == constant_count

    def test_raw(self):
        assert representations.get_representation("raw") == raw

    def test_voxel(self):
        assert representations.get_representation("voxel") == spatiotemporal_voxel_grid


class TestConstantCount:
    @pytest.mark.parametrize(
        "n_generated,num_events,H,W",
        [(1000, 100, 200, 300), (2000, 10, 100, 200), (5000, 100, 10, 200)],
    )
    def test_generator(self, n_generated, num_events, H, W):
        events = mock_events(n_generated, H, W)
        generator = constant_count.get_generator(events, num_events, (H, W))

        for event_frame in generator:
            assert event_frame.shape == (H, W, 1)


class TestConstantCountTimeBatch:
    @pytest.mark.parametrize(
        "n_generated,num_events,H,W",
        [(1000, 100, 200, 300), (2000, 10, 100, 200), (5000, 100, 10, 200)],
    )
    def test_generator(self, n_generated, num_events, H, W):
        events = mock_events(n_generated, H, W)
        time_batch = 50  # Hz
        generator = constant_count_fixed_batch.get_generator(
            events, num_events, (H, W), time_batch
        )
        expected_frames_count = self._count_frames_in_times(events[:, 2], time_batch)

        count_generated_frames = 0
        for event_frame in generator:
            count_generated_frames += 1
            assert event_frame.shape == (H, W, 1)

        assert expected_frames_count == count_generated_frames

    def _count_frames_in_times(self, times: np.array, time_batch: float):
        time_start = times[0]
        time_batch_ns = time_batch * 1e10
        result = 0
        for t in times:
            if t > time_start + time_batch_ns:
                result += 1
                time_start = t
        return result


class TestRaw:
    @pytest.mark.parametrize(
        "n_generated,num_events,H,W",
        [(1000, 100, 200, 300), (2000, 10, 100, 200), (5000, 100, 10, 200)],
    )
    def test_generator(self, n_generated, num_events, H, W):
        events = mock_events(n_generated, H, W)
        generator = raw.get_generator(events)
        for event in generator:
            assert event.shape == (4, 1)


class TestVoxel:
    @pytest.mark.parametrize(
        "n_generated,num_events,H,W,bins",
        [(1000, 100, 200, 300, 4), (2000, 10, 100, 200, 5), (5000, 100, 10, 200, 1)],
    )
    def test_generator(self, n_generated, num_events, H, W, bins):
        events = mock_events(n_generated, H, W)
        generator = spatiotemporal_voxel_grid.get_generator(
            events, num_events, (H, W), bins
        )

        for event_frame in generator:
            assert event_frame.shape == (H, W, bins)
