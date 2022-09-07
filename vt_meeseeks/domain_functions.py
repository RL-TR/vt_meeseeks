from xml import dom
from xml.dom.xmlbuilder import DOMImplementationLS
from datetime import datetime



def hello_world():
    print('hello world')

def add_column_headers(csv_obj):
    print('INFO: Attempting to add column headers')
    try:
        csv_obj.writerow(['date_added', 'domain', 'creation_date', 'malicious_results', 'total_results'])
        print('INFO: Successfully added headers to CSV.')
    
    except Exception as err:
        print('ERROR: Failed to add column heads to output file. {}'.format(err))



def get_domain_info(vt_client, domain):

    #print("DEBUG domain: ", domain  )

    domain_result = {}

    now = datetime.now()
    formatted_date = now.strftime("%Y%m%d")

    domain_result['date_added'] = formatted_date
    domain_result['domain'] = domain

    try:    
        result = vt_client.get_object("/domains/{}".format(domain))

        malicious_num = result.last_analysis_stats["malicious"]
        harmless_num = result.last_analysis_stats["harmless"]
        suspicious_num = result.last_analysis_stats["suspicious"]
        undetected_num = result.last_analysis_stats["undetected"]

        total_results = malicious_num + harmless_num + suspicious_num + undetected_num
        malicious_results = malicious_num + suspicious_num

        
        domain_result['malicious_results'] = malicious_results
        domain_result['total_results'] = total_results

        domain_result['creation_date'] = result.creation_date.strftime("%Y-%m-%d")

    except Exception as err:
        print('ERROR: {}'.format(err))

        domain_result['malicious_results'] = "-"
        domain_result['total_results'] = "-"
        domain_result['creation_date'] = "-"

    print(domain_result)

    return domain_result


def write_to_output(csv_obj, domain_result):

    try:
        csv_obj.writerow([domain_result['date_added'], domain_result['domain'], domain_result['creation_date'], domain_result['malicious_results'], domain_result['total_results']])
        print('INFO: Successfully added headers to CSV.')
    
    except Exception as err:
        print('ERROR: Failed to write results to file. {}'.format(err))