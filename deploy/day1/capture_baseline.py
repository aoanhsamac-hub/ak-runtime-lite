import sys, json
sys.path.insert(0, r'C:\AK')
sys.path.insert(0, r'C:\AK\services')
from services.day1_baseline import record_day1_baseline, get_latest_baseline
result = record_day1_baseline()
baseline = get_latest_baseline()
print(json.dumps({'activation': result, 'baseline': baseline}))
