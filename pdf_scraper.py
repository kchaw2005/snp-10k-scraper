import pandas as pd
from sec_api import QueryApi, XbrlApi, ExtractorApi
import yfinance as yf

YOUR_API_KEY = ""
xbrlApi = XbrlApi(YOUR_API_KEY)
extractorApi = ExtractorApi(YOUR_API_KEY)

log_file = open("final_urls_and_metadata.txt", "r")
urls = log_file.readlines()
log_file.close()

urls = urls[:15]
print(urls)

#dataframe for later
end_data = []

data_entry_object = {
    "Ticker": "",
    "Company Name": "",
    "Risk Factors (1A)": "",
    "Market Risk QQ Disclosures": ""
}

for i in range (0, 15, 3):
    ticker = urls[i].strip()
    company_name = urls[i + 1].strip()
    htm_url = urls[i + 2].strip()
    data_entry_object["Ticker"] = ticker
    data_entry_object["Company Name"] = company_name

    # Extract the text from the Risk Factors section
    risk_factors = extractorApi.get_section(htm_url, "1A", "text")
    data_entry_object["Risk Factors (1A)"] = risk_factors

    # Extract the text from the Market Risk QQ Disclosures section
    market_risk = extractorApi.get_section(htm_url, "7", "text")
    data_entry_object["Market Risk QQ Disclosures"] = market_risk

    end_data.append(data_entry_object)

    print(f"Data for {ticker} has been extracted")



# Create a DataFrame from the structured data
final_df = pd.DataFrame(end_data)

# Save the DataFrame to a CSV file
final_df.to_csv('final_data.csv', index=False)

print("Data has been saved to 'final_data.csv'")



# # .readLines documentation: https://www.tutorialspoint.com/python/file_readlines.htm
# # xbrl_json = xbrlApi.xbrl_to_json(htm_url=htm_url)

# # Extract and normalize the data from StatementsOfCashFlows
# # cash_flows_data = xbrl_json['StatementsOfCashFlows']

# # # List to store the structured data
# # structured_data = []

# # for item_key, item_values in cash_flows_data.items():
# #     for item in item_values:
# #         # Parse each item (dictionary) and extract the relevant fields
# #         entry = {
# #             "Item Name": item_key,
# #             "Value": item.get('value'),
# #             "Decimals": item.get('decimals'),
# #             "Unit": item.get('unitRef'),
# #             "Start Date": item.get('period', {}).get('startDate', None),
# #             "End Date": item.get('period', {}).get('endDate', None),
# #             "Instant": item.get('period', {}).get('instant', None)
# #         }
# #         structured_data.append(entry)

# # # Create a DataFrame from the structured data
# # cash_flows_df = pd.DataFrame(structured_data)

# # # Save the DataFrame to a CSV file
# # cash_flows_df.to_csv('cash_flows_cleaned.csv', index=False)

# # print("Data has been saved to 'cash_flows_cleaned.csv'")


# # url="https://www.sec.gov/Archives/edgar/data/1318605/000156459021004599/tsla-10k_20201231.htm"

# # section_text = extractorApi.get_section(url, "1A", "text")

