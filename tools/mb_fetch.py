# Builds src/mb.json: friendly artist facts from MusicBrainz (matched by exact Deezer artist id).
# Rate limit: one request per 1.1 s, identifying User-Agent, resumable cache. Run: python3 tools/mb_fetch.py [N]
import json, sys, time, urllib.request, urllib.parse, os
UA = 'FreshMic/1.0 (https://fresh-soldier.github.io/FRESH-MIC/)'
CACHE = 'src/mb_cache.json'
N = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
d = json.load(open('src/data.json'))
arts = sorted(d['n'], key=lambda a: -a[2])[:N]
cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
last = [0.0]
def get(url):
    for k in range(5):
        w = 1.1 - (time.time() - last[0])
        if w > 0: time.sleep(w)
        last[0] = time.time()
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': 'application/json'}), timeout=20) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 404: return None
            if e.code in (429, 503): time.sleep(5 * (k + 1)); continue
            raise
        except Exception:
            time.sleep(3)
    return 'ERR'
done = 0
for a in arts:
    key = str(a[0])
    if key in cache: continue
    u = get('https://musicbrainz.org/ws/2/url?resource=' + urllib.parse.quote('https://www.deezer.com/artist/' + key, safe='') + '&inc=artist-rels&fmt=json')
    if u == 'ERR': continue
    mbid = None
    if u:
        for r in u.get('relations', []):
            if 'artist' in r: mbid = r['artist']['id']; break
    if not mbid: cache[key] = None
    else:
        j = get('https://musicbrainz.org/ws/2/artist/' + mbid + '?inc=genres&fmt=json')
        if j == 'ERR' or not j: continue
        ls = j.get('life-span') or {}
        gen = [g['name'] for g in sorted(j.get('genres', []), key=lambda g: -g.get('count', 0))][:3]
        ba = (j.get('begin-area') or {}).get('name')
        cache[key] = {'m': mbid, 't': j.get('type'), 'c': (j.get('area') or {}).get('name'), 'b': ba,
                      'y': (ls.get('begin') or '')[:4], 'z': (ls.get('end') or '')[:4] if ls.get('ended') else '', 'g': gen}
    done += 1
    if done % 20 == 0:
        json.dump(cache, open(CACHE, 'w')); print(done, len(cache), flush=True)
json.dump(cache, open(CACHE, 'w'))
hit = sum(1 for v in cache.values() if v)
print('finished', len(cache), 'matched', hit)
