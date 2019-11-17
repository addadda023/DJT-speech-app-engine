# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python37_cloudsql_psql]
import os

from flask import Flask
from flask import render_template
import psycopg2
import random
import html

db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')

app = Flask(__name__)


@app.route('/')
def main():
    # When deployed to App Engine, the `GAE_ENV` environment variable will be
    # set to `standard`
    if os.environ.get('GAE_ENV') == 'standard':
        # If deployed, use the local socket interface for accessing Cloud SQL
        host = '/cloudsql/{}'.format(db_connection_name)
    else:
        # If running locally, use the TCP connections instead
        # Set up Cloud SQL Proxy (cloud.google.com/sql/docs/mysql/sql-proxy)
        # so that your application can use 127.0.0.1:3306 to connect to your
        # Cloud SQL instance
        host = '127.0.0.1'

    try:
        cnx = psycopg2.connect(dbname=db_name, user=db_user,
                               password=db_password, host=host)
        speech_id = random.randrange(1100) # Test using 1100 speeches.
        table = 'speeches'
        with cnx.cursor() as cursor:
            statement = 'SELECT speech FROM speeches WHERE speech_id = %s;'
            cursor.execute(statement, (speech_id,))
            result = cursor.fetchall()
        #current_time = result[0][0]
        speech = result[0][0]

        # Uncomment    
        # Divide speech to 1/3 and 2/3 parts
        len_speech = len(speech)
        speech_less = speech[:len_speech//3]
        speech_more = speech[len_speech//3:]

        # Markup speech myself
        speech_less = html.escape(speech_less)
        speech_less = speech_less.replace('\n', '<br />')

        speech_more = html.escape(speech_more)
        speech_more = speech_more.replace('\n', '<br />')

        # return str(current_time)
        # Render template
        return render_template('index.html', less=speech_less, more=speech_more)

        # return(str(count_speeches))

    except(Exception, psycopg2.Error) as error:
        print ("Error while fetching data from PostgreSQL", error)

    finally:
        if cnx:
            cnx.commit()
            cnx.close()

# [END gae_python37_cloudsql_psql]


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5432, debug=True)