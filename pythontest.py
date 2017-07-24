import nltk
from nltk import sentiment
from collections import defaultdict
from spacy.parts_of_speech import ADJ, ADV, NOUN, VERB
#import textacy
import spacy

#from textacy import data

str = "and the next second, Harry felt Quirrell's hand close on his wrist. At once, a needle-sharp pain seared across Harry's scar; his head felt as though it was about to split in two; he yelled, struggling with all his might, and to his surprise, Quirrell let go of him. The pain in his head lessened -- he looked around wildly to see where Quirrell had gone, and saw him hunched in pain, looking at his fingers -- they were blistering before his eyes."

str2 = "Even Harry, who knew nothing about the different brooms, thought it looked wonderful. Sleek and shiny, with a mahogany handle, it had a long tail of neat, straight twigs and Nimbus Two Thousand written in gold near the top. As seven o'clock drew nearer, Harry left the castle and set off in the dusk toward the Quidditch field. Held never been inside the stadium before. Hundreds of seats were raised in stands around the field so that the spectators were high enough to see what was going on. At either end of the field were three golden poles with hoops on the end. They reminded Harry of the little plastic sticks Muggle children blew bubbles through, except that they were fifty feet high. Too eager to fly again to wait for Wood, Harry mounted his broomstick and kicked off from the ground. What a feeling -- he swooped in and out of the goal posts and then sped up and down the field. The Nimbus Two Thousand turned wherever he wanted at his lightest touch."

str3 = "It was sweltering hot, especially in the large classroom where they did their written papers. They had been given special, new quills for the exams, which had been bewitched with an AntiCheating spell. They had practical exams as well. Professor Flitwick called them one by one into his class to see if they could make a pineapple tapdance across a desk. Professor McGonagall watched them turn a mouse into a snuffbox -- points were given for how pretty the snuffbox was, but taken away if it had whiskers. Snape made them all nervous, breathing down their necks while they tried to remember how to make a Forgetfulness potion. "

#nlp = spacy.load('en')
#sent = nlp("and the next second, Harry felt Quirrell's hand close on his wrist. At once, a needle-sharp pain seared across Harry's scar; his head felt as though it was about to split in two; he yelled, struggling with all his might, and to his surprise, Quirrell let go of him. The pain in his head lessened -- he looked around wildly to see where Quirrell had gone, and saw him hunched in pain, looking at his fingers -- they were blistering before his eyes.")
#for i in range(0,len(sent)):
#	x = sent[i:i+1]
#	print(x)
#	print(textacy.lexicon_methods.emotional_valence(x, 0.1))

#nltk.download()

#for i in range(0, len(str)):
#	print(str[i:i+20])
#	print(nltk.sentiment.util.demo_vader_instance(str[i:i+20]))

print(nltk.sentiment.util.demo_vader_instance(str))
print(nltk.sentiment.util.demo_vader_instance(str2))
print(nltk.sentiment.util.demo_vader_instance(str3))

SA = nltk.sentiment.vader.SentimentIntensityAnalyzer()

print(SA.polarity_scores(str))
