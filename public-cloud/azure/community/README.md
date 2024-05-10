# KENG-on-Azure-Boost-2-Agents-2-Eth-1-Vnet-1-Public-Subnet-1-Private-Subnet

## Description Sam
This deployment creates a topology with a single virtual network having a single public facing subnet and a single private subnet.

## Authentication Variables
```
terraform.hcp.auto.tfvars
```
You **MUST** uncomment all lines in this file and replace values to match your particular environment.  
Otherwise, Terraform will prompt the user to supply input arguents via cli.

## Required Variables
```
terraform.required.auto.tfvars
```
You **MUST** uncomment all lines in this file and replace values to match your particular environment.  
Otherwise, Terraform will prompt the user to supply input arguents via cli.

## Optional Variables
```
terraform.optional.auto.tfvars
```
You **MAY** uncomment one or more lines as needed in this file and replace values to match your particular environment.

## Required Usage
```
terraform init
terraform apply -auto-approve
terraform destroy -auto-approve
terraform output SshKey | tail -n +3 | head -n-3 | sed "s/^[ \t]*//" > SshKey.pem
Agent1DnsName=$(terraform output | grep agent1 | sed -n 's/.*=.//p' | tr -d '"')
```

## Optional Usage
```
terraform validate
terraform plan
terraform state list
terraform output
```

## KENG Sample Usage
```
chmod 400 SshKey.pem
ssh -i SshKey.pem ubuntu@$Agent1DnsName
$ source ./venv/bin/activate
$ cd keng-python
$ docker ps
$ ./unidirectional.sh -s 4100
 ```
