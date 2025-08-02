import math
import re
from collections import Counter

def shannon_entropy(text):
    """Calculate Shannon entropy of text"""
    if not text:
        return 0
    
    freq = {}
    for char in text:
        freq[char] = freq.get(char, 0) + 1
    
    total = len(text)
    entropy = 0
    for count in freq.values():
        probability = count / total
        entropy -= probability * math.log2(probability)
    
    return entropy

def index_of_coincidence(text):
    """Calculate Index of Coincidence"""
    text = ''.join([c for c in text.upper() if c.isalpha()])
    n = len(text)
    freqs = Counter(text)
    if n <= 1: 
        return 0
    return sum(f*(f-1) for f in freqs.values()) / (n*(n-1))

# English letter frequency distribution
english_freq = {
    'A':8.2,'B':1.5,'C':2.8,'D':4.3,'E':12.7,'F':2.2,'G':2.0,'H':6.1,'I':7.0,'J':0.2,
    'K':0.8,'L':4.0,'M':2.4,'N':6.7,'O':7.5,'P':1.9,'Q':0.1,'R':6.0,'S':6.3,'T':9.1,
    'U':2.8,'V':1.0,'W':2.4,'X':0.2,'Y':2.0,'Z':0.1
}

def chi_square_score(text):
    """Calculate Chi-square statistic against English letter frequencies"""
    text = ''.join([c for c in text.upper() if c.isalpha()])
    total = len(text)
    freq = Counter(text)
    score = 0
    for letter, exp in english_freq.items():
        obs = (freq.get(letter.upper(), 0) / total) * 100 if total > 0 else 0
        score += (obs - exp)**2 / exp
    return score

def extract_features(ciphertext):
    """Extract comprehensive features from ciphertext for ML prediction"""
    if not ciphertext:
        return [0, 0, 0, 0, 0, 0, 0]
    
    # Advanced features
    length = len(ciphertext)
    alpha_ratio = sum(c.isalpha() for c in ciphertext) / length if length else 0
    digit_ratio = sum(c.isdigit() for c in ciphertext) / length if length else 0
    symbol_ratio = sum(not c.isalnum() for c in ciphertext) / length if length else 0
    entropy = shannon_entropy(ciphertext)
    ic = index_of_coincidence(ciphertext)
    chi = chi_square_score(ciphertext)
    
    return [length, alpha_ratio, digit_ratio, symbol_ratio, entropy, ic, chi] 