import csv
import json

# --- Paste your JSON response here ---
data = {
    "message": "Query executed successfully",
    "rows": [
        {
            "date": "2025-01-31 00:00:00",
            "material_code": "100661-000000",
            "price_per_uom": "707.5",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-10-01",
            "material_code": "100055-000000",
            "price_per_uom": "369.12",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-11-01",
            "material_code": "100055-000000",
            "price_per_uom": "346.26",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2025-07-04",
            "material_code": "100724-000000",
            "price_per_uom": "286.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-12-01",
            "material_code": "100055-000000",
            "price_per_uom": "346.47",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2025-06-01",
            "material_code": "100055-000000",
            "price_per_uom": "254",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2025-05-01",
            "material_code": "100055-000000",
            "price_per_uom": "251.2",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2025-01-01",
            "material_code": "100055-000000",
            "price_per_uom": "302.3",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2025-09-11 00:00:00",
            "material_code": "102089-000000",
            "price_per_uom": "1250.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-08-30 00:00:00",
            "material_code": "100661-000000",
            "price_per_uom": "1012.5",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-03-01",
            "material_code": "100055-000000",
            "price_per_uom": "378.45",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-08-01",
            "material_code": "100055-000000",
            "price_per_uom": "350.01",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-04-01",
            "material_code": "100055-000000",
            "price_per_uom": "356.6",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-09-01",
            "material_code": "100055-000000",
            "price_per_uom": "347.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-05-01",
            "material_code": "100055-000000",
            "price_per_uom": "371.92",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-06-01",
            "material_code": "100055-000000",
            "price_per_uom": "370.03",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-07-01",
            "material_code": "100055-000000",
            "price_per_uom": "348.34",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-09-27 00:00:00",
            "material_code": "100661-000000",
            "price_per_uom": "850.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-08-01",
            "material_code": "100055-000000",
            "price_per_uom": "325.24",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-09-01",
            "material_code": "100055-000000",
            "price_per_uom": "350.84",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-10-01",
            "material_code": "100055-000000",
            "price_per_uom": "349.64",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-11-01",
            "material_code": "100055-000000",
            "price_per_uom": "343.48",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-12-01",
            "material_code": "100055-000000",
            "price_per_uom": "349.54",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-01-01",
            "material_code": "100055-000000",
            "price_per_uom": "360.6",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-02-01",
            "material_code": "100055-000000",
            "price_per_uom": "370.21",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-07-26 00:00:00",
            "material_code": "100661-000000",
            "price_per_uom": "1020.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2025-01-01",
            "material_code": "100519-000000",
            "price_per_uom": "912",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2025-02-01",
            "material_code": "100519-000000",
            "price_per_uom": "925",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2025-03-01",
            "material_code": "100519-000000",
            "price_per_uom": "851",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-04-26 00:00:00",
            "material_code": "100661-000000",
            "price_per_uom": "1060.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-06-28 00:00:00",
            "material_code": "100661-000000",
            "price_per_uom": "1070.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2025-04-01",
            "material_code": "100519-000000",
            "price_per_uom": "790",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2025-05-01",
            "material_code": "100519-000000",
            "price_per_uom": "723",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2025-06-01",
            "material_code": "100519-000000",
            "price_per_uom": "746",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2025-07-01",
            "material_code": "100519-000000",
            "price_per_uom": "720",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2025-08-01",
            "material_code": "100519-000000",
            "price_per_uom": "749",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2025-01-01",
            "material_code": "101881-000000",
            "price_per_uom": "869",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2025-02-01",
            "material_code": "101881-000000",
            "price_per_uom": "863",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2025-03-01",
            "material_code": "101881-000000",
            "price_per_uom": "843",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2025-04-01",
            "material_code": "101881-000000",
            "price_per_uom": "830",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2025-05-01",
            "material_code": "101881-000000",
            "price_per_uom": "812",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2025-06-01",
            "material_code": "101881-000000",
            "price_per_uom": "766",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2025-07-01",
            "material_code": "101881-000000",
            "price_per_uom": "755",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2025-08-01",
            "material_code": "101881-000000",
            "price_per_uom": "751",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2025-09-30",
            "material_code": "100661-000000",
            "price_per_uom": "560.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2025-02-01",
            "material_code": "100055-000000",
            "price_per_uom": "304",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2025-03-01",
            "material_code": "100055-000000",
            "price_per_uom": "301",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2025-04-01",
            "material_code": "100055-000000",
            "price_per_uom": "281",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2025-06-27 00:00:00",
            "material_code": "100661-000000",
            "price_per_uom": "750.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2025-07-01",
            "material_code": "100055-000000",
            "price_per_uom": "327.5",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-11-29 00:00:00",
            "material_code": "100661-000000",
            "price_per_uom": "780.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2025-08-01 00:00:00",
            "material_code": "100055-000000",
            "price_per_uom": "318.5",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2025-05-08 00:00:00",
            "material_code": "102089-000000",
            "price_per_uom": "859.00",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2025-07-04 00:00:00",
            "material_code": "100661-000000",
            "price_per_uom": "540.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-05-01 00:00:00",
            "material_code": "100661-000000",
            "price_per_uom": "1070.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-02-23 00:00:00",
            "material_code": "100661-000000",
            "price_per_uom": "1030.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-12-20 00:00:00",
            "material_code": "101834-000000",
            "price_per_uom": "900.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2025-08-01 00:00:00",
            "material_code": "101834-000000",
            "price_per_uom": "830",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2025-07-18 00:00:00",
            "material_code": "101834-000000",
            "price_per_uom": "865",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2025-08-01 00:00:00",
            "material_code": "100661-000000",
            "price_per_uom": "710.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2025-08-01 00:00:00",
            "material_code": "100519-000000",
            "price_per_uom": "720.0",
            "region": "China",
            "currency": "USD"
        },
        {
            "date": "2025-08-01 00:00:00",
            "material_code": "102089-000000",
            "price_per_uom": "1120.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-01-01",
            "material_code": "102089-000000",
            "price_per_uom": "515.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-01-01",
            "material_code": "100724-000000",
            "price_per_uom": "374.5",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-01-01",
            "material_code": "100060-000000",
            "price_per_uom": "691.5",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-01-01",
            "material_code": "100661-000000",
            "price_per_uom": "684.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-01-01",
            "material_code": "101834-000000",
            "price_per_uom": "865.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-01-01",
            "material_code": "101881-000000",
            "price_per_uom": "950.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-01-01",
            "material_code": "100055-000000",
            "price_per_uom": "336.49",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-02-01",
            "material_code": "102089-000000",
            "price_per_uom": "532.5",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-02-01",
            "material_code": "100724-000000",
            "price_per_uom": "375.625",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-02-01",
            "material_code": "100060-000000",
            "price_per_uom": "666.25",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-02-01",
            "material_code": "100661-000000",
            "price_per_uom": "706.3",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-02-01",
            "material_code": "101834-000000",
            "price_per_uom": "920.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-02-01",
            "material_code": "101881-000000",
            "price_per_uom": "810.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-02-01",
            "material_code": "100055-000000",
            "price_per_uom": "307.32",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-03-01",
            "material_code": "102089-000000",
            "price_per_uom": "548.8",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-03-01",
            "material_code": "100724-000000",
            "price_per_uom": "340.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-03-01",
            "material_code": "100060-000000",
            "price_per_uom": "650.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-03-01",
            "material_code": "100661-000000",
            "price_per_uom": "643.8",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-03-01",
            "material_code": "101834-000000",
            "price_per_uom": "795.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-03-01",
            "material_code": "101881-000000",
            "price_per_uom": "780.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-03-01",
            "material_code": "100055-000000",
            "price_per_uom": "286.76",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-04-01",
            "material_code": "102089-000000",
            "price_per_uom": "875.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-04-01",
            "material_code": "100724-000000",
            "price_per_uom": "313.75",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-04-01",
            "material_code": "100060-000000",
            "price_per_uom": "603.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-04-01",
            "material_code": "100661-000000",
            "price_per_uom": "590.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-04-01",
            "material_code": "101834-000000",
            "price_per_uom": "665.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-04-01",
            "material_code": "101881-000000",
            "price_per_uom": "560.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-04-01",
            "material_code": "100055-000000",
            "price_per_uom": "226.27",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-05-01",
            "material_code": "102089-000000",
            "price_per_uom": "1001.3",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-05-01",
            "material_code": "100724-000000",
            "price_per_uom": "326.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-05-01",
            "material_code": "100060-000000",
            "price_per_uom": "602.5",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-05-01",
            "material_code": "100661-000000",
            "price_per_uom": "784.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-05-01",
            "material_code": "101834-000000",
            "price_per_uom": "700.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-05-01",
            "material_code": "101881-000000",
            "price_per_uom": "680.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-05-01",
            "material_code": "100055-000000",
            "price_per_uom": "244.95",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-06-01",
            "material_code": "102089-000000",
            "price_per_uom": "823.8",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-06-01",
            "material_code": "100724-000000",
            "price_per_uom": "315.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-06-01",
            "material_code": "100060-000000",
            "price_per_uom": "612.5",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-06-01",
            "material_code": "100661-000000",
            "price_per_uom": "928.8",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-06-01",
            "material_code": "101834-000000",
            "price_per_uom": "840.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-06-01",
            "material_code": "101881-000000",
            "price_per_uom": "720.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-06-01",
            "material_code": "100055-000000",
            "price_per_uom": "216.04",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-07-01",
            "material_code": "102089-000000",
            "price_per_uom": "607.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-07-01",
            "material_code": "100724-000000",
            "price_per_uom": "337.5",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-07-01",
            "material_code": "100060-000000",
            "price_per_uom": "627.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-07-01",
            "material_code": "100661-000000",
            "price_per_uom": "953.5",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-07-01",
            "material_code": "101834-000000",
            "price_per_uom": "630.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-07-01",
            "material_code": "101881-000000",
            "price_per_uom": "780.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-07-01",
            "material_code": "100055-000000",
            "price_per_uom": "230.37",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-08-01",
            "material_code": "102089-000000",
            "price_per_uom": "610.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-08-01",
            "material_code": "100724-000000",
            "price_per_uom": "337.5",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-08-01",
            "material_code": "100060-000000",
            "price_per_uom": "617.5",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-08-01",
            "material_code": "100661-000000",
            "price_per_uom": "892.5",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-08-01",
            "material_code": "101834-000000",
            "price_per_uom": "625.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-08-01",
            "material_code": "101881-000000",
            "price_per_uom": "780.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-08-01",
            "material_code": "100055-000000",
            "price_per_uom": "236.64",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-09-01",
            "material_code": "102089-000000",
            "price_per_uom": "642.5",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-09-01",
            "material_code": "100724-000000",
            "price_per_uom": "361.25",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-09-01",
            "material_code": "100060-000000",
            "price_per_uom": "638.75",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-09-01",
            "material_code": "100661-000000",
            "price_per_uom": "885.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-09-01",
            "material_code": "101834-000000",
            "price_per_uom": "625.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-09-01",
            "material_code": "101881-000000",
            "price_per_uom": "850.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-09-01",
            "material_code": "100055-000000",
            "price_per_uom": "275.17",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-10-01",
            "material_code": "102089-000000",
            "price_per_uom": "667.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-10-01",
            "material_code": "100724-000000",
            "price_per_uom": "386.5",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-10-01",
            "material_code": "100060-000000",
            "price_per_uom": "696.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-10-01",
            "material_code": "100661-000000",
            "price_per_uom": "908.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-10-01",
            "material_code": "101834-000000",
            "price_per_uom": "645.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-10-01",
            "material_code": "101881-000000",
            "price_per_uom": "860.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-10-01",
            "material_code": "100055-000000",
            "price_per_uom": "284.07",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-11-01",
            "material_code": "102089-000000",
            "price_per_uom": "707.5",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-11-01",
            "material_code": "100724-000000",
            "price_per_uom": "426.25",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-11-01",
            "material_code": "100060-000000",
            "price_per_uom": "933.75",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-11-01",
            "material_code": "100661-000000",
            "price_per_uom": "963.8",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-11-01",
            "material_code": "101834-000000",
            "price_per_uom": "750.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-11-01",
            "material_code": "101881-000000",
            "price_per_uom": "850.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-11-01",
            "material_code": "100055-000000",
            "price_per_uom": "297.61",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-12-01",
            "material_code": "102089-000000",
            "price_per_uom": "732.5",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-12-01",
            "material_code": "100724-000000",
            "price_per_uom": "673.75",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-12-01",
            "material_code": "100060-000000",
            "price_per_uom": "1078.75",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-12-01",
            "material_code": "100661-000000",
            "price_per_uom": "1053.8",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-12-01",
            "material_code": "101834-000000",
            "price_per_uom": "850.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-12-01",
            "material_code": "101881-000000",
            "price_per_uom": "940.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-12-01",
            "material_code": "100055-000000",
            "price_per_uom": "343.26",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-01-01",
            "material_code": "102089-000000",
            "price_per_uom": "743.8",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-01-01",
            "material_code": "100724-000000",
            "price_per_uom": "645.625",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-01-01",
            "material_code": "100060-000000",
            "price_per_uom": "1238.75",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-01-01",
            "material_code": "100661-000000",
            "price_per_uom": "992.5",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-01-01",
            "material_code": "101834-000000",
            "price_per_uom": "875.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-01-01",
            "material_code": "101881-000000",
            "price_per_uom": "920.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-01-01",
            "material_code": "100055-000000",
            "price_per_uom": "394.6",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-02-01",
            "material_code": "102089-000000",
            "price_per_uom": "756.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-02-01",
            "material_code": "100724-000000",
            "price_per_uom": "812.5",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-02-01",
            "material_code": "100060-000000",
            "price_per_uom": "1370.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-02-01",
            "material_code": "100661-000000",
            "price_per_uom": "1085.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-02-01",
            "material_code": "101834-000000",
            "price_per_uom": "925.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-02-01",
            "material_code": "101881-000000",
            "price_per_uom": "930.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-02-01",
            "material_code": "100055-000000",
            "price_per_uom": "369.69",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-03-01",
            "material_code": "102089-000000",
            "price_per_uom": "854.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-03-01",
            "material_code": "100724-000000",
            "price_per_uom": "973.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-03-01",
            "material_code": "100060-000000",
            "price_per_uom": "1862.5",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-03-01",
            "material_code": "100661-000000",
            "price_per_uom": "1280.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-03-01",
            "material_code": "101834-000000",
            "price_per_uom": "1150.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-03-01",
            "material_code": "101881-000000",
            "price_per_uom": "1150.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-03-01",
            "material_code": "100055-000000",
            "price_per_uom": "395.41",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-04-01",
            "material_code": "102089-000000",
            "price_per_uom": "1040.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-04-01",
            "material_code": "100724-000000",
            "price_per_uom": "997.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-04-01",
            "material_code": "100060-000000",
            "price_per_uom": "1655.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-04-01",
            "material_code": "100661-000000",
            "price_per_uom": "1305.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-04-01",
            "material_code": "101834-000000",
            "price_per_uom": "1200.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-04-01",
            "material_code": "101881-000000",
            "price_per_uom": "1060.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-04-01",
            "material_code": "100055-000000",
            "price_per_uom": "367.9",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-05-01",
            "material_code": "102089-000000",
            "price_per_uom": "1120.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-05-01",
            "material_code": "100724-000000",
            "price_per_uom": "1040.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-05-01",
            "material_code": "100060-000000",
            "price_per_uom": "1793.75",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-05-01",
            "material_code": "100661-000000",
            "price_per_uom": "1237.5",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-05-01",
            "material_code": "101834-000000",
            "price_per_uom": "1300.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-05-01",
            "material_code": "101881-000000",
            "price_per_uom": "1090.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-05-01",
            "material_code": "100055-000000",
            "price_per_uom": "393.5",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-06-01",
            "material_code": "102089-000000",
            "price_per_uom": "1110.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-06-01",
            "material_code": "100724-000000",
            "price_per_uom": "1018.75",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-06-01",
            "material_code": "100060-000000",
            "price_per_uom": "1843.75",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-06-01",
            "material_code": "100661-000000",
            "price_per_uom": "1028.8",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-06-01",
            "material_code": "101834-000000",
            "price_per_uom": "1150.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-06-01",
            "material_code": "101881-000000",
            "price_per_uom": "920.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-06-01",
            "material_code": "100055-000000",
            "price_per_uom": "435.74",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-07-01",
            "material_code": "102089-000000",
            "price_per_uom": "1064.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-07-01",
            "material_code": "100724-000000",
            "price_per_uom": "897.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-07-01",
            "material_code": "100060-000000",
            "price_per_uom": "1880.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-07-01",
            "material_code": "100661-000000",
            "price_per_uom": "864.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-07-01",
            "material_code": "101834-000000",
            "price_per_uom": "1230.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-07-01",
            "material_code": "101881-000000",
            "price_per_uom": "940.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-07-01",
            "material_code": "100055-000000",
            "price_per_uom": "409.18",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-08-01",
            "material_code": "102089-000000",
            "price_per_uom": "1189.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-08-01",
            "material_code": "100724-000000",
            "price_per_uom": "861.25",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-08-01",
            "material_code": "100060-000000",
            "price_per_uom": "1950.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-08-01",
            "material_code": "100661-000000",
            "price_per_uom": "822.5",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-08-01",
            "material_code": "101834-000000",
            "price_per_uom": "1215.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-08-01",
            "material_code": "101881-000000",
            "price_per_uom": "940.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-08-01",
            "material_code": "100055-000000",
            "price_per_uom": "424.48",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-09-01",
            "material_code": "102089-000000",
            "price_per_uom": "1382.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-09-01",
            "material_code": "100724-000000",
            "price_per_uom": "973.75",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-09-01",
            "material_code": "100060-000000",
            "price_per_uom": "1940.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-09-01",
            "material_code": "100661-000000",
            "price_per_uom": "839.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-09-01",
            "material_code": "101834-000000",
            "price_per_uom": "1425.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-09-01",
            "material_code": "101881-000000",
            "price_per_uom": "940.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-09-01",
            "material_code": "100055-000000",
            "price_per_uom": "424.32",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-10-01",
            "material_code": "102089-000000",
            "price_per_uom": "1736.3",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-10-01",
            "material_code": "100724-000000",
            "price_per_uom": "1227.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-10-01",
            "material_code": "100060-000000",
            "price_per_uom": "1750.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-10-01",
            "material_code": "100661-000000",
            "price_per_uom": "902.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-10-01",
            "material_code": "101834-000000",
            "price_per_uom": "1375.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-10-01",
            "material_code": "101881-000000",
            "price_per_uom": "1020.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-10-01",
            "material_code": "100055-000000",
            "price_per_uom": "467.98",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-11-01",
            "material_code": "102089-000000",
            "price_per_uom": "1948.8",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-11-01",
            "material_code": "100724-000000",
            "price_per_uom": "1052.5",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-11-01",
            "material_code": "100060-000000",
            "price_per_uom": "1662.5",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-11-01",
            "material_code": "100661-000000",
            "price_per_uom": "893.8",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-11-01",
            "material_code": "101834-000000",
            "price_per_uom": "1250.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-11-01",
            "material_code": "101881-000000",
            "price_per_uom": "960.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-11-01",
            "material_code": "100055-000000",
            "price_per_uom": "449.94",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-12-01",
            "material_code": "102089-000000",
            "price_per_uom": "1803.75",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-12-01",
            "material_code": "100724-000000",
            "price_per_uom": "885.625",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-12-01",
            "material_code": "100060-000000",
            "price_per_uom": "1371.25",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-12-01",
            "material_code": "100661-000000",
            "price_per_uom": "835.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-12-01",
            "material_code": "101834-000000",
            "price_per_uom": "1225.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-12-01",
            "material_code": "101881-000000",
            "price_per_uom": "900.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-12-01",
            "material_code": "100055-000000",
            "price_per_uom": "439.55",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-01-01",
            "material_code": "102089-000000",
            "price_per_uom": "1631.3",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-01-01",
            "material_code": "100724-000000",
            "price_per_uom": "801.25",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-01-01",
            "material_code": "100060-000000",
            "price_per_uom": "1275.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-01-01",
            "material_code": "100661-000000",
            "price_per_uom": "822.5",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-01-01",
            "material_code": "101834-000000",
            "price_per_uom": "1475.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-01-01",
            "material_code": "101881-000000",
            "price_per_uom": "950.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-01-01",
            "material_code": "100055-000000",
            "price_per_uom": "416.18",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-02-01",
            "material_code": "102089-000000",
            "price_per_uom": "1725.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-02-01",
            "material_code": "100724-000000",
            "price_per_uom": "705.625",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-02-01",
            "material_code": "100060-000000",
            "price_per_uom": "1362.5",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-02-01",
            "material_code": "100661-000000",
            "price_per_uom": "875.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-02-01",
            "material_code": "101834-000000",
            "price_per_uom": "1495.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-02-01",
            "material_code": "101881-000000",
            "price_per_uom": "1200.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-02-01",
            "material_code": "100055-000000",
            "price_per_uom": "449.35",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-03-01",
            "material_code": "102089-000000",
            "price_per_uom": "1961.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-03-01",
            "material_code": "100724-000000",
            "price_per_uom": "701.875",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-03-01",
            "material_code": "100060-000000",
            "price_per_uom": "1470.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-03-01",
            "material_code": "100661-000000",
            "price_per_uom": "986.3",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-03-01",
            "material_code": "101834-000000",
            "price_per_uom": "1555.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-03-01",
            "material_code": "101881-000000",
            "price_per_uom": "1320.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-03-01",
            "material_code": "100055-000000",
            "price_per_uom": "516.9",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-04-01",
            "material_code": "102089-000000",
            "price_per_uom": "1812.5",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-04-01",
            "material_code": "100724-000000",
            "price_per_uom": "784.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-04-01",
            "material_code": "100060-000000",
            "price_per_uom": "1462.5",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-04-01",
            "material_code": "100661-000000",
            "price_per_uom": "962.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-04-01",
            "material_code": "101834-000000",
            "price_per_uom": "1455.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-04-01",
            "material_code": "101881-000000",
            "price_per_uom": "1290.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-04-01",
            "material_code": "100055-000000",
            "price_per_uom": "482.16",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-05-01",
            "material_code": "102089-000000",
            "price_per_uom": "1965.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-05-01",
            "material_code": "100724-000000",
            "price_per_uom": "730.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-05-01",
            "material_code": "100060-000000",
            "price_per_uom": "1487.5",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-05-01",
            "material_code": "100661-000000",
            "price_per_uom": "955.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-05-01",
            "material_code": "101834-000000",
            "price_per_uom": "1425.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-05-01",
            "material_code": "101881-000000",
            "price_per_uom": "1200.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-05-01",
            "material_code": "100055-000000",
            "price_per_uom": "421.71",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-06-01",
            "material_code": "102089-000000",
            "price_per_uom": "1730.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-06-01",
            "material_code": "100724-000000",
            "price_per_uom": "703.75",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-06-01",
            "material_code": "100060-000000",
            "price_per_uom": "1418.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-06-01",
            "material_code": "100661-000000",
            "price_per_uom": "960.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-06-01",
            "material_code": "101834-000000",
            "price_per_uom": "1475.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-06-01",
            "material_code": "101881-000000",
            "price_per_uom": "1040.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-06-01",
            "material_code": "100055-000000",
            "price_per_uom": "427.14",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-07-01",
            "material_code": "102089-000000",
            "price_per_uom": "1077.5",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-07-01",
            "material_code": "100724-000000",
            "price_per_uom": "581.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-07-01",
            "material_code": "100060-000000",
            "price_per_uom": "1118.75",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-07-01",
            "material_code": "100661-000000",
            "price_per_uom": "952.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-07-01",
            "material_code": "101834-000000",
            "price_per_uom": "1225.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-07-01",
            "material_code": "101881-000000",
            "price_per_uom": "950.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-07-01",
            "material_code": "100055-000000",
            "price_per_uom": "377.24",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-08-01",
            "material_code": "102089-000000",
            "price_per_uom": "908.8",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-08-01",
            "material_code": "100724-000000",
            "price_per_uom": "531.25",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-08-01",
            "material_code": "100060-000000",
            "price_per_uom": "962.5",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-08-01",
            "material_code": "100661-000000",
            "price_per_uom": "875.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-08-01",
            "material_code": "101834-000000",
            "price_per_uom": "1180.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-08-01",
            "material_code": "101881-000000",
            "price_per_uom": "890.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-08-01",
            "material_code": "100055-000000",
            "price_per_uom": "374.18",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-09-01",
            "material_code": "102089-000000",
            "price_per_uom": "927.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-09-01",
            "material_code": "100724-000000",
            "price_per_uom": "495.5",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-09-01",
            "material_code": "100060-000000",
            "price_per_uom": "934.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-09-01",
            "material_code": "100661-000000",
            "price_per_uom": "837.5",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-09-01",
            "material_code": "101834-000000",
            "price_per_uom": "1240.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-09-01",
            "material_code": "101881-000000",
            "price_per_uom": "890.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-09-01",
            "material_code": "100055-000000",
            "price_per_uom": "373.62",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-10-01",
            "material_code": "102089-000000",
            "price_per_uom": "755.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-10-01",
            "material_code": "100724-000000",
            "price_per_uom": "476.25",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-10-01",
            "material_code": "100060-000000",
            "price_per_uom": "950.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-10-01",
            "material_code": "100661-000000",
            "price_per_uom": "818.8",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-10-01",
            "material_code": "101834-000000",
            "price_per_uom": "1190.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-10-01",
            "material_code": "101881-000000",
            "price_per_uom": "890.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-10-01",
            "material_code": "100055-000000",
            "price_per_uom": "397.78",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-11-01",
            "material_code": "102089-000000",
            "price_per_uom": "625.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-11-01",
            "material_code": "100724-000000",
            "price_per_uom": "475.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-11-01",
            "material_code": "100060-000000",
            "price_per_uom": "950.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-11-01",
            "material_code": "100661-000000",
            "price_per_uom": "785.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-11-01",
            "material_code": "101834-000000",
            "price_per_uom": "1075.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-11-01",
            "material_code": "101881-000000",
            "price_per_uom": "850.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-11-01",
            "material_code": "100055-000000",
            "price_per_uom": "396.14",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-12-01",
            "material_code": "102089-000000",
            "price_per_uom": "650.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-12-01",
            "material_code": "100724-000000",
            "price_per_uom": "440.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-12-01",
            "material_code": "100060-000000",
            "price_per_uom": "935.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-12-01",
            "material_code": "100661-000000",
            "price_per_uom": "790.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-12-01",
            "material_code": "101834-000000",
            "price_per_uom": "955.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-12-01",
            "material_code": "101881-000000",
            "price_per_uom": "880.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-12-01",
            "material_code": "100055-000000",
            "price_per_uom": "392.04",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-01-01",
            "material_code": "102089-000000",
            "price_per_uom": "700.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-01-01",
            "material_code": "100724-000000",
            "price_per_uom": "440.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-01-01",
            "material_code": "100060-000000",
            "price_per_uom": "975.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-01-01",
            "material_code": "100661-000000",
            "price_per_uom": "790.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-01-01",
            "material_code": "101834-000000",
            "price_per_uom": "910.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-01-01",
            "material_code": "101881-000000",
            "price_per_uom": "880.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-01-01",
            "material_code": "100055-000000",
            "price_per_uom": "392.33",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-02-01",
            "material_code": "102089-000000",
            "price_per_uom": "710.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-02-01",
            "material_code": "100724-000000",
            "price_per_uom": "445.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-02-01",
            "material_code": "100060-000000",
            "price_per_uom": "1005.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-02-01",
            "material_code": "100661-000000",
            "price_per_uom": "833.8",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-02-01",
            "material_code": "101834-000000",
            "price_per_uom": "1000.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-02-01",
            "material_code": "101881-000000",
            "price_per_uom": "980.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-02-01",
            "material_code": "100055-000000",
            "price_per_uom": "398.09",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-03-01",
            "material_code": "102089-000000",
            "price_per_uom": "640.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-03-01",
            "material_code": "100060-000000",
            "price_per_uom": "975.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-03-01",
            "material_code": "100661-000000",
            "price_per_uom": "915.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-03-01",
            "material_code": "101834-000000",
            "price_per_uom": "940.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-03-01",
            "material_code": "101881-000000",
            "price_per_uom": "920.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-03-01",
            "material_code": "100055-000000",
            "price_per_uom": "392.27",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-04-01",
            "material_code": "102089-000000",
            "price_per_uom": "650.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-04-01",
            "material_code": "100724-000000",
            "price_per_uom": "447.5",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-04-01",
            "material_code": "100060-000000",
            "price_per_uom": "980.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-04-01",
            "material_code": "100661-000000",
            "price_per_uom": "915.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-04-01",
            "material_code": "101834-000000",
            "price_per_uom": "900.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-04-01",
            "material_code": "101881-000000",
            "price_per_uom": "940.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-04-01",
            "material_code": "100055-000000",
            "price_per_uom": "369.57",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-05-01",
            "material_code": "102089-000000",
            "price_per_uom": "660.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-05-01",
            "material_code": "100060-000000",
            "price_per_uom": "975.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-05-01",
            "material_code": "100661-000000",
            "price_per_uom": "932.5",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-05-01",
            "material_code": "101834-000000",
            "price_per_uom": "880.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-05-01",
            "material_code": "101881-000000",
            "price_per_uom": "890.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-05-01",
            "material_code": "100055-000000",
            "price_per_uom": "353.05",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-09-01",
            "material_code": "101834-000000",
            "price_per_uom": "1050.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-09-01",
            "material_code": "101881-000000",
            "price_per_uom": "805.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-08-01",
            "material_code": "101834-000000",
            "price_per_uom": "925.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-01-01",
            "material_code": "102089-000000",
            "price_per_uom": "575.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-12-01",
            "material_code": "102089-000000",
            "price_per_uom": "545.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-12-01",
            "material_code": "100724-000000",
            "price_per_uom": "452.5",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-12-01",
            "material_code": "100060-000000",
            "price_per_uom": "1000.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-12-01",
            "material_code": "100661-000000",
            "price_per_uom": "905.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-12-01",
            "material_code": "101834-000000",
            "price_per_uom": "905.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-10-01",
            "material_code": "102089-000000",
            "price_per_uom": "590.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-06-01",
            "material_code": "102089-000000",
            "price_per_uom": "640.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-06-01",
            "material_code": "100724-000000",
            "price_per_uom": "425.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-06-01",
            "material_code": "100060-000000",
            "price_per_uom": "870.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-06-01",
            "material_code": "100661-000000",
            "price_per_uom": "825.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-06-01",
            "material_code": "101834-000000",
            "price_per_uom": "825.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-06-01",
            "material_code": "101881-000000",
            "price_per_uom": "778.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-06-01",
            "material_code": "100055-000000",
            "price_per_uom": "304.52",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-10-01",
            "material_code": "100724-000000",
            "price_per_uom": "475.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-10-01",
            "material_code": "100060-000000",
            "price_per_uom": "1000.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-10-01",
            "material_code": "100661-000000",
            "price_per_uom": "920.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-10-01",
            "material_code": "101834-000000",
            "price_per_uom": "975.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-10-01",
            "material_code": "101881-000000",
            "price_per_uom": "794.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-12-01",
            "material_code": "101881-000000",
            "price_per_uom": "804.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-08-01",
            "material_code": "102089-000000",
            "price_per_uom": "625.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-08-01",
            "material_code": "100724-000000",
            "price_per_uom": "480.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-08-01",
            "material_code": "100060-000000",
            "price_per_uom": "960.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-08-01",
            "material_code": "100661-000000",
            "price_per_uom": "865.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-08-01",
            "material_code": "101881-000000",
            "price_per_uom": "854.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-01-01",
            "material_code": "100724-000000",
            "price_per_uom": "455.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-01-01",
            "material_code": "100060-000000",
            "price_per_uom": "1085.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-01-01",
            "material_code": "100661-000000",
            "price_per_uom": "960.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-01-01",
            "material_code": "101881-000000",
            "price_per_uom": "998.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-09-01",
            "material_code": "102089-000000",
            "price_per_uom": "615.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-09-01",
            "material_code": "100724-000000",
            "price_per_uom": "612.5",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-09-01",
            "material_code": "100060-000000",
            "price_per_uom": "1050.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-09-01",
            "material_code": "100661-000000",
            "price_per_uom": "925.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-11-01",
            "material_code": "102089-000000",
            "price_per_uom": "570.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-11-01",
            "material_code": "100724-000000",
            "price_per_uom": "435.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-11-01",
            "material_code": "100060-000000",
            "price_per_uom": "975.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-11-01",
            "material_code": "100661-000000",
            "price_per_uom": "930.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-11-01",
            "material_code": "101834-000000",
            "price_per_uom": "925.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-11-01",
            "material_code": "101881-000000",
            "price_per_uom": "804.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-01-26 00:00:00",
            "material_code": "101834-000000",
            "price_per_uom": "865.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-02-01",
            "material_code": "101881-000000",
            "price_per_uom": "860.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-03-01",
            "material_code": "102089-000000",
            "price_per_uom": "625.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-02-01",
            "material_code": "102089-000000",
            "price_per_uom": "585.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-02-01",
            "material_code": "100060-000000",
            "price_per_uom": "1082.5",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-02-23 00:00:00",
            "material_code": "101834-000000",
            "price_per_uom": "940.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-03-29 00:00:00",
            "material_code": "100724-000000",
            "price_per_uom": "452.5",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-03-01",
            "material_code": "100060-000000",
            "price_per_uom": "1030.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-03-01",
            "material_code": "101881-000000",
            "price_per_uom": "844.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-03-01 00:00:00",
            "material_code": "100661-000000",
            "price_per_uom": "1040.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-04-01",
            "material_code": "102089-000000",
            "price_per_uom": "605.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-04-26 00:00:00",
            "material_code": "100724-000000",
            "price_per_uom": "475.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-04-01",
            "material_code": "100060-000000",
            "price_per_uom": "1045.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-04-01",
            "material_code": "101834-000000",
            "price_per_uom": "945.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-04-01",
            "material_code": "101881-000000",
            "price_per_uom": "827.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-05-01",
            "material_code": "102089-000000",
            "price_per_uom": "595.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-05-01",
            "material_code": "100724-000000",
            "price_per_uom": "450.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-05-01",
            "material_code": "100060-000000",
            "price_per_uom": "1067.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-05-01",
            "material_code": "101881-000000",
            "price_per_uom": "827.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-06-05",
            "material_code": "100060-000000",
            "price_per_uom": "1075.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-06-05",
            "material_code": "101881-000000",
            "price_per_uom": "818.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-06-15 00:00:00",
            "material_code": "101834-000000",
            "price_per_uom": "930.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-11-01",
            "material_code": "102089-000000",
            "price_per_uom": "780.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-11-01",
            "material_code": "100060-000000",
            "price_per_uom": "865.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-11-01",
            "material_code": "101881-000000",
            "price_per_uom": "824.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-07-03",
            "material_code": "100724-000000",
            "price_per_uom": "445.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-07-03",
            "material_code": "100060-000000",
            "price_per_uom": "1025.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-07-03",
            "material_code": "101881-000000",
            "price_per_uom": "918.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-10-01",
            "material_code": "102089-000000",
            "price_per_uom": "790.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-10-01",
            "material_code": "100724-000000",
            "price_per_uom": "420.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-08-01",
            "material_code": "100060-000000",
            "price_per_uom": "990.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-08-01",
            "material_code": "101881-000000",
            "price_per_uom": "894.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-10-01",
            "material_code": "100060-000000",
            "price_per_uom": "910.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-10-01",
            "material_code": "101834-000000",
            "price_per_uom": "895.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-10-01",
            "material_code": "101881-000000",
            "price_per_uom": "822.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-09-01",
            "material_code": "100724-000000",
            "price_per_uom": "432.5",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-09-01",
            "material_code": "100060-000000",
            "price_per_uom": "940.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-09-01",
            "material_code": "101834-000000",
            "price_per_uom": "1025.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-09-01",
            "material_code": "101881-000000",
            "price_per_uom": "799.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-11-29 00:00:00",
            "material_code": "100724-000000",
            "price_per_uom": "407.5",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-11-29 00:00:00",
            "material_code": "101834-000000",
            "price_per_uom": "895.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-12-01",
            "material_code": "102089-000000",
            "price_per_uom": "795.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-12-01",
            "material_code": "100060-000000",
            "price_per_uom": "850.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-12-01",
            "material_code": "101881-000000",
            "price_per_uom": "829.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-12-20 00:00:00",
            "material_code": "100661-000000",
            "price_per_uom": "745.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-07-01",
            "material_code": "100519-000000",
            "price_per_uom": "400.9146945",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-08-01",
            "material_code": "100519-000000",
            "price_per_uom": "435.4741085",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-10-01",
            "material_code": "M0004",
            "price_per_uom": "612.24",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-01-01",
            "material_code": "102322-000000",
            "price_per_uom": "9853",
            "region": "China - Shanghai",
            "currency": "USD"
        },
        {
            "date": "2019-12-01",
            "material_code": "100519-000000",
            "price_per_uom": "699",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-05-01",
            "material_code": "100519-000000",
            "price_per_uom": "1096.509595",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-07-01",
            "material_code": "100519-000000",
            "price_per_uom": "1152.741651",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-08-01",
            "material_code": "100519-000000",
            "price_per_uom": "1039.030363",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-09-01",
            "material_code": "100519-000000",
            "price_per_uom": "1025.694823",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-11-01",
            "material_code": "100519-000000",
            "price_per_uom": "1014.766849",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-08-01",
            "material_code": "100519-000000",
            "price_per_uom": "1028.332095",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-09-01",
            "material_code": "100519-000000",
            "price_per_uom": "970.6117986",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-10-01",
            "material_code": "100519-000000",
            "price_per_uom": "961.2063417",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-07-01",
            "material_code": "100519-000000",
            "price_per_uom": "780",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-03-01",
            "material_code": "100519-000000",
            "price_per_uom": "915.8763564",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-04-01",
            "material_code": "100519-000000",
            "price_per_uom": "960.0127707",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-05-01",
            "material_code": "100519-000000",
            "price_per_uom": "878.4261224",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-06-01",
            "material_code": "100519-000000",
            "price_per_uom": "832.5136059",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2025-08-31 00:00:00",
            "material_code": "100724-000000",
            "price_per_uom": "275.0",
            "region": "China",
            "currency": "USD"
        },
        {
            "date": "2025-08-31 00:00:00",
            "material_code": "100724-000000",
            "price_per_uom": "540.0",
            "region": "West Europe",
            "currency": "USD"
        },
        {
            "date": "2025-08-31 00:00:00",
            "material_code": "100724-000000",
            "price_per_uom": "24.0",
            "region": "North America",
            "currency": "USD"
        },
        {
            "date": "2025-08-31 00:00:00",
            "material_code": "M020",
            "price_per_uom": "690.0",
            "region": "China",
            "currency": "USD"
        },
        {
            "date": "2023-08-01",
            "material_code": "100519-000000",
            "price_per_uom": "947.6881608",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-09-01",
            "material_code": "100519-000000",
            "price_per_uom": "1001.791268",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-01-01",
            "material_code": "100519-000000",
            "price_per_uom": "950.0332281",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-02-01",
            "material_code": "100519-000000",
            "price_per_uom": "1025.800854",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-03-01",
            "material_code": "100519-000000",
            "price_per_uom": "1035.707372",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2025-08-31 00:00:00",
            "material_code": "100055-000000",
            "price_per_uom": "98.0",
            "region": "North America",
            "currency": "USD"
        },
        {
            "date": "2024-07-01",
            "material_code": "100519-000000",
            "price_per_uom": "1071.186867",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2025-07-01 00:00:00",
            "material_code": "102089-000000",
            "price_per_uom": "985.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2025-08-31 00:00:00",
            "material_code": "100055-000000",
            "price_per_uom": "320.0",
            "region": "Southeast Asia",
            "currency": "USD"
        },
        {
            "date": "2020-03-01",
            "material_code": "102322-000000",
            "price_per_uom": "6667",
            "region": "China - Shanghai",
            "currency": "USD"
        },
        {
            "date": "2020-04-01",
            "material_code": "102322-000000",
            "price_per_uom": "5633",
            "region": "China - Shanghai",
            "currency": "USD"
        },
        {
            "date": "2020-07-01",
            "material_code": "102322-000000",
            "price_per_uom": "4367",
            "region": "China - Shanghai",
            "currency": "USD"
        },
        {
            "date": "2020-08-01",
            "material_code": "102322-000000",
            "price_per_uom": "4300",
            "region": "China - Shanghai",
            "currency": "USD"
        },
        {
            "date": "2020-09-01",
            "material_code": "102322-000000",
            "price_per_uom": "4333",
            "region": "China - Shanghai",
            "currency": "USD"
        },
        {
            "date": "2021-03-01",
            "material_code": "102322-000000",
            "price_per_uom": "12913",
            "region": "China - Shanghai",
            "currency": "USD"
        },
        {
            "date": "2021-06-01",
            "material_code": "102322-000000",
            "price_per_uom": "9600",
            "region": "China - Shanghai",
            "currency": "USD"
        },
        {
            "date": "2022-03-01",
            "material_code": "102322-000000",
            "price_per_uom": "12693",
            "region": "China - Shanghai",
            "currency": "USD"
        },
        {
            "date": "2022-04-01",
            "material_code": "102322-000000",
            "price_per_uom": "11873",
            "region": "China - Shanghai",
            "currency": "USD"
        },
        {
            "date": "2025-10-05",
            "material_code": "100724-000000",
            "price_per_uom": "355.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2025-02-13 00:00:00",
            "material_code": "102089-000000",
            "price_per_uom": "711.34",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2025-09-05 00:00:00",
            "material_code": "100724-000000",
            "price_per_uom": "395.0",
            "region": "Northeast Asia",
            "currency": "USD"
        },
        {
            "date": "2025-06-27 00:00:00",
            "material_code": "100724-000000",
            "price_per_uom": "370.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-05-01",
            "material_code": "102322-000000",
            "price_per_uom": "10833",
            "region": "China - Shanghai",
            "currency": "USD"
        },
        {
            "date": "2022-06-01",
            "material_code": "102322-000000",
            "price_per_uom": "11809",
            "region": "China - Shanghai",
            "currency": "USD"
        },
        {
            "date": "2022-07-01",
            "material_code": "102322-000000",
            "price_per_uom": "11648",
            "region": "China - Shanghai",
            "currency": "USD"
        },
        {
            "date": "2022-08-01",
            "material_code": "102322-000000",
            "price_per_uom": "10329",
            "region": "China - Shanghai",
            "currency": "USD"
        },
        {
            "date": "2022-09-01",
            "material_code": "102322-000000",
            "price_per_uom": "12194",
            "region": "China - Shanghai",
            "currency": "USD"
        },
        {
            "date": "2022-10-01",
            "material_code": "102322-000000",
            "price_per_uom": "13117",
            "region": "China - Shanghai",
            "currency": "USD"
        },
        {
            "date": "2023-05-01 00:00:00",
            "material_code": "100724-000000",
            "price_per_uom": "455.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2025-09-05 00:00:00",
            "material_code": "100724-000000",
            "price_per_uom": "365.0",
            "region": "Southeast Asia",
            "currency": "USD"
        },
        {
            "date": "2021-09-01",
            "material_code": "102322-000000",
            "price_per_uom": "10932",
            "region": "China - Shanghai",
            "currency": "USD"
        },
        {
            "date": "2025-05-01 00:00:00",
            "material_code": "101834-000000",
            "price_per_uom": "880.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2025-09-05 00:00:00",
            "material_code": "100724-000000",
            "price_per_uom": "340.0",
            "region": "South Asia",
            "currency": "USD"
        },
        {
            "date": "2025-03-28 00:00:00",
            "material_code": "101834-000000",
            "price_per_uom": "945.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2025-02-28 00:00:00",
            "material_code": "101834-000000",
            "price_per_uom": "860.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2025-09-05 00:00:00",
            "material_code": "100724-000000",
            "price_per_uom": "2220.0",
            "region": "East China",
            "currency": "USD"
        },
        {
            "date": "2024-11-01",
            "material_code": "102322-000000",
            "price_per_uom": "9100",
            "region": "China - Shanghai",
            "currency": "USD"
        },
        {
            "date": "2024-12-01",
            "material_code": "102322-000000",
            "price_per_uom": "9337",
            "region": "China - Shanghai",
            "currency": "USD"
        },
        {
            "date": "2025-06-05 00:00:00",
            "material_code": "102089-000000",
            "price_per_uom": "985.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2025-03-01 00:00:00",
            "material_code": "100661-000000",
            "price_per_uom": "795.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2025-09-05",
            "material_code": "100724-000000",
            "price_per_uom": "342.5",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2025-05-16 00:00:00",
            "material_code": "100724-000000",
            "price_per_uom": "385.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2025-04-25 00:00:00",
            "material_code": "100724-000000",
            "price_per_uom": "375.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2025-03-28 00:00:00",
            "material_code": "100724-000000",
            "price_per_uom": "450.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-12-20 00:00:00",
            "material_code": "100724-000000",
            "price_per_uom": "405.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2025-08-29 00:00:00",
            "material_code": "100724-000000",
            "price_per_uom": "390.0",
            "region": "Northeast Asia",
            "currency": "USD"
        },
        {
            "date": "2025-01-31 00:00:00",
            "material_code": "100724-000000",
            "price_per_uom": "402.5",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-06-28 00:00:00",
            "material_code": "100724-000000",
            "price_per_uom": "440.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2025-08-29 00:00:00",
            "material_code": "100724-000000",
            "price_per_uom": "360.0",
            "region": "Southeast Asia",
            "currency": "USD"
        },
        {
            "date": "2025-04-25 00:00:00",
            "material_code": "101834-000000",
            "price_per_uom": "1025.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2025-01-31 00:00:00",
            "material_code": "101834-000000",
            "price_per_uom": "464.5",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-12-01 00:00:00",
            "material_code": "101834-000000",
            "price_per_uom": "1017.5",
            "region": "Asia",
            "currency": "USD"
        },
        {
            "date": "2022-09-01",
            "material_code": "M039",
            "price_per_uom": "430.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2025-08-29 00:00:00",
            "material_code": "100724-000000",
            "price_per_uom": "340.0",
            "region": "South Asia",
            "currency": "USD"
        },
        {
            "date": "2022-10-01",
            "material_code": "M039",
            "price_per_uom": "339.375",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-11-01",
            "material_code": "M039",
            "price_per_uom": "264.375",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-12-01",
            "material_code": "M039",
            "price_per_uom": "280.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-07-01 00:00:00",
            "material_code": "101834-000000",
            "price_per_uom": "970.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2025-08-29 00:00:00",
            "material_code": "100724-000000",
            "price_per_uom": "2150.0",
            "region": "East China",
            "currency": "USD"
        },
        {
            "date": "2025-03-01 00:00:00",
            "material_code": "102089-000000",
            "price_per_uom": "800.59",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-02-01",
            "material_code": "M039",
            "price_per_uom": "323.75",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2025-05-30 00:00:00",
            "material_code": "100661-000000",
            "price_per_uom": "750.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2025-04-25 00:00:00",
            "material_code": "100661-000000",
            "price_per_uom": "750.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2025-08-01 00:00:00",
            "material_code": "100724-000000",
            "price_per_uom": "272.5",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2025-03-01",
            "material_code": "M039",
            "price_per_uom": "570.75",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2025-04-01",
            "material_code": "M039",
            "price_per_uom": "470.97",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2025-05-01",
            "material_code": "M039",
            "price_per_uom": "480.19",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2025-09-23 00:00:00",
            "material_code": "100724-000000",
            "price_per_uom": "830.0",
            "region": "Asia",
            "currency": "USD"
        },
        {
            "date": "2025-01-01 00:00:00",
            "material_code": "100724-000000",
            "price_per_uom": "830.0",
            "region": "Asia",
            "currency": "USD"
        },
        {
            "date": "2025-02-01 00:00:00",
            "material_code": "100724-000000",
            "price_per_uom": "840.0",
            "region": "Asia",
            "currency": "USD"
        },
        {
            "date": "2025-03-01 00:00:00",
            "material_code": "100724-000000",
            "price_per_uom": "830.0",
            "region": "Asia",
            "currency": "USD"
        },
        {
            "date": "2025-06-20 00:00:00",
            "material_code": "100519-000000",
            "price_per_uom": "800.67",
            "region": "India",
            "currency": "USD"
        },
        {
            "date": "2025-04-01 00:00:00",
            "material_code": "100724-000000",
            "price_per_uom": "840.0",
            "region": "Asia",
            "currency": "USD"
        },
        {
            "date": "2025-05-01 00:00:00",
            "material_code": "100724-000000",
            "price_per_uom": "830.0",
            "region": "Asia",
            "currency": "USD"
        },
        {
            "date": "2024-06-01",
            "material_code": "102089-000000",
            "price_per_uom": "640.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2025-06-01 00:00:00",
            "material_code": "100724-000000",
            "price_per_uom": "840.0",
            "region": "Asia",
            "currency": "USD"
        },
        {
            "date": "2024-10-01 00:00:00",
            "material_code": "100661-000000",
            "price_per_uom": "840.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-08-01",
            "material_code": "M039",
            "price_per_uom": "433.75",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-04-01",
            "material_code": "M039",
            "price_per_uom": "313.75",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2025-07-01 00:00:00",
            "material_code": "100724-000000",
            "price_per_uom": "830.0",
            "region": "Asia",
            "currency": "USD"
        },
        {
            "date": "2023-11-01",
            "material_code": "M039",
            "price_per_uom": "265.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2025-08-01 00:00:00",
            "material_code": "100724-000000",
            "price_per_uom": "840.0",
            "region": "Asia",
            "currency": "USD"
        },
        {
            "date": "2025-10-01 00:00:00",
            "material_code": "100724-000000",
            "price_per_uom": "840.0",
            "region": "Asia",
            "currency": "USD"
        },
        {
            "date": "2025-11-01 00:00:00",
            "material_code": "100724-000000",
            "price_per_uom": "830.0",
            "region": "Asia",
            "currency": "USD"
        },
        {
            "date": "2025-12-01 00:00:00",
            "material_code": "100724-000000",
            "price_per_uom": "840.0",
            "region": "Asia",
            "currency": "USD"
        },
        {
            "date": "2025-04-03 00:00:00",
            "material_code": "102089-000000",
            "price_per_uom": "841.19",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-08-01",
            "material_code": "102089-000000",
            "price_per_uom": "675.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-09-01",
            "material_code": "102089-000000",
            "price_per_uom": "680.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-12-01",
            "material_code": "102089-000000",
            "price_per_uom": "1025.5",
            "region": "IN",
            "currency": "USD"
        },
        {
            "date": "2024-10-01 00:00:00",
            "material_code": "M0005",
            "price_per_uom": "4.17",
            "region": "US",
            "currency": "USD"
        },
        {
            "date": "2023-10-01 00:00:00",
            "material_code": "M0005",
            "price_per_uom": "4.58",
            "region": "US",
            "currency": "USD"
        },
        {
            "date": "2025-06-01",
            "material_code": "M039",
            "price_per_uom": "520.41",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-07-01",
            "material_code": "M039",
            "price_per_uom": "537.5",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-08-01 00:00:00",
            "material_code": "101834-000000",
            "price_per_uom": "1090.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-11-01",
            "material_code": "M0005",
            "price_per_uom": "635.14",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-12-01",
            "material_code": "102322-000000",
            "price_per_uom": "10195",
            "region": "China - Shanghai",
            "currency": "USD"
        },
        {
            "date": "2020-01-01",
            "material_code": "100519-000000",
            "price_per_uom": "750.1462977",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-02-01",
            "material_code": "100519-000000",
            "price_per_uom": "730.3014474",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-03-01",
            "material_code": "100519-000000",
            "price_per_uom": "672.2539976",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-04-01",
            "material_code": "100519-000000",
            "price_per_uom": "333.3213872",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-05-01",
            "material_code": "100519-000000",
            "price_per_uom": "374.4558611",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-06-01",
            "material_code": "100519-000000",
            "price_per_uom": "450.9009565",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-09-01",
            "material_code": "100519-000000",
            "price_per_uom": "441.774165",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-11-01",
            "material_code": "100519-000000",
            "price_per_uom": "530.4703681",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-12-01",
            "material_code": "100519-000000",
            "price_per_uom": "603.7283746",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-01-01",
            "material_code": "100519-000000",
            "price_per_uom": "613.9678547",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-02-01",
            "material_code": "100519-000000",
            "price_per_uom": "772.6671936",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-04-01",
            "material_code": "100519-000000",
            "price_per_uom": "953.3274674",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-10-01",
            "material_code": "100519-000000",
            "price_per_uom": "1132.378886",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-12-01",
            "material_code": "100519-000000",
            "price_per_uom": "921.0619039",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-01-01",
            "material_code": "100519-000000",
            "price_per_uom": "1036.410045",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-06-01",
            "material_code": "102322-000000",
            "price_per_uom": "4433",
            "region": "China - Shanghai",
            "currency": "USD"
        },
        {
            "date": "2022-02-01",
            "material_code": "102322-000000",
            "price_per_uom": "13104",
            "region": "China - Shanghai",
            "currency": "USD"
        },
        {
            "date": "2021-04-01",
            "material_code": "102322-000000",
            "price_per_uom": "11012",
            "region": "China - Shanghai",
            "currency": "USD"
        },
        {
            "date": "2021-05-01",
            "material_code": "102322-000000",
            "price_per_uom": "10945",
            "region": "China - Shanghai",
            "currency": "USD"
        },
        {
            "date": "2022-11-01",
            "material_code": "102322-000000",
            "price_per_uom": "11597",
            "region": "China - Shanghai",
            "currency": "USD"
        },
        {
            "date": "2023-10-01",
            "material_code": "102322-000000",
            "price_per_uom": "11275",
            "region": "China - Shanghai",
            "currency": "USD"
        },
        {
            "date": "2023-11-01",
            "material_code": "102322-000000",
            "price_per_uom": "12525",
            "region": "China - Shanghai",
            "currency": "USD"
        },
        {
            "date": "2024-08-01",
            "material_code": "102322-000000",
            "price_per_uom": "10550",
            "region": "China - Shanghai",
            "currency": "USD"
        },
        {
            "date": "2022-02-01",
            "material_code": "100519-000000",
            "price_per_uom": "1104.383806",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-03-01",
            "material_code": "100519-000000",
            "price_per_uom": "1171.33206",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-04-01",
            "material_code": "100519-000000",
            "price_per_uom": "1134.6935",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-05-01",
            "material_code": "100519-000000",
            "price_per_uom": "1181.670909",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-06-01",
            "material_code": "100519-000000",
            "price_per_uom": "1267.974579",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-11-01",
            "material_code": "100519-000000",
            "price_per_uom": "874.2366422",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-12-01",
            "material_code": "100519-000000",
            "price_per_uom": "839.6777365",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-01-01",
            "material_code": "100519-000000",
            "price_per_uom": "911.2243183",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-04-01",
            "material_code": "100519-000000",
            "price_per_uom": "1062.022751",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-09-01",
            "material_code": "100519-000000",
            "price_per_uom": "1061.92355",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-10-01",
            "material_code": "100519-000000",
            "price_per_uom": "952.4577571",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-01-01",
            "material_code": "102322-000000",
            "price_per_uom": "6500",
            "region": "China - Shanghai",
            "currency": "USD"
        },
        {
            "date": "2020-02-01",
            "material_code": "102322-000000",
            "price_per_uom": "6500",
            "region": "China - Shanghai",
            "currency": "USD"
        },
        {
            "date": "2024-05-01",
            "material_code": "100519-000000",
            "price_per_uom": "1073.193073",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-11-01",
            "material_code": "100519-000000",
            "price_per_uom": "967.8602856",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2019-11-01",
            "material_code": "102322-000000",
            "price_per_uom": "8200",
            "region": "China - Shanghai",
            "currency": "USD"
        },
        {
            "date": "2019-12-01",
            "material_code": "102322-000000",
            "price_per_uom": "6633",
            "region": "China - Shanghai",
            "currency": "USD"
        },
        {
            "date": "2020-05-01",
            "material_code": "102322-000000",
            "price_per_uom": "4800",
            "region": "China - Shanghai",
            "currency": "USD"
        },
        {
            "date": "2020-10-01",
            "material_code": "102322-000000",
            "price_per_uom": "5300",
            "region": "China - Shanghai",
            "currency": "USD"
        },
        {
            "date": "2024-12-01",
            "material_code": "100519-000000",
            "price_per_uom": "911.7468784",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-11-01",
            "material_code": "102322-000000",
            "price_per_uom": "7000",
            "region": "China - Shanghai",
            "currency": "USD"
        },
        {
            "date": "2020-12-01",
            "material_code": "102322-000000",
            "price_per_uom": "7748",
            "region": "China - Shanghai",
            "currency": "USD"
        },
        {
            "date": "2021-01-01",
            "material_code": "102322-000000",
            "price_per_uom": "7900",
            "region": "China - Shanghai",
            "currency": "USD"
        },
        {
            "date": "2021-02-01",
            "material_code": "102322-000000",
            "price_per_uom": "9733",
            "region": "China - Shanghai",
            "currency": "USD"
        },
        {
            "date": "2021-07-01",
            "material_code": "102322-000000",
            "price_per_uom": "10092",
            "region": "China - Shanghai",
            "currency": "USD"
        },
        {
            "date": "2021-08-01",
            "material_code": "102322-000000",
            "price_per_uom": "10695",
            "region": "China - Shanghai",
            "currency": "USD"
        },
        {
            "date": "2021-10-01",
            "material_code": "102322-000000",
            "price_per_uom": "13237",
            "region": "China - Shanghai",
            "currency": "USD"
        },
        {
            "date": "2021-11-01",
            "material_code": "102322-000000",
            "price_per_uom": "13198",
            "region": "China - Shanghai",
            "currency": "USD"
        },
        {
            "date": "2021-12-01",
            "material_code": "102322-000000",
            "price_per_uom": "9557",
            "region": "China - Shanghai",
            "currency": "USD"
        },
        {
            "date": "2022-01-01",
            "material_code": "102322-000000",
            "price_per_uom": "11103",
            "region": "China - Shanghai",
            "currency": "USD"
        },
        {
            "date": "2023-02-01",
            "material_code": "102322-000000",
            "price_per_uom": "12200",
            "region": "China - Shanghai",
            "currency": "USD"
        },
        {
            "date": "2023-03-01",
            "material_code": "102322-000000",
            "price_per_uom": "13075",
            "region": "China - Shanghai",
            "currency": "USD"
        },
        {
            "date": "2023-04-01",
            "material_code": "102322-000000",
            "price_per_uom": "10775",
            "region": "China - Shanghai",
            "currency": "USD"
        },
        {
            "date": "2023-05-01",
            "material_code": "102322-000000",
            "price_per_uom": "11275",
            "region": "China - Shanghai",
            "currency": "USD"
        },
        {
            "date": "2023-06-01",
            "material_code": "102322-000000",
            "price_per_uom": "10913",
            "region": "China - Shanghai",
            "currency": "USD"
        },
        {
            "date": "2023-07-01",
            "material_code": "102322-000000",
            "price_per_uom": "9475",
            "region": "China - Shanghai",
            "currency": "USD"
        },
        {
            "date": "2023-08-01",
            "material_code": "102322-000000",
            "price_per_uom": "11142",
            "region": "China - Shanghai",
            "currency": "USD"
        },
        {
            "date": "2023-12-01",
            "material_code": "100519-000000",
            "price_per_uom": "866.0266028",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-06-01",
            "material_code": "100519-000000",
            "price_per_uom": "1130.778868",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-08-01",
            "material_code": "100519-000000",
            "price_per_uom": "1057.986977",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-11-01 00:00:00",
            "material_code": "101834-000000",
            "price_per_uom": "1032.5",
            "region": "Asia",
            "currency": "USD"
        },
        {
            "date": "2023-01-01",
            "material_code": "M039",
            "price_per_uom": "303.75",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-03-01",
            "material_code": "M039",
            "price_per_uom": "277.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-05-01",
            "material_code": "M039",
            "price_per_uom": "328.125",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-02-01",
            "material_code": "102322-000000",
            "price_per_uom": "10987.5",
            "region": "China - Shanghai",
            "currency": "USD"
        },
        {
            "date": "2023-06-01",
            "material_code": "M039",
            "price_per_uom": "295.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-03-01",
            "material_code": "102322-000000",
            "price_per_uom": "11437",
            "region": "China - Shanghai",
            "currency": "USD"
        },
        {
            "date": "2024-04-01",
            "material_code": "102322-000000",
            "price_per_uom": "11942.5",
            "region": "China - Shanghai",
            "currency": "USD"
        },
        {
            "date": "2024-05-01",
            "material_code": "102322-000000",
            "price_per_uom": "11268",
            "region": "China - Shanghai",
            "currency": "USD"
        },
        {
            "date": "2024-06-01",
            "material_code": "102322-000000",
            "price_per_uom": "12167.5",
            "region": "China - Shanghai",
            "currency": "USD"
        },
        {
            "date": "2024-07-01",
            "material_code": "102322-000000",
            "price_per_uom": "10995",
            "region": "China - Shanghai",
            "currency": "USD"
        },
        {
            "date": "2024-09-01",
            "material_code": "102322-000000",
            "price_per_uom": "10437",
            "region": "China - Shanghai",
            "currency": "USD"
        },
        {
            "date": "2024-10-01",
            "material_code": "102322-000000",
            "price_per_uom": "10700",
            "region": "China - Shanghai",
            "currency": "USD"
        },
        {
            "date": "2023-08-01",
            "material_code": "M039",
            "price_per_uom": "280.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-10-01",
            "material_code": "M039",
            "price_per_uom": "405.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-11-01",
            "material_code": "M039",
            "price_per_uom": "405.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-12-01",
            "material_code": "M039",
            "price_per_uom": "442.5",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2025-01-01",
            "material_code": "M039",
            "price_per_uom": "440.31",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-11-27 00:00:00",
            "material_code": "M0005",
            "price_per_uom": "1.56",
            "region": "US",
            "currency": "USD"
        },
        {
            "date": "2021-10-01",
            "material_code": "M039",
            "price_per_uom": "910.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-11-01",
            "material_code": "M039",
            "price_per_uom": "930.625",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-12-01",
            "material_code": "M039",
            "price_per_uom": "785.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-12-25 00:00:00",
            "material_code": "M0005",
            "price_per_uom": "1.59",
            "region": "US",
            "currency": "USD"
        },
        {
            "date": "2025-06-13 00:00:00",
            "material_code": "101834-000000",
            "price_per_uom": "875.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-09-01",
            "material_code": "M039",
            "price_per_uom": "270.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-10-01",
            "material_code": "M039",
            "price_per_uom": "270.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-08-01 00:00:00",
            "material_code": "100724-000000",
            "price_per_uom": "452.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-03-01",
            "material_code": "100519-000000",
            "price_per_uom": "881.9081591",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2021-06-01",
            "material_code": "100519-000000",
            "price_per_uom": "1085.960317",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-02-01",
            "material_code": "100519-000000",
            "price_per_uom": "895.8298454",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2019-10-01",
            "material_code": "100519-000000",
            "price_per_uom": "642.25",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2019-11-01",
            "material_code": "100519-000000",
            "price_per_uom": "627",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-10-01",
            "material_code": "100519-000000",
            "price_per_uom": "946.2566502",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-11-01",
            "material_code": "100519-000000",
            "price_per_uom": "893.244594",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2020-10-01",
            "material_code": "100519-000000",
            "price_per_uom": "446.9273152",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-07-01",
            "material_code": "100519-000000",
            "price_per_uom": "1196.095697",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-09-01",
            "material_code": "102322-000000",
            "price_per_uom": "11800",
            "region": "China - Shanghai",
            "currency": "USD"
        },
        {
            "date": "2023-12-01",
            "material_code": "102322-000000",
            "price_per_uom": "11100",
            "region": "China - Shanghai",
            "currency": "USD"
        },
        {
            "date": "2024-01-01",
            "material_code": "102322-000000",
            "price_per_uom": "10737",
            "region": "China - Shanghai",
            "currency": "USD"
        },
        {
            "date": "2025-02-01",
            "material_code": "M039",
            "price_per_uom": "450.53",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-07-01",
            "material_code": "M039",
            "price_per_uom": "270.625",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-07-01",
            "material_code": "102089-000000",
            "price_per_uom": "675.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2025-07-01",
            "material_code": "M039",
            "price_per_uom": "555.63",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-03-01 00:00:00",
            "material_code": "100724-000000",
            "price_per_uom": "452.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2025-09-01",
            "material_code": "101834-000000",
            "price_per_uom": "860.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-05-24 00:00:00",
            "material_code": "101834-000000",
            "price_per_uom": "945.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-03-29 00:00:00",
            "material_code": "101834-000000",
            "price_per_uom": "910.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-01-01",
            "material_code": "M039",
            "price_per_uom": "742.5",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-02-01",
            "material_code": "M039",
            "price_per_uom": "855.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-03-01",
            "material_code": "M039",
            "price_per_uom": "1023.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-04-01",
            "material_code": "M039",
            "price_per_uom": "957.5",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-05-01",
            "material_code": "M039",
            "price_per_uom": "963.75",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2022-06-01",
            "material_code": "M039",
            "price_per_uom": "938.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-12-01",
            "material_code": "M039",
            "price_per_uom": "250.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-01-01",
            "material_code": "M039",
            "price_per_uom": "275.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-02-01",
            "material_code": "M039",
            "price_per_uom": "290.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-03-01",
            "material_code": "M039",
            "price_per_uom": "297.5",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-04-01",
            "material_code": "M039",
            "price_per_uom": "282.5",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-05-01",
            "material_code": "M039",
            "price_per_uom": "285.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-06-01",
            "material_code": "M039",
            "price_per_uom": "300.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-07-01",
            "material_code": "M039",
            "price_per_uom": "320.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-08-01",
            "material_code": "M039",
            "price_per_uom": "350.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-09-01",
            "material_code": "M039",
            "price_per_uom": "355.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2025-07-18 00:00:00",
            "material_code": "100519-000000",
            "price_per_uom": "710.0",
            "region": "China",
            "currency": "USD"
        },
        {
            "date": "2025-02-28 00:00:00",
            "material_code": "100724-000000",
            "price_per_uom": "432.5",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2024-02-23 00:00:00",
            "material_code": "100724-000000",
            "price_per_uom": "465.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2023-07-01 00:00:00",
            "material_code": "100724-000000",
            "price_per_uom": "3250.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        },
        {
            "date": "2025-02-28 00:00:00",
            "material_code": "100661-000000",
            "price_per_uom": "795.0",
            "region": "Asia-Pacific",
            "currency": "USD"
        }
    ]
}
rows = data["rows"]

with open("price_history_data.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([
        "material_price_type_period_id", "material_id", "period_start_date", "period_end_date",
        "country", "price", "price_currency", "price_history_source", "price_type", "location_id"
    ])

    for i, r in enumerate(rows, start=1):
        if r["material_code"].startswith("M0"):
            continue
        writer.writerow([
            f"MPTP{i:04d}",            # Primary key
            r["material_code"],           # material_id
            r["date"].split(" ")[0],   # period_start_date
            r["date"].split(" ")[0],   # period_end_date
            "",                        # country (empty)
            r["price_per_uom"],        # price
            r["currency"] or "",       # price_currency
            "External Source",         # price_history_source
            "Standard",                # price_type
            212                        # location_id
        ])

print("✅ CSV file 'price_history_data.csv' generated successfully!")
