import pytest
import event_library.generator.representations as representation

class TestConstantCount:
    @pytest.mark.parametrize("H,W", [(10, 100), (100, 10)])
    def test_init(self, H, W):
        r = representation.ConstantRepresentation(H, W, 2)
        assert r is not None
        
        
