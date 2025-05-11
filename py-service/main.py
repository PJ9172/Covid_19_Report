from flask import Flask, request, jsonify
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as spark_sum, max as spark_max

app = Flask(__name__)
spark = SparkSession.builder.appName("Covid Report").getOrCreate()

# load and cache data
confirmed_df = (
    spark.read.parquet("data/time_series_covid19_confirmed_global.parquet")
    .withColumnRenamed("Province/State", "Province_State")
    .withColumnRenamed("Country/Region", "Country_Region")
    .cache()
)

deaths_df = (
    spark.read.parquet("data/time_series_covid19_deaths_global.parquet")
    .withColumnRenamed("Province/State", "Province_State")
    .withColumnRenamed("Country/Region", "Country_Region")
    .cache()
)
recovered_df = (
    spark.read.parquet("data/time_series_covid19_recovered_global.parquet")
    .withColumnRenamed("Province/State", "Province_State")
    .withColumnRenamed("Country/Region", "Country_Region")
    .cache()
)

# utility functions
def get_total(df, country):
    try:
        df_filtered = df.filter(col("Country_Region") == country)
        if df_filtered.count() == 0:
            return 0
        last_col = df.columns[-1]
        df_filtered = df_filtered.withColumn(last_col, col(last_col).cast("int"))
        total = df_filtered.agg(spark_max(col(last_col))).collect()[0][0]
        return total if total else 0
    except Exception as e:
        print(f"Error getting total for {country}: {e}" )
        return 0

def melt(df, id_vars, var_name="variable", value_name="value" ):
    # Simulate pandas melt (unpivot wide format to long)
    value_columns = [c for c in df.columns if c not in id_vars]
    kv_expr = ", ".join([f"'{c}', {c}" for c in value_columns])
    return df.selectExpr(*id_vars, f"stack({len(value_columns)}, {kv_expr}) as ({var_name}, {value_name})")


# Melt and pre-aggregate recovered once
melted_recovered_df = (
    melt(recovered_df, ["Province_State", "Country_Region", "Lat", "Long"])
    .filter(col("value").cast("float") > 0.0)
    .groupBy("Country_Region")
    .agg(spark_max("value").alias("max_recovered"))
    .cache()
)


def get_valid_recovered(country, confirmed):
    print(f"Looking for recovered data for: {country}")
    row = melted_recovered_df.filter(col("Country_Region").contains(country)).first()
    if row:
        recovery_ratio = float(row["max_recovered"])
        recovered_estimate = int(recovery_ratio * confirmed)
        return recovered_estimate
    else:
        return 0


# Flask API
@app.route("/report", methods=["POST"])
def GenerateReport():
    data = request.get_json()
    country = data.get("country")
    try:
        confirmed = get_total(confirmed_df, country)
        deaths = get_total(deaths_df, country)
        recovered = get_valid_recovered(country, confirmed)

        report = {
            "country": country,
            "confirmed": str(confirmed),
            "deaths": str(deaths),
            "recovered": str(recovered)
        }
        return jsonify(report)
    except Exception as e:
        print(f"Server error: {e}")
        return jsonify({"error": str(e)}), 500
    
if __name__ == "__main__":
    app.run(port=5000)