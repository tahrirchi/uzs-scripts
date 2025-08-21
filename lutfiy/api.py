import os
from pathlib import Path
from typing import Optional, Union
from .ngram_zwnj import GenericNGramPredictor
from .transliterate import SouthernUzbekTransliterator

class Lutfiy:
    """
    High-level API for Southern Uzbek text processing
    """
    
    def __init__(self, model_path: Optional[Union[str, Path]] = None):
        """
        Initialize Lutfiy with optional custom model path
        
        Args:
            model_path: Path to custom ngram model. If None, uses default bundled model.
        """
        self.transliterator = SouthernUzbekTransliterator()
        self.ngram_predictor = None
        
        # Load ngram model
        try:
            if model_path is None:
                self.ngram_predictor = GenericNGramPredictor.from_default_model()
            else:
                self.ngram_predictor = GenericNGramPredictor.from_file(model_path)
        except (FileNotFoundError, ValueError) as e:
            print(f"Warning: Could not load ngram model: {e}")
            print("ZWNJ correction will not be available.")
    
    def fix_zwnj(self, text: str, window_size: Optional[int] = None) -> str:
        """
        Fix ZWNJ (Zero Width Non-Joiner) placement in Southern Uzbek text
        
        Args:
            text: Input text in Southern Uzbek Arabic script
            window_size: Context window size for ngram analysis
            
        Returns:
            Text with corrected ZWNJ placement
        """
        if self.ngram_predictor is None:
            raise ValueError("Ngram model not loaded. Cannot perform ZWNJ correction.")
        
        return self.ngram_predictor.process_text(text, window_size)
    
    def transliterate(self, text: str) -> str:
        """
        Transliterate Southern Uzbek Arabic script to Latin script
        
        Args:
            text: Input text in Southern Uzbek Arabic script
            
        Returns:
            Transliterated text in Latin script
        """
        return self.transliterator.transliterate(text)
    
    def process(self, text: str, fix_zwnj: bool = True, transliterate: bool = False) -> str:
        """
        Process text with multiple operations
        
        Args:
            text: Input text in Southern Uzbek Arabic script
            fix_zwnj: Whether to fix ZWNJ placement
            transliterate: Whether to transliterate to Latin
            
        Returns:
            Processed text
        """
        result = text
        
        if fix_zwnj and self.ngram_predictor is not None:
            result = self.fix_zwnj(result)
        
        if transliterate:
            result = self.transliterate(result)
        
        return result
    
    def analyze_zwnj(self, text: str, window_size: Optional[int] = None) -> list:
        """
        Analyze ZWNJ decisions in detail
        
        Args:
            text: Input text in Southern Uzbek Arabic script
            window_size: Context window size for ngram analysis
            
        Returns:
            List of detailed analysis for each ه character
        """
        if self.ngram_predictor is None:
            raise ValueError("Ngram model not loaded. Cannot perform ZWNJ analysis.")
        
        return self.ngram_predictor.analyze_text(text, window_size)

# Convenience functions for quick usage
def fix_zwnj(text: str, model_path: Optional[Union[str, Path]] = None) -> str:
    """Quick function to fix ZWNJ in text"""
    lutfiy = Lutfiy(model_path)
    return lutfiy.fix_zwnj(text)

def transliterate(text: str) -> str:
    """Quick function to transliterate text"""
    lutfiy = Lutfiy()
    return lutfiy.transliterate(text)

def process_text(text: str, fix_zwnj: bool = True, transliterate: bool = False, 
                model_path: Optional[Union[str, Path]] = None) -> str:
    """Quick function to process text with multiple operations"""
    lutfiy = Lutfiy(model_path)
    return lutfiy.process(text, fix_zwnj, transliterate)