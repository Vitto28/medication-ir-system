# Medication Information Retrieval (IR) System

## Overview

TODO: Add description

## Features

TODO: List features

## Project Structure

TODO: Add structure

## Setup

### Solr Server
The project has a pre-defined Solr core, which includes configuration files (such as a schema) included in the 'indexing/medications_core' directory. To start the Solr service, run the start command and specifying this as the home directory <br/><br/>
```bin/solr start -p 8983 -s path/to/project/medication-ir-system/backend/indexing/``` <br/><br/>
This will start the server on port 8983 (the default).

### Vue Interface
From the frontend directory, 'frontend/med-ui', run the corresponding Vue command to start the server<br/><br/>
```npm run serve```

### Scraper script
TODO

### Indexing documents
To try out the search functionality, first we need to index some documents into Solr. <br/><br/>
```bin/solr post -c path/to/project/backend/indexing/medications_core path/to/document/sample.json```
