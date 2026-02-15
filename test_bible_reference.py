#!/usr/bin/env python3
# Real scenario test for the comma separation fix

import regex
from bs4 import BeautifulSoup
import sys
import importlib
sys.path.append('.')

# Import the main function
from SDA_SS_to_MyBible_devotions import adventech_ref_to_MyBible_ref

def process_tag_with_language(temp_tag, language_code):
    """Process a tag with specific language settings"""
    try:
        # Import language-specific functionality
        bible_codes = importlib.import_module('lang_' + language_code)
    except ImportError:
        # Create mock if language module doesn't exist
        class MockBibleCodes:
            @staticmethod
            def ref_tag_preprocess(text):
                return text
            book_index_to_MyBible = {
                'Рим': 450, '1Кор': 460, 'Кол': 510, 'Быт': 10, 
                'Пс': 190, '2Тим': 550, 'Евр': 580,
                'Rom': 520, '1Cor': 530, 'Col': 580, 'Gen': 10,
                'Romanos': 520, '1Corintios': 530,
                'Génesis': 10, 'Colosenses': 580, 'Juan': 500,
                'Efesios': 560, '1 Corintios': 530, 'Romanos': 520
            }
        bible_codes = MockBibleCodes()
    
    # Temporarily set bible_codes for the function
    import SDA_SS_to_MyBible_devotions
    SDA_SS_to_MyBible_devotions.bible_codes = bible_codes
    
    return bible_codes

def test_real_scenario():
    """Test with real HTML content similar to what the function would process"""
    
    # Language-specific test content
    test_contents = {
        'ru': """
        <p>Read <a class="verse">Рим.12:3, 1Кор.4:6</a> for today's study.</p>
        <p>Also consider <a class="verse">Кол.3:8, 9</a> and <a class="verse">Быт. 1,2</a>.</p>
        <p>Another reference: <a class="verse">Рим.12:3, 1Кор.4:6, 8</a></p>
        """,
        'en': """
        <p>Read <a class="verse">Romans 12:3, 1Corinthians 4:6</a> for today's study.</p>
        <p>Also consider <a class="verse">Colossians 3:8, 9</a> and <a class="verse">Genesis 1,2</a>.</p>
        <p>Another reference: <a class="verse">Romans 12:3, 1Corinthians 4:6, 8</a></p>
        """,
        'es': """
        <p>Read <a class="verse">Romanos 12:3, 1Corintios 4:6</a> for today's study.</p>
        <p>Also consider <a class="verse">Colosenses 3:8, 9</a> and <a class="verse">Génesis 1,2</a>.</p>
        <p>Another reference: <a class="verse">Romanos 12:3, 1Corintios 4:6, 8</a></p>
        """
    }
    
    # Test for each language
    languages = ['ru', 'en', 'es']
    
    for language_code in languages:
        print(f"\n--- Testing {language_code} language ---")
        
        # Get language-specific HTML content
        test_html = test_contents[language_code]
        
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
                
                # Process with specific language
                bible_codes = process_tag_with_language(temp_tag, language_code)
                
                # Process the tag
                adventech_ref_to_MyBible_ref(language_code, temp_soup, temp_tag)
                
                # Get the result
                result_html = str(temp_soup)
                print(f"   Result: {result_html}")
                
            except Exception as e:
                print(f"   Error: {e}")
    
    # Test the main problematic cases specifically for each language
    print("\n" + "="*50)
    print("Testing the main problematic cases specifically for each language:")
    
    test_cases = {
        'ru': "Рим.12:3, 1Кор.4:6",
        'en': "Romans 12:3, 1Corinthians 4:6",
        'es': "Romanos 12:3, 1Corintios 4:6"
    }
    
    for lang, test_case in test_cases.items():
        print(f"\nLanguage: {lang}, Input: '{test_case}'")
        
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
            def insert(self, position, content):
                # Simulate inserting content at position
                pass
        
        class MockDoc:
            def new_tag(self, tag, **attrs):
                return MockTag("")
        
        mock_tag = MockTag(test_case)
        mock_doc = MockDoc()
        
        try:
            # Process with specific language
            bible_codes = process_tag_with_language(mock_tag, lang)
            
            adventech_ref_to_MyBible_ref(lang, mock_doc, mock_tag)
            print(f"✓ {lang} case processed successfully!")
        except Exception as e:
            print(f"Error in {lang} case: {e}")

def test_spanish_references_with_spaces():
    """Test Spanish references with spaces after colons which is the new issue"""
    print("\n" + "="*50)
    print("Testing Spanish references with spaces after colons:")
    
    # Test cases with spaces after colons (new format)
    spanish_test_cases_with_spaces = [
        "Génesis 1: 26, 27",
        "Colosenses 1: 13–19",
        "Juan 1: 1–3",
        "Efesios 1: 22",
        "1 Corintios 4: 9",
        "1 Corintios 12: 12–27",
        "Romanos 6: 3, 4",
        # Multiple references with spaces
        "Génesis 1: 26, 27; Colosenses 1: 13–19; Juan 1: 1–3",
        # Mixed format (old and new)
        "Génesis 1:26, 27; Colosenses 1: 13–19; Juan 1:1–3"
    ]
    
    # Create mock tag and doc classes
    class MockTag:
        def __init__(self, text):
            self.text = text
        def get_text(self):
            return self.text
        def insert_after(self, content):
            pass
        def decompose(self):
            pass
        def insert(self, position, content):
            pass
    
    class MockDoc:
        def new_tag(self, tag, **attrs):
            return MockTag("")
    
    # Process each test case
    for i, test_case in enumerate(spanish_test_cases_with_spaces):
        print(f"\nTest case {i+1}: '{test_case}'")
        
        mock_tag = MockTag(test_case)
        mock_doc = MockDoc()
        
        try:
            # Process with Spanish language settings
            bible_codes = process_tag_with_language(mock_tag, 'es')
            
            adventech_ref_to_MyBible_ref('es', mock_doc, mock_tag)
            print(f"✓ Spanish reference with spaces processed successfully!")
        except Exception as e:
            print(f"Error in Spanish reference test case: {e}")

if __name__ == "__main__":
    test_real_scenario()
    test_spanish_references_with_spaces()
