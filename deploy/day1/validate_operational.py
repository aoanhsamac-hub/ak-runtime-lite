import sys, json
sys.path.insert(0, r'C:\AK')
sys.path.insert(0, r'C:\AK\services')
checks = {}
try:
    from services.day1_forecast_handler import run_forecast_handler, get_forecasts
    r = run_forecast_handler()
    checks['forecast_created'] = {'pass': len(get_forecasts()) > 0, 'detail': r.get('status')}
except Exception as e:
    checks['forecast_created'] = {'pass': False, 'error': str(e)}
try:
    from services.day1_reality_handler import run_reality_handler, get_benchmarks
    r = run_reality_handler()
    checks['reality_created'] = {'pass': len(get_benchmarks()) > 0, 'detail': r.get('status')}
except Exception as e:
    checks['reality_created'] = {'pass': False, 'error': str(e)}
try:
    from services.day1_lesson_handler import run_lesson_handler, get_lessons
    r = run_lesson_handler()
    checks['lesson_created'] = {'pass': len(get_lessons()) > 0, 'detail': r.get('status')}
except Exception as e:
    checks['lesson_created'] = {'pass': False, 'error': str(e)}
try:
    from services.day1_evidence_handler import run_evidence_handler, get_evidence
    r = run_evidence_handler()
    checks['evidence_created'] = {'pass': len(get_evidence()) > 0, 'detail': r.get('status')}
except Exception as e:
    checks['evidence_created'] = {'pass': False, 'error': str(e)}
try:
    from services.day1_kace_handler import run_kace_handler, get_scorecards
    r = run_kace_handler()
    checks['scorecard_pipeline'] = {'pass': len(get_scorecards()) > 0, 'detail': r.get('status')}
except Exception as e:
    checks['scorecard_pipeline'] = {'pass': False, 'error': str(e)}
try:
    from services.day1_telegram_integration import verify_commands
    r = verify_commands()
    checks['telegram_valid'] = {'pass': r.get('status') == 'OK', 'detail': r.get('status')}
except Exception as e:
    checks['telegram_valid'] = {'pass': False, 'error': str(e)}
checks['all_pass'] = all(c.get('pass', False) for c in checks.values())
print(json.dumps(checks))
