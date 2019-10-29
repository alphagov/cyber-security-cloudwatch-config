# Cyber Security CloudWatch Config

The aim of this repository is to automate the generation of CloudWatch 
alarm config. 

We are starting to build a collection of standardised CloudWatch Alarm 
terraform modules in 
[cyber-security-shared-terraform-modules](https://github.com/alphagov/cyber-security-shared-terraform-modules)

This repository uses `cloudwatch list-metrics` to identify resources to be 
monitored, queries the tags for those resources in order to classify them 
into services and environments. 

The aim is to produce a set of `tfvar` files containing lists of maps 
containing the config for the standard modules. 

Then we can implement the modules to count across those lists. 

Hopefully we can then automatically generate a pull request to terraform 
the alarm config. 

