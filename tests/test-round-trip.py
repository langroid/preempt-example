"""
Run like this:
    uv run tests/test-round-trip.py
"""

import langroid as lr
import langroid.language_models as lm
from preempt.ner import *
from preempt.sanitizer import *


# Load NER object
# ner_model = NER("/path/to/UniNER-7B-all", device="cuda:1")
ner_model = NER("/path/to/Meta-Llama-3-8B-Instruct/", device="cuda:1")

# Load Sanitizer objects for name and money
sanitizer_name = Sanitizer(ner_model, key = "EF4359D8D580AA4F7F036D6F04FC6A94", tweak = "D8E7920AFA330A73")
sanitizer_money = Sanitizer(ner_model, key = "FF4359D8D580AA4F7F036D6F04FC6A94", tweak = "E8E7920AFA330A73")

# Sentences
sentences = [
    "Ben Parker and John Doe went to the bank and withdrew $200.", 
    "Adam won $20 in the lottery."
]


# Sanitizing names
sanitized_sentences, _ = sanitizer_name.encrypt(
    sentences, 
    entity='Name', 
    epsilon=1,
)
print("Sanitized sentences:")
print(sanitized_sentences)
"""
Prints:

Sanitized sentences:
['Jay Francois and Lamine Franklin went to the bank and withdrew $200.', 'Elie Vinod won $20 in the lottery.']
"""

# Sanitizing currency values
sanitized_sentences, _ = sanitizer_money.encrypt(
    sanitized_sentences, 
    entity='Money', 
    epsilon=1,
)
print("Sanitized sentences:")
print(sanitized_sentences)
"""
Prints:

Sanitized sentences:
['Jay Francois and Lamine Franklin went to the bank and withdrew $769451698.', 'Elie Vinod won $37083668 in the lottery.']
"""

# Desanitizing names
desanitized_sentences = sanitizer_name.decrypt(sanitized_sentences, entity='Name', use_cache=True)
print("Desanitized sentences:")
print(desanitized_sentences)

"""
Prints:

Desanitized sentences:
['Ben Parker and John Doe went to the bank and withdrew $769451698.', 'Adam won $37083668 in the lottery.']
"""

# Desanitizing currency values
desanitized_sentences = sanitizer_money.decrypt(desanitized_sentences, entity='Money', use_cache=True)
print("Desanitized sentences:")
print(desanitized_sentences)
"""
Prints:

Desanitized sentences:
['Ben Parker and John Doe went to the bank and withdrew $200.', 'Adam won $20 in the lottery.']
"""

assert desanitized_sentences == sentences