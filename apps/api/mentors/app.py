import os
from flask import Flask, jsonify
import pandas as pd
import psycopg2

app = Flask(__name__)

def get_db_connection():
  conn = psycopg2.connect(host="db-01.c5tpqhbcgvqu.eu-north-1.rds.amazonaws.com",
                            database="postgres",
                            user=os.environ['DB_USERNAME'],
                            password=os.environ['DB_PASSWORD'])
  return conn


def load_data_from_sheet(sheet_name):
  # Load data from the specified sheet in the Excel file
  
  df = pd.read_excel('mentor_checklist.xlsx', sheet_name=sheet_name)
  # Fill empty cells with empty string
  df.fillna('', inplace=True)
  return df

def transform_data(df):
  # Rename the columns of the dataframe to match the table structure
  df.rename(columns={
    'ID': 'id',
    'CME Completion Date': 'cme_completion_date',
    'CME Topic': 'cme_topic',
    'CME Unique ID': 'cme_unique_id',
    'County': 'county',
    'Date Submitted': 'date_submitted',
    'Drill Topic': 'drill_topic',
    'Drill Unique ID': 'drill_unique_id',
    'Essential CME Topic': 'essential_cme_topic',
    'Essential Drill Topic': 'essential_drill_topic',
    'Facility Code': 'facility_code',
    'Facility Name': 'facility_name',
    'ID Number CME': 'id_number_cme',
    'ID Number Drill': 'id_number_drill',
    'Mentor Name': 'mentor_name',
    'Submission ID': 'submission_id',
    'Success Story': 'success_story'
  }, inplace=True)

   # Convert the date columns to proper date format
  df['cme_completion_date'] = pd.to_datetime(df['cme_completion_date'])
  df['date_submitted'] = pd.to_datetime(df['date_submitted'])

  # Transform the data to fit into the table structure
  transformed_df = df[[
    'id', 'cme_completion_date', 'cme_topic', 'cme_unique_id', 'county', 'date_submitted', 'drill_topic',
    'drill_unique_id', 'essential_cme_topic', 'essential_drill_topic', 'facility_code', 'facility_name',
    'id_number_cme', 'id_number_drill', 'mentor_name', 'submission_id', 'success_story'
  ]]

  return transformed_df


def load_data_to_db(data):
  # Connect to the PostgreSQL database
  conn = get_db_connection()

  # Create a cursor
  cursor = conn.cursor()

  # Prepare the insert statement
  insert_query = """
    INSERT INTO mentor_checklist (
        id, cme_completion_date, cme_topic, cme_unique_id, county, date_submitted, drill_topic,
        drill_unique_id, essential_cme_topic, essential_drill_topic, facility_code, facility_name,
        id_number_cme, id_number_drill, mentor_name, submission_id, success_story
    ) VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
    )
  """
  # Load the data into the table
  for row in data.itertuples(index=False):
    values = (
      row.id, row.cme_completion_date, row.cme_topic, row.cme_unique_id, row.county, row.date_submitted,
      row.drill_topic, row.drill_unique_id, row.essential_cme_topic, row.essential_drill_topic,
      row.facility_code, row.facility_name, row.id_number_cme, row.id_number_drill, row.mentor_name,
      row.submission_id, row.success_story
    )

    # Check if the record already exists in the table based on the id
    select_query = "SELECT COUNT(*) FROM mentor_checklist WHERE id = %s"
    cursor.execute(select_query, (row.id,))
    result = cursor.fetchone()[0]
    if result == 0:  # If record does not exist, insert it into the table
      cursor.execute(insert_query, values)

  # Commit the changes
  conn.commit()

  # Close the cursor and connection
  cursor.close()
  conn.close()


@app.route('/')
def hello():
  return '<h1>Hello from Flask & Docker</h2>'

@app.route('/api/load_data', methods=['GET'])
def load_data():
  # Load the data from the Google Sheets
  data = load_data_from_sheet("Test Data")

  # Transform the data
  transformed_data = transform_data(data)

  # Load the transformed data into the database
  load_data_to_db(transformed_data)

  return jsonify({'message': 'Data loaded successfully'})


@app.route('/api/all', methods=['GET'])
def get_all_records():
  # Connect to the PostgreSQL database
  conn = get_db_connection()

  # Create a cursor
  cursor = conn.cursor()

  # Execute the select query
  select_query = "SELECT * FROM mentor_checklist"
  cursor.execute(select_query)

  # Fetch all rows
  rows = cursor.fetchall()

  # Close the cursor and connection
  cursor.close()
  conn.close()

  # Convert rows to list of dictionaries
  columns = [desc[0] for desc in cursor.description]
  result = [dict(zip(columns, row)) for row in rows]

  # Return the result as JSON response
  return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
