import os
import psycopg2

conn = psycopg2.connect(
        host="db-01.c5tpqhbcgvqu.eu-north-1.rds.amazonaws.com",
        database="postgres",
        user=os.environ['DB_USERNAME'],
        password=os.environ['DB_PASSWORD'])

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a command: this creates a new table
cur.execute('DROP TABLE IF EXISTS mentor_checklist;')
cur.execute('CREATE TABLE mentor_checklist (id BIGINT PRIMARY KEY,'
                                'cme_completion_date DATE,'
                                'cme_topic TEXT,'
                                'cme_unique_id BIGINT,'
                                'county TEXT,'
                                'date_submitted TIMESTAMP,'
                                'drill_topic TEXT,'
                                'drill_unique_id TEXT,'
                                'essential_cme_topic BOOLEAN,'
                                'essential_drill_topic BOOLEAN,'
                                'facility_code TEXT,'
                                'facility_name TEXT,'
                                'id_number_cme TEXT,'
                                'id_number_drill TEXT,'
                                'mentor_name TEXT,'
                                'submission_id BIGINT,'
                                'success_story TEXT);'
                                 )


conn.commit()

cur.close()
conn.close()
