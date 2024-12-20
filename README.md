# Medication Information Retrieval (IR) System

## Data Download
The main file we created and then indexed into Solr can be found at the following link (https://drive.google.com/file/d/1YH5HZEKHzPP2obnchOzLxvG8NWtR8fW7/view?usp=sharing)

## Setup

### Solr Server
The project has a pre-defined Solr core, which includes configuration files (such as a schema) included in the 'indexing/medications_core' directory. To start the Solr service, run the start command and specifying this as the home directory <br/><br/>
```bin/solr start -p 8983 -s path/to/project/medication-ir-system/backend/indexing/``` <br/><br/>
This will start the server on port 8983 (the default).

### Vue Interface
From the frontend directory, 'frontend/med-ui', run the corresponding Vue command to start the server<br/><br/>
```npm run serve```

### Scraper script
If you wish to rerun the scraping scripts, we have conveniently grouped all of them in the scrape.py script, located at /backend/scraping. Navigate to this directory and run<br/><br/>
```python scrape.py```

### Indexing documents
To try out the search functionality, first we need to index some documents into Solr (ensure the server is running). <br/><br/>
```bin/solr post -c medications_core path/to/document/filename.json```
