import pandas as pd
from sec_api import QueryApi
import time

# Fetch S&P 500 CIKs
sp500_tickers_df = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
sp500_ciks = sp500_tickers_df['CIK'].tolist()  # no padding




# Initialize the SEC API
queryApi = QueryApi(api_key="86cf173f8aa0f24a7e0e256fad0e1587ba70ffaeb93fccd4d52fd98a4ccabe9d")

# Open the file to store the filing URLs
log_file = open("final_urls_and_metadata.txt", "a")

# Create a concatenated string of every 12 CIKs in sp500_test. It should be in the form of "(cik1 OR cik2 OR ... OR cik12)"
# This is necessary because the API only allows 12 CIKs in a single query
cik_str = "(" 

i = 0;

for cik in sp500_ciks:
    i += 1
    cik_str += str(cik) + " OR "
    i += 1

    

    if i % 25 == 0: 
        cik_str = cik_str[:-4] + ")"  # Remove the last " OR " and add a closing parenthesis
        try:
            base_query = {
                "query": "formType:\"10-K\" AND cik:" + cik_str,
                "from": "0",
                "size": "200", # dont change this
                # sort by filedAt
                "sort": [{ "filedAt": { "order": "desc" } }]
            }
            
            # Fetch the filings for the current batch
            response = queryApi.get_filings(base_query)
            
            # Extract URLs for the filings in the batch
            for i in range (0, 25):
                log_file.write(response["filings"][i]["ticker"] + "\n")
                log_file.write(response["filings"][i]["companyName"] + "\n")
                log_file.write(response["filings"][i]["linkToFilingDetails"] + "\n")
            
            # Delay to avoid rate limiting
            time.sleep(2)  # 2-second delay between batch requests
            cik_str = "(" # Reset the CIK string
        
        except Exception as e:
            print(f"Error processing batch {cik}: {e}")

        # If there are any remaining CIKs, process them 
# Handle the last batch if there are remaining CIKs
if cik_str != "(":
    cik_str = cik_str[:-4] + ")"  # Remove the last " OR " and add a closing parenthesis
    try:
        base_query = {
            "query": f"formType:\"10-K\" AND {cik_str}",
            "from": "0",
            "size": "1",  # Get only the most recent filing per batch
            "sort": [{"filedAt": {"order": "desc"}}]
        }
        
        # Fetch the filings for the current batch
        response = queryApi.get_filings(base_query)
        
        # Extract URLs for the filings in the batch
        for filing in response.get("filings", []):
            log_file.write(filing["ticker"] + "\n")
            log_file.write(filing["companyName"] + "\n")
            log_file.write(filing["linkToFilingDetails"] + "\n")
        
        print(f"Downloaded URLs for the final batch")
    
    except Exception as e:
        print(f"Error processing the final batch: {e}")




# Close the file
log_file.close()
print("All URLs downloaded")
