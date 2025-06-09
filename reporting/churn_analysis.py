import pandas as pd
import os

def generate_churn_report():
    # Recreate the extended churn dataset directly
    data = {
        'customer_id': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15],
        'age': [34,29,45,23,37,52,28,41,36,30,48,25,55,32,27],
        'gender_code': [1,0,0,1,1,1,0,1,0,1,0,1,0,1,0],
        'region_code': [0,1,2,3,4,2,1,0,4,3,2,1,0,4,3],
        'num_transactions': [12,5,20,3,15,7,2,18,9,4,22,6,30,11,1],
        'total_spend': [1200.50,300.75,2500.00,150.20,1800.00,800.00,120.00,2100.30,950.40,400.00,2600.00,500.00,3200.75,1100.00,75.00],
        'days_since_last': [20,159,8,190,86,45,200,12,105,170,5,130,2,95,250],
        'customer_age_days': [511,567,96,344,638,722,630,484,400,540,810,449,910,580,445],
        'churned': [0,1,0,1,0,0,1,0,1,1,0,1,0,0,1]
    }
    df = pd.DataFrame(data)

    #codes to labels mapping
    region_map = {0: 'North', 1: 'South', 2: 'East', 3: 'West', 4: 'Central'}
    gender_map = {1: 'Male', 0: 'Female'}
    df['Region'] = df['region_code'].map(region_map)
    df['Gender'] = df['gender_code'].map(gender_map)

    #output directory
    output_dir = os.path.join('data', 'reporting')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'churn_analysis.xlsx')

    # write to Excel with pivot tables and charts
    with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
        #data sheet
        df.to_excel(writer, sheet_name='RawData', index=False)

        workbook  = writer.book
        worksheet = workbook.add_worksheet('PivotAnalysis')
        writer.sheets['PivotAnalysis'] = worksheet

        #rate be region
        df['churned'] = df['churned'].astype(float)  # Ensure churned is float for mean calculation
        region_rates = df.groupby('Region')['churned'].mean().reset_index()
        worksheet.write('A1', 'Region')
        worksheet.write('B1', 'Churn Rate')
        for idx, row in region_rates.iterrows():
            worksheet.write(idx+1, 0, row['Region'])
            worksheet.write(idx+1, 1, row['churned'])

        #churn Rate chart by Region
        chart1 = workbook.add_chart({'type': 'column'})
        chart1.add_series({
            'name':       'Churn Rate',
            'categories': ['PivotAnalysis', 1, 0, len(region_rates), 0],
            'values':     ['PivotAnalysis', 1, 1, len(region_rates), 1],
        })
        chart1.set_title({'name': 'Churn Rate by Region'})
        chart1.set_y_axis({'name': 'Churn Rate'})
        chart1.set_x_axis({'name': 'Region'})
        worksheet.insert_chart('D2', chart1)

        #pivot: Churn Rate by Gender
        gender_rates = df.groupby('Gender')['churned'].mean().reset_index()
        start_row = len(region_rates) + 3
        worksheet.write(start_row, 0, 'Gender')
        worksheet.write(start_row, 1, 'Churn Rate')
        for idx, row in gender_rates.iterrows():
            worksheet.write(start_row+idx+1, 0, row['Gender'])
            worksheet.write(start_row+idx+1, 1, row['churned'])

        #chart: Churn Rate by Gender
        chart2 = workbook.add_chart({'type': 'pie'})
        chart2.add_series({
            'name':       'Churn Rate by Gender',
            'categories': ['PivotAnalysis', start_row+1, 0, start_row+len(gender_rates), 0],
            'values':     ['PivotAnalysis', start_row+1, 1, start_row+len(gender_rates), 1],
        })
        chart2.set_title({'name': 'Churn Rate by Gender'})
        worksheet.insert_chart('D12', chart2)

    print(f"Report written to {output_path}")

if __name__ == '__main__':
    generate_churn_report()