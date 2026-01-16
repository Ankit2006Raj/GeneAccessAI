"""
Quick verification script to check if navigation is properly configured
"""

import os

def check_file_exists(filepath):
    """Check if file exists"""
    exists = os.path.exists(filepath)
    status = "✅" if exists else "❌"
    print(f"{status} {filepath}: {'EXISTS' if exists else 'NOT FOUND'}")
    return exists

def check_content_in_file(filepath, search_text):
    """Check if specific content exists in file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            found = search_text in content
            status = "✅" if found else "❌"
            print(f"{status} '{search_text}' in {filepath}: {'FOUND' if found else 'NOT FOUND'}")
            return found
    except Exception as e:
        print(f"❌ Error reading {filepath}: {e}")
        return False

def main():
    print("\n" + "="*70)
    print("NAVIGATION VERIFICATION SCRIPT")
    print("="*70 + "\n")
    
    # Check template files
    print("📁 Checking Template Files:")
    print("-" * 70)
    base_html = check_file_exists('templates/base.html')
    ethnicity_html = check_file_exists('templates/ethnicity_risk.html')
    genomic_html = check_file_exists('templates/genomic_profile.html')
    clinical_html = check_file_exists('templates/clinical_tests.html')
    overview_html = check_file_exists('templates/advanced_features_overview.html')
    
    print("\n📝 Checking Navigation Content in base.html:")
    print("-" * 70)
    if base_html:
        check_content_in_file('templates/base.html', 'Advanced Features')
        check_content_in_file('templates/base.html', 'advancedFeaturesDropdown')
        check_content_in_file('templates/base.html', 'Risk Timeline')
        check_content_in_file('templates/base.html', 'Family Pedigree')
        check_content_in_file('templates/base.html', 'Ethnicity Risk Adjuster')
        check_content_in_file('templates/base.html', 'Genomic Profile')
        check_content_in_file('templates/base.html', 'Clinical Test Recommender')
        check_content_in_file('templates/base.html', 'bootstrap@5.3.2')
    
    print("\n🔗 Checking Routes in app.py:")
    print("-" * 70)
    if os.path.exists('app.py'):
        check_content_in_file('app.py', '@app.route(\'/ethnicity-risk\')')
        check_content_in_file('app.py', '@app.route(\'/genomic-profile\')')
        check_content_in_file('app.py', '@app.route(\'/clinical-tests\')')
        check_content_in_file('app.py', '@app.route(\'/advanced-features\')')
    
    print("\n🎨 Checking CSS Styles:")
    print("-" * 70)
    if base_html:
        check_content_in_file('templates/base.html', '.dropdown-menu')
        check_content_in_file('templates/base.html', 'pulse-badge')
        check_content_in_file('templates/base.html', 'slideDown')
    
    print("\n" + "="*70)
    print("VERIFICATION COMPLETE")
    print("="*70)
    
    print("\n📋 NEXT STEPS:")
    print("-" * 70)
    print("1. If all checks passed (✅), restart Flask server:")
    print("   - Stop server: Ctrl + C")
    print("   - Start server: python app.py")
    print("\n2. Hard refresh browser:")
    print("   - Press: Ctrl + Shift + R")
    print("\n3. Check navigation bar for 'Advanced Features' dropdown")
    print("\n4. If still not visible, open browser console (F12) and check for errors")
    print("\n5. Try accessing directly:")
    print("   - http://127.0.0.1:5000/ethnicity-risk")
    print("   - http://127.0.0.1:5000/genomic-profile")
    print("   - http://127.0.0.1:5000/clinical-tests")
    print("   - http://127.0.0.1:5000/advanced-features")
    print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    main()
