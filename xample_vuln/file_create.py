import os
import tempfile
import random
import hashlib
from django.http import HttpResponse
from insecure_files.models import File, Type


def create_temp_file(request):
    """
    INTENTIONALLY INTRODUCED VULNERABILITIES:
    - B111: use of |Random| for sensitive values
    - B306: Use of insecure and deprecated function (mktemp)
    - B605: Starting a process with a shell
    - B324: Use of weak MD5 hash for security
    """

    file_name = request.GET.get("name", "temp_file.txt")
    type_id = request.GET.get("type_id")

    file_type = Type.objects.get(id=type_id)

    # -------------------------------
    # B111: use of random (not safe)
    # -------------------------------
    random_suffix = random.randint(1000, 9999)

    # -------------------------------------------------
    # B306: unsafe use of tempfile.mktemp()
    # -------------------------------------------------
    temp_path = tempfile.mktemp(prefix=f"{random_suffix}_", suffix=file_name)

    # Create file without validations
    with open(temp_path, "w") as f:
        f.write("This is a temporary file created insecurely.\n")

    # -------------------------------------------------
    # B605: command execution with shell=True
    # -------------------------------------------------
    os.system(f"chmod 777 {temp_path}")

    File.objects.create(name=file_name, file=temp_path, type=file_type)

    # -------------------------------------------------
    # B324: Use of insecure MD5 hash function
    # -------------------------------------------------
    copy_name = file_name
    md5_hash_object = hashlib.md5(copy_name.encode("utf-8"))
    hex_digest = md5_hash_object.hexdigest()

    return HttpResponse(
        f"Temporary file created at {temp_path}",
        content_type="text/plain",
        code_file=hex_digest,
    )
