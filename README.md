# ServerlessCrawler-Vancouver Real State
## What is this project all about?
This project is a showcase of a concept I've been playing with for a while: Serverless Crawlers.
(If you don't know what a Crawler is, feel free to visit my [Crawler101 Repository](https://github.com/MarcelloLins/WebCrawling101))

The goal here was to write an automatic data mining process (crawler) to capture real state data from Greater Vancouver Area listings. The catch? There's no actual server to be maintained. Once this is setup, all you need is a trigger to start the capture, and it runs by itself 100% on #AWS, nearly zero dolars a month.

We can leverage the Free Tier of 2 out of the 4 AWS services used on the project. Only Dynamo DB and RDS MySQL will cost anything, but still, you can keep a DynamoDB table running for 2 bucks a month, and an RDS MySQL database for cents (keeping it stopped while you're not using it) For more details you can refer to the [cost's page on this project's wiki](https://github.com/MarcelloLins/ServerlessCrawler-VancouverRealState/wiki)

## What do I need before I start?
An Amazon Web Services Account, some python knowledge

## What is the Tech Stack behind this?
* AWS Lambda for the processing of the HTML pages and data scraping
* DynamoDB for caching the urls to be captured, and to trigger lambda functions
* RDS MySQL as the end database for the processed and structured data to be stored

![Architecture](https://s3.amazonaws.com/CodeToShare/ServerlessCrawler_Diagram.png)

# About Me
Marcello Lins is passionate about technology and crunching data for fun. Feel free to connect with me through Linkedin and find more about what I'm working at via my [AboutMe Profile](http://www.about.me/marcellolins).
Visit https://techflow.me/ for more awesomeness !
