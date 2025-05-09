provider "aws" {
  access_key = var.aws_access_key_id
  secret_key = var.aws_secret_access_key
  token      = var.aws_session_token
  region     = "us-east-1"
}

resource "aws_security_group" "mysg-id" {
  name_prefix = "giglo"
  description = "My security group"

  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "ALL"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "ALL"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "web_server" {
  ami           = "ami-0e1bed4f06a3b463d"
  instance_type = "t2.micro"
  key_name      = "giglo"

  vpc_security_group_ids = [aws_security_group.mysg-id.id]

  tags = {
    Name = "nginx-web-server"
  }

  provisioner "remote-exec" {
    inline = [
      "sudo apt update",
      "sudo apt install nginx -y",
      "sudo systemctl start nginx"
    ]

    connection {
      type        = "ssh"
      user        = "ubuntu"
      private_key = file("C:/Users/ASUS/Downloads/giglo.pem")
      host        = self.public_ip
    }
  }
}

