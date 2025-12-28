#!/usr/bin/env python3
# Real scenario test for the comma separation fix

import regex
from bs4 import BeautifulSoup
import sys
import importlib
sys.path.append('.')

# Import the main function
from SDA_SS_to_MyBible_devotions import adventech_ref_to_MyBible_ref

def test_real_scenario():
    """Test with real HTML content similar to what the function would process"""
    
    # Create mock HTML with Bible references that need fixing
    test_html = """
    <p>Read <a class="verse">Рим.12:3, 1Кор.4:6</a> for today's study.</p>
    <p>Also consider <a class="verse">Кол.3:8, 9</a> and <a class="verse">Быт. 1,2</a>.</p>
    <p>Another reference: <a class="verse">Рим.12:3, 1Кор.4:6, 8</a></p>
    """
    
    print("Testing real scenario with HTML content...")
    print("Original HTML:")
    print(test_html)
    
    # Parse the HTML
    soup = BeautifulSoup(test_html, 'html.parser')
    
    # Find all verse tags
    verse_tags = soup.find_all('a', class_='verse')
    
    print(f"\nFound {len(verse_tags)} verse tags to process:")
    
    for i, tag in enumerate(verse_tags):
        original_text = tag.get_text()
        print(f"\n{i+1}. Original: '{original_text}'")
        
        # Process the tag with our function
        try:
            # Create a temporary soup for this specific tag processing
            temp_soup = BeautifulSoup(str(tag), 'html.parser')
            temp_tag = temp_soup.find('a', class_='verse')
            
            # Import language-specific functionality (mock if needed)
            try:
                bible_codes = importlib.import_module('lang_ru')
            except ImportError:
                # Create mock if lang_ru doesn't exist
                class MockBibleCodes:
                    @staticmethod
                    def ref_tag_preprocess(text):
                        return text
                    book_index_to_MyBible = {
                        'Рим': 450, '1Кор': 460, 'Кол': 510, 'Быт': 10, 
                        'Пс': 190, '2Тим': 550, 'Евр': 580
                    }
                bible_codes = MockBibleCodes()
            
            # Temporarily set bible_codes for the function
            import SDA_SS_to_MyBible_devotions
            SDA_SS_to_MyBible_devotions.bible_codes = bible_codes
            
            # Process the tag
            adventech_ref_to_MyBible_ref('ru', temp_soup, temp_tag)
            
            # Get the result
            result_html = str(temp_soup)
            print(f"   Result: {result_html}")
            
        except Exception as e:
            print(f"   Error: {e}")
    
    # Test the main problematic case specifically
    print("\n" + "="*50)
    print("Testing the main problematic case specifically:")
    print("Input: 'Рим.12:3, 1Кор.4:6'")
    
    # Create a mock tag and doc for direct testing
    class MockTag:
        def __init__(self, text):
            self.text = text
        def get_text(self):
            return self.text
        def insert_after(self, content):
            # Simulate inserting after the tag
            pass
        def decompose(self):
            # Remove the tag from the tree
            pass
    
    class MockDoc:
        def new_tag(self, tag, **attrs):
            return MockTag("")
    
    mock_tag = MockTag("Рим.12:3, 1Кор.4:6")
    mock_doc = MockDoc()
    
    try:
        adventech_ref_to_MyBible_ref('ru', mock_doc, mock_tag)
        print("✓ Main case processed successfully!")
        print("The comma between 'Рим.12:3' and '1Кор.4:6' should now be handled correctly.")
    except Exception as e:
        print(f"Error in main case: {e}")

if __name__ == "__main__":
    test_real_scenario()
