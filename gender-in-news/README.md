# gender_in_news.py usage


## Running the demo from iqoqo app
 1. Upload the script gender_in_news.py
 2. Upload the dataset files as input files from: [iqoqo storage](https://iqoqo/s3) or straight from the [Kaggale site](https://www.kaggle.com/snapcrack/all-the-news)
 3. For our case you need to upload the file english.pickle as a 'Constant File'.
The only modules that are needed is nltk, which is a powerful suite for text processing and analysis. For this analysis, we are only using the NLTK function that splits text into sentences. 

## Preparing the data for the analysis
The data structure at the dataset from Kaggale is as follow:
columns=["id","title", "publication", "author", "date", "year", "month", "url", "content"].

This data is open using pandas structure.
We group by the publication name (meaning the name of the news websit that this article is from) and looking at the content column.
The content column is the article text.
The analysis then run over each publication for all the articles from it.
The results files are as follow:
For each news website source:
1.  nameOfPublication_publication_detailes.txt with the number of articles.
2.  nameOfPublication_results_summary with statistic for example:
        25.9% gendered
        2131 sentences about men.
        552 sentences about women.
        3.9 sentences about men for each sentence about women.
        number of sentences about both 153
        number of sentences about none 7519 

In case you need to merge files, the gengered calculation is:
(100*(sentence_counter['male']+sentence_counter['female'])/
                          (sentence_counter['male']+sentence_counter['female']+sentence_counter['both']+sentence_counter['none']))

## Gender in news

An NLP research of gender appearnces gap in 150,000 publication from 15 different news websites usign the IQOQO distribution framework.
Code is based on an [article by Neal Caren](http://nbviewer.jupyter.org/gist/nealcaren/5105037) and evaluates [all the news](https://www.kaggle.com/snapcrack/all-the-news) dataset
