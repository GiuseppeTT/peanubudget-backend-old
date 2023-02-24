#!/bin/bash

helm upgrade \
    --install \
    peanubudget \
    ./kubernetes \
    --set database.username=${DATABASE_USERNAME} \
    --set database.password=${DATABASE_PASSWORD} \
    --set database.fqdn=${DATABASE_FQDN}
