import json
from datetime import datetime, timedelta
import pandas as pd


def main():
    with open('/Users/yahe16/Documents/GitHub/wuhan2020/data/fe/patient_detail/1anhui.json', encoding='utf-8') as f:
        data = json.load(f)
    output = []
    for p in data:
        id = p['id']
        province = p['province']
        city = p['city']
        activity = []
        activity.append((p['confirmHospital'], p['confirmDate'][:10]))  # append event pair (location, date)
        if len(p['travelData']) >= 1:
            for item in p['travelData']:
                if item['travelDate'] != '' and item['travelFrom'].strip() != '':
                    if item['travelMethod'] in ['火车', '高铁', '动车'] and '站' not in item['travelFrom']:
                        activity.append((item['travelFrom'] + '站', item['travelDate'][:10]))
                    else:
                        activity.append((item['travelFrom'], item['travelDate'][:10]))
                if item['travelDate'] != '' and item['travelTo'].strip() != '':
                    if item['travelMethod'] in ['火车', '高铁', '动车'] and '站' not in item['travelTo']:
                        activity.append((item['travelTo'] + '站', item['travelDate'][:10]))
                    else:
                        activity.append((item['travelTo'], item['travelDate'][:10]))
        if len(p['eventData']) >= 1:
            for item in p['eventData']:
                if item['eventAddr'].strip() != '' and item['eventStartTime'] != '':
                    activity.append((item['eventAddr'], item['eventStartTime'][:10]))
        for row in activity:
            output.append((id, province, city, row[0], row[1], 0.8))    # Day 0
            output.append((id, province, city, row[0], (datetime.strptime(row[1],'%Y-%m-%d') + timedelta(1)).strftime('%Y-%m-%d'), 0.482))  # Day 1
            output.append((id, province, city, row[0], (datetime.strptime(row[1],'%Y-%m-%d') + timedelta(2)).strftime('%Y-%m-%d'), 0.108))  # Day 2
            output.append((id, province, city, row[0], (datetime.strptime(row[1],'%Y-%m-%d') + timedelta(3)).strftime('%Y-%m-%d'), 0.009))  # Day 3
    # with open('output.txt', 'w', encoding='utf-8') as f_out:
    #     for line in output:
    #         line_str = ','.join(line) + '\n'
    #         f_out.write(line_str)
    df = pd.DataFrame(output, columns=['ID', 'Province', 'City', 'Location', 'Date', 'Weight'])
    df_g = df.groupby(['Province', 'City', 'Location', 'Date'])['Weight'].agg('sum')
    df_g.to_csv('output.csv', header=True)





if __name__ == '__main__':
    main()