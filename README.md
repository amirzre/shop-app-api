<h1 align="center"> Ecommerce APP API </h1> <br>

<h3 align="center">
  An Ecommerce Store Backend to Sell Products. Built with Python/Django Rest Framework.
</h3>

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation Process](#installation-process)

## Introduction

DRF-Ecommerce-API provides API endpoints to Sell Physical Products. Built with Python/Django and 100% free to use.

## Features

A few of the things you can do with this app:

* Admin can create/update/delete Product Category
* Admin can create/update/delete Product Detail
* Authenticated Users can make POST requests to Product Category & Product Detail
* Unauthenticated Users can only make GET requests to Product Category & Product Detail
* Users can register to be authorized
* Authentication system works with JWT and generate refresh and access token
* Authorized Users can Order Products
* Authorized User can write Review for product and rating
* Document project with swagger
* Dockerized project

## Installation Process

**Installation Process (Linux)**

1. Install docker engine `https://docs.docker.com/engine/install/`
2. Install docker compose `https://docs.docker.com/compose/install/`
3. Clone This Project `git clone git@github.com:zanull/shop-app-api.git`
4. Go To Project Directory `cd shop-app-api`
5. Build docker images `sudo docker compose build`
6. Do make migrations `sudo docker compose run --rm app sh -c "python3 manage.py makemigrations"`
7. Run the project `sudo docker compose run`
