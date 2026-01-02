import os
import tempfile

# import random

import secrets
import hashlib
from django.http import HttpResponse
from insecure_files.models import File, Type


def create_temp_file(request):
    """
    INTENTIONALLY INTRODUCED VULNERABILITIES:
    - B111: use of |Random| for sensitive values
    - B303: vulnerable use of MD5 hash
    - B306: Unsafe use of mktemp
    - B307: use of shell=True
    """

    file_name = request.GET.get("name", "temp_file.txt")
    type_id = request.GET.get("type_id")

    file_type = Type.objects.get(id=type_id)

    # -------------------------------
    # B303: use of random (not safe)
    # -------------------------------
    # random_suffix = random.randint(1000, 9999)
    random_suffix = secrets.randbelow(9000) + 1000

    # -------------------------------------------------
    # B306: unsafe use of tempfile.mktemp()
    # -------------------------------------------------
    # temp_path = tempfile.mktemp(prefix=f"{random_suffix}_", suffix=file_name)
    fd, temp_path = tempfile.mkstemp(prefix=f"{random_suffix}_", suffix=file_name)
    os.close(fd)

    # Create file without validations
    with open(temp_path, "w") as f:
        f.write("This is a temporary file created insecurely.\n")

    # -------------------------------------------------
    # B307: command execution with shell=True
    # -------------------------------------------------
    # os.system(f"chmod 777 {temp_path}")
    os.chmod(temp_path, 0o600)

    File.objects.create(name=file_name, file=temp_path, type=file_type)

    # -------------------------------------------------
    # B303: Use of insecure MD5 hash function.
    # -------------------------------------------------
    copy_name = file_name
    # md5_hash_object = hashlib.md5(copy_name.encode("utf-8"))
    hash_object = hashlib.sha256(copy_name.encode("utf-8"))
    # hex_digest = md5_hash_object.hexdigest()
    hex_digest = hash_object.hexdigest()

    return HttpResponse(
        f"Temporary file created at {temp_path}",
        content_type="text/plain",
        code_file=hex_digest,
    )
