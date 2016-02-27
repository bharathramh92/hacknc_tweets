Following is the demo for this app

Website URL: http://hacknctweetsbl.mybluemix.net/tweet/

Video URL: https://youtu.be/W6SpM8yVky0

This app rates any live/active events based on the twitter data. Bluemix Twitter API is used for tweets analysis.
- User search term is searched directly in twitter.
- Twitter tags are extracted from the retrieved result and top 2 tags are taken. This on the assumption that most used tweets about the subject would be the most relevant tags.
- Positive sentiment(ps) and negative sentiments(ns) are again queried for the 2 retrieved tags and the ratio of ps/(ps+ns) is showed as the Output/Score (score on a scale of 0-1, were 0 is towards negative and 1 is towards overall positive sentiment).
P.S We are taking only the tweets publised 48hrs prior to the user query.
