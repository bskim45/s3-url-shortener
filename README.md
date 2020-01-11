# s3-url-shortener

[![](https://images.microbadger.com/badges/image/bskim45/s3-url-shortener.svg)](https://microbadger.com/images/bskim45/s3-url-shortener "Get your own image badge on microbadger.com")
[![](https://images.microbadger.com/badges/version/bskim45/s3-url-shortener.svg)](https://microbadger.com/images/bskim45/s3-url-shortener "Get your own version badge on microbadger.com")
[![Docker Stars](https://img.shields.io/docker/stars/bskim45/s3-url-shortener.svg?style=flat)](https://hub.docker.com/r/bskim45/s3-url-shortener/)
[![Docker Pulls](https://img.shields.io/docker/pulls/bskim45/s3-url-shortener.svg)]()

Super simple flask-based URL shortener leveraging AWS S3

## Background

> For the full serverless solution, refer to [Build a Serverless, Private URL Shortener | AWS Compute Blog](https://aws.amazon.com/blogs/compute/build-a-serverless-private-url-shortener/)

I hate API Gateway (you know, it's expensive)

## Architecture

```text
App(flask) -> S3 Redirect(with a optional custom domain) -> Target Site
```

- S3 Redirect: https://docs.aws.amazon.com/AmazonS3/latest/dev/how-to-page-redirect.html
- S3 Custom Doamin: https://docs.aws.amazon.com/AmazonS3/latest/dev/website-hosting-custom-domain-walkthrough.html

## Requirements

- Python 3.6 or above
- S3 Bucket(optionally custom domain)

## Prerequisites

- Create S3 bucket, and enable static website hosting: https://docs.aws.amazon.com/AmazonS3/latest/dev/EnableWebsiteHosting.html

- Optionally, set custom domain for the target bucket: https://docs.aws.amazon.com/AmazonS3/latest/dev/website-hosting-custom-domain-walkthrough.html

- Prepare IAM role or API key with proper permission to the target S3 bucket.

> Thanks to `boto3`, all options for providing credentions in [boto3 document](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html) is good enough.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "",
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:GetObject",
        "s3:ListBucket",
        "s3:PutObjectAcl"
      ],
      "Resource": [
        "arn:aws:s3:::your_s3_bucket",
        "arn:aws:s3:::your_s3_bucket/*"
      ]
    }
  ]
}
```

## Configuration

| ENV          | Default       | Required | Example             |
|--------------|---------------|----------|---------------------|
| PORT         | 5000          |          | 8080                |
| S3_REGION    | us-east-1     | Yes      | us-east-1           |
| S3_BUCKET    |               | Yes      | hello-bucket        |
| SHORT_DOMAIN |               |          | https://example.com |

## Deploy

### Old Skool Way

Clone and install requirements:

```shell
$ pip install -r requirements.txt
```

Configure env:

```shell
$ cp .env.example .env
$ vi .env
```

Run app:

```shell
$ python run.py
```

### docker-compose

```shell
$ cp docker-compose-prod.yaml docker-compose.yaml
# fill in ENV values
$ vi docker-compose.yaml
# run
$ docker-compose up -d
```

### Helm chart

> Check out [helm-git](https://github.com/aslafy-z/helm-git) plugin if you don't want to clone entire repository

```shell
$ helm install --name my-release -f values.yaml deploy/charts/s3-url-shortener
```

## Inspired by

- [freeCodeCamp - How to build a Serverless URL shortener using AWS Lambda and S3](https://www.freecodecamp.org/news/how-to-build-a-serverless-url-shortener-using-aws-lambda-and-s3-4fbdf70cbf5c/)
- [AWS Compute Blog - Build a Serverless, Private URL Shortener](https://aws.amazon.com/blogs/compute/build-a-serverless-private-url-shortener/)

## License

MIT licensed. See [LICENSE](https://github.com/bskim45/s3-url-shortener/blob/master/LICENSE) for full details.
