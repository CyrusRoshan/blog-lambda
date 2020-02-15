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
* If you don't have an SSH key pair you'd like to use:
    * Create a new SSH key pair (e.g. `ssh-keygen -t rsa -b 4096 -C "lambda-ssh"`)
    * [Add the public SSH key](https://help.github.com/en/github/authenticating-to-github/adding-a-new-ssh-key-to-your-github-account) to your account on Github
* Send a request to the AWS Lambda
    * In curl, this might look like `curl https://YOUR_LAMBDA_ID.execute-api.us-east-1.amazonaws.com/scar/launch -d "$(node generator.js | base64)" | base64 --decode`
    * Request body format shown in `generator.js`
* Your blog repo is downloaded, your post is added, compiled with `hugo`, committed, and pushed back to master!

## Why?

Because I can't use static site generators like [Hugo](https://github.com/gohugoio/hugo) from mobile, and because I don't think it's worth running a dedicated server instance with [my current post frequency](https://blog.cyrusroshan.com/).

## Best Practices

Presumably you're hosting this on your own Lambda and sending data over HTTPS, but even so, you don't need to use an SSH key with pull/push access to all of your repos.

I'd recommend making a separate user or service account which is only given access to the git repo which it needs to push to, and creating an SSH key authenticated to use that account.