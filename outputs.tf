output "instance_public_ip" {
  value = aws_instance.web_server.public_ip
}

output "mysg-id" {
  value = aws_security_group.mysg-id.id
}