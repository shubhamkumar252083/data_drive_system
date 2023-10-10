import os
import datetime

class RequestResponseLoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log the request information
        log_request(request)
        
        response = self.get_response(request)

        # Log the response information
        log_response(request, response)

        return response

def log_request(request):
    log_dir = 'request_logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file = os.path.join(log_dir, f'request_{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}.txt')
    
    with open(log_file, 'w') as f:
        f.write(f"Request Method: {request.method}\n")
        f.write(f"Request URL: {request.get_full_path()}\n")
        # f.write(f"Request Headers:\n")
        # for header, value in request.headers.items():
        #     f.write(f"{header}: {value}\n")
        # f.write(f"Request Body:\n{request.body.decode('utf-8')}\n")

def log_response(request, response):
    log_dir = 'response_logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file = os.path.join(log_dir, f'response_{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}.txt')
    
    with open(log_file, 'w') as f:
        f.write(f"Request Method: {request.method}\n")
        f.write(f"Request URL: {request.get_full_path()}\n")
        f.write(f"Response Status Code: {response.status_code}\n")
        # f.write(f"Response Headers:\n")
        # for header, value in response.items():
        #     f.write(f"{header}: {value}\n")
        # f.write(f"Response Content:\n{response.content.decode('utf-8')}\n")
