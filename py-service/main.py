from flask import Flask, request, jsonify
from pyspark.sql import SparkSession

app = Flask(__name__)
spark = SparkSession.builder.appName("Covid Report").getOrCreate()

@app.route("/generate-report", methods=["POST"])
def GenerateReport():
    data = request.get_json()
    country = data.get("country")
    
    confirmed_df = spark.read.csv("data/time_series_covid19_confirmed_global.csv", header=True)
    deaths_df = spark.read.csv("data/time_series_covid19_deaths_global.csv", header=True)
    recovered_df = spark.read.csv("data/time_series_covid19_recovered_global.csv", header=True)
    
    def get_total(df, country):
        df_filtered = df.filter(df["Country/Region"] == country)
        cols = df.columns[-1]
        total = df_filtered.select(cols).rdd.map(lambda row: int( row[0])).sum()
        return total
    
    try: 
        report = {
            "country" : country,
            "confirmed": get_total(confirmed_df, country),
            "deaths": get_total(deaths_df, country),
            "recovered": get_total(recovered_df, country)
        }
    except Exception as e:
        return jsonify({"error" : str(e)}), 500
    
    return jsonify(report)

if __name__ == "main":
    app.run(port=5000)