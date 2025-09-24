#!/usr/bin/env python3
"""
Test untuk memverifikasi konversi decimal hours
Menguji berbagai kasus untuk memastikan konversi HH:MM ke decimal sudah benar
"""

def test_decimal_hours_conversion():
    """Test decimal hours conversion with various cases"""
    
    test_cases = [
        # (duration_seconds, expected_hh_mm, expected_decimal)
        (1800, "00:30", 0.50),   # 30 minutes = 0.5 hours
        (3600, "01:00", 1.00),   # 1 hour = 1.0 hours
        (5400, "01:30", 1.50),   # 1 hour 30 minutes = 1.5 hours
        (7200, "02:00", 2.00),   # 2 hours = 2.0 hours
        (900, "00:15", 0.25),    # 15 minutes = 0.25 hours
        (2700, "00:45", 0.75),   # 45 minutes = 0.75 hours
        (9900, "02:45", 2.75),   # 2 hours 45 minutes = 2.75 hours
        (14400, "04:00", 4.00),  # 4 hours = 4.0 hours
        (600, "00:10", 0.17),    # 10 minutes ≈ 0.17 hours (rounded)
        (1200, "00:20", 0.33),   # 20 minutes ≈ 0.33 hours (rounded)
        (12600, "03:30", 3.50),  # 3 hours 30 minutes = 3.5 hours
    ]
    
    print("🧭 orutego - Decimal Hours Conversion Test\n")
    print("Testing conversion from seconds to HH:MM and decimal hours...\n")
    
    all_passed = True
    
    for i, (duration_seconds, expected_hh_mm, expected_decimal) in enumerate(test_cases, 1):
        # Backend conversion logic (same as in app.py)
        duration_minutes = duration_seconds / 60
        hours = int(duration_minutes // 60)
        minutes = int(duration_minutes % 60)
        duration_formatted = f"{hours:02d}:{minutes:02d}"
        decimal_hours = round(hours + (minutes / 60), 2)
        
        # Test HH:MM format
        hh_mm_passed = duration_formatted == expected_hh_mm
        
        # Test decimal format
        decimal_passed = decimal_hours == expected_decimal
        
        # Overall test result
        test_passed = hh_mm_passed and decimal_passed
        all_passed = all_passed and test_passed
        
        # Print result
        status = "✅ PASS" if test_passed else "❌ FAIL"
        print(f"Test {i:2d}: {status}")
        print(f"         Input: {duration_seconds:5d} seconds")
        print(f"         HH:MM: {duration_formatted} (expected: {expected_hh_mm}) {'✅' if hh_mm_passed else '❌'}")
        print(f"       Decimal: {decimal_hours} (expected: {expected_decimal}) {'✅' if decimal_passed else '❌'}")
        print()
    
    print("-" * 50)
    if all_passed:
        print("🎉 All tests PASSED! Decimal hours conversion is working correctly.")
    else:
        print("⚠️  Some tests FAILED! Please check the conversion logic.")
    
    print(f"\nConversion Formula: decimal_hours = hours + (minutes / 60)")
    print(f"Example: 1:30 = 1 + (30/60) = 1 + 0.5 = 1.50 hours")

if __name__ == "__main__":
    test_decimal_hours_conversion()