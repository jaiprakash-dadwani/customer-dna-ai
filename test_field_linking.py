"""
Test field linking validation
"""
print("Testing Field Linking...")

# Simulate session data
session_data = {
    'balance': 500,
    'wagered': 300,
    'deposits': [400, 200],  # Total: 600
    'wagers': [150, 150]     # Total: 300
}

total_deposits = sum(session_data['deposits'])
total_wagered = session_data['wagered']
balance = session_data['balance']

print(f"Deposits: {session_data['deposits']} = £{total_deposits}")
print(f"Wagers: {session_data['wagers']} = £{total_wagered}")
print(f"Balance: £{balance}")

# Validation: Balance should equal Deposits - Wagered
expected_balance = total_deposits - total_wagered
print(f"Expected Balance: £{total_deposits} - £{total_wagered} = £{expected_balance}")

if abs(balance - expected_balance) > 0.01:
    print("❌ VALIDATION FAILED: Balance mismatch!")
    print(f"Correcting balance from £{balance} to £{expected_balance}")
else:
    print("✅ VALIDATION PASSED: Fields properly linked")

print("Field linking test complete!")