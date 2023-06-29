variable "my_access_key" {
  description = "Access-key-for-AWS"
  default     = "no_access_key_value_found"
}

variable "my_secret_key" {
  description = "Secret-key-for-AWS"
  default     = "no_secret_key_value_found"
}

provider "aws" {
  region     = "us-east-2"
  access_key = var.my_access_key
  secret_key = var.my_secret_key
}

resource "aws_instance" "E0-Arquitectura" {
  ami           = "ami-0568936c8d2b91c4e"
  instance_type = "t2.micro"

  tags = {
    "Name" : "E0-Arquitectura"
  }
}