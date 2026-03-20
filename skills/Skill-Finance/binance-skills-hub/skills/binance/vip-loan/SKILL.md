---
name: vip-loan
description: Binance Vip-loan request using the Binance API. Authentication requires API key and secret key. 
metadata:
  version: 1.0.0
  author: Binance
license: MIT
---

# Binance Vip-loan Skill

Vip-loan request on Binance using authenticated API endpoints. Requires API key and secret key for certain endpoints. Return the result in JSON format.

## Quick Reference

| Endpoint | Description | Required | Optional | Authentication |
|----------|-------------|----------|----------|----------------|
| `/sapi/v1/loan/vip/request/interestRate` (GET) | Get Borrow Interest Rate(USER_DATA) | loanCoin | recvWindow | Yes |
| `/sapi/v1/loan/vip/collateral/data` (GET) | Get Collateral Asset Data(USER_DATA) | None | collateralCoin, recvWindow | Yes |
| `/sapi/v1/loan/vip/loanable/data` (GET) | Get Loanable Assets Data(USER_DATA) | None | loanCoin, vipLevel, recvWindow | Yes |
| `/sapi/v1/loan/vip/interestRateHistory` (GET) | Get VIP Loan Interest Rate History (USER_DATA) | coin, recvWindow | startTime, endTime, current, limit | Yes |
| `/sapi/v1/loan/vip/borrow` (POST) | VIP Loan Borrow(TRADE) | loanAccountId, loanCoin, loanAmount, collateralAccountId, collateralCoin, isFlexibleRate | loanTerm, recvWindow | Yes |
| `/sapi/v1/loan/vip/renew` (POST) | VIP Loan Renew(TRADE) | orderId, loanTerm | recvWindow | Yes |
| `/sapi/v1/loan/vip/repay` (POST) | VIP Loan Repay(TRADE) | orderId, amount | recvWindow | Yes |
| `/sapi/v1/loan/vip/collateral/account` (GET) | Check VIP Loan Collateral Account (USER_DATA) | None | orderId, collateralAccountId, recvWindow | Yes |
| `/sapi/v1/loan/vip/accruedInterest` (GET) | Get VIP Loan Accrued Interest (USER_DATA) | None | orderId, loanCoin, startTime, endTime, current, limit, recvWindow | Yes |
| `/sapi/v1/loan/vip/ongoing/orders` (GET) | Get VIP Loan Ongoing Orders(USER_DATA) | None | orderId, collateralAccountId, loanCoin, collateralCoin, current, limit, recvWindow | Yes |
| `/sapi/v1/loan/vip/request/data` (GET) | Query Application Status(USER_DATA) | None | current, limit, recvWindow | Yes |

---

## Parameters

### Common Parameters

* **loanCoin**: 
* **recvWindow**:  (e.g., 5000)
* **collateralCoin**: 
* **loanCoin**: 
* **vipLevel**: default:user's vip level (e.g., 1)
* **coin**: 
* **startTime**:  (e.g., 1623319461670)
* **endTime**:  (e.g., 1641782889000)
* **current**: Current querying page. Start from 1; default: 1; max: 1000 (e.g., 1)
* **limit**: Default: 10; max: 100 (e.g., 10)
* **recvWindow**:  (e.g., 5000)
* **loanAccountId**:  (e.g., 1)
* **loanAmount**:  (e.g., 1.0)
* **collateralAccountId**: Multiple split by `,` (e.g., 1)
* **collateralCoin**: Multiple split by `,`
* **isFlexibleRate**: Default: TRUE. TRUE : flexible rate; FALSE: fixed rate (e.g., true)
* **loanTerm**: Mandatory for fixed rate. Optional for fixed interest rate. Eg: 30/60 days
* **orderId**:  (e.g., 1)
* **loanTerm**: 30/60 days
* **amount**:  (e.g., 1.0)
* **orderId**:  (e.g., 1)
* **collateralAccountId**:  (e.g., 1)


## Authentication

For endpoints that require authentication, you will need to provide Binance API credentials.
Required credentials:

* apiKey: Your Binance API key (for header)
* secretKey: Your Binance API secret (for signing)

Base URLs:
* Mainnet: https://api.binance.com

## Security

### Share Credentials

Users can provide Binance API credentials by sending a file where the content is in the following format:

```bash
abc123...xyz
secret123...key
```

### Never Disclose API Key and Secret

Never disclose the location of the API key and secret file.

Never send the API key and secret to any website other than Mainnet and Testnet.

### Never Display Full Secrets

When showing credentials to users:
- **API Key:** Show first 5 + last 4 characters: `su1Qc...8akf`
- **Secret Key:** Always mask, show only last 5: `***...aws1`

Example response when asked for credentials:
Account: main
API Key: su1Qc...8akf
Secret: ***...aws1

### Listing Accounts

When listing accounts, show names and environment only — never keys:
Binance Accounts:
* main (Mainnet)
* futures-keys (Mainnet)

### Transactions in Mainnet

When performing transactions in mainnet, always confirm with the user before proceeding by asking them to write "CONFIRM" to proceed.

---

## Binance Accounts

### main
- API Key: your_mainnet_api_key
- Secret: your_mainnet_secret

### TOOLS.md Structure

```bash
## Binance Accounts

### main
- API Key: abc123...xyz
- Secret: secret123...key
- Description: Primary trading account


### futures-keys
- API Key: futures789...def
- Secret: futuressecret...uvw
- Description: Futures trading account
```

## Agent Behavior

1. Credentials requested: Mask secrets (show last 5 chars only)
2. Listing accounts: Show names and environment, never keys
3. Account selection: Ask if ambiguous, default to main
4. When doing a transaction in mainnet, confirm with user before by asking to write "CONFIRM" to proceed
5. New credentials: Prompt for name, environment, signing mode

## Adding New Accounts

When user provides new credentials:

* Ask for account name
* Store in `TOOLS.md` with masked display confirmation 

## Signing Requests

For trading endpoints that require a signature:

1. Build query string with all parameters, including the timestamp (Unix ms).
2. Percent-encode the parameters using UTF-8 according to RFC 3986.
3. Sign query string with secretKey using HMAC SHA256, RSA, or Ed25519 (depending on the account configuration).
4. Append signature to query string.
5. Include `X-MBX-APIKEY` header.

Otherwise, do not perform steps 3–5.

## User Agent Header

Include `User-Agent` header with the following string: `binance-vip-loan/1.0.0 (Skill)`

See [`references/authentication.md`](./references/authentication.md) for implementation details.
