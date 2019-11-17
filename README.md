# DJT-speech-app-engine
Speeches hosted in Google Cloud SQL and app served from Google App Engine. [App Link](https://composite-area-256123.appspot.com/). 

This repo is continuation of [DJT-Speech-Generator](https://github.com/addadda023/DJT-speech-generator) repo. 
The model hosted in Google Cloud Run uses CPU to generate speech in real-time, but it takes up to 60 sec because 
it's being served by CPU. 

To serve the speech faster, I batch generated 10,000+ speeches from the finetuned GPT-2 model. The speeches are 
stored in a database in Google Cloud SQL. I created a Google Cloud App to take to display a randomly selected speech. 

### Front end

* Flask
* Jinja
* Bootstrap

### Back end

* Postgre
* Python
