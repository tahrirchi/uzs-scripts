# Lutfiy - Southern Uzbek Text Processing

A Python library for processing Southern Uzbek text, including transliteration and ZWNJ correction.

## Installation

```bash
pip install lutfiy
```

## Quick Start

```python
from lutfiy import fix_zwnj, transliterate

# Fix ZWNJ placement
text = 'اۉزبېکستان کېلهجگی بویوک دولت دیر.'
corrected = fix_zwnj(text)

# Transliterate to Latin
latin = transliterate(text)
```

## Advanced Usage

```python
from lutfiy import Lutfiy

# Initialize processor
processor = Lutfiy()

# Process with multiple operations
result = processor.process(
    text='اۉزبېکستان کېلهجگی بویوک دولت دیر.',
    fix_zwnj=True,
    transliterate=True
)
```