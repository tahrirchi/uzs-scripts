class SouthernUzbekTransliterator:
    def __init__(self):
        # Vowel mappings (including diacritics)
        self.vowels = {
            # Vowels with alif
            'اَ': 'a',
            'آ': 'o',
            'اِیـ': 'i',
            'اِی': 'i',
            'اېـ': 'e',
            'اې': 'e',
            'اۉ': 'oʻ',
            'اُو': 'u',
            'او': 'u',
            'اِ': 'i',
            'اُ': 'u',
            
            # Vowels without alif
            'ـَه': 'a',
            'ـه': 'a',
            'ـَ': 'a',
            'ـ': 'a',
            'ـا': 'o',
            'ـِی': 'i',
            'ـې': 'e',
            'ـِه': 'e',
            'ـِ': 'i',
            'ي': 'i',
            'ـُو': 'u',
            'ـۉ': 'oʻ',
            'ـُ': 'u',
            
            # Standalone vowels
            'ا': 'a',
            'ې': 'e',
            'ۉ': 'oʻ',
            'ی': 'y',
            'و': 'v',
        }
        
        # Consonant mappings
        self.consonants = {
            # Final, Medial, Initial, Isolated forms
            'ب': 'b', 'بـ': 'b', 'ـبـ': 'b', 'ـب': 'b',
            'پ': 'p', 'پـ': 'p', 'ـپـ': 'p', 'ـپ': 'p',
            'ت': 't', 'تـ': 't', 'ـتـ': 't', 'ـت': 't',
            'ث': 's', 'ثـ': 's', 'ـثـ': 's', 'ـث': 's',
            'ج': 'j', 'جـ': 'j', 'ـجـ': 'j', 'ـج': 'j',
            'چ': 'ch', 'چـ': 'ch', 'ـچـ': 'ch', 'ـچ': 'ch',
            'ح': 'h', 'حـ': 'h', 'ـحـ': 'h', 'ـح': 'h',
            'خ': 'x', 'خـ': 'x', 'ـخـ': 'x', 'ـخ': 'x',
            'د': 'd', 'ـد': 'd',
            'ذ': 'z', 'ـذ': 'z',
            'ر': 'r', 'ـر': 'r',
            'ز': 'z', 'ـز': 'z',
            'ژ': 'j', 'ـژ': 'j',
            'س': 's', 'سـ': 's', 'ـسـ': 's', 'ـس': 's',
            'ش': 'sh', 'شـ': 'sh', 'ـشـ': 'sh', 'ـش': 'sh',
            'ص': 's', 'صـ': 's', 'ـصـ': 's', 'ـص': 's',
            'ض': 'z', 'ضـ': 'z', 'ـضـ': 'z', 'ـض': 'z',
            'ط': 't', 'طـ': 't', 'ـطـ': 't', 'ـط': 't',
            'ظ': 'z', 'ظـ': 'z', 'ـظـ': 'z', 'ـظ': 'z',
            'ع': 'ʻ', 'عـ': 'ʻ', 'ـعـ': 'ʻ', 'ـع': 'ʻ',
            'غ': 'gʻ', 'غـ': 'gʻ', 'ـغـ': 'gʻ', 'ـغ': 'gʻ',
            'ف': 'f', 'فـ': 'f', 'ـفـ': 'f', 'ـف': 'f',
            'ق': 'q', 'قـ': 'q', 'ـقـ': 'q', 'ـق': 'q',
            'ک': 'k', 'کـ': 'k', 'ـکـ': 'k', 'ـک': 'k',
            'گ': 'g', 'گـ': 'g', 'ـگـ': 'g', 'ـگ': 'g',
            'ل': 'l', 'لـ': 'l', 'ـلـ': 'l', 'ـل': 'l',
            'م': 'm', 'مـ': 'm', 'ـمـ': 'm', 'ـم': 'm',
            'ن': 'n', 'نـ': 'n', 'ـنـ': 'n', 'ـن': 'n',
            'نگ': 'ng', 'نگـ': 'ng', 'ـنگـ': 'ng', 'ـنگ': 'ng',
            'و': 'v', 'ـو': 'v',
            'ه': 'h', 'هـ': 'h', 'ـهـ': 'h', 'ـه': 'h',
            'ی': 'i', 'یـ': 'i', 'ـیـ': 'i', 'ـی': 'i',
            'ء': 'ʻ', 'ئـ': 'ʻ', 'ـئـ': 'ʻ', 'أ': 'ʻ', 'ـأ': 'ʻ', 'ؤ': 'ʻ', 'ـؤ': 'ʻ',
        }
        
        # Combine all mappings
        self.all_mappings = {**self.vowels, **self.consonants}
        
        # Sort by length (longest first) to handle multi-character sequences
        self.sorted_keys = sorted(self.all_mappings.keys(), key=len, reverse=True)
    
    def transliterate(self, arabic_text):
        """
        Transliterate Southern Uzbek Arabic script to Latin script
        """
        result = ""
        i = 0
        
        while i < len(arabic_text):
            found = False
            
            # Try to match the longest possible sequence first
            for key in self.sorted_keys:
                if i + len(key) <= len(arabic_text):
                    if arabic_text[i:i+len(key)] == key:
                        result += self.all_mappings[key]
                        i += len(key)
                        found = True
                        break
            
            if not found:
                # If no mapping found, keep the original character
                result += arabic_text[i]
                i += 1
        
        return result
    
    def transliterate_to_latin(self, word):
        """
        Transliterate a single word with basic cleanup
        """
        transliterated = self.transliterate(word)
        
        # Basic cleanup - remove extra spaces and diacritics that weren't mapped
        transliterated = ''.join(char for char in transliterated if char.isprintable())
        
        return transliterated