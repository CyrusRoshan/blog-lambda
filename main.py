import subprocess
import json
import os
import base64

def main():
    print("Hello world!")

    # # Get request body as json
    # input_file_path = os.getenv("INPUT_FILE_PATH")
    # try:
    #     with open(input_file_path, "rb") as f:
    #         request_body = f.read()
    #     print("RAW request body:", request_body)
    # except Exception as e:
    #     print("error:", e, "couldn't load file:", input_file_path)
    #     return

    # try:
    #     request_body_json = json.loads(request_body)
    # except:
    #     print("couldn't load body:", request_body)
    #     return
    # print(request_body_json)

    # # TODO perform basic auth in case lambda is actually as stateful as it seems
    # # if request_body_json["code"] is not os.getenv("BASIC_AUTH_CODE") {
    # #     print("Invalid code")
    # #     exit(1)
    # # }

    # # Get ssh key from json, save as file
    # encoded_ssh_key = request_body_json["ssh_key"]
    # print(encoded_ssh_key)

    # ssh_key = base64.b64decode(encoded_ssh_key).decode("utf-8")
    # print(ssh_key)

    ssh_key = "asdf-ssh-key"
    print(ssh_key)

    ssh_key_path = "/tmp/ssh_key"

    # Write ssh key
    f = open(ssh_key_path, "w")
    f.write(ssh_key)
    f.close()

    # Add proper permissions
    print("chmod: \n", subprocess.run([
        "chmod",
        "400",
        ssh_key_path
    ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.decode("utf-8"), "\n")

    # Do an authed clone of a repo with the new ssh key
    print("restart ssh-agent: \n", subprocess.run([
        "sudo",
        "sh",
        "-c",
        "\"eval $(ssh-agent -s)\"",
    ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.decode("utf-8"), "\n")

    print("add ssh key: \n", subprocess.run([
        "ssh-add",
        "-K",
        ssh_key_path,
    ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.decode("utf-8"), "\n")

    print("git clone: \n", subprocess.run([
        "git",
        "clone",
        "git@github.com:CyrusRoshan/newspaper.git",
    ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.decode("utf-8"), "\n")

    print("ls: \n", subprocess.run([
        "ls",
        "-a",
    ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.decode("utf-8"), "\n")

    print("Bye, World!")

if __name__ == "__main__":
    main()