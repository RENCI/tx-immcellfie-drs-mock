# tx-immcellfie-drs-mock

## install 

works under python 3.9

```
pip install -r requirements.txt
```

put gene file at gene.csv and phenotype file at phenotype.csv

```
./start.sh 0.0.0.0 80
```

## use

### get jwt

```
curl -XPOST "http://<host>:<port>/irods-rest2/token" --user rods:woot
```

returns a token. assuming that you store it in env var `token`

### get bundle info

```
curl -XGET "http://<host>:<port>/ga4gh/drs/v1/objects/mock_obj1" -H "Authorization: Bearer $token"
```

returns a json that contains ids of "phenotypic data" and "genetic data"

the ids are "phenotype_csv" and "gene_data"

### get phenotype/genetic data access url

To get phenotypic data,

```
curl -XGET "http://<host>:<port>/ga4gh/drs/v1/objects/phenotype_csv/access/irods-rest" -H "Authorization: Bearer $token"
```

returns a url and an api-key
```
curl -XGET "<url>" -H "Authorization: Bearer $token"
```

To get genetic data,

```
curl -XGET "http://<host>:<port>/ga4gh/drs/v1/objects/gene_data/access/irods-rest" -H "Authorization: Bearer $token"
```

returns a url and an api-key
```
curl -XGET "<url>" -H "Authorization: Bearer $token"
```
