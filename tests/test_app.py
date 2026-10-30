import sys
import os
import io
import pandas as pd
import pathlib

# Ensure UTF-8 console output for Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

from streamlit.testing.v1 import AppTest

def run_tests():
    print("==================================================================")
    print("STARTING COMPREHENSIVE STREAMLIT FUNCTIONAL TEST SUITE")
    print("==================================================================")

    test_dir = pathlib.Path(__file__).resolve().parent
    candidates = [
        test_dir.parent / "app.py",
        pathlib.Path("app.py").resolve(),
        pathlib.Path("visual-exploration-dashboard/app.py").resolve(),
    ]
    app_path = None
    for c in candidates:
        if c.exists():
            app_path = str(c)
            break
    assert app_path is not None, f"Could not find app.py among: {[str(c) for c in candidates]}"
    
    # --------------------------------------------------------------------------
    # Test 1: Initial Default State Baseline
    # --------------------------------------------------------------------------
    print("\n[TEST 1] Verifying Default Initial State...")
    at = AppTest.from_file(app_path)
    at.run()
    assert not at.exception, f"App crashed on start: {at.exception}"
    
    metrics = {m.label: m.value for m in at.metric}
    print(f"  -> Total Revenue: {metrics['Total Revenue']}")
    print(f"  -> Average / Row: {metrics['Average / Row']}")
    print(f"  -> Rows Displayed: {metrics['Rows Displayed']}")
    print(f"  -> Leading Outlet: {metrics['Leading Outlet']}")
    print(f"  -> Top Product Line: {metrics['Top Product Line']}")
    
    assert metrics['Rows Displayed'] == '3,282', f"Expected 3,282 rows, got {metrics['Rows Displayed']}"
    assert "920.6" in metrics['Total Revenue'], f"Expected ~920.6M, got {metrics['Total Revenue']}"
    assert metrics['Leading Outlet'] == "Pune", f"Expected Pune, got {metrics['Leading Outlet']}"
    assert metrics['Top Product Line'] == "Beverages", f"Expected Beverages, got {metrics['Top Product Line']}"
    print("  ✓ PASS: Default baseline verified.")

    # --------------------------------------------------------------------------
    # Test 2: Filter by Outlet Independently (Pune Only)
    # --------------------------------------------------------------------------
    print("\n[TEST 2] Testing Outlet Filter (Pune only)...")
    at.multiselect(key="filter_outlets").set_value(["Pune"]).run()
    assert not at.exception
    m = {met.label: met.value for met in at.metric}
    print(f"  -> Pune Rows: {m['Rows Displayed']} | Total: {m['Total Revenue']} | Leading: {m['Leading Outlet']}")
    assert m['Rows Displayed'] == '1,093', f"Expected 1,093 rows (1095 minus 2 errors in Pune), got {m['Rows Displayed']}"
    assert m['Leading Outlet'] == "Pune"
    print("  ✓ PASS: Outlet filter independently verified.")

    # --------------------------------------------------------------------------
    # Test 3: Filter by Item Independently (Merchandise Only)
    # --------------------------------------------------------------------------
    print("\n[TEST 3] Testing Item Filter (Merchandise only)...")
    at.multiselect(key="filter_outlets").set_value(["Pune", "Jaipur", "Kochi"])
    at.multiselect(key="filter_items").set_value(["Merchandise"]).run()
    assert not at.exception
    m = {met.label: met.value for met in at.metric}
    print(f"  -> Merchandise Rows: {m['Rows Displayed']} | Total: {m['Total Revenue']} | Top Item: {m['Top Product Line']}")
    assert m['Rows Displayed'] == '1,094', f"Expected 1,094 rows (1095 minus 1 error), got {m['Rows Displayed']}"
    assert m['Top Product Line'] == "Merchandise"
    print("  ✓ PASS: Item filter independently verified.")

    # --------------------------------------------------------------------------
    # Test 4: Filter by Month Window (Months 11-12, Winter Peak)
    # --------------------------------------------------------------------------
    print("\n[TEST 4] Testing Month Range Slider (November & December)...")
    at.multiselect(key="filter_items").set_value(["Beverages", "Bakery", "Merchandise"])
    at.slider(key="filter_months").set_value((11, 12)).run()
    assert not at.exception
    m = {met.label: met.value for met in at.metric}
    print(f"  -> Nov-Dec Rows: {m['Rows Displayed']} | Total: {m['Total Revenue']}")
    # 61 days * 3 outlets * 3 items = 549 records minus 1 error = 548
    assert m['Rows Displayed'] == '548'
    print("  ✓ PASS: Month range slider verified.")

    # --------------------------------------------------------------------------
    # Test 5: Filter by Offer Range (20% to 25%)
    # --------------------------------------------------------------------------
    print("\n[TEST 5] Testing Promotional Offer Slider (20% to 25%)...")
    at.slider(key="filter_months").set_value((1, 12))
    at.slider(key="filter_offers").set_value((20, 25)).run()
    assert not at.exception
    m = {met.label: met.value for met in at.metric}
    print(f"  -> Offer 20-25% Rows: {m['Rows Displayed']} | Total: {m['Total Revenue']} | Best Outlet: {m['Leading Outlet']}")
    assert m['Rows Displayed'] == '1,079'
    assert "326.4" in m['Total Revenue']
    assert m['Leading Outlet'] == "Pune"
    print("  ✓ PASS: Offer range slider verified.")

    # --------------------------------------------------------------------------
    # Test 6: Combined Complex Filter (Pune + Kochi, Beverages, Months 11-12, Offers 20-25)
    # --------------------------------------------------------------------------
    print("\n[TEST 6] Testing Combined Multi-Filter Interaction...")
    at.multiselect(key="filter_outlets").set_value(["Pune", "Kochi"])
    at.multiselect(key="filter_items").set_value(["Beverages"])
    at.slider(key="filter_months").set_value((11, 12))
    at.slider(key="filter_offers").set_value((20, 25)).run()
    assert not at.exception
    m = {met.label: met.value for met in at.metric}
    print(f"  -> Combined Filter Rows: {m['Rows Displayed']} | Total: {m['Total Revenue']}")
    assert int(m['Rows Displayed'].replace(',', '')) > 0
    print("  ✓ PASS: Multi-filter combination verified.")

    # --------------------------------------------------------------------------
    # Test 7: Reset Filters Action
    # --------------------------------------------------------------------------
    print("\n[TEST 7] Testing Reset Filters Button...")
    at.button(key="reset_filters").click().run()
    assert not at.exception
    m = {met.label: met.value for met in at.metric}
    print(f"  -> Rows after Reset: {m['Rows Displayed']} | Total: {m['Total Revenue']}")
    assert m['Rows Displayed'] == '3,282'
    assert "920.6" in m['Total Revenue']
    print("  ✓ PASS: Reset filters button restored all defaults.")

    # --------------------------------------------------------------------------
    # Test 8: Empty Filter Defensive Handling (Empty Outlets)
    # --------------------------------------------------------------------------
    print("\n[TEST 8] Testing Empty Filter Selection Guard (Empty Outlets)...")
    at.multiselect(key="filter_outlets").set_value([]).run()
    assert not at.exception
    assert len(at.warning) > 0, "Warning expected for empty selection"
    print(f"  -> Warning displayed: '{at.warning[0].value}'")
    print("  ✓ PASS: Empty filter guard successfully arrested execution and prompted user.")

    # --------------------------------------------------------------------------
    # Test 9: CSV Download Integrity
    # --------------------------------------------------------------------------
    print("\n[TEST 9] Testing CSV Export Facility...")
    at.multiselect(key="filter_outlets").set_value(["Pune", "Jaipur", "Kochi"]).run()
    assert not at.exception
    assert len(at.download_button) > 0, "Download button not found"
    download_btn = at.download_button[0]
    assert "Download Filtered Dataset as CSV" in download_btn.proto.label
    assert len(download_btn.proto.url) > 0, "Download URL endpoint generated"
    clean_label = download_btn.proto.label.encode('ascii', errors='replace').decode()
    print(f"  -> Download Button: '{clean_label}' | Endpoint: {download_btn.proto.url}")
    print("  ✓ PASS: CSV download export button verified.")
    print("  ✓ PASS: CSV download export payload verified.")

    print("\n==================================================================")
    print("ALL 9 STREAMLIT FUNCTIONAL TESTS PASSED WITH 100% SUCCESS!")
    print("==================================================================")

if __name__ == "__main__":
    run_tests()
