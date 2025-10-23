import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string

class TextPreprocessor:
    def __init__(self):
        # Download required NLTK data if not present
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt', quiet=True)
        
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords', quiet=True)
        
        self.stop_words = set(stopwords.words('english'))
        self.custom_stop_words = {
            'resume', 'cv', 'curriculum', 'vitae', 'page', 'email', 'phone', 
            'mobile', 'tel', 'address', 'linkedin', 'github', 'portfolio'
        }
        
        # Combine standard and custom stop words
        self.all_stop_words = self.stop_words.union(self.custom_stop_words)
    
    def clean_text(self, text):
        """Clean and normalize text"""
        if not text or not isinstance(text, str):
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        
        # Remove phone numbers
        text = re.sub(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]', '', text)
        
        # Remove special characters but keep basic punctuation for sentence detection
        text = re.sub(r'[^\w\s\.\,\!\\?]', '', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def tokenize_text(self, text):
        """Tokenize text into words"""
        try:
            return word_tokenize(text)
        except Exception as e:
            print(f"Tokenization error: {e}")
            return text.split()  # Fallback to simple split
    
    def remove_stopwords(self, tokens):
        """Remove stopwords from token list"""
        return [token for token in tokens if token not in self.all_stop_words]
    
    def preprocess(self, text):
        """Complete preprocessing pipeline"""
        try:
            # Clean text
            cleaned_text = self.clean_text(text)
            
            # Tokenize
            tokens = self.tokenize_text(cleaned_text)
            
            # Remove stopwords
            filtered_tokens = self.remove_stopwords(tokens)
            
            return ' '.join(filtered_tokens)
            
        except Exception as e:
            print(f"Preprocessing error: {e}")
            return text  # Return original text if preprocessing fails
    
    def extract_sentences(self, text):
        """Extract sentences from text"""
        try:
            # Simple sentence splitting
            sentences = re.split(r'[.!?]+', text)
            return [sentence.strip() for sentence in sentences if sentence.strip()]
        except Exception as e:
            print(f"Sentence extraction error: {e}")
            return [text]
    
    def extract_paragraphs(self, text):
        """Extract paragraphs from text"""
        try:
            paragraphs = text.split('\n\n')
            return [para.strip() for para in paragraphs if para.strip()]
        except Exception as e:
            print(f"Paragraph extraction error: {e}")
            return [text]
    
    def calculate_readability_score(self, text):
        """Calculate basic readability score"""
        try:
            sentences = self.extract_sentences(text)
            words = self.tokenize_text(text)
            
            if len(sentences) == 0 or len(words) == 0:
                return 0
            
            # Average sentence length
            avg_sentence_length = len(words) / len(sentences)
            
            # Simple readability score (lower = more complex)
            readability_score = avg_sentence_length
            
            return min(readability_score, 50)  # Cap at 50
            
        except Exception as e:
            print(f"Readability calculation error: {e}")
            return 0

# Test the preprocessor
if __name__ == "__main__":
    print("🧪 Testing Text Preprocessor...")
    
    preprocessor = TextPreprocessor()
    
    # Test with sample text
    sample_text = """
    John Doe is a Senior Software Engineer with 5 years of experience.
    He specializes in Python development and machine learning.
    Email: john.doe@email.com
    Phone: (555) 123-4567
    """
    
    processed_text = preprocessor.preprocess(sample_text)
    sentences = preprocessor.extract_sentences(sample_text)
    readability = preprocessor.calculate_readability_score(sample_text)
    
    print("✅ Preprocessor tested successfully!")
    print(f"Original: {sample_text[:100]}...")
    print(f"Processed: {processed_text[:100]}...")
    print(f"Sentences: {len(sentences)}")
    print(f"Readability Score: {readability:.2f}")