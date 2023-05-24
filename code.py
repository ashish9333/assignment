import os
import requests

def lambda_handler(event, context):
    # Get the file name from the event
    file_name = event['Records'][0]['s3']['object']['key']

    # Download the file from S3
    file_path = os.path.join('/tmp', file_name)
    response = requests.get('https://s3.amazonaws.com/{}/{}'.format(event['Records'][0]['s3']['bucket']['name'], file_name))
    open(file_path, 'wb').write(response.content)

    # Convert the file to PDF
    import docx2pdf
    docx2pdf.convert(file_path, '/tmp/output.pdf')

    # Upload the PDF file to S3
    response = requests.put('https://s3.amazonaws.com/{}/{}'.format(event['Records'][0]['s3']['bucket']['name'], 'output.pdf'), data=open('/tmp/output.pdf', 'rb').read())

    # Return the success message
    return {
        'statusCode': 200,
        'body': 'success'
    }