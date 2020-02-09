import subprocess
import json
import os
import base64

def run(desc, command):
    print(
        "RUN: " + desc + ": \n" +
        "Output: " + subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True).stdout.read().decode("utf-8"),
    )

def main():
    run(
        "env",
        "env",
    )

    # Get request body as json
    input_file_path = os.getenv("INPUT_FILE_PATH")
    try:
        with open(input_file_path, "rb") as f:
            request_body = f.read()
        print("RAW request body:", request_body)
    except Exception as e:
        print("error:", e, "couldn't load file:", input_file_path)
        return

    try:
        request_body_json = json.loads(request_body)
    except:
        print("couldn't load body:", request_body)
        return
    print(request_body_json)

    # # TODO perform basic auth in case lambda is actually as stateful as it seems
    # if request_body_json["code"] is not os.getenv("BASIC_AUTH_CODE") {
    #     print("Invalid code")
    #     exit(1)
    # }

    ssh_private_key = base64.b64decode(request_body_json["ssh_private_key"]).decode("utf-8")
    ssh_public_key = base64.b64decode(request_body_json["ssh_public_key"]).decode("utf-8")
    new_post_file_name = request_body_json["post_file_name"]
    new_post_type = request_body_json["post_type"]
    new_post_body = base64.b64decode(request_body_json["post_body"]).decode("utf-8")

    new_post_path = "/out/blog/content/" + new_post_type + "/" + new_post_file_name + ".md"

    run(
        "Make ssh dir",
        "mkdir -p /root/.ssh",
    )

    ssh_private_key_path = "/root/.ssh/id_rsa"
    ssh_public_key_path = "/root/.ssh/id_rsa.pub"

    # Write ssh public/private key
    f = open(ssh_private_key_path, "w")
    f.write(ssh_private_key)
    f.close()

    f = open(ssh_public_key_path, "w")
    f.write(ssh_public_key)
    f.close()

    home = os.getenv("HOME")
    run(
        "Copy public key to authorized keys",
        "cp " + ssh_public_key_path + " " + home + "/.ssh/authorized_keys",
    )
    run(
        "Add proper key permissions",
        "chmod 600 " + ssh_private_key_path,
    )
    run(
        "ssh-add",
        "ssh-add " + ssh_private_key_path,
    )

    os.environ["GIT_SSH_COMMAND"] = "ssh -i " + ssh_private_key_path + " -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no"

    # Do an authed clone of a repo with the new ssh key
    run(
        "clone",
        "git clone git@github.com:CyrusRoshan/blog.git",
    )

    run(
        "rm new post file if it exists",
        "rm -f " + new_post_path,
    )

    f = open(new_post_path, "w")
    f.write(new_post_body)
    f.close()

    os.chdir("blog")

    run(
        "add git config",
        '''
        git config --global user.email "cyrusroshan@users.noreply.github.com" && git config --global user.name "Cyrus Roshan"
        '''
    )
    run(
        "commit new file",
        "git add " + new_post_path + " && git commit -m 'Lambda commit new post'"
    )
    run(
        "build hugo",
        "hugo",
    )
    run(
        "commit new build",
        "git add -A && git commit -m 'Lambda commit new build release.'"
    )
    run(
        "git push",
        "git push origin master"
    )

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Main exception when running:", e)