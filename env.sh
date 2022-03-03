#!/bin/bash

echo "Enter database user"
read user
echo "Enter the database password"
read password
echo "Enter database name"
read name

source bin/activate

export DB_USER=$user
export DB_PASSWORD=$password
export DB_NAME=$name

