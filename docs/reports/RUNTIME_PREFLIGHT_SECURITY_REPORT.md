# RUNTIME PREFLIGHT SECURITY REPORT

## Authority
Yết Kiêu
Support: Sage

## Validation Results

| Check | Status | Finding |
|-------|--------|---------|
| **Telegram Security** | FAIL | No Telegram implementation exists. Token not stored. No authentication. |
| **Token Storage** | WARNING | No .env file in project root. D:\AK\.env.example exists but is a template. Secrets storage not configured. |
| **Tailscale Exposure** | PASS | Tailscale IP: 100.124.11.14 (tailnet only). Not publicly exposed. Service running, Automatic start. |
| **Open Ports** | WARNING | Listening ports found: 445 (SMB), 5040 (svchost), 20128 (node), 5357 (WSDAPI). SMB exposed on LAN (10.249.41.114:139/445). |
| **Remote Access** | WARNING | MSTSC process running (287 MB). Remote Desktop access is active. |
| **Credential Storage** | FAIL | No centralized credential management found. No encrypted storage. Telegram token has no storage location. |
| **Runtime Permissions** | PASS | Agent runtime uses RoleBoundary and governance gates. Read-only enforced for MT5. |
| **Windows Firewall** | WARNING | Firewall enabled for all profiles. `DefaultInboundAction: NotConfigured` - this means default inbound behavior depends on firewall rules. Default Inbound is NOT set to Block. |
| **Build Validation Security** | PASS | BuildValidationRuntime checks for forbidden patterns: `import os.system`, `subprocess.call`, `eval(`, `exec(`, `order_send`. |
| **Reviewer Runtime Security** | PASS | ReviewerRuntime forbids: `self_approve`, `auto_promote`, `bypass_review`, `skip_validation`. |

## Security Risks

### CRITICAL
1. **No Telegram infrastructure** - Bot token, authentication, command handling all missing.
2. **No credential storage** - No .env, no encrypted config, no secrets management.

### HIGH
3. **SMB exposed on LAN** - Ports 139/445 listening on 10.249.41.114. Firewall not blocking inbound by default.
4. **Windows Firewall misconfiguration** - `DefaultInboundAction: NotConfigured` means inbound traffic may be allowed by implicit rules.

### MEDIUM
5. **Remote Desktop active** - MSTSC running. Potential attack vector if credentials compromised.
6. **Node process on port 20128** - Unknown service listening.

## Recommendations
1. Create `.env` with restricted permissions (0600 equivalent via icacls).
2. Implement Telegram bot with whitelist authentication before deployment.
3. Configure Windows Firewall default inbound action to Block.
4. Block SMB ports 139/445 on external interfaces.
5. Audit the node service on port 20128.
6. Establish credential rotation policy.
