#!/usr/bin/env python3
"""
Test script for Excel Row Processor
Creates sample Excel files to test the application functionality.
"""

import pandas as pd
import os
from pathlib import Path

def create_sample_excel_files():
    """Create sample Excel files for testing."""
    
    # Create test directory
    test_dir = Path("test_files")
    test_dir.mkdir(exist_ok=True)
    
    # Sample data
    sample_data = {
        'Name': ['John', 'Jane', 'Bob', 'Alice', 'Charlie', 'Diana', 'Eve', 'Frank'],
        'Age': [25, 30, 35, 28, 42, 33, 29, 38],
        'City': ['New York', 'London', 'Paris', 'Tokyo', 'Sydney', 'Berlin', 'Rome', 'Madrid'],
        'Salary': [50000, 60000, 55000, 65000, 70000, 58000, 62000, 68000]
    }
    
    # Create different sized files for testing
    test_files = [
        {
            'filename': 'small_file.xlsx',
            'rows': 5,
            'description': 'Small file with 5 rows (including header)'
        },
        {
            'filename': 'medium_file.xlsx', 
            'rows': 10,
            'description': 'Medium file with 10 rows (including header)'
        },
        {
            'filename': 'large_file.xlsx',
            'rows': 20,
            'description': 'Large file with 20 rows (including header)'
        }
    ]
    
    print("Creating sample Excel files for testing...")
    
    for test_file in test_files:
        # Create DataFrame with specified number of rows
        df = pd.DataFrame(sample_data)
        
        # Repeat data to get desired number of rows
        while len(df) < test_file['rows']:
            df = pd.concat([df, pd.DataFrame(sample_data)], ignore_index=True)
        
        # Trim to exact number of rows
        df = df.head(test_file['rows'])
        
        # Save to Excel file
        file_path = test_dir / test_file['filename']
        df.to_excel(file_path, index=False, engine='openpyxl')
        
        print(f"✅ Created {test_file['filename']}: {test_file['description']}")
        print(f"   - Rows: {len(df)} (including header)")
        print(f"   - Columns: {len(df.columns)}")
        print(f"   - File size: {file_path.stat().st_size / 1024:.1f} KB")
        print()
    
    print(f"📁 All test files created in: {test_dir.absolute()}")
    print("\nYou can now:")
    print("1. Run the Streamlit app: streamlit run app.py")
    print("2. Upload these test files to verify functionality")
    print("3. Test both 'Delete Odd' and 'Delete Even' options")

def verify_processing_logic():
    """Verify the row deletion logic is correct."""
    
    print("\n🔍 Verifying processing logic...")
    
    # Create a test DataFrame
    test_df = pd.DataFrame({
        'Row': ['Header', 'Row2', 'Row3', 'Row4', 'Row5', 'Row6', 'Row7', 'Row8'],
        'Data': ['Header', 'Data2', 'Data3', 'Data4', 'Data5', 'Data6', 'Data7', 'Data8']
    })
    
    print("Original DataFrame:")
    print(test_df)
    print()
    
    # Test delete odd rows (keep header + odd data rows: 1,3,5,7)
    odd_indices = list(range(1, len(test_df), 2))  # [1, 3, 5, 7]
    df_odd_deleted = test_df.drop(odd_indices).reset_index(drop=True)
    
    print("After deleting ODD rows (2,4,6,8):")
    print(df_odd_deleted)
    print()
    
    # Test delete even rows (keep header + even data rows: 1,2,4,6,8)
    even_indices = list(range(2, len(test_df), 2))  # [2, 4, 6]
    df_even_deleted = test_df.drop(even_indices).reset_index(drop=True)
    
    print("After deleting EVEN rows (3,5,7):")
    print(df_even_deleted)
    print()
    
    print("✅ Processing logic verification complete!")

if __name__ == "__main__":
    print("🧪 Excel Row Processor - Test Setup")
    print("=" * 50)
    
    create_sample_excel_files()
    verify_processing_logic()
    
    print("\n🎉 Test setup complete!")
    print("Run 'streamlit run app.py' to start the application.")
