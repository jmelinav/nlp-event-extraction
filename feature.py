import random
import re
from ConstructGenderDict import getGenderNouns,get_emotion_words,getCollectiveNouns,getAbstractNouns

PUNCTUATION = ["-LRB-", "-RRB-", "$", "#", "``", "''", ",", ".", ":", "SYM"]
GENDER_ROLES_STR = "GENDER_ROLES"
EMOTIONS_STR = "EMOTIONS"
COLLECTIVE_NOUNS_STR="COLLECTIVE_NOUNS"
ABSTRACT_NOUNS_STR="ABSTRACT_NOUNS"

# Yahya///0-5///PERSON///NNP///1 -> word///index-index///NER///POS///arg
PATTERN = re.compile(r"(.+?)///(\d+-\d+)///(.+?)///(.+?)///(.+?)")

class Feature:
    def __init__(self, word_dictionary, entity_type_dictionary, window_size=10):
        self.word_dictionary = word_dictionary
        self.unknow_index = 0
        self.zero_index = 0

        self.entity_type_dictionary = entity_type_dictionary
        self.window_size = window_size

    def word_2_index(self, word):
        return self.word_dictionary.get(word.lower(), self.unknow_index)

    def words_2_index(self, words):
        indexs = [
            self.word_dictionary.get(word.lower(), self.unknow_index) 
                if word is not None 
                else self.zero_index
            for word in words
        ]
        return indexs

    def entities_2_index(self, entities):
        indexs = [
            self.entity_type_dictionary.get(entity, 0)
            for entity in entities
        ]
        return indexs 

    def context_word_feature(self, sent_info):
        tokens = sent_info["tokens"]
        trigger_word = sent_info["trigger_word"]
        if trigger_word is not None:
            trigger_word_index = trigger_word[2]
            category = trigger_word[1][:-8]
        else:
            trigger_word_index = random.randint(0, len(tokens)-1)
            category = "none"
        context_word = [
            tokens[i].split('///')[0] if 0 <= i < len(tokens) else None
            for i in range(trigger_word_index-self.window_size, trigger_word_index+self.window_size+1)
                if i != trigger_word_index
        ]
        context_index = self.words_2_index(context_word)
        target_word_index = self.word_2_index(tokens[trigger_word_index].split('///')[0])

        return target_word_index, context_index, category

    def context_word_and_entity_feature(self, sent_info):
        tokens = sent_info["tokens"]
        trigger_word = sent_info["trigger_word"]
        if trigger_word is not None:
            trigger_word_index = trigger_word[2]
            category = trigger_word[1][:-8]
        else:
            trigger_word_index = random.randint(0, len(tokens)-1)
            category = "none"
        context_word = [
            tokens[i].split('///')[0] if 0 <= i < len(tokens) else None
            for i in range(trigger_word_index-self.window_size, trigger_word_index+self.window_size+1)
                if i != trigger_word_index
        ]
        context_index = self.words_2_index(context_word)
        target_word_index = self.word_2_index(tokens[trigger_word_index].split('///')[0])
        entities = [
            tokens[i].split('///')[2] if 0 <= i < len(tokens) else None
            for i in range(trigger_word_index-self.window_size, trigger_word_index+self.window_size+1)
                if i != trigger_word_index
        ]
        entity_index = self.entities_2_index(entities)

        return target_word_index, context_index, entity_index, category
    
    # remove puntuation?
    def all_context_word_and_entity_feature(self, sent_info, negative=True):
        gender_dict = getGenderNouns()
        emotion_dict= get_emotion_words()
        collective_noun_dict = getCollectiveNouns()
        abstract_nouns = getAbstractNouns()
        try:
            tokens = [PATTERN.match(token).groups() for token in sent_info["tokens"]]
        except AttributeError as e:
            print(e)
            from pprint import pprint
            pprint(sent_info)
            quit()
        trigger_word = sent_info["trigger_word"]
        trigger_word_index = trigger_word[2] if trigger_word is not None else None
        split = sent_info["split"]
        if trigger_word is None:
            return None

        result = []
        for index, token in enumerate(tokens):
            if token[3] in PUNCTUATION: 
                continue
            else:
                category = "none" if trigger_word_index is None or index != trigger_word_index else trigger_word[1]
                target_word_index = self.word_2_index(token[0])
                context_word = [
                    tokens[i][0] if 0 <= i < len(tokens) else None
                    for i in range(index-self.window_size, index+self.window_size+1)
                        if i != index
                ]
                context_index = self.words_2_index(context_word)

                entities =[]
                for i in range(index - self.window_size, index + self.window_size + 1):
                    if i != index:
                        if 0 <= i < len(tokens):
                            self.add_feature(entities, gender_dict,emotion_dict,collective_noun_dict,abstract_nouns, i, tokens)
                        else:
                            entities.append(None)



                # entities = [
                #     tokens[i][2] if 0 <= i < len(tokens) else None
                #     for i in range(index-self.window_size, index+self.window_size+1)
                #         if i != index
                # ]
                entity_index = self.entities_2_index(entities)
                arguments = [
                    int(tokens[i][4]) if 0 <= i < len(tokens) else 0
                    for i in range(index-self.window_size, index+self.window_size+1)
                        if i != index
                ]
                result.append((
                    target_word_index, 
                    context_index, 
                    entity_index, 
                    category,
                    arguments,
                    split,
                ))

        return result

    def add_feature(self, entities, gender_dict,emotion_dict,collective_noun_dict ,abstract_noun_dict,i, tokens):
        flag = False
        if tokens[i][2] == 'O':
            current_word = tokens[i][0].lower()
            if GENDER_ROLES_STR in self.entity_type_dictionary and current_word in gender_dict:
                entities.append(GENDER_ROLES_STR)
                flag = True
            elif EMOTIONS_STR in self.entity_type_dictionary and current_word in emotion_dict:
                entities.append(EMOTIONS_STR)
                flag = True
            elif ABSTRACT_NOUNS_STR in self.entity_type_dictionary and current_word in abstract_noun_dict:
                entities.append(ABSTRACT_NOUNS_STR)
                flag = True
            elif COLLECTIVE_NOUNS_STR in self.entity_type_dictionary and current_word in collective_noun_dict:

                next_two_words = collective_noun_dict[current_word]
                str =""
                for j in range(i+1,i+3):
                    if(j<len(tokens)):
                        str=str+tokens[j][0]+'_'
                if str[:-1].lower() in next_two_words:
                    flag = True
                    entities.append(COLLECTIVE_NOUNS_STR)
                    #exit(0)


            if not flag:
                entities.append(tokens[i][2])
            # print(entities)
            # exit(0)
        else:
            entities.append(tokens[i][2])



