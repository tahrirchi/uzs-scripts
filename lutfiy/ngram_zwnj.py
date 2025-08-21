import re
import math
import pickle
from collections import defaultdict
from typing import List, Dict, Optional, Union
from pathlib import Path

class GenericNGramPredictor:
    def __init__(self, n=4, model_path: Optional[Union[str, Path]] = None):
        self.n = n  # n-gram size
        self.ngram_counts = defaultdict(int)
        self.context_counts = defaultdict(int)
        self.vocab = set()
        self.smoothing = 1e-6  # Laplace smoothing
        self.total_ngrams = 0
        self.is_trained = False
        
        # Load model if path is provided
        if model_path is not None:
            self.load_model(model_path)
    
    @classmethod
    def from_file(cls, model_path: Union[str, Path]) -> 'GenericNGramPredictor':
        """
        Create a GenericNGramPredictor instance from a saved model file
        
        Args:
            model_path: Path to the saved model file
            
        Returns:
            GenericNGramPredictor instance with loaded model
        """
        instance = cls()
        instance.load_model(model_path)
        return instance
    
    # @classmethod
    # def from_default_model(cls) -> 'GenericNGramPredictor':
    #     """
    #     Create a GenericNGramPredictor instance using the default bundled model
        
    #     Returns:
    #         GenericNGramPredictor instance with default model
    #     """
    #     # Get the default model path relative to this file
    #     default_model_path = Path(__file__).parent.parent / "files" / "ngram_predictor.pkl"
        
    #     if not default_model_path.exists():
    #         raise FileNotFoundError(
    #             f"Default model not found at {default_model_path}. "
    #             "Please ensure the model file is included in the package."
    #         )
        
    #     return cls.from_file(default_model_path)

    # In lutfiy/ngram_zwnj.py, update the from_default_model method:

    @classmethod
    def from_default_model(cls) -> 'GenericNGramPredictor':
        """
        Create a GenericNGramPredictor instance using the default bundled model
        
        Returns:
            GenericNGramPredictor instance with default model
        """
        # Get the model path relative to this module
        model_path = Path(__file__).parent / "files" / "ngram_predictor.pkl"
        
        if not model_path.exists():
            raise FileNotFoundError(
                f"Default model not found at {model_path}. "
                "Please ensure the model file is included in the package."
            )
        
        return cls.from_file(model_path)
    
    def load_model(self, model_path: Union[str, Path]):
        """
        Load a trained model from file
        
        Args:
            model_path: Path to the model file
        """
        model_path = Path(model_path)
        
        if not model_path.exists():
            raise FileNotFoundError(f"Model file not found: {model_path}")
        
        try:
            with open(model_path, "rb") as f:
                loaded_model = pickle.load(f)
            
            # Copy attributes from loaded model
            if isinstance(loaded_model, GenericNGramPredictor):
                self.n = loaded_model.n
                self.ngram_counts = loaded_model.ngram_counts
                self.context_counts = loaded_model.context_counts
                self.vocab = loaded_model.vocab
                self.smoothing = loaded_model.smoothing
                self.total_ngrams = loaded_model.total_ngrams
                self.is_trained = True
                # print(f"Successfully loaded model from {model_path}")
                # print(f"Model info: n={self.n}, vocab_size={len(self.vocab)}, total_ngrams={self.total_ngrams}")
            else:
                raise ValueError("Loaded object is not a GenericNGramPredictor instance")
                
        except Exception as e:
            raise ValueError(f"Error loading model from {model_path}: {e}")
    
    def save_model(self, model_path: Union[str, Path]):
        """
        Save the trained model to file
        
        Args:
            model_path: Path where to save the model
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before saving")
        
        model_path = Path(model_path)
        model_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(model_path, "wb") as f:
                pickle.dump(self, f)
            print(f"Model saved to {model_path}")
        except Exception as e:
            raise ValueError(f"Error saving model to {model_path}: {e}")
        
    def train(self, texts: List[str]):
        """Train the model on a list of texts"""
        print("Training model...")
        
        # Reset counters
        self.ngram_counts = defaultdict(int)
        self.context_counts = defaultdict(int)
        self.vocab = set()
        self.total_ngrams = 0
        
        for text in texts:
            # Clean text (remove extra whitespaces, normalize)
            text = re.sub(r'\s+', ' ', text.strip())
            
            # Extract all n-grams from text
            for i in range(len(text) - self.n + 1):
                ngram = text[i:i + self.n]
                self.ngram_counts[ngram] += 1
                self.total_ngrams += 1
                
                # Update vocabulary
                for char in ngram:
                    self.vocab.add(char)
                
                # Count context for conditional probability
                if self.n > 1:
                    context = ngram[:-1]
                    self.context_counts[context] += 1
        
        self.is_trained = True
        print(f"Training completed. Vocabulary size: {len(self.vocab)}")
        print(f"Total n-grams: {self.total_ngrams}")
        print(f"Unique n-grams: {len(self.ngram_counts)}")
    
    def get_ngram_probability(self, ngram: str, given_context: Optional[str] = None) -> float:
        """
        Calculate probability of n-gram
        If given_context is provided, calculates conditional probability P(last_char | context)
        Otherwise calculates joint probability P(ngram)
        """
        if not self.is_trained:
            raise ValueError("Model must be trained or loaded before use")
            
        if given_context is not None:
            # Conditional probability P(last_char | context)
            context_count = self.context_counts[given_context]
            ngram_count = self.ngram_counts[ngram]
            
            if context_count == 0:
                # Use unigram probability as fallback
                vocab_size = len(self.vocab)
                return (ngram_count + self.smoothing) / (self.total_ngrams + self.smoothing * vocab_size)
            
            # Apply Laplace smoothing
            vocab_size = len(self.vocab)
            return (ngram_count + self.smoothing) / (context_count + self.smoothing * vocab_size)
        else:
            # Joint probability P(ngram)
            vocab_size = len(self.vocab) ** self.n
            return (self.ngram_counts[ngram] + self.smoothing) / (self.total_ngrams + self.smoothing * vocab_size)
    
    def get_sequence_score(self, text: str, start_pos: int, window_size: int) -> float:
        """
        Get probability score for a sequence starting at start_pos with given window_size
        Uses sliding window of n-grams within the specified window
        """
        if not self.is_trained:
            raise ValueError("Model must be trained or loaded before use")
            
        end_pos = min(start_pos + window_size, len(text))
        sequence = text[start_pos:end_pos]
        
        if len(sequence) < self.n:
            # For sequences shorter than n, use what we have
            return self.get_ngram_probability(sequence)
        
        total_log_prob = 0
        count = 0
        
        # Extract all n-grams from the sequence
        for i in range(len(sequence) - self.n + 1):
            ngram = sequence[i:i + self.n]
            context = ngram[:-1]
            prob = self.get_ngram_probability(ngram, context)
            total_log_prob += math.log(prob)
            count += 1
        
        if count == 0:
            return self.smoothing
        
        return math.exp(total_log_prob / count)
    
    def decide_after_heh(self, text: str, heh_pos: int, window_size: int = None) -> Dict[str, float]:
        """
        Given position of ه, decide what to do next:
        1. Leave as is (no change)
        2. Insert ZWNJ after ه
        3. Replace space after ه with ZWNJ (if there's a space)
        
        Returns scores for each option
        """
        if not self.is_trained:
            raise ValueError("Model must be trained or loaded before use")
            
        if window_size is None:
            window_size = self.n * 2  # Default window size
        
        zwnj = '\u200c'
        options = {}
        
        # Option 1: Leave as is (no change)
        original_score = self.get_sequence_score(text, heh_pos, window_size)
        options['no_change'] = original_score
        
        # Option 2: Insert ZWNJ after ه
        if heh_pos + 1 <= len(text):
            text_with_zwnj = text[:heh_pos + 1] + zwnj + text[heh_pos + 1:]
            zwnj_score = self.get_sequence_score(text_with_zwnj, heh_pos, window_size + 1)
            options['insert_zwnj'] = zwnj_score
        
        # Option 3: Replace space with ZWNJ (if there's a space after ه)
        if (heh_pos + 1 < len(text) and text[heh_pos + 1] == ' '):
            text_replace_space = text[:heh_pos + 1] + zwnj + text[heh_pos + 2:]
            space_replace_score = self.get_sequence_score(text_replace_space, heh_pos, window_size)
            options['replace_space_with_zwnj'] = space_replace_score
        
        return options
    
    def process_text(self, text: str, window_size: int = None) -> str:
        """
        Process entire text and apply best decisions for each ه
        """
        if not self.is_trained:
            raise ValueError("Model must be trained or loaded before use")
            
        if window_size is None:
            window_size = self.n * 2
        
        zwnj = '\u200c'
        result = list(text)  # Work with list for easier manipulation
        offset = 0  # Track position changes due to insertions
        
        # Find all positions of ه
        heh_positions = [i for i, char in enumerate(text) if char == 'ه']
        
        for original_pos in heh_positions:
            current_pos = original_pos + offset
            current_text = ''.join(result)
            
            # Get scores for different options
            options = self.decide_after_heh(current_text, current_pos, window_size)
            
            # Find best option
            best_option = max(options.keys(), key=lambda k: options[k])
            
            # Apply the best option
            if best_option == 'insert_zwnj':
                result.insert(current_pos + 1, zwnj)
                offset += 1
            elif best_option == 'replace_space_with_zwnj':
                if current_pos + 1 < len(result) and result[current_pos + 1] == ' ':
                    result[current_pos + 1] = zwnj
            # For 'no_change', do nothing
        
        return ''.join(result)
    
    def analyze_text(self, text: str, window_size: int = None) -> List[Dict]:
        """
        Analyze text and return detailed information about each ه decision
        """
        if not self.is_trained:
            raise ValueError("Model must be trained or loaded before use")
            
        if window_size is None:
            window_size = self.n * 2
        
        results = []
        heh_positions = [i for i, char in enumerate(text) if char == 'ه']
        
        for pos in heh_positions:
            options = self.decide_after_heh(text, pos, window_size)
            best_option = max(options.keys(), key=lambda k: options[k])
            
            # Get context around ه for display
            start_context = max(0, pos - 5)
            end_context = min(len(text), pos + 6)
            context = text[start_context:end_context]
            
            results.append({
                'position': pos,
                'context': context,
                'options': options,
                'best_option': best_option,
                'confidence': options[best_option] / sum(options.values()) if sum(options.values()) > 0 else 0
            })
        
        return results

# Example usage
if __name__ == "__main__":
    # Example 1: Load from default model
    try:
        predictor = GenericNGramPredictor.from_default_model()
        result = predictor.process_text('اۉزبېکستان کېلهجگی بویوک دولت دیر.')
        print(f"Result: {result}")
    except FileNotFoundError as e:
        print(f"Default model not found: {e}")
    
    # Example 2: Load from custom path
    # predictor = GenericNGramPredictor.from_file("path/to/your/model.pkl")
    
    # Example 3: Train new model
    # training_texts = ["your", "training", "data"]
    # predictor = GenericNGramPredictor(n=4)
    # predictor.train(training_texts)
    # predictor.save_model("new_model.pkl")