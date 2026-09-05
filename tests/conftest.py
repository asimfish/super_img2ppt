import copy

import pytest
from super_img2ppt.fonts import FontCatalog


@pytest.fixture(scope="session")
def fonts():
    return FontCatalog()


@pytest.fixture
def scene():
    return copy.deepcopy(
        {
            "version": 1,
            "slides": [
                {
                    "id": "page_001",
                    "width": 1280,
                    "height": 720,
                    "reviewed": True,
                    "notes": "原样保留\nsecond line",
                    "elements": [
                        {
                            "id": "title",
                            "kind": "text",
                            "z": 2,
                            "box": [80, 60, 700, 100],
                            "text": "Hello 中文 123",
                            "font_size": 36,
                        }
                    ],
                }
            ],
        }
    )
