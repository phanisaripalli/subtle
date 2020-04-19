**serverless**

## subtle

This is an experimental hobby project aimed towards auto translation of subtitle files. 
To do this, the project relies on AWS. The following services are used:

1. s3 for storing `.srt` files (potentially other formats but haven't tested).
    **Format**
    
    ```
    Bucket
    |
    |__<media_id>
            <language_code1.srt>
            <language_code2.srt>
            <language_code3.srt>
    ```    

2. Dynamodb to make sure only one combination of media_id, from and to languages are processed at a given time.
    E.g. keys in dynamodb: 1-en-fr, 2-fr-es etc.
    After translation, the keys in the table are deleted.

3. Amazon Translate    
    
    There are two ways to translate: per dialogue and bulk (in a batch of 100 lines).
    I found the bulk breaks in the region `eu-central` but is fine in `eu-west-1`. A matter for further investigation.
    
    Dialogues are parsed by taking timestamps and new lines into considerations.   


`config_sample.yml` should be renamed to `config.yml` filled with details.


**How to run**

```
# navigate to the root of the project
python3 runner.py --from=<from_lang> --to=<to_lang> --media_id=1

# e.g.
python3 runner.py --from=en --to=fr --media_id=1
```

## Deploying the AWS resources

```
cd serverless
serverless deploy --profile <profile> --region <region>
```