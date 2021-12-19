from riot_api.client import Client
from redis_wrapper.session import Session
import datetime
import time
import json


'''
Q_s := Queue<SummonerIds>
Q_m := Queue<MatchIds>

D := Queue<MatchInfo>

P_s := Set<SummonerIds>
P_m := Set<MatchIds>

R := SummonerName

func resolve := SummonerName -> SummonerId
func resolve := MatchId -> MatchInfo
func fetch := SummonerId -> List<MatchIds>

primer_id = resolve(R)
Q_s.enqueue(primer_id)

while Q_s not empty:
    current = Q_s.dequeue
    # Should never happen but it's a good sanity check
    if current in P_s:
        loop again

    matches = fetch(current)
    for match in matches:
        if match in P_m:
            loop again

        match_info = resolve(match)
        D.enqueue(match_info)
        Q_s.enqueue(match_info.participants)

        # Add this match to the processed set
        P_m.add(match)

    if D.len >= Batch_Size
        dequeue Batch_Size elements and write to file

    # Add this summoner to the processed set
    P_s.add(current)
'''


def write_batch(session_id: str, json_data: str):
    ts = datetime.datetime.now().isoformat()
    out_file_name = session_id + '-' + ts + '.json'
    data = [json.loads(game) for game in json_data]
    with open(out_file_name, 'w+') as out_file:
        out_file.write(json.dumps(data))


def run(root):
    BATCH_SIZE = 50
    PAUSE_TIME = 0.05  # 50 ms
    client = Client()
    session = Session(session_id=root)

    print(f"Starting traversal from {root}")
    primer_id = client.get_summoner_puuid(root)
    time.sleep(PAUSE_TIME)

    session.enqueue_to('summoners', primer_id)

    while session.queue_len('summoners') >= 0:
        if session.num_stored_matches() >= BATCH_SIZE:
            print(f"Redis contains {session.num_stored_matches()}, writing batch of {BATCH_SIZE} games")
            matches_to_write = session.dequeue_match_bulk(BATCH_SIZE)
            write_batch(root, matches_to_write)

        current = session.dequeue_from('summoners').decode('utf-8')
        print(f"Processing summoner: {current}")

        if session.is_member_of('processed.summoners', current):
            continue

        this_users_matches = client.get_match_ids(current)
        for idx, match_id in enumerate(this_users_matches):
            print(f"Processing match {idx+1} of {len(this_users_matches)}")

            if session.is_member_of('processed.matches', match_id):
                continue

            match_info = client.fetch_match_info(match_id)
            participants = match_info['metadata']['participants']
            session.cache_match_info(json.dumps(match_info))
            session.add_to('processed.matches', match_id)

            for summoner_puuid in participants:
                session.enqueue_to('summoners', summoner_puuid)

            time.sleep(PAUSE_TIME)

        session.add_to('processed.summoners', current)
