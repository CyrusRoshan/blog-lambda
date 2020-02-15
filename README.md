# blog-lambda
Publish new blog posts from anywhere!

## How does this work?

1. Deploy this to an AWS Lambda
2. Send requests to this AWS Lambda
    * (Even from your mobile device!)
3. Blog posts are published!

## With more detail:

* Install and configure [scar](https://scar.readthedocs.io/en/latest/installation.html), to use containers inside AWS Lambda
* Customize the environment variables in `blog-lambda.yaml` and run `scar init -f blog-lambda.yaml` to create your Lambda
* Create a new SSH Key and add it to your account on Github
* Send a request to the AWS Lambda.
    * In curl, this might look like `curl https://qxl9mjtpz0.execute-api.us-east-1.amazonaws.com/scar/launch -d "$(node generator.js | base64)" | base64 --decode`
    * Request body format shown in `generator.js`
* Your blog repo is downloaded, your post is added, compiled with `hugo`, committed, and pushed back to master!

## Why?

Because I can't use static site generators like [Hugo](https://github.com/gohugoio/hugo) from mobile, and because I don't think it's worth running a dedicated server instance with [my current post frequency](https://blog.cyrusroshan.com/).