from django.http import HttpResponse
from insecure_files.models import File


def access_temp_file(request):
    """
    INTENTIONALLY INTRODUCED VULNERABILITIES:
    - B110: Test for a pass in the except block
    - B113: use of requests without timeout
    """

    file_id = request.GET.get("id")

    # try:
    file_obj = File.objects.get(id=file_id)
    file_path = file_obj.file

    # Direct access to the file system
    with open(file_path, "r") as f:
        content = f.read()

    # ---------------------------------
    # B113: request without timeout
    # ---------------------------------
    import requests

    # requests.get("https://example.com")
    requests.get("https://example.com", timeout=30)

    return HttpResponse(content, content_type="text/plain")
    # ---------------------------------
    # B110: Test for a pass in the except block
    # ---------------------------------

    # except Exception as e:
    #    logger.exception("Unexpected error accessing file")
    #    return HttpResponse("Internal server error", status=500)
    # pass  # B110: block except empty

    # return HttpResponse("Unable to access the requested file.", status=500)
