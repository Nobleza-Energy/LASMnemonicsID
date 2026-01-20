import pytest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))


@pytest.fixture
def sample_las_paths():
    data_dir = Path(__file__).parent / 'data'
    paths = list(data_dir.glob('*.las'))  # All .las files
    assert len(paths) > 0, f"No LAS files in {data_dir}"
    return sorted(paths)

@pytest.fixture
def single_las_path(sample_las_paths):
    return sample_las_paths[0]


