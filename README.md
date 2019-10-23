# mwe_identifier

This is a proof-of-concept version of a multiword-expression identifier for Turkish, designed with a "Construction Grammar" framework in mind. For an early description of Construction Grammar, see Fried, M., & Östman, J. O. (2004). Construction Grammar: A thumbnail sketch. Construction Grammar in a cross-language perspective, 11-86.

The identifier processes the Turkish sentences in data/sentences.txt (UTF-8) and marks any multiword expressions / constructions described in data/constructicon.txt (UTF-8). For faster processing, data/morphs.zip contains the morphological analyses of all tokens in sentences.txt. The Turkish morphological analyzer developed by Çağrı Çöltekin must be installed in the directory named TRmorph-master.

The identifier processes the sentences token by token. Every token has three layers of representation: Surface layer, morphological layer, and semantic layer. A multiword expression is identified whenever a sequence of word-forms, lemmas or suffixes in a sentence matches all requirements of a construction described in the constructicon. Constructions can be described using the surface and/or morphology and/or semantics layers. Iterative identification has not been fully implemented yet.  

Sample constructicon entries:

'[Number]':
    [
        [992, None, 1, '<Adj>', '[Number]', (1, '[LargeNumber]', None)]
    ]
    
Construction 992 states that, whenever a surface form that has the semantic tag [Number] is followed (at Position +1) by a surface form that has the semantic tag [LargeNumber], the two surface forms constitute a multiword expression that has the semantic tag [Number] and the syntactic category <Adj>. Sequences like beş milyon 'five million', 340 milyar '340 billion' would be identified as instances of this construction.

'her<Det:def>':
    [
        [997, None, 1, '<Adv>', None, (1, 'zaman<N>', None )
    ]
    
Construction 997 states that, whenever the surface form "her", which has the part-of-speech tag <Det:def>, is followed (at Position +1) by the surface form "zaman", which has the part-of-speech tag <N>, the two surface forms constitute a multiword expression that has the part of speech <Adv>. In other words, the sequence her zaman 'always' is a multiword adverb in Turkish. 






