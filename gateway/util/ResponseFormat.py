from flask_api import exceptions, status


class RequestHandler(object):

    @staticmethod
    def formatResponse(status_code=500, data=None, message='', error=''):
        results = {'data': []}
        if status_code == 400:
            results['error'] = exceptions.ParseError.detail
            results['message'] = message
            results['status'] = status.HTTP_400_BAD_REQUEST
        elif status_code == 401:
            results['error'] = exceptions.AuthenticationFailed.detail
            results['message'] = message
            results['status'] = status.HTTP_401_UNAUTHORIZED
        elif status_code == 403:
            results['error'] = exceptions.PermissionDenied.detail
            results['message'] = message
            results['status'] = status.HTTP_403_FORBIDDEN
        elif status_code == 404:
            results['error'] = error
            results['message'] = message
            results['status'] = status.HTTP_404_NOT_FOUND
        elif status_code == 408:
            results['error'] = "Request Timeout"
            results['message'] = message
            results['status'] = status.HTTP_408_REQUEST_TIMEOUT
        elif status_code == 502:
            results['error'] = "Bad gateway"
            results['message'] = message
            results['status'] = status.HTTP_502_BAD_GATEWAY
        elif status_code == 503:
            results['error'] = "Service is unavailable"
            results['message'] = message
            results['status'] = status.HTTP_503_SERVICE_UNAVAILABLE
        elif status_code == 500:
            results['error'] = "Internal Server Error"
            results['message'] = message
            results['status'] = status.HTTP_500_INTERNAL_SERVER_ERROR
        else:
            results['error'] = error
            results['message'] = 'Successfully'
            results['status'] = status.HTTP_200_OK

        if type(data) == list:
            results['data'] = data
        elif data is not None:
            results['data'].append(data)

        if error:
            results['error'] = error

        if message:
            results['message'] = message

        return results
