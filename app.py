from flask import Flask, render_template, request, redirect
import boto3
import pymysql
import mysql.connector

app = Flask(__name__)

# Configure AWS S3 credentials
S3_BUCKET_NAME = "addinfostudent123"
AWS_ACCESS_KEY = "AKIASAVNSENFL7NTYDHR"
AWS_SECRET_KEY = "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"
AWS_REGION = "ap-south-1"

# Configure MySQL database credentials
DB_HOST = "stduent.ceqyug3pcotn.ap-south-1.rds.amazonaws.com"
DB_USER = "tejas"
DB_PASSWORD = "12345678"
DB_NAME = "student"

# Initialize AWS S3 client and MySQL connection
s3_client = boto3.client("s3", aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY, region_name=AWS_REGION)
db_connection = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            name = request.form["name"]
            student_id = request.form["id"]
            age = request.form["age"]
            branch = request.form["branch"]

            # Save student information to RDS database
            with db_connection.cursor() as cursor:
                sql = "INSERT INTO students (name, student_id, age, branch) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (name, student_id, age, branch))
                db_connection.commit()

            # Save image to S3 bucket
            if request.files:
                image = request.files["image"]
                image_path = f"students/{student_id}.jpg"
                s3_client.upload_fileobj(image, S3_BUCKET_NAME, image_path)

            return redirect("/success")
        except Exception as e:
            print(f"Error occurred: {e}")
            return redirect("/error")

    return render_template("index.html")

@app.route("/success")
def success():
    return render_template("success.html")

@app.route("/error")
def error():
    return render_template("error.html")

if __name__ == "__main__":
    app.run(debug=True)
