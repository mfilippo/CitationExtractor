# The CRF++ template for the baseline
# with only lexical features

#unigram
U01:%x[-2,0]
U02:%x[-1,0]
U03:%x[0,0]
U04:%x[1,0]
U05:%x[2,0]

# unigrams within context
U06:%x[-2,0]/%x[-1,0]/%x[0,0]
U07:%x[-1,0]/%x[0,0]/%x[1,0]
U08:%x[0,0]/%x[1,0]/%x[2,0]