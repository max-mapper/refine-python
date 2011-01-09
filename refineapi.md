# Refine API

When uploading files you will need to send the data as `multipart/form-data`, e.g.:

      Content-Disposition: form-data; name="project-file"; filename="operations.json"

      Content-Disposition: form-data; name="project-name"

      myproject
      
The other operations are just normal POST parameters

## Create project:

POST /command/core/create-project-from-upload

multipart form-data:

      'project-file' : file contents...
      'project-name' : project name...
      
Returns new project ID and other metadata

## Apply operations

POST /command/core/apply-operations

multipart form-data:

      'project' : project id...
      'operations' : file contents...
      
Returns JSON response
    
## Export rows

POST /command/core/export-rows

      'engine' : JSON string... (e.g. '{"facets":[],"mode":"row-based"}')
      'project' : project id...
      'format' : format... (e.g 'tsv', 'csv')
      
Returns exported row data
    
## Delete project

POST /command/core/delete-project

      'project' : project id...
      
Returns JSON response
    
## Check status of async processes

POST /command/core/get-processes

      'project' : project id...
      
Returns JSON response
