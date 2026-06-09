import os, re, json

ak_dir = r'C:\AK\services'
results = {}

exclude = {'build_validation_runtime.py'}
issues = []
for root, dirs, files in os.walk(ak_dir):
    for f in files:
        if not f.endswith('.py') or f in exclude:
            continue
        path = os.path.join(root, f)
        with open(path, 'r') as fh:
            for i, line in enumerate(fh, 1):
                if re.search(r'order_send|order_modify|order_close', line):
                    issues.append(f'{path}:{i}')
results['no_live_trading'] = 'PASS' if not issues else f'FAIL: {"; ".join(issues)}'

issues = []
patterns = [
    (r'TELEGRAM_BOT_TOKEN\s*=\s*["\x27](?!\{)', 'Hardcoded Telegram token'),
    (r'MT5_LOGIN\s*=\s*\d+', 'Hardcoded MT5 login'),
    (r'MT5_PASSWORD\s*=\s*["\x27]', 'Hardcoded MT5 password'),
]
for root, _, files in os.walk(ak_dir):
    for f in files:
        if not f.endswith('.py'):
            continue
        path = os.path.join(root, f)
        with open(path, 'r') as fh:
            for i, line in enumerate(fh, 1):
                for pat, desc in patterns:
                    if re.search(pat, line):
                        issues.append(f'{desc} at {path}:{i}')
results['no_plaintext_secrets'] = 'PASS' if not issues else f'FAIL: {"; ".join(issues)}'

print(json.dumps(results, indent=2))
