# Using Tinybird for UX Personalization

This repository contains the data project —[datasources](./datasources) and [endpoints](./endpoints)— and [script](./script) for a UX personalization example using Tinybird.

In this example, we adjust the order of images on a website based on realtime sales or website clicks. This [Observable app](https://observablehq.com/@3c8ed2c9862da582/ux-personalization) shows the idea.

Check out this [video](https://youtu.be/YsPYObGz2IU ) of the live-coding session walking you through the whole process.



To clone the repository:

`git clone git@github.com:tinybirdco/demo-ux-person.git`

`cd demo-ux-person`

## Working with the Tinybird CLI

To start working with data projects as if they were software projects, let's install the Tinybird CLI in a virtual environment.
Check the [CLI documentation](https://docs.tinybird.co/cli.html) for other installation options and troubleshooting.

```bash
virtualenv -p python3 .e
. .e/bin/activate
pip install tinybird-cli
tb auth --interactive
```

Choose your region: __1__ for _us-east_, __2__ for _eu_

Go to your workspace, copy a token with admin rights and paste it. A new `.tinyb` file will be created.  

## Project description

```bash
├── datasources
│   ├── sales.datasource
│   ├── articles.datasource
│   ├── clicks.datasource
│   ├── shoes_and_shirts.datasource
│   └── fixtures
│       └── shoes_and_shirts.csv
├── endpoints
│   ├── api_ranking.pipe
│   └── check.pipe
```

In the `/datasources` folder:
- sales.datasource: where we'll be ingesting sales event data via a python script
- articles.datasource: descriptions of the articles sold
- clicks.datasource: where we will record website activity
- shoes_and_shirts.datasource: containing links to the image files used in the demo

In the `/fixtures` folder:
- shoes_and_shirts.csv

In the `/endpoints` folder:
- api_ranking: a pipe to rank sales or clicks for the articles in shoes_and_shirts and join them to the info in articles.
- check: a single node pipe to check how ingestion of the sales data is progressing.

Note:
Typically, in big projects, we split the .pipe files across two folders: /pipes and /endpoints
- `/pipes` where we store the pipes ending in a datasource, that is, [materialized views](https://guides.tinybird.co/guide/materialized-views)
- `/endpoints` for the pipes that end in API endpoints. 

## Pushing the data project to your Tinybird workspace

Push the data project —datasources, pipes and fixtures— to your workspace

```bash
tb push --fixtures
```
You will see something like this:
```
** Processing ./datasources/shoes_and_shirts.datasource
** Processing ./datasources/clicks.datasource
** Processing ./datasources/articles.datasource
** Processing ./datasources/sales.datasource
** Processing ./endpoints/api_ranking.pipe
** Processing ./endpoints/check.pipe
** Building dependencies
** Running shoes_and_shirts 
** 'shoes_and_shirts' created
** Running articles 
** 'articles' created
** Running clicks 
** 'clicks' created
** Running sales 
** 'sales' created
** Running check 
** => Test endpoint at https://api.tinybird.co/v0/pipes/check.json
** 'check' created
** Running api_ranking 
** => Test endpoint at https://api.tinybird.co/v0/pipes/api_ranking.json
** 'api_ranking' created
** Pushing fixtures
** Checking ./datasources/shoes_and_shirts.datasource (appending 1.9 kb)
**  OK (1 blocks)
** Warning: datasources/fixtures/articles.csv file not found
** Warning: datasources/fixtures/clicks.csv file not found
** Warning: datasources/fixtures/sales.csv file not found
```

You can check the UI's Data flow:

![Data flow](data_flow.jpg?raw=true "Data flow in UI")

## Ingesting data using high-frequency ingestion (HFI)

Add sales data through the [HFI endpoint](https://www.tinybird.co/guide/high-frequency-ingestion).

Download transactions_train.csv to datasources/fixtures from the Kaggle competition [H&M Personalized Fashion Recommendations](https://www.kaggle.com/competitions/h-and-m-personalized-fashion-recommendations/data).

Then run the ingestion script

```bash
python3 script/hfi_sales.py
```
Leave this running while you look at the website to see changing rankings.

## Uploading from a local CSV

Download articles.csv from the Kaggle competition [H&M Personalized Fashion Recommendations](https://www.kaggle.com/competitions/h-and-m-personalized-fashion-recommendations/data). Upload this via the UI and append to the articles Data Source.

## Token security

You now have your Data Sources and pipes that end in API endpoints. 

You need a [token](https://www.tinybird.co/guide/serverless-analytics-api) to consume the api_ranking endpoint and write to the clicks Data Source. You should not expose your admin token, so let's create one with more limited scope.

```bash
pip install jq

TOKEN=$(cat .tinyb | jq '.token'| tr -d '"')
HOST=$(cat .tinyb | jq '.host'| tr -d '"')

curl -H "Authorization: Bearer $TOKEN" \
-d "name=ux_demo" \
-d "scope=PIPES:READ:api_ranking" \
-d "scope=DATASOURCES:READ:clicks" \
-d "scope=DATASOURCES:APPEND:clicks" \
$HOST/v0/tokens/
```

You will receive a response similar to this:

```json
{
    "token": <new_token>,
    "scopes": [
        {
            "type": "PIPES:READ",
            "resource": "api_ranking",
            "filter": ""
        },
        {
            "type": "DATASOURCES:READ",
            "resource": "clicks",
            "filter": ""
        },
        {
            "type": "DATASOURCES:APPEND",
            "resource": "clicks"
        }
    ],
    "name": "ux_demo"
}
```

## Ecommerce website

The demo website is based on Vercel's [Next.js commerce](https://github.com/vercel/commerce). "The all-in-one starter kit for high-performance e-commerce sites. With a few clicks, Next.js developers can clone, deploy and fully customize their own store." 

Use node version 16.14.0

```
nvm use 16
git clone git@github.com:tinybirdco/commerce.git
cd commerce
git stash
git checkout live_coding
npm install
vim .env.local  # add your region and ux_demo token
        NEXT_PUBLIC_TINYBIRD_API_2=https://api.tinybird.co  # or https://api.us-east.tinybird.co
        NEXT_PUBLIC_TINYBIRD_TOKEN_2=< token >
npm run dev
```

The website will run on http://localhost:3000/search

With Auto Refresh selected:

- Sales ranking changes as data is ingested - note the green and red locations. This is the website responding to external data.
- Image positions change in response the the number of clicks. This is the website responding to what is happening on the web.

This project shows just some of the features of Tinybird. If you have any questions, come along and join our community [Slack](https://join.slack.com/t/tinybird-community/shared_invite/zt-yi4hb0ht-IXn9iVuewXIs3QXVqKS~NQ)!
