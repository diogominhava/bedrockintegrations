exports.handler = async function (event, context) {
  console.log("EVENT: \n" + JSON.stringify(event, null, 2));
  const apiPath = event.apiPath;
  const apiMethod = event.httpMethod;
  let body;
  let response_body;
  
  if (apiPath === '/event') {
      if (apiMethod === 'GET') {
        body = [
            {
                "eventId": 1,
                "eventDate": "20240214",
                "eventTime": "16:00"
            },
            {
                "eventId": 2,
                "eventDate": "20250214",
                "eventTime": "16:00"
            },
            {
                "eventId": 3,
                "eventDate": "20260214",
                "eventTime": "16:00"
            }
        ];        
      }
  }
  
  response_body = {
      'application/json': {
          'body': body
      }
  }
  
  const action_response = {
        'actionGroup': event['actionGroup'],
        'apiPath': event['apiPath'],
        'httpMethod': event['httpMethod'],
        'httpStatusCode': 200,
        'responseBody': response_body
  }
  return action_response
};