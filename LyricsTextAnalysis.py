import pandas as pd   # for importing & transforming data
import re   # for regular expressions
import matplotlib.pyplot as plt   # for plots
import seaborn as sns   # for charts
from wordcloud import WordCloud   # for the wordcloud
from spacy.lang.en import English  # for tokenising text
nlp = English()   # for tokenising text
from collections import Counter   # for getting freq of words
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# import the csv file into a Pandas dataframe
lyrics_df = pd.read_csv("lyricsrealcoleworld.csv")
artists = ["J. Cole"]
# you can also add multiple artists by separating with a comma:
# artists = ["J. Cole", "Drake", "Kendrick Lamar", "Nicki Minaj"]
# but make sure that these artists are also present in the csv file

# view the shape of the data (the number of rows and columns)
print(f"The shape of the data is: {lyrics_df.shape}")

df1 = lyrics_df['lyrics']
print(df1.head(10))

# Create a single string containing all the lyrics,
# This will be needed to be able to create a wordcloud
lyrics_string = " ".join(lyrics for lyrics in lyrics_df["lyrics"])
print(lyrics_string)

# Create the wordcloud
lyrics_wordcloud = WordCloud(background_color="black", max_words=100).generate(lyrics_string)

# View the wordcloud
plt.imshow(lyrics_wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()

print("\n")
print("\n")
print("\n")

# Data Cleaning
# Convert the text to lower case
lyrics_string_lower = lyrics_string.lower()

# View the first 200 elements of the string to check this worked as expected
print(lyrics_string_lower[0:200])

print("\n")
print("\n")
print("\n")

# Remove extra white spaces so there is only one space between words
lyrics_string_space = re.sub(r'\s+',' ', lyrics_string_lower)

# View the first 200 elements of the string to check this worked as expected
print(lyrics_string_space[0:200])

# Create the wordcloud
lyrics_cleaned_wordcloud = WordCloud(background_color="black", max_words=100).generate(lyrics_string_space)

# View the wordcloud
plt.imshow(lyrics_cleaned_wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()

# Create a spacy document by pointing spacy to the lyrics string
lyrics_doc = nlp(lyrics_string_space)

# Get all tokens that aren't punctuation
lyrics_words = [token.text for token in lyrics_doc if token.is_punct != True]

# Get the frequency of each word (token) in the lyrics string
lyrics_word_freq = Counter(lyrics_words)

# Get the 10 most frequent words
ten_most_common_words = lyrics_word_freq.most_common(10)

# View the 10 most common words
print(ten_most_common_words)

# Create a Pandas dataframe containing the tokens (words) and their frequencies
freq_df = pd.DataFrame.from_dict(lyrics_word_freq, orient='index').reset_index()

# Rename the columns to "word" and "freq"
freq_df.columns=["word", "freq"]

# Sort the dataframe so that the most frequent word is at the top and view the first 3 rows
print(freq_df.sort_values(by="freq", ascending=False).head(3))

# Display a bar chart showing the top 25 words and their frequencies
fig, ax = plt.subplots(figsize=(8,6))
sns.barplot(data=freq_df.sort_values(by="freq", ascending=False).head(25), y="word", x="freq", color='#7bbcd5')
plt.ylabel("Word")
plt.xlabel("Frequency")
plt.title("Top 25 Most Frequent Words")
sns.despine()
plt.show()

# Get all tokens that aren't punctuation and aren't stopwords
# Stopwords are the words that are not really important for analysis
# Examples of stopwords are: "a," "and," "but," "how," "or,"
lyrics_words = [token.text for token in lyrics_doc if token.is_punct != True and token.is_stop != True]

# Get the frequency of each word (token) in the lyrics string
lyrics_word_freq = Counter(lyrics_words)

# Re-create the Pandas dataframe containing the tokens (words) and their frequencies
freq_df = pd.DataFrame.from_dict(lyrics_word_freq, orient='index').reset_index()

# Rename the columns to "word" and "freq"
freq_df.columns=["word", "freq"]

# Display a bar chart showing the top 25 words and their frequencies (which will exclude the stopwords this time)
fig, ax = plt.subplots(figsize=(12,6))
sns.barplot(data=freq_df.sort_values(by="freq", ascending=False).head(25), y="word", x="freq", color='#7bbcd5')
plt.ylabel("Word")
plt.xlabel("Frequency")
plt.title("Top 25 Most Frequent Words (Excluding Stopwords)")
sns.despine()
plt.show()

# Number of words used by J Cole in his top 10 songs.
plt.rcParams['figure.figsize'] = (3, 2)

wordsdf = pd.DataFrame(columns=('artist', 'words'))
i=0
for artist in artists:
    num_words = 0
    all_text = ''
    for sentence in lyrics_string_space:
        num_words_this = len(sentence.split(" "))
        num_words += num_words_this

    wordsdf.loc[i] = (artist, num_words)
    i+=1

print(wordsdf)
# If you want you can also show this using a plot, just uncomment the next two code lines (141 and 142)
# I would recommend showing it in plot form when there are multiple artists
# wordsdf.plot.bar(x='artist', y='words', title='Number of Words in J. Cole songs');
# plt.show()

lexicaldf = pd.DataFrame(columns=('artist', 'lexicalrichness'))
for artist in artists:
    all_words = ''
    num_words = 0
    raw_text = ""
    for sentence in lyrics_string_space:
        raw_text += sentence

    words = raw_text.split(" ")
    filtered_words = [word for word in words if word not in stopwords.words('english') and len(word) > 1 and word not in ['na', 'la']]  # remove the stopwords

    a = len(set(filtered_words))
    b = len(words)
    lexicaldf.loc[i] = (artist, (a / float(b)) * 100)
    i += 1

print(lexicaldf)
# If you want you can also show this using a plot, just uncomment the next two code lines (163 and 164)
# I would recommend showing it in plot form when there are multiple artists
# lexicaldf.plot.bar(x='artist', y='lexicalrichness', title='Lexical richness of each Artist');
# plt.show()

# Let's perform Sentiment Analysis
sentimentanalysisdf = pd.DataFrame(columns=('artist', 'positive', 'neutral', 'negative'))
sid = SentimentIntensityAnalyzer()
i = 0
for artist in artists:
    num_positive = 0
    num_negative = 0
    num_neutral = 0

    for sentence in lyrics_string_space:
        comp = sid.polarity_scores(sentence)
        comp = comp['compound']
        if comp >= 0.5:
            num_positive += 1
        elif comp > -0.5 and comp < 0.5:
            num_neutral += 1
        else:
            num_negative += 1

    num_total = num_negative + num_neutral + num_positive
    percent_negative = (num_negative / float(num_total)) * 100
    percent_neutral = (num_neutral / float(num_total)) * 100
    percent_positive = (num_positive / float(num_total)) * 100
    sentimentanalysisdf.loc[i] = (artist, percent_positive, percent_neutral, percent_negative)
    i += 1
print(sentimentanalysisdf)
# If you want you can also show this using a plot, just uncomment the next two code lines (194 and 195)
# I would recommend showing it in plot form when there are multiple artists
# sentimentanalysisdf.plot.bar(x='artist', stacked=True)
# plt.show()