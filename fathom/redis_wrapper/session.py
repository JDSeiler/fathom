from typing import Literal, List, Optional
import redis
r = redis.Redis(host='localhost', port='6379', db=0)

QueueId = Literal['summoners', 'matches']
SetId = Literal['processed.summoners', 'processed.matches']
JsonString = str


class Session:
    def __init__(self, session_id):
        self.r = redis.Redis(host='localhost', port='6379', db=0)
        self.session_id = session_id
        self.match_info_id = 'pending_matches'

    def __structure_id(self, path: str) -> str:
        return self.session_id + '.' + path

    def enqueue_to(self, q_id: QueueId, value: str) -> int:
        q_path = self.__structure_id(q_id)
        return r.rpush(q_path, value)

    def dequeue_from(self, q_id: QueueId) -> int:
        q_path = self.__structure_id(q_id)
        return r.lpop(q_path)

    def queue_len(self, q_id: QueueId) -> int:
        q_path = self.__structure_id(q_id)
        return r.llen(q_path)

    def add_to(self, s_id: SetId, value: str) -> int:
        s_path = self.__structure_id(s_id)
        return r.sadd(s_path, value)

    def is_member_of(self, s_id: SetId, value: str) -> int:
        s_path = self.__structure_id(s_id)
        return r.sismember(s_path, value)

    def cache_match_info(self, value: JsonString) -> int:
        q_path = self.__structure_id(self.match_info_id)
        return r.rpush(q_path, value)

    def num_stored_matches(self) -> int:
        q_path = self.__structure_id(self.match_info_id)
        return r.llen(q_path)

    def dequeue_match_bulk(self, batch_size: int) -> Optional[List[JsonString]]:
        q_path = self.__structure_id(self.match_info_id)

        # Redis will not fail if the end of the range goes past the end
        # of a list. It will just return as big a list as it can or an
        # empty list (if applicable) But I'd like to fail a bit louder.
        if self.num_stored_matches() < batch_size:
            return None

        # Last element is included so we subtract one to retreive
        # exactly `batch_size` elements
        return r.lrange(q_path, 0, batch_size-1)
