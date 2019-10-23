# coding=utf-8
__author__ = 'Orhan Bilgin'

from subprocess import Popen,PIPE
import zipfile
from codecs import iterdecode

def normalize(word): 
    word = word.replace('İ', 'i').lower().replace('â', 'a').replace('î', 'i').replace('.', '').replace(',', '').replace(';', '')
    word = word.replace(':', '').replace('?', '').replace('!', '').replace('"', '').replace('“', '').replace('”', '')
    word = word.replace('(', '').replace(')', '')
    return word

def isInteger(string):
    if len(string) != 0:
        for char in string:
            if char not in digits:
                return False        
        if string[0] != '0':
            return eval(string)
        else:
            return False
    else:
        return False

def getSemantics(token_mor):
    to_be_added = {}
    for lemma_and_pos, suffix_sequences in token_mor.items():
        if lemma_and_pos in bundled_lemmas:
            sem_classes = bundled_lemmas[lemma_and_pos]
            for sem_class in sem_classes:
                to_be_added[sem_class] = lemma_and_pos

        lemma = lemma_and_pos.split('<')[0]
        pos = '<' + lemma_and_pos.split('<')[1]
        
        # Check membership in number-related semantic classes
        int_value = isInteger(lemma)

        if int_value is not False:
            to_be_added['[Integer]'] = lemma_and_pos
            if int_value >= 1 and int_value <= 31:
                to_be_added['[DayOfMonth]'] = lemma_and_pos
            elif int_value >= 1200 and int_value <= 2200:
                to_be_added['[Year]'] = lemma_and_pos
        
        # Check for membership in morphologically determined semantic classes
        for suffix_sequence in suffix_sequences:             
            if (pos + suffix_sequence).endswith('<Num><ord>'):
                to_be_added['[Ordinal]'] = lemma_and_pos
        
    return to_be_added

def getMorphology(token, morph_db):
    classified_analyses = {}
    if token in morph_db:
        analyses = morph_db[token]
    else:
        p = Popen(flookup, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        p.stdin.write(bytes(token, 'utf-8'))
        analyses = p.communicate()[0].decode('utf-8').split('\n')
    for analysis in analyses:
        if '>' in analysis:
            split_data = analysis.split('>', 1)
            key = split_data[0] + '>'
            # Ignore <cpl:pres> for now
            value = split_data[1].replace('<cpl:pres>', '')
            if key not in classified_analyses:
                classified_analyses[key] = [value]
            elif value not in classified_analyses[key]:
                classified_analyses[key].append(value)
    return classified_analyses

digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

possessives = {
    'kendim': 'kendi+nom', 'kendin': 'kendi+nom', 'kendi': 'kendi+nom', 'kendisi': 'kendi+nom', 'kendimiz': 'kendi+nom', 'kendiniz': 'kendi+nom', 'kendileri': 'kendi+nom',
    'kendimi': 'kendi+acc', 'kendini': 'kendi+acc', 'kendisini': 'kendi+acc', 'kendimizi': 'kendi+acc', 'kendinizi': 'kendi+acc', 'kendilerini': 'kendi+acc',
    'kendime': 'kendi+dat', 'kendine': 'kendi+dat', 'kendisine': 'kendi+dat', 'kendimize': 'kendi+dat', 'kendinize': 'kendi+dat', 'kendilerine': 'kendi+dat',
    'kendimde': 'kendi+loc', 'kendinde': 'kendi+loc', 'kendisinde': 'kendi+loc', 'kendimizde': 'kendi+loc', 'kendinizde': 'kendi+loc', 'kendilerinde': 'kendi+loc',
    'kendimden': 'kendi+abl', 'kendinden': 'kendi+abl', 'kendisinden': 'kendi+abl', 'kendimizden': 'kendi+abl', 'kendinizden': 'kendi+abl', 'kendilerinden': 'kendi+abl',
    'kendimle': 'kendi+ins', 'kendinle': 'kendi+ins', 'kendiyle': 'kendi+ins', 'kendisiyle': 'kendi+ins', 'kendimizle': 'kendi+ins',  'kendinizle': 'kendi+ins',  'kendileriyle': 'kendi+ins',
    'aklıma': 'akıl+dat', 'aklına': 'akıl+dat', 'aklımıza': 'akıl+dat', 'aklınıza': 'akıl+dat', 'akıllarına': 'akıl+dat'
    }

bundled_lemmas = {
    'salise<N>': ['[Time]'], 'saniye<N>': ['[Time]'], 'dakika<N>': ['[Time]'], 'saat<N>': ['[Time]'], 'gün<N>': ['[Time]'], 'hafta<N>': ['[Time]'], 'ay<N>': ['[Time]'], 'yıl<N>': ['[Time]'], 'yüzyıl<N>': ['[Time]'], 'binyıl<N>': ['[Time]'], 'asır<N>': ['[Time]'],
    'orhan<N:prop>': ['[FirstName]'], 'abdurrahman<N:prop>': ['[FirstName]'],
    'eryılmaz<N:prop>': ['[LastName]'], 'yalçınkaya<N:prop>': ['[LastName]'],
    'tsk<N:prop:abbr>': ['[Institution'],
    'ocak<N>': ['[Month]'], 'şubat<N>': ['[Month]'], 'mart<N>': ['[Month]'], 'nisan<N>': ['[Month]'], 'mayıs<N>': ['[Month]'], 'haziran<N>': ['[Month]'], 'temmuz<N>': ['[Month]'], 'ağustos<N>': ['[Month]'], 'eylül<N>': ['[Month]'], 'ekim<N>': ['[Month]'], 'kasım<N>': ['[Month]'], 'aralık<N>': ['[Month]'],
    'milyon<Num>': ['[LargeNumber]'], 'milyar<Num>': ['[LargeNumber]'], 'trilyon<Num>': ['[LargeNumber]'], 'katrilyon<Num>': ['[LargeNumber]'],
    'dolar<N>': ['[Currency]'], 'euro<N>': ['[Currency]'], 'avro<N>': ['[Currency]'], 'lira<N>': ['[Currency]'],
    'bir<Num>': ['[Number]'], 'iki<Num>': ['[Number]'], 'üç<Num>': ['[Number]'], 'dört<Num>': ['[Number]'], 'beş<Num>': ['[Number]'], 'altı<Num>': ['[Number]'], 'yedi<Num>': ['[Number]'], 'sekiz<Num>': ['[Number]'], 'dokuz<Num>': ['[Number]'], 'on<Num>': ['[Number]'], 'yirmi<Num>': ['[Number]'], 'otuz<Num>': ['[Number]'], 'kırk<Num>': ['[Number]'], 'elli<Num>': ['[Number]'], 'altmış<Num>': ['[Number]'], 'yetmiş<Num>': ['[Number]'], 'seksen<Num>': ['[Number]'], 'doksan<Num>': ['[Number]'], 'yüz<Num>': ['[Number]'],
    'do<N>': ['[MusicalNote]'], 're<N>': ['[MusicalNote]'], 'mi<N>': ['[MusicalNote]'], 'fa<N>': ['[MusicalNote]'], 'sol<N>': ['[MusicalNote]'], 'la<N>': ['[MusicalNote]'], 'si<N>': ['[MusicalNote]'], 
    'yüz<N>': ['[BodyPart]'], 'ağız<N>': ['[BodyPart]'], 'kulak<N>': ['[BodyPart]'], 'burun<N>': ['[BodyPart]'], 'ayak<N>': ['[BodyPart]'], 'bacak<N>': ['[BodyPart]']
    }

with open('data/constructicon.txt', 'r', encoding='utf-8') as cxfile:
    constructicon = eval(cxfile.read())

cx_ids = {}

for key, cxs in constructicon.items():
    for cx in cxs:
        cx_ids[cx[0]] = key

# ISSUES
# "tek baş<" cannot identify "tek başlarına".
# Passive marker requires different case marker on subject (x<acc> hastaneye kaldır- vs. x<nom> hastaneye kadırıl-).
# Elements are not always contiguous ("<N><acc> tehdit et-" can be realized as "<N><acc> sürekli olarak ölümle tehdit et-").
# Therefore, construction notation should allow us to specify which elements are contiguous and which are not.
# The output of a construction can be used in other constructions.
# (e.g. "[Integer] [LargeNumber]" is an [Integer] and can be used in the construction "[Integer] [Currency]", which is an NP)
# Sentence must be processed iteratively, until nothing new can be found
# A mechanism should be in place to resolve repetitious / overlapping constructions 


# Initialize morphological analyzer
morphs = {}
flookup = '/usr/bin/flookup -b -x TRmorph-master/trmorph.fst'

zf = zipfile.ZipFile('data/morphs.zip', 'r')

with zf.open('morphs.txt', 'r') as readFile:
    for line in iterdecode(readFile, 'utf8'):
        linedata = line.strip().split('\t')
        try:
            morphs[linedata[0]] = eval(linedata[1])
        except IndexError:
            pass

# Process sentences one by one
with open('data/sentences.txt', 'r', encoding='utf-8') as infile,\
open('data/sentences_log.txt', 'w', encoding='utf-8') as outfile:
    for sentence_id, sentence in enumerate(infile):        
        mwe_log = []
        fully_processed = 0

        # Initialize the three layers of representation
        sur = [normalize(token) for token in sentence.strip().replace('/', ' ').split(' ')]
        mor = [getMorphology(token, morphs) for token in sur]
        sem = [getSemantics(token_mor) for token_mor in mor]

        while fully_processed == 0:
            new_mwes = []

            for focus_position in range(0, len(mor)):
                constructions = []

                # Get potential constructions
                for item in {**mor[focus_position], **sem[focus_position]}:
                    if item in constructicon:
                        for construction in constructicon[item]:
                            constructions.append(construction)
                    if item + '<' in constructicon:
                        for construction in constructicon[item + '<']:
                            constructions.append(construction)
                
                for construction in constructions:
                    construction_id = construction[0]
                    parent_id = construction[1]
                    head_idx = construction[2]
                    syn_output = construction[3]
                    sem_output = construction[4]
                    requirements = construction[5:]
                    focus_lem_or_sem = cx_ids[construction_id]

                    # Get the position of the head
                    if head_idx == 0:
                        head_position = 0
                    elif head_idx is None:
                        head_position = None
                    else:
                        head_position = requirements[head_idx - 1][0]

                    # Check if all obligatory target positions exist (i.e. if sentence can be an instance of the construction)
                    can_be_instance = True

                    for requirement in requirements:
                        # Check obligatory requirements only (ignore optional requirements)
                        if isinstance(requirement, tuple):
                            offset = requirement[0]
                            target_position = focus_position + offset
                            if target_position < 0 or target_position >= len(mor):
                                can_be_instance = False
                                break
                    
                    # Process the construction only if the sentence can be an instance of it
                    if can_be_instance:
                        # Initiate checklist
                        checklist = []

                        for requirement in requirements:
                            # if requirement is obligatory
                            if isinstance(requirement, tuple):
                                checklist.append([False, 0, None, None])
                            # if requirement is optional
                            elif isinstance(requirement, list):
                                checklist.append([None, 0, None, None])

                        # Check requirements one by one
                        for checklist_position, requirement in enumerate(requirements):
                            offset = requirement[0]
                            required_lem_or_sem = requirement[1]
                            required_suffix_sequence = requirement[2]                        
                            target_position = focus_position + offset
                            possible_suffix_sequences = []
                                                        
                            lem_sem_satisfied = 0
                            suffix_sequence_satisfied = 0

                            if required_lem_or_sem is not None:
                                if required_lem_or_sem in mor[target_position]:
                                    lem_sem_satisfied = 1
                                    checklist[checklist_position][1] = offset                                    
                                    checklist[checklist_position][2] = required_lem_or_sem                                    
                                    possible_suffix_sequences = mor[target_position][required_lem_or_sem]

                                elif required_lem_or_sem in sem[target_position]:
                                    lem_sem_satisfied = 1
                                    checklist[checklist_position][1] = offset                                    
                                    checklist[checklist_position][2] = required_lem_or_sem
                                    possible_suffix_sequences = mor[target_position][sem[target_position][required_lem_or_sem]]
                                
                                if required_suffix_sequence is not None:
                                    for possible_suffix_sequence in possible_suffix_sequences:
                                        if possible_suffix_sequence.startswith(required_suffix_sequence):
                                            suffix_sequence_satisfied = 1
                                            checklist[checklist_position][1] = offset                                    
                                            checklist[checklist_position][3] = required_suffix_sequence

                                else:
                                    suffix_sequence_satisfied = 1                            
                                    
                            else:
                                lem_sem_satisfied = 1 
                                possible_suffix_sequences = sum(mor[target_position].values(), [])                        
                            
                                for possible_suffix_sequence in possible_suffix_sequences:
                                    if possible_suffix_sequence.endswith(required_suffix_sequence):
                                        suffix_sequence_satisfied = 1
                                        checklist[checklist_position][1] = offset                                    
                                        checklist[checklist_position][3] = required_suffix_sequence
                            
                            if lem_sem_satisfied == 1 and suffix_sequence_satisfied == 1:
                                checklist[checklist_position][0] = True                                

                        # If all requirements are met, store the identified construction, and modify mor, and sem accordingly
                        if False not in [c[0] for c in checklist] and set([c[0] for c in checklist]) != {None}:
                            new_mwes.append([focus_position, construction_id, checklist])                        
                            
                            # Modify mor and sem
                            if focus_lem_or_sem[-1:] == '<':
                                focus_lem_or_sem = focus_lem_or_sem[:-1]

                            if focus_lem_or_sem[0] != '[':
                                if focus_lem_or_sem[-1:] != '<':
                                    mor[focus_position] = {focus_lem_or_sem: mor[focus_position][focus_lem_or_sem]}
                                else:
                                    mor[focus_position] = {focus_lem_or_sem: ['']}
                                #print('\tmor modified - focus lemma: ' + focus_lem_or_sem + ' - ' + str(mor[focus_position]))

                            else:
                                sem[focus_position] = {focus_lem_or_sem: sem[focus_position][focus_lem_or_sem]}
                                #print('\tsem modified - focus semantic class: ' + focus_lem_or_sem + ' - ' + str(sem[focus_position]))
                                if focus_lem_or_sem[-1:] != '<':
                                    mor[focus_position] = {sem[focus_position][focus_lem_or_sem] : mor[focus_position][sem[focus_position][focus_lem_or_sem]]}
                                else:
                                    mor[focus_position] = {sem[focus_position][focus_lem_or_sem] : ['']}
                                #print('\tmor modified - focus semantic class: ' + focus_lem_or_sem + ' - ' + str(mor[focus_position]))

                            for checklist_item in checklist:
                                status = checklist_item[0]
                                offset = checklist_item[1]
                                target_position = focus_position + offset
                                target_lem_or_sem = checklist_item[2]
                                target_suffix_sequence = checklist_item[3]
                                if status is True:                                    
                                    if target_lem_or_sem is not None:
                                        if target_lem_or_sem[0] != '[':
                                            mor[target_position] = {target_lem_or_sem: mor[target_position][target_lem_or_sem]}
                                            #print('\tmor modified - target lemma: ' + target_lem_or_sem + ' - ' + str(mor[target_position]))
                                        else:
                                            sem[target_position] = {target_lem_or_sem: sem[target_position][target_lem_or_sem]}
                                            #print('\tsem modified - target semantic class: ' + target_lem_or_sem + ' - ' + str(sem[target_position]))
                                            mor[target_position] = {sem[target_position][target_lem_or_sem] : mor[target_position][sem[target_position][target_lem_or_sem]]}
                                            #print('\tmor modified - target semantic class: ' + target_lem_or_sem + ' - ' + str(mor[target_position]))

                                        if target_suffix_sequence is not None:
                                            surviving_items = {}
                                            # Include special case for -(s)I suffix
                                            if target_suffix_sequence == '<p3':
                                                extended_target_suffix_sequence = ('<p3s>', '<p3p>')
                                            for potential_lemma, potential_suffix_sequences in mor[target_position].items():
                                                for potential_suffix_sequence in potential_suffix_sequences:
                                                    if potential_suffix_sequence.startswith(extended_target_suffix_sequence):
                                                        if potential_lemma not in surviving_items:
                                                            surviving_items[potential_lemma] = [potential_suffix_sequence]
                                                        else:
                                                            surviving_items[potential_lemma].append(potential_suffix_sequence)
                                            mor[target_position] = surviving_items
                                            #print('\tmor modified - target suffix sequence: ' + target_suffix_sequence + ' - ' + str(mor[target_position]))
                                    
                                    else:
                                        surviving_items = {}
                                        for potential_lemma, potential_suffix_sequences in mor[target_position].items():
                                            for potential_suffix_sequence in potential_suffix_sequences:
                                                if potential_suffix_sequence.endswith(target_suffix_sequence):
                                                    if potential_lemma not in surviving_items:
                                                        surviving_items[potential_lemma] = [potential_suffix_sequence]
                                                    else:
                                                        surviving_items[potential_lemma].append(potential_suffix_sequence)
                                        mor[target_position] = surviving_items
                                        #print('\tmor modified - target suffix sequence: ' + target_suffix_sequence + ' - ' + str(mor[target_position]))                            
                                    
                                    print('Multiword expression identified in Sentence ' + str(sentence_id))
                                    print('Sentence: ' + sentence.strip())
                                    print('Target token position: ' + str(target_position) + '- Target token: ' + sur[target_position])
                                    print('Morphology: ' + str(mor[target_position]))
                                    print('Semantics: ' + str(sem[target_position]))
                            print('Focus token position: ' + str(focus_position) + '- Focus token: ' + str(sur[focus_position]))
                            print('Morphology: ' + str(mor[focus_position]))
                            print('Semantics: ' + str(sem[focus_position]))
                            print('Syntactic output: ' + str(syn_output))
                            print('Syntactic head position: ' + str(head_position))
                            print('Semantic output: ' + str(sem_output))
                            print('\n')

                            # TBD: Merge mor and sem entries to reflect the construction that has been identified
            
            if len(new_mwes) == 0:
                fully_processed = 1
            else:
                mwe_log.append(new_mwes)
                #print(new_mwes)

            fully_processed = 1

            #print(mor)
            #print(sem)