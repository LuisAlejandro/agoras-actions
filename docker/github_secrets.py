#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import base64
import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request

from nacl import encoding, public

SECRET_NAME_PATTERN = re.compile(r"^[A-Za-z][A-Za-z0-9_]*$")


class GitHubSecretsError(Exception):
    """Raised when GitHub Secrets API calls fail."""


def _api_request(method, url, token, payload=None):
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    data = None
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"

    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            body = response.read().decode("utf-8")
            if not body:
                return {}
            return json.loads(body)
    except urllib.error.HTTPError as exc:
        raise GitHubSecretsError(f"HTTP {exc.code}") from exc


def encrypt_secret(public_key_b64, secret_value):
    public_key = public.PublicKey(public_key_b64.encode("utf-8"), encoding.Base64Encoder())
    sealed_box = public.SealedBox(public_key)
    encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
    return base64.b64encode(encrypted).decode("utf-8")


def _validate_secret_name(secret_name):
    if not secret_name or not SECRET_NAME_PATTERN.match(secret_name):
        raise GitHubSecretsError("invalid secret name")


def put_repository_secret(secret_name, secret_value, token=None, repository=None, api_url=None):
    _validate_secret_name(secret_name)
    token = token or os.environ.get("GITHUB_SECRET_UPDATE_TOKEN", "")
    repository = repository or os.environ.get("GITHUB_REPOSITORY", "")
    api_url = (api_url or os.environ.get("GITHUB_API_URL", "https://api.github.com")).rstrip("/")

    if not token:
        raise GitHubSecretsError("missing write token")
    if "/" not in repository:
        raise GitHubSecretsError("invalid GITHUB_REPOSITORY")

    owner, repo = repository.split("/", 1)
    key_url = f"{api_url}/repos/{owner}/{repo}/actions/secrets/public-key"
    key_data = _api_request("GET", key_url, token)

    encrypted_value = encrypt_secret(key_data["key"], secret_value)
    encoded_name = urllib.parse.quote(secret_name, safe="")
    put_url = f"{api_url}/repos/{owner}/{repo}/actions/secrets/{encoded_name}"
    _api_request(
        "PUT",
        put_url,
        token,
        {
            "encrypted_value": encrypted_value,
            "key_id": key_data["key_id"],
        },
    )
