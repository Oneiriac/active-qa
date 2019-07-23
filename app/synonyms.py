import math
from typing import Iterable, Tuple, List, Dict
from collections import defaultdict
import spacy
from pattern.text.en import conjugate, pluralize
from spacy.tokens import Token

from spacy_wordnet.wordnet_annotator import WordnetAnnotator

university_domains = (
    'university',
    'student',
    'college',
    'education',
    'parking',
    'fees',
    'course',
    'faculty',
    'teacher',
    'campus',
    'permit',
    'cycling',
    'law',
)

allowed_pos = {'ADJ', 'NOUN', 'NUM', 'VERB'}

excluded_lemmas = {'be', 'have', ''}

sample_questions = [
    "Where can I find parking with a blue parking permit?",
    "How do I lodge a complaint about a staff member?",
    "Where is Monash University?",
    "Is it possible to buy a blue parking permit as a student?"
]


class SuggestionEngine:
    def __init__(self, spacy_model: str = 'en_core_web_sm', domains: Iterable[str] = university_domains):
        self.nlp = spacy.load(spacy_model)
        self.nlp.add_pipe(WordnetAnnotator(self.nlp.lang), after='tagger')
        self.domains = set(domains)

    def suggest_synonyms(self, text: str) -> str:
        sentence = self.nlp(text)
        enriched_sentence = []
        print(sentence.ents)
        for token in sentence:
            print(token, token.pos_, token.dep_)
            # We get those synsets within the desired domains
            synsets = token._.wordnet.wordnet_synsets_for_domain(self.domains)
            if synsets \
                    and token.pos_ in allowed_pos \
                    and token.dep_ != 'aux' \
                    and not (token.dep_ == 'ROOT' and self.subj_verb_inversion(token)):  # TODO: Disable synonyms for inverted auxiliaries / copulas: REVISIT THIS
                synonyms = defaultdict(int)
                synonyms[token.text] = float("inf")  # Value = frequency: will order (descending) by frequency
                for s in synsets:
                    for l in s.lemmas():
                        fixed_lemma = l.name().replace('_', ' ')
                        count = l.count()
                        if count > synonyms[fixed_lemma]:
                            synonyms[fixed_lemma] = count

                if token.pos_ == 'VERB':
                    synonyms = {conjugate(stem, tense=token.tag_): count for stem, count in synonyms.items()}

                sorted_synonyms = [kv[0] for kv in sorted(synonyms.items(), key=lambda kv: kv[1], reverse=True)]
                enriched_sentence.append('({})'.format('|'.join(sorted_synonyms)))
            else:
                enriched_sentence.append(token.text)
        return " ".join(enriched_sentence)

    @staticmethod
    def subj_verb_inversion(verb: Token) -> bool:
        """
        Check whether subject-verb inversion has occurred.
        :param verb: the verb Token which may have been inverted (not necessarily the root of the dependency tree).
        :return:
        """
        for r_child in verb.rights:
            if 'subj' in r_child.dep_:
                return True
        return False


def main():
    engine = SuggestionEngine(spacy_model='en_core_web_sm')
    for q in sample_questions:
        print(engine.suggest_synonyms(q))
        print('='*20)


if __name__ == "__main__":
    main()
