## Repository structure

```
├── .gitignore                <- Directories and files to be ignored by git
├── .poetry.lock              <- Current poetry settings.
├── .pre-commit-config.yaml   <- Settings for pre-commit
├── .python-version           <- Current Python version
│
├── app.py                    <- Streamlit App
│
├── data
│   ├── external              <- Data from third party sources.
│   ├── processed             <- Data that has been transformed.
│   ├── raw                   <- The original, immutable data dump.
│   └── user_output           <- User output data.
│
├── docs                      <- Markdowns with pertinent documentation.
│
├── notebooks                 <- Jupyter notebooks. Naming convention is a zero followed by a number,
│                                if the number has single digit, or just the number if it has more
│                                than one digit, followed by the creator's initials, and a short
│                                `-` delimited description, e.g.`1.0-jqp-initial-data-exploration`.
│
├── pyproject.toml            <- Project configuration file with package metadata.
│
│
├── README.md                 <- The top-level README for developers using this project.
│
├── streamlit_rfm_app         <- Package folder
│   └── __init__.py           <- Init file representing package.
│
└── templates                   <- HTML templates.
```

## Using AWS Services

This project consists in a Streamlit App running in a EC2 instance.

The app displays a table and requests that user enters their name opinion regarding each row of the table.
Once the user is satisfied with their entries, they can submit the data by clicking a submit button.

Upon submission, the data is either saved to a pre-configured S3 bucket if the service is running on the EC2 instance, or stored locally if S3 is not accessible.

### Create IAM role

An IAM role was created to grant the EC2 instance access to S3, eliminating the need to manually provide AWS credentials. This approach is in line with AWS best practices.

The role was named "EC2_S3_Access_Role" and was assigned the AmazonS3FullAccess policy.

### Create Security Group

Created new security group named "MyStreamlitApps".

As inbound rules, created two rules:

1. type SSH, using TCP protocol, port 22 and source "My IP" - named it "SSH access - developers"
2. type Custom TCP, using TCP protocol, port 8501 and source "Anywhere IPv4" - named it "Streamlit"


### Create S3 bucket

An S3 bucket named "rfmanalysisuseroutput" was created with the default settings to store user submissions.

### Create EC2 instance

Named EC2 instance "nn" running on Amazon Linux AMI and using t3.micro instance type (free tier).
In Network settings, used existing security group "MyStreamlitApps".

As login, created a new RSA key-pair and saved .pem file in my config directory.

After creating the EC2 instance, confirmed there was no IAM role associated with the instance, and used the menu Actions->Security->Modify IAM role to select role "EC2_S3_Access_Role".

Registered my public address (13.48.249.248).

## Accessing EC2 instance

```
# Enter EC2 instance
$ ssh -i config/rfm_key.pem ec2-user@13.48.249.248 # enter in EC2 instance

# Install git and curl
[ec2-instance]$ sudo yum install git -y
[ec2-instance]$ sudo yum install curl -y

# Install poetry following ([instructions](https://github.com/python-poetry/install.python-poetry.org))
[ec2-instance]$ curl -sSL https://install.python-poetry.org | python3 -

# Clone public repo; if private, would need to setup SSH in EC2 instance
[ec2-instance]$ git clone https://github.com/fmsrosa/streamlit_rfm_app.git # clone public repo; if private, setup SSH in EC2 instance.

# Install pyenv
[ec2-instance]$ curl https://pyenv.run | bash
[ec2-instance]$ echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> ~/.bashrc
[ec2-instance]$ echo 'eval "$(pyenv init --path)"' >> ~/.bashrc
[ec2-instance]$ echo 'eval "$(pyenv init -)"' >> ~/.bashrc
[ec2-instance]$ source ~/.bashrc

# `pyenv install 3.12` was not working; installing generic development tools
[ec2-instance]$ sudo yum groupinstall "Development Tools"

# Setup pyenv 3.12 locally
[ec2-instance]$ pyenv install 3.12
[ec2-instance]$ pyenv local 3.12

# Install project Python packages
[ec2-instance]$ poetry install

# Deploy app and make it accessible online
[ec2-instance]$ poetry run streamlit run app.py --server.port 8501 --server.enableCORS false --server.enableXsrfProtection false
```
