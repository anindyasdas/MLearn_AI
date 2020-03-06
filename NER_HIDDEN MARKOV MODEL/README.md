#######################HMM without LIBRARY####################################################3
Named-entity recognition (NER) seeks to locate and classify named entities in text
into predefined categories such as the names of persons, organizations, locations
etc.
Design a named entity recognition system for Twitter that identifies the presence of
named entities in a tweet.
Input: A tokenized sentence.
Output: NER tags for each token of the sentence.
Setups:
1. Identify all the named entity, i.e., whether a token is a named entity or not.
2. First identify all the named entity and then find the types of each name entity.
3. Identify the named entity types in one step.
Approach: Solve the problem of NER through following approaches and compare
their performances.
● Hidden Markov Model (HMM)
HMM implementation from scratch. Calculate emission and transition probabilities and use Viterbi
to get the NER sequence.
Crosvalidation is used size 3
