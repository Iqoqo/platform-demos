# Don't overlook the iceberg!

## A deep look at Titanic dataset Logistic Regression samples

 When it comes to Logistic Regression using python, it seems that the Titanic survival prediction using the passenger dataset had became the ["Hello World"](https://en.wikipedia.org/wiki/%22Hello,_World!%22_program) of the domain.

for instance [SarahG](https://www.kaggle.com/sgus1318/titanic-analysis-learning-to-swim-with-python) and [Baligh Mnassri](https://www.kaggle.com/mnassrib/titanic-logistic-regression-with-python/notebook) amazing examples in [Keggle](https://www.kaggle.com/) gives the user a very clear and well written guide, going from basic data purification and preparation through understanding the data structure to analysis. But as I read through the examples, I couldn't help feeling that something is missing there, the examples are working too well and to the point, it feels as if we see only the tip of the ice berg (icebergs... Titanic... I couldnt stop myself...) some very interesting work is being hidden under the water line, in the ocean of the writer's experience. How do we know which parameters to use with the algorithms?

## Going beyond the tip of the iceberg

Learning which columns has no effect on the Logistic Regression is a repetative work which require several runs of the code on the same data and result exemination. This task can take some time and require certain amount of planning. Basicaly you will need to run the same algorithm using different parameters and compare the results, hoping to find the parameters combination that lead to the best results.
These jobs can run sequencially (e.g. one after the other) but since these runs are independent we can save some time by parallelazing the jobs.
In this article we will use [IQOQO]() elastic grid to parallelize the jobs (being IQOQO CTO I guess this was fairly expectable) you can use IQOQO free tier for this sample or parallelize it in any other way you prefer. IQOQO allows researchers to focus on their research and not waist time and mony on DevOps and cluster managememnt.

## Prepering the data
The titanic dataset needs some cleanup and preperation before it can be used. Some columns in the dataset are hardly poplulated and some other columns are missing portion of the data. to handle these issues I've extracted the script `data-prep.py` in this article's [GitHub Repository]() out of [Baligh Mnassri](https://www.kaggle.com/mnassrib/titanic-logistic-regression-with-python/notebook) Keggle (Reading the Kaggle is highly recommended, it is discribes data purification in a very clear and simple way)

## Prepering the algorithm

## Setting up IQOQO

Our first step is getting IQOQO free tier access,  IQOQO free tier alpha is invite only and you can [request access]() to the IQOQO free tier alpha [here]().

## Putting it all together

## Collecting the results

## Conclusion