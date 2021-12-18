from riot_api.client import Client
from pprint import pprint
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

        # Add this match to the processed set
        P_m.add(match)

    if D.len >= Batch_Size
        dequeue Batch_Size elements and write to file

    # Add this summoner to the processed set
    P_s.add(current)
'''


def run(root):
    client = Client()
    print(f"Starting traversal from {root}")
    stuff = client.get_summoner_matches(root)
    pprint(stuff)
    with open('out.json', 'w+') as out_f:
        out_f.write(json.dumps(stuff))
