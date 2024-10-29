from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional


class ElementSpec:
    def __init__(
        self,
        ds_num: Optional[int],  # depth number
        data_map: List[int],  # at what index the values are present
        post_processor: Callable = None,  # function applied after value is parsed
        fallback_value: Any = None,  # backtracking if any exception is occurred
    ):
        self.ds_num = ds_num
        self.data_map = data_map
        self.post_processor = post_processor
        self.fallback_value = fallback_value

    def extract_content(self, source: Dict) -> Any:
        try:
            target_source = (
                source if self.ds_num is None else source.get(f"ds:{self.ds_num}", {})
            )
            result = nested_lookup(target_source, self.data_map)
            if self.post_processor:
                result = self.post_processor(result)
        except Exception:
            result = (
                self.fallback_value.extract_content(source)
                if isinstance(self.fallback_value, ElementSpec)
                else self.fallback_value
            )
        return result


@dataclass
class ElementSpecs:
    Review: Dict[str, ElementSpec] = field(
        default_factory=lambda: {
            "reviewId": ElementSpec(None, [0]),
            "userName": ElementSpec(None, [1, 0]),
            "userImage": ElementSpec(None, [1, 1, 3, 2]),
            "content": ElementSpec(None, [4]),
            "score": ElementSpec(None, [2]),
            "thumbsUpCount": ElementSpec(None, [6]),
            "reviewCreatedVersion": ElementSpec(None, [10]),
            "at": ElementSpec(None, [5, 0], lambda v: datetime.fromtimestamp(v)),
            "replyContent": ElementSpec(None, [7, 1]),
            "repliedAt": ElementSpec(
                None, [7, 2, 0], lambda v: datetime.fromtimestamp(v)
            ),
            "appVersion": ElementSpec(None, [10]),
        }
    )


def nested_lookup(source, indexes):
    try:
        if len(indexes) == 1:
            return source[indexes[0]]
        return nested_lookup(source[indexes[0]], indexes[1:])
    except (TypeError, KeyError, IndexError):
        return None
