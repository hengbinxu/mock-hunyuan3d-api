import random

from datetime import datetime, UTC
from dataclasses import dataclass
from constants import ImageProcessStatus


@dataclass
class ResponseResult:
    uid: str
    image_content: str
    expected_response_time: int
    status: ImageProcessStatus


class ResponseSimulator:
    def __init__(self, expired_time: int = 60 * 60 * 12) -> None:
        self.response_records: dict[str, ResponseResult] = {}
        self.expired_time = expired_time

    def save_record(self, uid: str, image_content: str) -> None:
        wait_time = random.randint(10, 15)
        expected_response_time = self.get_current() + wait_time
        self.response_records[uid] = ResponseResult(
            uid=uid,
            image_content=image_content,
            expected_response_time=expected_response_time,
            status=ImageProcessStatus.PROCESSING,
        )

    def get_record(self, uid: str) -> ResponseResult:
        res = self.response_records.get(uid, None)
        if res is None:
            raise KeyError(f"uid: {uid} not exists in request_records")

        if self.get_current() > res.expected_response_time:
            res.status = ImageProcessStatus.COMPLETED
            return res
        else:
            return res

    def delete_record_by_expired_time(self) -> None:
        deleted_uids: list[str] = []
        for uid, record in self.response_records.items():
            if (record.expected_response_time + self.expired_time) < self.get_current():
                deleted_uids.append(uid)

        for uid in deleted_uids:
            self.response_records.pop(uid, None)
            print(f"Delete uid: {uid}")

    @staticmethod
    def get_current() -> int:
        return int(datetime.now(UTC).timestamp())
