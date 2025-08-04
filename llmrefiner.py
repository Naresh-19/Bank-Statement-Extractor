import pandas as pd
import google.generativeai as genai
import os
import re
import io
from dotenv import load_dotenv

def refine_csv_with_llm(df):
    """
    Enhanced function to refine CSV using Gemini LLM with better handling of merged columns/values
    
    Args:
        df (pandas.DataFrame): Original CSV data
        
    Returns:
        tuple: (refined_dataframe, success_status)
    """
    try:
        # Setup Gemini
        load_dotenv()
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        model = genai.GenerativeModel('gemini-2.5-flash-lite')
        
        # Convert DataFrame to CSV string
        csv_string = df.to_csv(index=False)
        
        # Create enhanced prompt
        prompt = f"""You are a CSV data cleaning expert. Fix this bank statement CSV by following these rules EXACTLY:

Your only task : 
1. Seperate the header and give that as csv string , only headers are enough(USe only existing column names)
2. Remove dummy columns, if any (like this formatcolumn_1, column_5, etc.) and make sure you replace with proper column names.
3. Make sure the extracted number of columns in the header matches the number of columns in the data ie the longest row.


**YOUR CSV DATA:**
{csv_string}

Return ONLY the corrected CSV. No explanations, no code blocks, no ```csv``` markers. Just the raw CSV data with proper comma separation."""

        # Get response from Gemini
        response = model.generate_content(prompt)
        print(response.text)
        # Clean response more thoroughly
        cleaned_csv = response.text.strip()
        
        # Remove any markdown formatting
        cleaned_csv = re.sub(r'```csv\s*\n?', '', cleaned_csv)
        cleaned_csv = re.sub(r'```\s*\n?', '', cleaned_csv)
        cleaned_csv = re.sub(r'^csv\s*\n', '', cleaned_csv, flags=re.MULTILINE)
        
        # Remove any leading/trailing whitespace
        cleaned_csv = cleaned_csv.strip()
        
        # Split into lines and clean each line
        lines = cleaned_csv.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            if line:  # Skip empty lines
                cleaned_lines.append(line)
        
        # Rejoin the cleaned lines
        cleaned_csv = '\n'.join(cleaned_lines)
        print(cleaned_csv)
        # Convert back to DataFrame
        refined_df = pd.read_csv(io.StringIO(cleaned_csv))
        
        # Validate that we didn't lose data
        if len(refined_df) == 0:
            print("Warning: Refined DataFrame is empty, returning original")
            return df, False
            
        return refined_df, True
        
    except Exception as e:
        print(f"LLM refinement failed: {str(e)}")
        print(f"Response received: {response.text[:500] if 'response' in locals() else 'No response'}")
        return df, False