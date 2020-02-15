var body = {
  "ssh_private_key": Buffer.from(`-----BEGIN OPENSSH PRIVATE KEY-----
[...]
-----END OPENSSH PRIVATE KEY-----
`).toString('base64'),

  "ssh_public_key": Buffer.from(
    'ssh-rsa [...] lambda-ssh\n'
  ).toString('base64'),

  "post_file_name": 'example_post',
  "post_type": 'draft',

  "post_body": Buffer.from(
`---
title: "Example post!"
date: 2020-1-15T12:16:16+02:00
description: "An example!"
draft: false
---

Truly an inspiring post right here. Wow!`
  ).toString('base64'),
}

console.log(JSON.stringify(body))