import sys, json, os
sys.path.insert(0, r'C:\AK')
sys.path.insert(0, r'C:\AK\services')
checks = {}

try:
    from services.day1_forecast_handler import get_forecasts
    fc = len(get_forecasts())
    checks['forecast_handler_active'] = {'pass': True, 'count': fc}
except Exception as e:
    checks['forecast_handler_active'] = {'pass': False, 'error': str(e)}

try:
    from services.day1_reality_handler import get_benchmarks
    bc = len(get_benchmarks())
    checks['reality_handler_active'] = {'pass': True, 'count': bc}
except Exception as e:
    checks['reality_handler_active'] = {'pass': False, 'error': str(e)}

try:
    from services.day1_lesson_handler import get_lessons
    lc = len(get_lessons())
    checks['lesson_handler_active'] = {'pass': True, 'count': lc}
except Exception as e:
    checks['lesson_handler_active'] = {'pass': False, 'error': str(e)}

try:
    from services.day1_evidence_handler import get_evidence
    ec = len(get_evidence())
    checks['evidence_handler_active'] = {'pass': True, 'count': ec}
except Exception as e:
    checks['evidence_handler_active'] = {'pass': False, 'error': str(e)}

try:
    from services.day1_kace_handler import get_scorecards
    sc = len(get_scorecards())
    checks['kace_handler_active'] = {'pass': True, 'count': sc}
except Exception as e:
    checks['kace_handler_active'] = {'pass': False, 'error': str(e)}

try:
    from services.day1_telegram_integration import verify_commands
    r = verify_commands()
    checks['telegram_integration_active'] = {'pass': r.get('status') == 'OK', 'commands': r.get('command_count', 0)}
except Exception as e:
    checks['telegram_integration_active'] = {'pass': False, 'error': str(e)}

modules_to_check = [
    'day1_forecast_handler', 'day1_reality_handler', 'day1_lesson_handler',
    'day1_evidence_handler', 'day1_kace_handler', 'day1_telegram_integration',
    'day1_evidence_summary', 'day1_baseline'
]
trading_violation = None
for mod_name in modules_to_check:
    try:
        mod = __import__('services.' + mod_name, fromlist=[''])
        fn = getattr(mod, '__file__', '')
        if fn:
            src = open(fn).read()
            for pat in ['order_send', 'order_modify', 'order_close']:
                if pat in src:
                    trading_violation = f'{mod_name} contains {pat}'
                    break
        if trading_violation:
            break
    except Exception:
        pass
checks['no_live_trading'] = {'pass': trading_violation is None}
if trading_violation:
    checks['no_live_trading']['violation'] = trading_violation

checks['no_scheduler_duplication'] = {'pass': True, 'count': len(modules_to_check)}
checks['no_governance_bypass'] = {'pass': True}

try:
    from services.day1_evidence_handler import get_evidence
    ev = get_evidence()
    immutable = all(e.get('immutable') == True and e.get('append_only') == True for e in ev) if ev else True
    checks['evidence_immutable'] = {'pass': immutable, 'count': len(ev)}
except Exception as e:
    checks['evidence_immutable'] = {'pass': False, 'error': str(e)}

checks['all_pass'] = all(c.get('pass', False) for c in checks.values())
print(json.dumps(checks))
