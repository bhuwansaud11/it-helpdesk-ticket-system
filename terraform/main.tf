terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

provider "docker" {}

resource "docker_image" "helpdesk_app" {
  name = "it-helpdesk-app:v1"
  build {
    context = "../"
  }
}

resource "docker_container" "helpdesk_container" {
  name  = "it-helpdesk-terraform"
  image = docker_image.helpdesk_app.image_id
  ports {
    internal = 8000
    external = 8002
  }
}
