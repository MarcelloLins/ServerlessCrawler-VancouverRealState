# ServerlessCraler-Vancouver Real State
## What is this project all about?
This project is a showcase of a concept I've been playing with for a while: Serverless Crawlers.
(If you don't know what a Crawler is, feel free to visit my [Crawler101 Repository](https://github.com/MarcelloLins/WebCrawling101))

The goal here was to write an automatic data mining process (crawler) to capture real state data from Greater Vancouver Area listings. The catch? There's no actual server to be maintained. Once this is setup, all you need is a trigger to start the capture, and it runs by itself 100% on #AWS, nearly zero dolars a month.

We can leverage the Free Tier of 3 out of the 4 AWS services used on the project. Only Dynamo DB will cost money, but still, you can keep a DynamoDB table running for 2 bucks a month.

## What do I need before I start?
An Amazon Web Services Account, some python knowledge

## What is the Tech Stack behind this?
* AWS SNS to trigger the capture process
* AWS Lambda for the processing of the HTML pages and data scraping
* DynamoDB for caching the urls to be captured, and to trigger lambda functions
* RDS MySQL as the end database for the processed and structured data to be stored
